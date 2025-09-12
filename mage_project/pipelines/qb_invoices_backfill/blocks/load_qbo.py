# mage_project/pipelines/qb_invoices_backfill/blocks/load_qbo.py
from mage_ai.data_preparation.decorators import data_loader
from src.qbo_client import refresh_access_token, query_qbo
from mage_ai.data_preparation.variable_manager import get_secret
from datetime import datetime, timedelta
import logging, json

LOG = logging.getLogger("load_qbo")

@data_loader
def load(fecha_inicio, fecha_fin, chunk_size_days=1, page_size=100, **kwargs):
    # Leer secretos desde Mage Secrets
    client_id = get_secret('qbo_client_id')
    client_secret = get_secret('qbo_client_secret')
    refresh_token = get_secret('qbo_refresh_token')
    realm_id = get_secret('qbo_realm_id')
    qbo_env = get_secret('qbo_env') or 'sandbox'  # 'sandbox' -> use sandbox host

    host = "sandbox-quickbooks.api.intuit.com" if qbo_env == "sandbox" else "quickbooks.api.intuit.com"

    # chunking por días
    start = datetime.fromisoformat(fecha_inicio.replace("Z","+00:00"))
    end = datetime.fromisoformat(fecha_fin.replace("Z","+00:00"))
    cur = start
    results = []
    while cur < end:
        next_chunk = min(end, cur + timedelta(days=chunk_size_days))
        LOG.info("Processing chunk %s to %s", cur.isoformat(), next_chunk.isoformat())

        token_resp = refresh_access_token(client_id, client_secret, refresh_token)
        access_token = token_resp["access_token"]
        # IMPORTANT: After refresh, Intuit returns new refresh_token; you must rotate it
        # Save it in documentation/runbook and instruct admin to update Mage Secret manually.
        # (Automatizar rotación requiere acceso administrativo a Mage Secrets).
        for page_number, items, raw in query_qbo("Invoice", cur.isoformat().replace("+00:00","Z"),
                                               next_chunk.isoformat().replace("+00:00","Z"),
                                               page_size, host, realm_id, access_token):
            # yield a structured object for write block
            results.append({
                "chunk_start": cur.isoformat()+"Z",
                "chunk_end": next_chunk.isoformat()+"Z",
                "page_number": page_number,
                "page_size": page_size,
                "items": items,
                "request_payload": {"query_response_meta": raw.get("QueryResponse")},
            })
        cur = next_chunk

    return results
