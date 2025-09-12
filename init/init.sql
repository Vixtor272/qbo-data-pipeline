-- Crear el esquema raw si no existe
CREATE SCHEMA IF NOT EXISTS raw;

-- Crear la tabla de invoices
CREATE TABLE IF NOT EXISTS raw.qb_invoices (
  id TEXT PRIMARY KEY,
  payload JSONB NOT NULL,
  ingested_at_utc TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  extract_window_start_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  extract_window_end_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  page_number INTEGER,
  page_size INTEGER,
  last_seen TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Crear la tabla de customers
CREATE TABLE IF NOT EXISTS raw.qb_customers (
  id TEXT PRIMARY KEY,
  payload JSONB NOT NULL,
  create_time TIMESTAMP WITH TIME ZONE,
  last_updated_time TIMESTAMP WITH TIME ZONE,
  ingested_at_utc TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  extract_window_start_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  extract_window_end_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  page_number INTEGER,
  page_size INTEGER,
  last_seen TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Crear la tabla de items
CREATE TABLE IF NOT EXISTS raw.qb_items (
  id TEXT PRIMARY KEY,
  payload JSONB NOT NULL,
  create_time TIMESTAMP WITH TIME ZONE,
  last_updated_time TIMESTAMP WITH TIME ZONE,
  ingested_at_utc TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  extract_window_start_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  extract_window_end_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  page_number INTEGER,
  page_size INTEGER,
  last_seen TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Crear la tabla de log de ingestas
CREATE TABLE IF NOT EXISTS raw.qb_ingest_log (
  id SERIAL PRIMARY KEY,
  entity TEXT NOT NULL,
  window_start_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  window_end_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  pages_read INTEGER DEFAULT 0,
  rows_inserted INTEGER DEFAULT 0,
  rows_updated INTEGER DEFAULT 0,
  rows_skipped INTEGER DEFAULT 0,
  duration_seconds DOUBLE PRECISION DEFAULT 0,
  run_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  notes TEXT
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_qb_invoices_extract_time ON raw.qb_invoices (extract_window_start_utc);
CREATE INDEX IF NOT EXISTS idx_qb_customers_extract_time ON raw.qb_customers (extract_window_start_utc);
CREATE INDEX IF NOT EXISTS idx_qb_items_extract_time ON raw.qb_items (extract_window_start_utc);
CREATE INDEX IF NOT EXISTS idx_qb_ingest_log_entity ON raw.qb_ingest_log (entity);
CREATE INDEX IF NOT EXISTS idx_qb_ingest_log_run_at ON raw.qb_ingest_log (run_at);

-- Insertar un registro de ejemplo en el log
INSERT INTO raw.qb_ingest_log (entity, window_start_utc, window_end_utc, notes) 
VALUES ('system', NOW(), NOW(), 'Database initialized successfully')
ON CONFLICT (id) DO NOTHING;