# ennui-rag
> Sistema RAG para Google Drive (Colab) con persistencia en Supabase/Mongo y CSV por proyecto.

## ✨ Propósito y alcance
- Indexar carpetas de Drive por proyecto.
- Normalizar a CSV y preparar registros.
- Persistir con idempotencia en BD.
- Enriquecer (descripciones/embeddings) en siguiente fase.

## 📦 Instalación / Setup (Colab)
1. Monta Google Drive.
2. Abre `notebooks/ennui-rag-v1.ipynb`.
3. `pip install -r requirements.txt`.
4. Variables: `SB_SECRET`, `MONGO_URI`, `OPENAI_API_KEY` (si usarás LLM).

## ⚡️ Uso rápido
```python
from ennui_rag.pipelines import select_project, ensure_catalog, project_status
proj = select_project('<folder_id>')
csv_path = ensure_catalog(proj['project_id'], force=False, persist=True)
print(project_status(proj['project_id']))
```
```python
from ennui_rag.pipelines import run_index
df = run_index(env='dev', folder_id='<folder_id>', max_items=500)
```

## 📂 Estructura mínima
```
ennui-rag-v1/
├─ notebooks/ennui-rag-v1.ipynb
├─ src/ennui_rag/{settings.py, pipelines/, indexing/, persistence/, io/, app/}
├─ configs/{base,dev}.yaml
├─ data/<project_id>/{catalog_base.csv,sessions.json}
└─ requirements.txt
```

## 🔎 Estado actual
- Indexación estable (DFS con Shortcuts/Shared Drives).
- CSV por proyecto y sessions.json.
- Persistencia idempotente en BD.
- UI Streamlit funcional (secciones: indexing, enrichment, state).

**Notas recientes (del autor):**

He actualizado gen_kb para que haga una comparación de los archivos que describen el sistema

## 🧭 Roadmap breve
- Enrichment (descripciones + embeddings).
- Test suite.
- Métricas de indexación/persistencia.
- Vector store opcional.

---
> Breve descripción de la fuente del contenido: README generado automáticamente desde `KB_ennui_rag_v1.md` y estado del repositorio.

v1.49 — Generado el 17 de septiembre de 2025