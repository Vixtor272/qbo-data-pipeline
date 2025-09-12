import os
import requests
import base64
import logging
import pandas as pd
from datetime import datetime, timezone, timedelta
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# Configurar logging
logging.basicConfig(
    filename='qb_invoices.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def _get_access_token():
    refresh_token = get_secret_value('qb_refresh_token')
    client_secret = get_secret_value('qb_client_secret')
    client_id = get_secret_value('qb_client_id')
    url = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
    auth_header = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        logging.info("Nuevo access token obtenido correctamente")
        return tokens["access_token"]
    else:
        logging.error(f"Error al obtener token: {response.json()}")
        raise Exception("Error obteniendo token")

def _fetch_qb_data(realm_id, access_token, query, base_url, minor_version, start_position=1):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    params = {
        'query': f"{query} STARTPOSITION {start_position} MAXRESULTS 1000",
        'minorversion': minor_version
    }
    url = f"{base_url.rstrip('/')}/v3/company/{realm_id}/query"
    max_retries = 5

    for i in range(max_retries):
        try:
            logging.info(f"Request API: STARTPOSITION={start_position}")
            response = requests.get(url, headers=headers, params=params, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.warning(f'Reintento {i+1}/{max_retries}. Error: {e}')
    raise Exception(f"No se pudo obtener la data después de {max_retries} intentos.")

@data_loader
def load_data_from_api(*args, **kwargs):
    fecha_inicio = '2025-07-01'
    fecha_fin = '2025-08-01'

    start_date = datetime.fromisoformat(fecha_inicio)
    end_date = datetime.fromisoformat(fecha_fin)

    realm_id = get_secret_value('qb_realm_id')
    access_token = _get_access_token()
    minor_version = 75
    base_url = 'https://sandbox-quickbooks.api.intuit.com'

    extract_window_start = datetime.now(timezone.utc)
    all_invoices = []

    while start_date <= end_date:
        next_day = start_date + timedelta(days=1)
        query = f"SELECT * FROM Invoice WHERE TxnDate >= '{start_date.date()}' AND TxnDate < '{next_day.date()}'"

        start_position = 1
        page_number = 1

        logging.info(f"Procesando fecha {start_date.date()}...")

        while True:
            data = _fetch_qb_data(realm_id, access_token, query, base_url, minor_version, start_position)
            invoices = data.get('QueryResponse', {}).get('Invoice', [])
            if not invoices:
                break

            for invoice in invoices:
                all_invoices.append({
                    'id': invoice['Id'],
                    'payload': invoice,
                    'extract_window_start_utc': extract_window_start,
                    'extract_window_end_utc': datetime.now(timezone.utc),
                    'page_number': page_number,
                    'page_size': 1000,
                    'last_seen': datetime.now(timezone.utc)
                })

            logging.info(f'Fecha {start_date.date()}, Página {page_number}: {len(invoices)} registros.')
            print(f'Fecha {start_date.date()}, Página {page_number}: {len(invoices)} registros.')

            if len(invoices) < 1000:
                break
            start_position += 1000
            page_number += 1

        start_date = next_day

    df = pd.DataFrame(all_invoices)
    logging.info(f"Proceso completado. Total de registros: {len(df)}")
    return df

@test
def test_output(output, *args) -> None:
    assert isinstance(output, pd.DataFrame), 'El output no es un DataFrame'
    assert len(output) >= 0, 'No se insertaron registros'
