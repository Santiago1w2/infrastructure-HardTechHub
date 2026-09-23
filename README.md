# Infraestructura HardTechHub

| Servicio | Motor/base | Cuenta técnica |
|---|---|---|
| catalog-service | MongoDB: hardtech_catalog | catalog_app |
| inventory-service | PostgreSQL: hardtech_inventory | inventory_app |
| order-service | MySQL: hardtech_orders | orders_app |
| compatibility-service | PostgreSQL: hardtech_compatibility | compatibility_app |
| analytics-service | S3 + Glue Data Catalog + Athena | rol IAM de ejecución |

## Local

```powershell
# Solo para configurar un entorno nuevo:
Copy-Item .env.example .env
docker compose config --quiet
docker compose build
docker compose up -d --wait --wait-timeout 180
docker compose ps
docker compose logs --tail 100
```

Después levantar el repositorio de servicios. Ambos Compose usan la red
`hardtech-business` (`HARDTECH_NETWORK`). Los puertos internos siempre son
MongoDB 27017, PostgreSQL 5432 y MySQL 3306. Los puertos del host por defecto
son 27018, 55432 y 3307 respectivamente, configurables en .env.

Configurar las contraseñas de .env y las correspondientes de servicios antes de
crear los volúmenes. Las credenciales de los ejemplos son solo para desarrollo.
Cambiar .env no cambia contraseñas de bases ya inicializadas.

Los volúmenes `mongo_business_data`, `postgres_business_data` y
`mysql_business_data` son propios de esta arquitectura. Los init scripts solo
se ejecutan al inicializar un volumen vacío. No se eliminan ni migran
automáticamente datos de volúmenes anteriores. Antes de retirar volúmenes
previos, revisar y respaldar cualquier información de negocio que se conserve.
No montar un volumen de otro motor ni reutilizar esquemas incompatibles.

PostgreSQL crea dos bases con propietarios separados y revoca CONNECT público.
El esquema de inventario contiene `inventory`, `inventory_reservations`,
`inventory_movements`; compatibilidad contiene `compatibility_checks`,
`compatibility_components`, `compatibility_messages`.
MySQL crea `orders` y `order_items` con IDs AUTO_INCREMENT.
MongoDB inicializa `products`, `categories`, `brands`, `counters`,
validación de documentos e índices. Solo el catálogo tiene los cinco productos
seed previos; registrar existencias por API para poder crear pedidos.

## AWS

No había IaC AWS en este repositorio. Se añade
`aws/analytics.cloudformation.json`. Crea un bucket privado/cifrado, una base
Glue, una tabla JSONL externa `business_snapshot`, un workgroup Athena con
resultados en `query-results/` y límite de 1 GiB escaneado por consulta,
y una política IAM restringida a estos recursos.

`ExistingBucketName` permite reutilizar un bucket en la misma región. El
bucket creado por el stack se retiene al eliminar el stack. La política se
puede adjuntar a un rol existente mediante `RuntimeRoleName`. No crea ni
almacena claves AWS. Los nombres Glue/Workgroup deben estar libres o gestionarse
mediante el stack existente: no desplegar otro stack con los mismos nombres.

Ejemplo (requiere una cuenta AWS y permisos de despliegue):

```powershell
aws cloudformation validate-template --template-body file://aws/analytics.cloudformation.json
aws cloudformation deploy --template-file aws/analytics.cloudformation.json --stack-name hardtech-analytics --capabilities CAPABILITY_IAM --parameter-overrides GlueDatabaseName=hardtech_analytics WorkGroupName=hardtech-analytics
aws cloudformation describe-stacks --stack-name hardtech-analytics --query "Stacks[0].Outputs"
```

Para reutilizar recursos, agregar `ExistingBucketName=nombre-real` y
`RuntimeRoleName=rol-real` al comando deploy. Adjuntar la política devuelta al
rol del runtime si no se especificó rol. Configurar en servicios los outputs:
`S3_BUCKET`, `GLUE_DATABASE`, `ATHENA_WORKGROUP`,
`ATHENA_OUTPUT_LOCATION` y `AWS_DEFAULT_REGION`.

Los datos operacionales llegan por `POST /api/analytics/refresh` en servicios.
Glue describe `s3://bucket/analytics/business/`; Athena consulta JSONL.
La ruta de resultados de Athena queda fuera de los datos de negocio.
Los eventos de visualización existentes se leen desde `raw/events/`.
Las operaciones de AWS requieren ejecución real para validar permisos de la
cuenta; las pruebas locales simulan los SDK.

Referencias: [consultas Athena](https://docs.aws.amazon.com/boto3/latest/reference/services/athena/client/start_query_execution.html),
[resultados paginados](https://docs.aws.amazon.com/boto3/latest/reference/services/athena/client/get_query_results.html),
[workgroups CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-athena-workgroup.html).
