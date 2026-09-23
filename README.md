# Infraestructura HardTechHub en EC2 Database

Ejecutar este Compose en la máquina de bases. Los microservicios se ejecutan
en la instancia MV PROD; cada Compose crea su red local automáticamente.

1. Copiar `.env.example` a `.env` y cambiar las contraseñas.
2. Coordinar las contraseñas técnicas de `catalog_app`, `inventory_app` y
   `orders_app` con el `.env` de servicios.
3. Ejecutar:

```bash
docker compose config --quiet
docker compose up -d --wait --wait-timeout 180
docker compose ps
```

Publica PostgreSQL 5432, MySQL 3306 y MongoDB 27017. Si se cambian, ajustar también
los puertos del cliente en servicios y las reglas AWS. El Security Group Database
permite esos puertos desde SG-PROD; no se necesitan reglas públicas para bases.
Usar la IP privada de Database, nunca nombres Docker desde otra máquina.

## Bases y cuentas técnicas

- PostgreSQL → `hardtech_catalog`, cuenta `catalog_app`.
- MySQL → `hardtech_orders`, cuenta `orders_app`.
- MongoDB → `hardtech_inventory`, cuenta `inventory_app`.

Los init scripts se ejecutan solo al inicializar volúmenes vacíos. No usar
`down --volumes` para actualizar una instalación con datos.