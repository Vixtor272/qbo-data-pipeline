# mage_project/pipelines/qb_invoices_backfill/blocks/write_pg.py
from mage_ai.data_preparation.decorators import transformer
from src.pg_loader import get_conn_from_secrets, upsert_entity
from mage_ai.data_preparation.variable_manager import get_secret
import logging

LOG = logging.getLogger("write_pg")

@transformer
def write_to_pg(data, **kwargs):
    host = get_secret('pg_host') or 'postgres'
    port = get_secret('pg_port') or 5432
    db = get_secret('pg_database')
    user = get_secret('pg_user')
    password = get_secret('pg_password')

    conn = get_conn_from_secrets(host, port, db, user, password)
    inserted = 0
    for page in data:
        pg_table = 'qb_invoices'  # for this pipeline
        page_number = page['page_number']
        page_size = page['page_size']
        for item in page['items']:
            # QuickBooks internal id field often 'Id'
            record_id = item.get('Id') or item.get('id') or item.get('Id')
            upsert_entity(conn, pg_table, record_id, item, page['chunk_start'], page['chunk_end'], page_number, page_size, page['request_payload'], last_updated_at=item.get('MetaData', {}).get('LastUpdatedTime'))
            inserted += 1
    conn.close()
    return {"inserted": inserted}
