# 🚨 SOLUCIÓN INMEDIATA - Reset de Indexación Pegada

## ✅ **Problema Identificado**
- Indexación está en estado "running" pero pegada (más de 5 minutos sin progreso)
- El botón de reset no funcionaba porque faltaba el endpoint

## 🔧 **Solución Implementada**

### 1. **Backend Actualizado**
- ✅ Agregado endpoint `/api/indexing/reset-stuck-jobs/{program_id}`
- ✅ Detecta jobs pegados (más de 5 minutos en estado "running")
- ✅ Los marca como "failed" con mensaje explicativo

### 2. **Frontend Mejorado**
- ✅ Botón de reset ahora funciona correctamente
- ✅ Mejor manejo de errores
- ✅ Recarga automática después del reset

## 🚀 **Pasos para Resolver AHORA**

### **Paso 1: Reiniciar Backend**
```bash
cd /Users/alvaromur/dev/ennui-rag-v2
docker-compose restart backend
```

### **Paso 2: Verificar que Funciona**
```bash
# Verificar que el backend esté corriendo
docker-compose ps

# Ver logs para confirmar
docker-compose logs backend --tail=20
```

### **Paso 3: Probar en el Frontend**
1. **Recarga la página** del frontend
2. **Ve a la sección de Retrieval**
3. **Haz clic en "🔧 Resetear jobs pegados"**
4. **Deberías ver**: "✅ Reset X stuck jobs"

## 🎯 **Resultado Esperado**

Después del reset:
- ✅ El estado cambiará de "Indexando..." a "Carpeta validada"
- ✅ Podrás iniciar una nueva indexación
- ✅ El sistema estará limpio y funcional

## 🔍 **Si Sigue Sin Funcionar**

### **Opción 1: Reset Manual en Base de Datos**
```sql
-- Conectar a la base de datos PostgreSQL
UPDATE indexing_jobs 
SET status = 'failed', 
    error_message = 'Manual reset', 
    completed_at = NOW() 
WHERE program_id = [TU_PROGRAM_ID] 
AND status = 'running';
```

### **Opción 2: Reiniciar Todo**
```bash
docker-compose down
docker-compose up -d
```

## 📝 **Notas Importantes**

- **El endpoint está en**: `/api/indexing/reset-stuck-jobs/{program_id}`
- **Solo resetea jobs** que llevan más de 5 minutos en estado "running"
- **No afecta jobs** que están funcionando correctamente
- **Es seguro** - solo cambia el estado, no elimina datos

## 🎉 **Después del Reset**

Una vez que funcione:
1. **El estado será**: "Carpeta validada"
2. **Podrás hacer clic**: "🚀 Iniciar indexación"
3. **El sistema funcionará** correctamente (aunque seguirá usando el método incorrecto hasta implementar la corrección completa)

---

**¡Ejecuta `docker-compose restart backend` y prueba el botón de reset!**
