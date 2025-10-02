# Before anything (activate the project) if you don't see (venv) in prompt
source venv/bin/activate

# To start the app
sh working.sh (To exit use ctrl+c)

# To install new dependencies (assuming new dependendencies are in requirements.txt)
# add dependency to requirements.txt
pip install -r requirements.txt



tmux new -s jupyter
source venv/bin/activate
jupyter lab \
    --no-browser \
    --ip=0.0.0.0 \
    --port=8888 \
    --allow-root \
    --NotebookApp.token='48LpdLb5v~+AhAdkhC' \
    --NotebookApp.password='Y8qFN@Vd3U.*=cy}d5cj' \
    --NotebookApp.allow_origin='*'
(Then use ctrl+b) (then press key b)

http://34.171.12.47:8888/tree?token=48LpdLb5v~+AhAdkhC

# SSH para conectar el cliente a la BD
export DB_HOST=localhost
export DB_PORT=3306
export DB_USERNAME=alvaro
export DB_PASSWORD=n8PUqbXXA6pBYGjdvx7Z
export DB_NAME=ennui_rag

# 🚀 Guía completa: Exportar e importar el esquema `public` en Postgres con Docker Compose

Este documento explica los pasos para **respaldar** el esquema `public` en un entorno local, **transferir** el archivo a un servidor remoto y **restaurar** el contenido limpiando previamente el esquema.

---

## 📤 Paso 1. Exportar en Local

1. Crear carpeta de backups:

```bash
mkdir -p backups
```

2. Generar dump del esquema `public`:

```bash
docker compose exec -T postgres \
  pg_dump -U user -d mydatabase \
  -n public --no-owner --no-privileges \
  > ./backups/backup.sql
```

3. Copiar el dump al servidor remoto:

```bash
scp ./backups/backup.sql dev:/tmp/
```

---

## 📥 Paso 2. Restaurar en el Servidor Remoto

1. Borrar y recrear el esquema `public`:

```bash
docker compose exec -T postgres \
  psql -U user -d mydatabase -v ON_ERROR_STOP=1 \
  -c "DROP SCHEMA IF EXISTS public CASCADE; \
      CREATE SCHEMA public; \
      GRANT ALL ON SCHEMA public TO \"user\"; \
      GRANT ALL ON SCHEMA public TO PUBLIC;"
```

2. Importar el dump en la base de datos:

```bash
cat /tmp/backup.sql | docker compose exec -T postgres \
  psql -U user -d mydatabase
```

---

## ✅ Notas

- Cambia `postgres` por el nombre real del servicio definido en tu `docker-compose.yml` (ejemplo: `db`).
- Usa comillas dobles (`"user"`) ya que `user` es palabra reservada en Postgres.
- Si aparece el warning `the attribute version is obsolete`, elimina la línea `version:` de tu `docker-compose.yml`.
