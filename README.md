# QBO Data Pipeline

Este proyecto implementa un pipeline ETL para extraer datos de QuickBooks Online (QBO) mediante su API REST, transformarlos y cargarlos en una base de datos PostgreSQL. La solución utiliza Mage AI como orquestador y se ejecuta en contenedores Docker, con pipelines específicos para invoices, customers e items.

## Arquitectura

El siguiente diagrama ilustra la arquitectura del sistema:

```
+----------------+     +-------------+     +----------------+     +-------------------+
| QuickBooks API | --> | Mage AI ETL | --> | PostgreSQL RAW | --> | PGAdmin (Monitoring) |
+----------------+     +-------------+     +----------------+     +-------------------+
       ^                       |                   |                       |
       |                       +---- Docker Network (qbo_net) ------------+
       |                               |
       +--------- OAuth 2.0 -----------+
```

## Requisitos Previos

- Docker
- Docker Compose

## Configuración e Instalación

1. Clona este repositorio:
   ```bash
   git clone <url_del_repositorio>
   cd qbo-data-pipeline
   ```

2. Levanta los contenedores:
   ```bash
   docker-compose up -d
   ```

3. Accede a las herramientas:
   - Mage: http://localhost:6789
   - PGAdmin: http://localhost:5050 (usuario: admin@example.com, contraseña: admin)
   - PostgreSQL: localhost:5432 (base de datos: qbo_raw_db, usuario: qbo_user, contraseña: qbo_password)

## Gestión de Secrets

Los siguientes secrets deben configurarse en la interfaz de Mage (Secrets Management):

| Nombre | Propósito | Rotación | Responsable |
|--------|-----------|----------|-------------|
| refresh_token | Autenticación OAuth2 | 90 días | DevOps |
| client_secret | Autenticación aplicación | Anual | Security |
| client_id | Identificación aplicación | Anual | Security |
| realm_id | Identificación compañía QBO | Estático | Admin QBO |

## Pipelines de Backfill

El proyecto incluye tres pipelines principales para extraer datos de QuickBooks:

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

**Runbook Común**:
1. Verificar que los secrets estén configurados correctamente
2. Establecer el rango de fechas para la extracción
3. Ejecutar el pipeline desde la interfaz de Mage
4. Validar la volumetría y consistencia de los datos

## Trigger One-Time

Cada pipeline puede ejecutarse con triggers one-time independientes:
- **Ejecución UTC**: 2023-11-15 14:00:00
- **Equivalencia en Guayaquil**: 2023-11-15 09:00:00 (UTC-5)
- **Política**: Cada trigger se deshabilita automáticamente después de la ejecución

## Esquema de la Base de Datos RAW

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

La idempotencia se garantiza mediante claves primarias y el uso de UPSERT en todas las tablas.



¡Tu proyecto con tres pipelines está listo para ser compartido y colaborado en GitHub!
