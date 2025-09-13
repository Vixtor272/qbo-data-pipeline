## Definiciones de Mage

### qb_invoices_backfill
- **Entidad**: Facturas (Invoices)
- **Parámetros**: fecha_inicio, fecha_fin (formato ISO)
- **Segmentación**: Diaria con paginación de 1000 registros
- **Límites**: 5 reintentos por página, timeout de 60s

### qb_customers_backfill
- **Entidad**: Clientes (Customers)
- **Parámetros**: fecha_inicio, fecha_fin (formato ISO)
- **Segmentación**: Diaria con paginación de 1000 registros
- **Límites**: 5 reintentos por página, timeout de 60s

### qb_items_backfill
- **Entidad**: Productos/Servicios (Items)
- **Parámetros**: fecha_inicio, fecha_fin (formato ISO)
- **Segmentación**: Diaria con paginación de 1000 registros
- **Límites**: 5 reintentos por página, timeout de 60s

## Trigger One-Time

Cada pipeline puede ejecutarse con triggers one-time independientes:
- **Ejecución UTC**: 2023-11-15 14:00:00
- **Equivalencia en Guayaquil**: 2023-11-15 09:00:00 (UTC-5)
- **Política**: Cada trigger se deshabilita automáticamente después de la ejecución


