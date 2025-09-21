---



\## Nota de contexto: desarrollo y factorización de `search`



Durante esta iteración se consolidó el componente de \*\*LLM-aided search\*\* en el paquete `ennui\_rag`.

Originalmente se probó como prototipo en celdas de Colab, pero se \*\*factorizó\*\* a un subpaquete propio:



```

src/ennui\_rag/search/

├─ loader.py      # Carga corpus desde CSV enriquecidos o base

├─ retrieve.py    # Recuperación lexical + filtros + opción híbrida embeddings

├─ rerank.py      # Rerankeado con LLM usando llm\_json

├─ answers.py     # Generación de respuesta breve con citas

├─ search.py      # Orquestador end-to-end

└─ \_\_init\_\_.py    # expone search\_llm

```



\### Evolución



\* Se implementó un \*\*loader robusto\*\* con fallback a `catalog\_base.csv`.

\* `retrieve.py` ahora soporta \*\*filtros\*\* (`by\_path`, `by\_mime`, `modified\_from`, `modified\_to`) además de scoring lexical.

\* Se añadió \*\*modo híbrido\*\* que combina lexical con embeddings si están disponibles.

\* `rerank.py` encapsula la llamada a `llm\_json` para ordenar candidatos por relevancia semántica.

\* `answers.py` ofrece un \*\*modo answer\*\* que devuelve un texto conciso acompañado de citas de documentos.

\* `search.py` es la \*\*API pública\*\* (`search\_llm`) que une todo y expone flags como `as\_answer`, `debug` o `return\_candidates`.



\### Invocación en Colab



1\. Selecciona proyecto (`select\_project`) y asegúrate de que existan los CSV enriquecidos.

2\. Importa la función principal:



```python

from ennui\_rag.search import search\_llm



PROJ\_ID = proj\["project\_id"]



\# Búsqueda clásica (tabla)

res = search\_llm("actas de comité y cronograma",

&nbsp;                project\_id=PROJ\_ID, k=40, n=12)

display(res.head(10))



\# Búsqueda con respuesta breve y citas

ans = search\_llm("¿Qué documentos resumen resultados y cronograma?",

&nbsp;                project\_id=PROJ\_ID, k=60, n=12,

&nbsp;                as\_answer=True, answer\_k=5)

print(ans\["answer"])

for c in ans\["citations"]:

&nbsp;   print("•", c\["title"], "—", c\["path"], c\["web\_url"])

```

---

## Nota de contexto: actualización de la app con panel de búsqueda

En esta iteración se actualizó la aplicación **Streamlit** (`ui_streamlit.py`) para incorporar un **panel de búsqueda LLM-aided** integrado en la interfaz. Los cambios principales fueron:

### 1. Barra lateral

* Se añadió una **sidebar persistente** para:

  * Visualizar y editar el **Project ID** activo.
  * Activar el proyecto desde entrada manual o variable de entorno (`ENNUI_PROJECT_ID`).
  * Limpiar el estado (`st.session_state`).
  * Navegar entre secciones: **Indexing**, **Enrichment**, **State**, **Search**.
* Se implementó `_rerun()` como wrapper compatible (`st.rerun` / `st.experimental_rerun`), evitando errores entre versiones de Streamlit.

### 2. Nuevo panel de búsqueda

* Se creó un panel **Search** integrado a la app principal.
* Basado en `ennui_rag.search.search_llm`, con soporte para:

  * Búsquedas léxicas rerankeadas con LLM.
  * **Modo tabla** (resultados ordenados con metadatos: score, título, ruta, mime, URL).
  * **Modo respuesta** (`as_answer=True`) con párrafo breve y **citas** a los documentos fuente.
* Controles incluidos en el formulario:

  * Parámetros `k` (candidatos) y `n` (Top N).
  * Selector de tipo (`file`, `folder`).
  * Filtros avanzados: ruta (`by_path`), MIME, fechas (`modified_from`, `modified_to`), debug.
* Resultados presentados en tabla (`st.dataframe`) o como respuesta con citas.

### 3. Flujo de uso

1. Seleccionar un proyecto en la **sidebar**.
2. Acceder a la pestaña **Search**.
3. Ingresar consulta y, opcionalmente, filtros.
4. Visualizar resultados como tabla o respuesta breve con citas.

---

