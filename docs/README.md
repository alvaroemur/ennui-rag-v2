# Documentación ennui-rag

## Estructura de Documentación

### 📚 [Knowledge Base (KB)](kb/)
- **Snapshots** - Documentación versionada por fecha
- **Índice** - Acceso a la versión más reciente

### 🎨 [Design](design/)
- **Vision Narrativa** - Concepto del sistema
- **ERD Objetivo** - Modelo de datos
- **Blueprints** - Flujos y arquitectura
- **Decisiones (ADR)** - Decisiones arquitectónicas

### 📋 [Playbooks](playbooks/)
- **Prompts** - Plantillas para IA
- **Operación** - Procedimientos estandarizados

### 🔧 [Technical](technical/)
- **Complete** - Documentación técnica completa del sistema
- **Development** - Notas de desarrollo y configuración
- **Persistence** - Actualizaciones del sistema de persistencia
- **Context** - Notas de contexto del desarrollo

### 🗄️ [Database](database/)
- **Status** - Estado actual de la base de datos
- **Schema** - Esquemas y migraciones

## Uso

1. **Para desarrollo** → Consulta KB snapshots y technical
2. **Para diseño** → Revisa design documentation
3. **Para operación** → Usa playbooks
4. **Para base de datos** → Consulta database documentation

## Navegación Rápida

- [KB Latest](kb/index.md) - Documentación más reciente
- [Design Overview](design/README.md) - Diseño del sistema
- [Playbooks](playbooks/) - Procedimientos operativos
- [Technical Complete](technical/complete.md) - Documentación técnica completa
- [Database Status](database/status.md) - Estado de la base de datos

## Estructura del Proyecto

```
ennui-rag/
├─ docs/                           # 📚 Documentación completa
│  ├─ README.md                   # Este archivo (índice)
│  ├─ technical/                  # Documentación técnica
│  ├─ database/                   # Documentación de BD
│  ├─ kb/                        # Knowledge Base
│  ├─ design/                    # Diseño del sistema
│  └─ playbooks/                 # Procedimientos
├─ src/ennui_rag/                # Código fuente principal
├─ scripts/                      # Scripts de utilidad
├─ configs/                      # Configuración
├─ data/                         # Datos del proyecto
└─ tests/                        # Tests unitarios
```

---
*Documentación reorganizada siguiendo mejores prácticas de estructura de proyectos*