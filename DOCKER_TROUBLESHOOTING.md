# Docker Troubleshooting - ennui-rag-v2

## Problema Resuelto: Error de Volumen de PostgreSQL

### Error Original
```
(HTTP code 400) unexpected - failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: error mounting "/var/lib/docker/volumes/ennui-rag-v2_postgres_data/_data" to rootfs at "/var/lib/postgresql/data": change mount propagation through procfd: open o_path procfd: open /var/lib/docker/rootfs/overlayfs/dbbfc0e88ddfc31dab93f0f93fc4ac712320bf55c6a6265a8ef017f6199a7eb6/var/lib/postgresql/data: no such file or directory: unknown
```

### Soluciones Aplicadas

#### 1. Limpieza de Volúmenes
```bash
docker-compose down -v
```
- Eliminó todos los volúmenes corruptos
- Limpió contenedores y redes

#### 2. Actualización de Docker Compose
- Cambió de `version: '2.2'` a `version: '3.8'`
- Mejoró la compatibilidad con versiones recientes de Docker

#### 3. Mejora de Configuración de PostgreSQL
```yaml
postgres:
  image: postgres:15  # Versión específica en lugar de 'latest'
  restart: unless-stopped
  volumes:
    - postgres_data:/var/lib/postgresql/data
  environment:
    POSTGRES_DB: mydatabase
    POSTGRES_USER: user
    POSTGRES_PASSWORD: password
    POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
  ports:
    - "5432:5432"
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U user -d mydatabase"]
    interval: 10s
    timeout: 5s
    retries: 5
```

#### 4. Dependencias Mejoradas
```yaml
backend:
  depends_on:
    postgres:
      condition: service_healthy  # Espera a que PostgreSQL esté listo
```

### Estado Final
Todos los servicios funcionando correctamente:
- ✅ PostgreSQL: Up (healthy)
- ✅ Backend: Up
- ✅ Frontend: Up

### Comandos de Verificación
```bash
# Ver estado de servicios
docker-compose ps

# Ver logs de un servicio específico
docker-compose logs postgres
docker-compose logs backend
docker-compose logs frontend

# Reiniciar un servicio específico
docker-compose restart postgres
```

### Prevención de Problemas Futuros
1. Usar versiones específicas de imágenes en lugar de 'latest'
2. Implementar health checks para servicios críticos
3. Usar `depends_on` con condiciones de salud
4. Limpiar volúmenes periódicamente si hay problemas
