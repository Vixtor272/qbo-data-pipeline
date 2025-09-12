CREATE SCHEMA IF NOT EXISTS raw;

-- Template para cada entidad (Invoices, Customers, Items)
CREATE TABLE IF NOT EXISTS raw.qb_invoices (
  id TEXT PRIMARY KEY,                 -- id de QuickBooks (string)
  payload JSONB NOT NULL,              -- payload completo
  ingested_at_utc TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  extract_window_start_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  extract_window_end_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  page_number INT,
  page_size INT,
  request_payload JSONB,
  last_updated_at_utc TIMESTAMP WITH TIME ZONE, -- opcional: timestamp del recurso
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS raw.qb_customers (
  id TEXT PRIMARY KEY,
  payload JSONB NOT NULL,
  ingested_at_utc TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  extract_window_start_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  extract_window_end_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  page_number INT,
  page_size INT,
  request_payload JSONB,
  last_updated_at_utc TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS raw.qb_items (
  id TEXT PRIMARY KEY,
  payload JSONB NOT NULL,
  ingested_at_utc TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  extract_window_start_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  extract_window_end_utc TIMESTAMP WITH TIME ZONE NOT NULL,
  page_number INT,
  page_size INT,
  request_payload JSONB,
  last_updated_at_utc TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
