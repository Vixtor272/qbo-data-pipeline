## Definiciones y esquema de la Base de Datos RAW

### Tabla: qb_invoices
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | VARCHAR(255) PRIMARY KEY | ID del registro en QBO |
| payload | JSONB | Datos crudos de la factura |
| extract_window_start_utc | TIMESTAMPTZ | Inicio de la extracción |
| extract_window_end_utc | TIMESTAMPTZ | Fin de la extracción |
| page_number | INTEGER | Número de página |
| page_size | INTEGER | Tamaño de página (1000) |
| last_seen | TIMESTAMPTZ | Última vez visto |

### Tabla: qb_customers
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | VARCHAR(255) PRIMARY KEY | ID del registro en QBO |
| payload | JSONB | Datos crudos del cliente |
| extract_window_start_utc | TIMESTAMPTZ | Inicio de la extracción |
| extract_window_end_utc | TIMESTAMPTZ | Fin de la extracción |
| page_number | INTEGER | Número de página |
| page_size | INTEGER | Tamaño de página (1000) |
| last_seen | TIMESTAMPTZ | Última vez visto |

### Tabla: qb_items
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | VARCHAR(255) PRIMARY KEY | ID del registro en QBO |
| payload | JSONB | Datos crudos del ítem |
| extract_window_start_utc | TIMESTAMPTZ | Inicio de la extracción |
| extract_window_end_utc | TIMESTAMPTZ | Fin de la extracción |
| page_number | INTEGER | Número de página |
| page_size | INTEGER | Tamaño de página (1000) |
| last_seen | TIMESTAMPTZ | Última vez visto |
