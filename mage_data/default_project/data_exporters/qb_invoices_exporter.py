import json
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Exporta un DataFrame procesado desde Mage a PostgreSQL.
    Consistente con el esquema y tabla creados en el dataloader.
    Evita errores de duplicados mediante UPSERT automático.
    """
    schema_name = 'raw'
    table_name = 'qb_invoices'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    if df.empty:
        print('DataFrame vacío, no se exporta nada.')
        return None

    # Asegurar que payload se almacene como JSON string
    if 'payload' not in df.columns:
        df['payload'] = df.apply(
            lambda row: json.dumps({
                k: (v.isoformat() if hasattr(v, 'isoformat') else v)
                for k, v in row.to_dict().items()
            }),
            axis=1
        )

    # Columnas alineadas con la tabla del dataloader
    export_columns = [
        'id',
        'payload',
        'extract_window_start_utc',
        'extract_window_end_utc',
        'page_number',
        'page_size',
        'last_seen'
    ]
    # Filtrar solo columnas que existen en el df
    export_columns = [col for col in export_columns if col in df.columns]
    df_export = df[export_columns].copy()

    # Exportar a Postgres usando Mage con UPSERT
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df_export,
            schema_name,
            table_name,
            index=False,
            if_exists='append',                 # No sobrescribe la tabla
            unique_constraints=['id'],          # Clave primaria para conflict
            unique_conflict_method='update',    # UPSERT: actualiza si existe
        )

    print(f'{len(df_export)} registros exportados a {schema_name}.{table_name}')


