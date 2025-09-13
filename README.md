# QBO Data Pipeline

Este proyecto implementa un pipeline ETL para extraer datos de QuickBooks Online (QBO) mediante su API REST, transformarlos y cargarlos en una base de datos PostgreSQL. La solución utiliza Mage AI como orquestador y se ejecuta en contenedores Docker, con pipelines específicos para invoices, customers e items.
# QuickBooks Backfill Project

## Descripción
Este proyecto implementa pipelines de backfill para extraer datos históricos de QuickBooks Online (QBO) mediante su API y almacenarlos en una base de datos PostgreSQL. El sistema utiliza Mage AI como orquestador de pipelines y se ejecuta en contenedores Docker.

## Arquitectura

El siguiente diagrama ilustra la arquitectura del sistema:

```
+----------------+     +-------------+     +----------------+     +-------------------+
| QuickBooks API | --> |   Mage AI   | --> | PostgreSQL RAW | --> |     PGAdmin       |
+----------------+     +-------------+     +----------------+     +-------------------+
       ^                       |                   |                       |
       |                       +---- Docker Network (qbo_net) ------------+
       |                               |
       +--------- OAuth 2.0 -----------+
```

## Pasos para levantar contenedores y configurar el proyecto

### Prerrequisitos
- Docker y Docker Compose instalados
- Credenciales de QuickBooks API

### Configuración inicial
1. Clonar el repositorio
2. Configurar secrets en Mage AI:
```bash
docker exec -it mage mage-secrets set refresh_token <valor>
docker exec -it mage mage-secrets set client_secret <valor>
docker exec -it mage mage-secrets set client_id <valor>
docker exec -it mage mage-secrets set realm_id <valor>
```

3. Iniciar los contenedores:
```bash
docker-compose up -d
```

4. Acceder a las interfaces:
   - Mage AI: http://localhost:6789
   - PGAdmin: http://localhost:5050

## Gestión de Secretos

| Nombre | Propósito | Rotación | Responsable |
|--------|-----------|----------|-------------|
| refresh_token | Autenticación OAuth2 con QBO | 101 días | DevOps Team |
| client_secret | Autenticación OAuth2 con QBO | Anual | DevOps Team |
| client_id | Identificación de aplicación QBO | Anual | DevOps Team |
| realm_id | Identificación de compañía QBO | No requiere | Business Team |

## Pipelines qb_<entidad>_backfill

### Parámetros comunes
- `fecha_inicio`: Fecha de inicio en formato ISO (UTC)
- `fecha_fin`: Fecha de fin en formato ISO (UTC)

### Segmentación
- **Customers/Items**: Por rango de fechas usando Metadata.CreateTime y Metadata.LastUpdatedTime
- **Invoices**: Por día natural usando TxnDate

### Límites y Reintentos
- Límite de paginación: 1000 registros por página
- Máximo de reintentos: 5 por solicitud
- Timeout: 60 segundos por solicitud

### Runbook de Reanudación
1. Verificar logs de última ejecución exitosa
2. Identificar último timestamp procesado
3. Reanudar pipeline con fecha_inicio = último timestamp + 1 segundo

## Trigger One-Time

### Configuración UTC/Guayaquil
- Ejecución programada: 2024-01-15T02:00:00Z (UTC)
- Equivalente en Guayaquil: 2024-01-14T21:00:00-05:00 (ECT)

### Política de Deshabilitación
- Los triggers one-time se deshabilitan automáticamente después de la ejecución
- Se debe marcar como "completed" en el sistema de monitoreo
- Eliminar configuración del scheduler post-ejecución

## Esquema Raw

### Tablas por Entidad
1. `qb_customers` - Datos de clientes de QBO
2. `qb_invoices` - Datos de facturas de QBO  
3. `qb_items` - Datos de items de QBO

### Metadatos Obligatorios
- `extract_window_start_utc`: Timestamp de inicio de extracción
- `extract_window_end_utc`: Timestamp de fin de extracción
- `last_seen`: Última vez que el registro fue visto

### Idempotencia
- UPSERT basado en campo `id`
- No se generan duplicados en re-ejecuciones

## Validaciones y Volumetría

### Ejecución de Validaciones
```bash
# Correr validaciones desde Mage UI
1. Navegar a pipeline
2. Seleccionar "Trigger" > "Run tests"
```

### Interpretación de Resultados
- Verde: Todas las validaciones pasaron
- Amarillo: Advertencias en volumetría
- Rojo: Errores críticos en datos

## Troubleshooting

### Autenticación
- Verificar vigencia de refresh_token (101 días)
- Confirmar credenciales en Mage Secrets
Nota: El refresh_token puede cambiar en un par de días por razones desconocidas, puede que sea necesario generar otro refresh_token sin que hayan pasado los 101 días de validez.

### Paginación
- Máximo 1000 registros por página
- STARTPOSITION incrementa en múltiplos de 1000

### Límites de API
- Límite de tasa: 500 requests por minuto
- Timeout: 60 segundos por request

### Timezones
- Todas las fechas se manejan en UTC
- Conversiones necesarias para tiempo local

### Almacenamiento
- Volúmenes Docker para persistencia
- `pgdata`: Datos de PostgreSQL
- `mage_data`: Pipelines y configuración

### Permisos
- Usuario PostgreSQL: qbo_user
- Permisos de escritura en volúmenes Docker

## Checklist de Aceptación

- [x] Mage y Postgres se comunican por nombre de servicio
- [x] Todos los secretos (QBO y Postgres) están en Mage Secrets; no hay secretos en el repo/entorno expuesto
- [x] Pipelines qb_<entidad>_backfill acepta fecha_inicio y fecha_fin (UTC) y segmenta el rango
- [x] Trigger one-time configurado, ejecutado y luego deshabilitado/marcado como completado
- [x] Esquema raw con tablas por entidad, payload completo y metadatos obligatorios
- [x] Idempotencia verificada: reejecución de un tramo no genera duplicados
- [x] Paginación y rate limits manejados y documentados
- [x] Volumetría y validaciones mínimas registradas y archivadas como evidencia
- [x] Runbook de reanudación y reintentos disponible y seguido
