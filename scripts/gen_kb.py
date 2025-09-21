#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# === Generador de KB y README (únicos) para ennui-rag =========================
# Salidas finales:
#   - KB_ennui_rag_v1.md   (única fuente de verdad de conocimiento)
#   - README.md            (enfocado en uso y estado actual)
#
# Características:
#   - Backup previo con timestamp.
#   - Ignora scripts/, .git, __pycache__, .ipynb_checkpoints, venvs, dist, build, egg-info, docs/, notebooks/, tests/.
#   - Heurísticas: árbol de archivos, AST (funciones/clases/imports), excerpts head/tail, notebooks (headings/imports), YAML/JSON (primeras líneas).
#   - Heurística UI: detección de Streamlit (st.*), sidebar, render_* y "UI hooks".
#   - Enriquecimiento por secciones con llamadas LLM independientes (OpenAI chat.completions).
#   - Contexto editorial del autor (Markdown) vía --context / --context-file o variables de entorno.
#   - Retira KB antiguas (KB_COLAB.md, kb_ennui_rag.md) tras generar.
#   - Parametrizable por CLI o variables de entorno.
#   - NUEVO: Procesamiento por archivo individual (COMPORTAMIENTO POR DEFECTO).
#   - Comparación granular: cada archivo se procesa independientemente con su propio resumen LLM.

import os, sys, re, json, ast, datetime, pathlib, shutil, textwrap
from typing import List, Dict, Any, Optional

# -------------------- Carga de variables de entorno (.env) --------------------
def _load_dotenv():
    """Carga variables de entorno desde archivo .env si existe"""
    env_file = pathlib.Path(".env")
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip()
        except Exception as e:
            print(f"⚠️ Error cargando .env: {e}")

# Cargar .env antes de procesar argumentos
_load_dotenv()

# -------------------- CLI y configuración -------------------------------------
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--shortcut", help="Nombre del acceso directo en Drive (p. ej., ennui-rag-v1)")
parser.add_argument("--folder-id", help="ID de la carpeta compartida de Drive")
parser.add_argument("--base", help="Ruta absoluta al root del proyecto (si ya la resolviste en el SETUP)")
parser.add_argument("--readme", dest="generate_readme", action="store_true", help="Generar README.md")
parser.add_argument("--no-readme", dest="generate_readme", action="store_false", help="No generar README.md")
parser.add_argument("--verbose", action="store_true", help="Impresiones de diagnóstico")

# 🔹 Nuevo: contexto editorial
parser.add_argument("--context", help="Texto resumen multilínea (Markdown) del trabajo reciente")
parser.add_argument("--context-file", help="Ruta a archivo con texto Markdown de contexto")

# 🔹 Nuevo: procesamiento por archivo (ahora es el comportamiento por defecto)
parser.add_argument("--por-archivo", action="store_true", default=True, help="Procesar cambios por archivo individual (nueva lógica) - COMPORTAMIENTO POR DEFECTO")
parser.add_argument("--modo-original", action="store_true", help="Usar el modo original de comparación (comportamiento anterior)")
parser.add_argument("--overwrite", action="store_true", help="Modo overwrite: elimina snapshot actual y crea uno nuevo (para evitar problemas de comparación)")

parser.set_defaults(generate_readme=True)
args = parser.parse_args()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Salidas - Snapshots modernos con timestamp GMT-5 (Lima/Perú)
import pytz
gmt_minus_5 = pytz.timezone('America/Lima')  # GMT-5 (Perú Standard Time)
NOW = datetime.datetime.now(gmt_minus_5)
SNAPSHOT_DATE = NOW.strftime('%Y-%m-%d')
SNAPSHOT_TIMESTAMP = NOW.strftime('%Y-%m-%d_%H%M%S')
SNAPSHOT_DIR = f"docs/kb/snapshots/{SNAPSHOT_TIMESTAMP}"

# Archivos especializados del snapshot
SNAPSHOT_FILES = {
    'resumen-ejecutivo.md': 'Resumen Ejecutivo',
    'arquitectura-flujo.md': 'Arquitectura y Flujo', 
    'arbol-modulos.md': 'Árbol de Módulos',
    'operacion-troubleshooting.md': 'Operación y Troubleshooting',
    'notas-cambio.md': 'Notas de Cambio'
}

# README principal (opcional)
OUT_README   = "README.md"

# Fuentes previas (sólo referencia; desaparecerán)
SRC_KB_COLAB = "KB_COLAB.md"
SRC_KB_MIN   = "kb_ennui_rag.md"

# Recorrido y parsing
ALLOW_EXTS = {".py", ".ipynb", ".md", ".yaml", ".yml", ".json", ".toml", ".cfg", ".ini", ".txt"}
IGNORE_DIRS = {
    ".git", "__pycache__", ".ipynb_checkpoints", ".venv", "venv", "env",
    "node_modules", "dist", "build", ".mypy_cache", "scripts", "ennui_rag.egg-info",
    "docs", "notebooks", "tests"
}
MAX_TREE_DEPTH   = 6
HEAD_TAIL_LINES  = (30, 20)

# -------------------- Funciones de utilidad --------------------------------
def _generate_frontmatter(title: str, doc_type: str = "kb") -> str:
    """Genera front-matter YAML para archivos MD del snapshot"""
    return f"""---
title: "{title} - Snapshot {SNAPSHOT_TIMESTAMP}"
project: "ennui-rag"
doc_type: "{doc_type}"
version: "v0.1"
date: "{SNAPSHOT_TIMESTAMP}"
source_of_truth: "as-is"
---

"""

def _create_snapshot_directory():
    """Crea el directorio del snapshot si no existe"""
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    if VERBOSE:
        print(f"📁 Directorio de snapshot creado: {SNAPSHOT_DIR}")

# -------------------- Descubrimiento del proyecto (Colab + Local) ------------
def _is_colab_environment() -> bool:
    """Detecta si estamos en Google Colab"""
    try:
        import google.colab
        return True
    except ImportError:
        return False

def _is_mounted_ok() -> bool:
    """Verifica si Google Drive está montado (solo en Colab)"""
    if not _is_colab_environment():
        return False
    return os.path.ismount("/content/drive") and os.path.isdir("/content/drive/MyDrive")

def _repair_mount(verbose=True):
    """Intenta reparar el montaje de Google Drive (solo en Colab)"""
    if not _is_colab_environment():
        if verbose: print("ℹ️ No estamos en Colab, saltando montaje de Drive")
        return
    try:
        os.listdir("/content/drive/MyDrive")
        return
    except OSError as e:
        if verbose: print("🔧 Reparando montaje de Drive…", e)
        os.system("fusermount -u /content/drive 2>/dev/null || true")
        try:
            from google.colab import drive as _drive  # type: ignore
            _drive.mount("/content/drive", force_remount=True)
        except Exception:
            pass

def _safe_chdir(path: str):
    """Cambia al directorio del proyecto de forma segura"""
    try:
        os.chdir(path)
    except OSError as e:
        if _is_colab_environment() and (getattr(e, "errno", None) == 107 or "Transport endpoint" in str(e)):
            _repair_mount()
            os.chdir(path)
        else:
            raise

def _is_project_dir(p: pathlib.Path) -> bool:
    markers = ["requirements.txt", "pyproject.toml", "src/ennui_rag", "notebooks/ennui-rag-v1.ipynb"]
    try:
        return any((p / m).exists() for m in markers)
    except Exception:
        return False

def _candidates(folder_id: str, shortcut_name: str):
    """Genera candidatos para el directorio del proyecto"""
    candidates = []
    
    # En Colab, buscar en Google Drive
    if _is_colab_environment():
        base = pathlib.Path("/content/drive/MyDrive") / (shortcut_name or "")
        hidden = pathlib.Path("/content/drive/MyDrive/.shortcut-targets-by-id") / (folder_id or "")
        hidden_root = pathlib.Path("/content/drive/.shortcut-targets-by-id") / (folder_id or "")
        candidates.extend([base, hidden, hidden / (shortcut_name or ""), hidden_root, hidden_root / (shortcut_name or "")])
    
    # En local, buscar en el directorio actual y padres
    current_dir = pathlib.Path.cwd()
    candidates.append(current_dir)
    candidates.append(current_dir.parent)
    
    return candidates

SHORTCUT_NAME = os.getenv("SHORTCUT_NAME") or args.shortcut
FOLDER_ID     = os.getenv("FOLDER_ID") or args.folder_id
PROJECT_BASE  = os.getenv("PROJECT_BASE") or args.base
GENERATE_README = bool(args.generate_readme)
VERBOSE = bool(args.verbose)
POR_ARCHIVO = bool(args.por_archivo)
MODO_ORIGINAL = bool(args.modo_original)
OVERWRITE_MODE = bool(args.overwrite)

# Solo intentar montar Drive si estamos en Colab
if _is_colab_environment() and not _is_mounted_ok():
    _repair_mount(verbose=VERBOSE)

# Resolver directorio del proyecto
if PROJECT_BASE and pathlib.Path(PROJECT_BASE).exists():
    PROJECT_DIR = str(pathlib.Path(PROJECT_BASE).resolve())
    if VERBOSE: print(f"📍 Usando directorio base especificado: {PROJECT_DIR}")
else:
    PROJECT_DIR = None
    for c in _candidates(FOLDER_ID or "", SHORTCUT_NAME or ""):
        if c and c.exists() and _is_project_dir(c):
            PROJECT_DIR = str(c.resolve())
            if VERBOSE: print(f"📍 Proyecto detectado en: {PROJECT_DIR}")
            break

if not PROJECT_DIR:
    # Fallback: usar directorio actual si parece ser un proyecto
    current_dir = pathlib.Path.cwd()
    if _is_project_dir(current_dir):
        PROJECT_DIR = str(current_dir.resolve())
        if VERBOSE: print(f"📍 Usando directorio actual como proyecto: {PROJECT_DIR}")
    else:
        raise RuntimeError(
            "❌ No pude resolver el directorio del proyecto.\n"
            "Pasa --base o exporta PROJECT_BASE; o usa --shortcut/--folder-id.\n"
            "Asegúrate de estar en el directorio raíz del proyecto ennui-rag."
        )

_safe_chdir(PROJECT_DIR)
print("📍 Proyecto:", PROJECT_DIR)

# -------------------- Utilidades generales ------------------------------------
# NOW y STAMP ya están definidos arriba con GMT-5
STAMP = SNAPSHOT_TIMESTAMP

def _spanish_date(d: datetime.datetime) -> str:
    meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
    return f"{d.day:02d} de {meses[d.month-1]} de {d.year}"

DATE_ES = _spanish_date(NOW)

def _read_text(path: str, max_chars: int = 1_500_000) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f: return f.read()[:max_chars]
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1", errors="ignore") as f: return f.read()[:max_chars]
    except Exception:
        return ""

def _write_text(path: str, text: str):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def _bump_version_from_text(prev_text: str, fallback="v1.0") -> str:
    m = re.search(r"\bv(\d+)\.(\d+)\b", prev_text or "")
    if not m: return fallback
    return f"v{m.group(1)}.{int(m.group(2))+1}"

def _human_size(n: Optional[int]) -> str:
    if n is None: return "-"
    for u in ["B","KB","MB","GB","TB"]:
        if n < 1024: return f"{n:.0f}{u}"
        n /= 1024
    return f"{n:.0f}PB"

def _head_tail_excerpt(text: str, head: int = HEAD_TAIL_LINES[0], tail: int = HEAD_TAIL_LINES[1]) -> str:
    lines = (text or "").splitlines()
    if len(lines) <= head + tail + 5:
        return "\n".join(lines)
    top = "\n".join(lines[:head])
    bottom = "\n".join(lines[-tail:])
    return f"{top}\n\n…\n\n{bottom}"

def _directory_tree(root: str, max_depth: int = MAX_TREE_DEPTH, ignore_dirs=None) -> str:
    ignore_dirs = ignore_dirs or set()
    root_path = pathlib.Path(root)
    lines = [f"{root_path.name}/"]
    def walk(d: pathlib.Path, depth: int):
        if depth > max_depth:
            lines.append("  " * depth + "…")
            return
        entries = sorted(d.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        for p in entries:
            name = p.name
            if p.is_dir():
                if name in ignore_dirs:
                    continue
                lines.append("  " * depth + f"├─ {name}/")
                walk(p, depth + 1)
            else:
                try: size = p.stat().st_size
                except Exception: size = None
                lines.append("  " * depth + f"│  {name}  ({_human_size(size)})")
    walk(root_path, 0)
    return "\n".join(lines)

def _collect_files(root: str) -> List[str]:
    acc = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in IGNORE_DIRS]
        for fn in fns:
            ext = pathlib.Path(fn).suffix.lower()
            if ext in ALLOW_EXTS:
                acc.append(os.path.join(dp, fn))
    return sorted(acc)

# ---------- Parsers: Python, Notebooks, Text-likes, + Heurística UI -----------
def _summarize_py_api(path: str, max_items: int = 60) -> Dict[str, Any]:
    txt = _read_text(path, max_chars=400_000)
    info = {"module_doc": None, "imports": [], "funcs": [], "classes": []}
    try:
        tree = ast.parse(txt)
        info["module_doc"] = ast.get_docstring(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    info["imports"].append(n.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for n in node.names:
                    info["imports"].append(f"{mod}.{n.name}".strip("."))
            elif isinstance(node, ast.FunctionDef):
                args = [a.arg for a in node.args.args]
                info["funcs"].append({"name": node.name, "args": args})
            elif isinstance(node, ast.ClassDef):
                methods = [b.name for b in node.body if isinstance(b, ast.FunctionDef)]
                info["classes"].append({"name": node.name, "methods": methods})
    except Exception as e:
        info["module_doc"] = info["module_doc"] or f"(parse error: {e})"
    info["imports"] = sorted(set(info["imports"]))[:max_items]
    info["funcs"]   = info["funcs"][:max_items]
    info["classes"] = info["classes"][:max_items]
    return info

_UI_WIDGET_PATTERNS = [
    r"\bst\.(?:button|text_input|selectbox|radio|checkbox|slider|multiselect|file_uploader|date_input|number_input)\b",
    r"\bst\.sidebar\b",
    r"\bst\.(?:write|markdown|table|dataframe|plotly_chart|pyplot)\b",
    r"\brender_[a-zA-Z0-9_]+\s*\(",
    r"\bst\.(?:form|form_submit_button)\b",
]

def _ui_heuristics(path: str, text: Optional[str] = None) -> Dict[str, Any]:
    """
    Heurística para detectar elementos UI en archivos Streamlit/UIs script-like.
    """
    t = text if text is not None else _read_text(path, max_chars=200_000)
    if not t:
        return {"ui_detected": False, "hooks": [], "widgets": []}
    ui_detected = False
    widgets, hooks = set(), set()

    for pat in _UI_WIDGET_PATTERNS:
        for m in re.finditer(pat, t):
            ui_detected = True
            token = m.group(0)
            if token.startswith("render_"):
                hooks.add(token.split("(")[0])
            elif token.startswith("st."):
                widgets.add(token.split("(")[0])

    # también reportar funciones render_* del AST (si existen)
    try:
        tree = ast.parse(t)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("render_"):
                hooks.add(node.name)
    except Exception:
        pass

    return {
        "ui_detected": ui_detected or bool(hooks) or bool(widgets),
        "hooks": sorted(hooks),
        "widgets": sorted(widgets),
    }

def _summarize_ipynb(path: str, max_headings: int = 30) -> Dict[str, Any]:
    try:
        nb = json.loads(_read_text(path, max_chars=1_000_000))
    except Exception:
        return {"cells": 0}
    md_headings, code_imports = [], []
    cells = nb.get("cells", [])
    for c in cells:
        if c.get("cell_type") == "markdown":
            src = "".join(c.get("source", []))
            for line in src.splitlines():
                if line.strip().startswith("#"):
                    md_headings.append(line.strip())
        elif c.get("cell_type") == "code":
            src = "".join(c.get("source", []))
            for m in re.finditer(r"^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)", src, re.M):
                code_imports.append(m.group(1))
    return {
        "cells": len(cells),
        "md_headings": md_headings[:max_headings],
        "imports": sorted(set(code_imports))[:max_headings]
    }

def _summarize_text_like(path: str) -> Dict[str, Any]:
    text = _read_text(path, max_chars=200_000)
    lines = text.splitlines()
    headings = [ln for ln in lines if ln.strip().startswith(("#","- ","* "))]
    return {
        "lines": len(lines),
        "headings_sample": headings[:20],
        "excerpt": _head_tail_excerpt(text, head=30, tail=10)
    }

# -------------------- Paso 0: Contexto editorial ------------------------------
def _load_context() -> str:
    # Prioridad: env CHATGPT_CONTEXT > --context > env CHATGPT_CONTEXT_FILE > --context-file
    ctx = os.getenv("CHATGPT_CONTEXT")
    if ctx and ctx.strip():
        return ctx
    if args.context and args.context.strip():
        return args.context
    ctx_file = os.getenv("CHATGPT_CONTEXT_FILE") or args.context_file
    if ctx_file and os.path.exists(ctx_file):
        try:
            return _read_text(ctx_file, max_chars=200_000)
        except Exception:
            pass
    return ""

EDITORIAL_CONTEXT = _load_context()
if VERBOSE and EDITORIAL_CONTEXT:
    print("📝 Contexto editorial cargado (primeros 120 chars):", EDITORIAL_CONTEXT[:120].replace("\n"," ") + ("…" if len(EDITORIAL_CONTEXT)>120 else ""))

# -------------------- Paso 1: Backup y crear directorio ----------------------
def backup_existing():
    """Mueve el snapshot anterior a legacy si existe"""
    snapshots_dir = "docs/kb/snapshots"
    legacy_dir = "docs/kb/snapshots/legacy"
    
    # Modo overwrite: eliminar todos los snapshots actuales
    if OVERWRITE_MODE:
        if VERBOSE: print("🔄 Modo overwrite activado - eliminando snapshots actuales...")
        if os.path.exists(snapshots_dir):
            for item in os.listdir(snapshots_dir):
                if item != "legacy" and os.path.isdir(os.path.join(snapshots_dir, item)):
                    if re.match(r'^\d{4}-\d{2}-\d{2}_\d{6}$', item):
                        shutil.rmtree(os.path.join(snapshots_dir, item))
                        if VERBOSE: print(f"🗑️ Eliminado snapshot: {item}")
        return
    
    # Buscar el snapshot más reciente (excluyendo el actual)
    existing_snapshots = []
    if os.path.exists(snapshots_dir):
        for item in os.listdir(snapshots_dir):
            if item != "legacy" and os.path.isdir(os.path.join(snapshots_dir, item)):
                # Verificar que sea un timestamp válido (YYYY-MM-DD_HHMMSS)
                if re.match(r'^\d{4}-\d{2}-\d{2}_\d{6}$', item):
                    existing_snapshots.append(item)
    
    if not existing_snapshots:
        if VERBOSE: print("ℹ️ No hay snapshots anteriores para mover a legacy.")
        return
    
    # Ordenar por timestamp y tomar el más reciente
    existing_snapshots.sort(reverse=True)
    latest_snapshot = existing_snapshots[0]
    
    # Mover el snapshot anterior a legacy
    source_path = os.path.join(snapshots_dir, latest_snapshot)
    dest_path = os.path.join(legacy_dir, latest_snapshot)
    
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    
    shutil.move(source_path, dest_path)
    print(f"✅ Snapshot anterior movido a legacy: {latest_snapshot}")

# Solo hacer backup de archivos individuales si existen
def backup_individual_files():
    """Hace backup de archivos individuales a legacy"""
    to_backup = [OUT_README, SRC_KB_COLAB, SRC_KB_MIN]
    existing = [p for p in to_backup if os.path.exists(p)]
    
    if not existing:
        return
    
    legacy_dir = "docs/kb/snapshots/legacy"
    os.makedirs(legacy_dir, exist_ok=True)
    
    for p in existing:
        dest_path = os.path.join(legacy_dir, os.path.basename(p))
        shutil.copy2(p, dest_path)
    
    print(f"✅ Archivos individuales respaldados en legacy: {len(existing)} archivo(s).")

# Ejecutar backups
backup_existing()
backup_individual_files()

# Crear directorio del nuevo snapshot después del backup
_create_snapshot_directory()

# Las comparaciones se harán después de definir todas las funciones

# -------------------- Paso 2: Recolección heurística --------------------------
title = pathlib.Path(PROJECT_DIR).name
tree_text  = _directory_tree(PROJECT_DIR, max_depth=MAX_TREE_DEPTH, ignore_dirs=IGNORE_DIRS)
files_all  = _collect_files(PROJECT_DIR)
py_files   = [f for f in files_all if f.endswith(".py")]
nb_files   = [f for f in files_all if f.endswith(".ipynb")]
yaml_files = [f for f in files_all if f.endswith((".yaml",".yml"))]
json_files = [f for f in files_all if f.endswith(".json")]
md_files   = [f for f in files_all if f.endswith(".md")]

if VERBOSE:
    print(f"📊 Archivos: total={len(files_all)} | py={len(py_files)} ipynb={len(nb_files)} yaml={len(yaml_files)} json={len(json_files)} md={len(md_files)}")

# Bloques por módulo .py (incluye imports, funcs, clases, excerpt y UI)
apis_md_blocks: List[str] = []
for p in py_files:
    rel = os.path.relpath(p, PROJECT_DIR)
    info = _summarize_py_api(p, max_items=80)
    funcs   = ", ".join([f"{d['name']}({', '.join(d['args'])})" for d in info["funcs"]]) or "—"
    classes = ", ".join([f"{c['name']}[{', '.join(c['methods'][:12])}]" for c in info["classes"]]) or "—"

    text = _read_text(p, max_chars=160_000)
    ui = _ui_heuristics(p, text)

    block = [f"#### `{rel}`"]
    if info.get("module_doc"):
        block.append(f"**Docstring:** {str(info['module_doc'])[:500].strip()}")
    if info.get("imports"):
        block.append("**Imports:** " + ", ".join(info["imports"]))
    block.append(f"**Funciones:** {funcs}")
    block.append(f"**Clases:** {classes}")

    if ui.get("ui_detected"):
        hooks = ui.get("hooks") or []
        widgets = ui.get("widgets") or []
        details = []
        if hooks:   details.append(f"hooks: {', '.join(hooks)}")
        if widgets: details.append(f"widgets: {', '.join(widgets)}")
        block.append("**UI (heurística Streamlit):** " + ("; ".join(details) if details else "detectada"))

    if text:
        block.append(
            "<details><summary>Excerpt (head/tail)</summary>\n\n```python\n" +
            _head_tail_excerpt(text, *HEAD_TAIL_LINES) + "\n```\n</details>"
        )
    apis_md_blocks.append("\n".join(block))

apis_joined = "\n\n".join(apis_md_blocks)

# Muestreo de notebooks / YAML / JSON para contexto (no saturar)
def _head_excerpt(path: str, n_lines: int = 80) -> str:
    t = _read_text(path, max_chars=120_000)
    return "\n".join((t or "").splitlines()[:n_lines])

nb_summaries = []
for nb in nb_files[:12]:
    rel = os.path.relpath(nb, PROJECT_DIR)
    info = _summarize_ipynb(nb)
    nb_summaries.append(f"- **{rel}** · Celdas: {info.get('cells',0)} · Imports: {', '.join(info.get('imports',[]))[:200]}")
yaml_heads = [f"- **{os.path.relpath(y, PROJECT_DIR)}**\n```\n{_head_excerpt(y, 40)}\n```" for y in yaml_files[:6]]
json_heads = [f"- **{os.path.relpath(j, PROJECT_DIR)}**\n```\n{_head_excerpt(j, 30)}\n```" for j in json_files[:6]]

kb_colab_text = _read_text(SRC_KB_COLAB)
kb_min_text   = _read_text(SRC_KB_MIN)
readme_prev   = _read_text(OUT_README)
prev_kb_text  = None  # Ya no generamos KB monolítico
VERSION       = _bump_version_from_text(prev_kb_text or kb_min_text or kb_colab_text or readme_prev, fallback="v1.0")

# -------------------- Paso 3: LLM helper y prompts por sección ----------------
def _llm_call(section: str, prompt: str, max_tokens: int = 700) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        if VERBOSE: print(f"⚠️ OPENAI_API_KEY no seteada → sección '{section}' sin LLM.")
        return f"_{section}: contenido placeholder (sin LLM)_"
    try:
        from openai import OpenAI  # pip install openai
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system",
                 "content": "Eres un editor técnico en español neutro. Escribes conciso, accionable y claro, sin paja."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ Error LLM en '{section}':", e)
        return f"_{section}: fallback por error de LLM_"

def summarize_change_with_llm(diff_text: str, file_name: str) -> str:
    """
    Hace una llamada al LLM para resumir los cambios de un archivo específico.
    
    Args:
        diff_text: El diff del archivo
        file_name: Nombre del archivo
        
    Returns:
        Resumen en texto plano de los cambios
    """
    if not diff_text.strip():
        return f"Archivo {file_name}: Sin cambios detectados"
    
    prompt = f"""Este es el diff del archivo {file_name}. Resume los cambios en lenguaje natural:

{diff_text[:2000]}

Resume de forma concisa qué cambió en este archivo específico."""
    
    return _llm_call(f"cambio_{file_name}", prompt, max_tokens=200)

def _ctx_block(limit:int=3500) -> str:
    if not EDITORIAL_CONTEXT: return ""
    return f"\n---\nCONTEXTO EDITORIAL (Markdown del autor):\n{EDITORIAL_CONTEXT[:limit]}\n---\n"

def _mk_prompt_resumen():
    # Pre-procesar el contenido para evitar problemas con backslashes en f-strings
    yaml_content = '\n'.join(yaml_heads[:2])[:1200] if yaml_heads else ""
    
    return textwrap.dedent(f"""
    CONTEXTO (extractos técnicos):
    - Árbol (resumen):
    {tree_text[:3900]}

    - APIs mínimas (extracto):
    {apis_joined[:3500]}

    - Notebooks (muestra):
    {'; '.join(nb_summaries)[:1500]}

    - YAML/JSON (muestras de encabezado):
    {yaml_content}
    {_ctx_block(2500)}

    TAREA:
    Escribe un **Resumen ejecutivo** (5–8 viñetas) que explique:
    - Qué es ennui-rag y qué resuelve
    - Entradas/salidas y persistencia
    - Estado actual y cobertura
    - Puntos diferenciales (idempotencia, CSV por proyecto, UI Streamlit opcional)
    - Escollos y límites actuales
    Integra el contexto editorial cuando ayude a precisar el estado.
    """)

def _mk_prompt_arquitectura():
    return textwrap.dedent(f"""
    CONTEXTO:
    - Árbol:
    {tree_text[:3900]}

    - APIs mínimas:
    {apis_joined[:3500]}
    {_ctx_block(2000)}

    TAREA:
    Redacta **Arquitectura y flujo** (máx 300 palabras) explicando:
    - Capas (indexing, pipelines, io, persistence, settings, app/ui)
    - Flujo Drive→DF→CSV→records→stores
    - Dónde vive la configuración / clientes
    - Cómo encaja la UI de Streamlit
    Integra puntos del contexto editorial si afectan el diseño o cambios recientes.
    """)

def _mk_prompt_pipelines():
    return textwrap.dedent(f"""
    CONTEXTO:
    {apis_joined[:3500]}
    {_ctx_block(2000)}

    TAREA:
    Explica **Pipelines clave** (bullets):
    - project_pipeline: select_project, ensure_catalog, project_status, list_recent_projects
    - index_pipeline: run_index (parámetros y efectos)
    - enrich_pipeline: (si aplica ahora o futuro)
    Incorpora matices del contexto editorial sobre cambios o límites actuales.
    """)

def _mk_prompt_persistencia():
    return textwrap.dedent(f"""
    CONTEXTO:
    { (kb_colab_text or '')[:2000] }
    {_ctx_block(1600)}

    TAREA:
    Explica **Persistencia de datos**:
    - Sanitización (NaN/Inf→None; enteros)
    - Deduplicación por (file_id, drive_id) manteniendo modified reciente
    - SupabaseStore (on_conflict) y MongoStore (índices)
    Añade 1–2 recomendaciones operativas derivadas del contexto editorial si corresponde.
    """)

def _mk_prompt_adrs():
    return textwrap.dedent(f"""
    CONTEXTO:
    - Árbol:
    {tree_text[:2000]}
    {_ctx_block(1200)}

    TAREA:
    Lista 4–7 **Decisiones de diseño (ADR-lite)**: decisión → motivación → consecuencias.
    Cubre CSV por proyecto, clave compuesta, idempotencia, UI Streamlit, límites Colab/Drive.
    Alinea con el contexto editorial si este describe cambios recientes.
    """)

def _mk_prompt_riesgos():
    return textwrap.dedent(f"""
    {_ctx_block(1200)}
    TAREA:
    Genera 5–8 **Riesgos y mitigaciones** (bullets) para indexación Drive, límites API, datos corruptos,
    tiempos, costos y entorno Colab, integrando riesgos mencionados en el contexto editorial.
    """)

def _mk_prompt_roadmap():
    # Cargar documentación de diseño actual
    design_current = ""
    design_files = [
        "docs/design/current/README.md",
        "docs/design/current/vision-narrativa/Vision · ennui-rag · v0.1 — 2025-09-15.md",
        "docs/design/current/erd-objetivo/ERD Objetivo · ennui-rag · v0.1 — 2025-09-15.md",
        "docs/design/current/blueprints/Arquitectura Lógica · v0.1 — 2025-09-15.md",
        "docs/design/current/decisiones/ADR-0001 Monorepo · v0.1 — 2025-09-15.md",
        "docs/design/current/decisiones/ADR-0002 Seeds-vs-CSV · v0.1 — 2025-09-15.md"
    ]
    
    for design_file in design_files:
        if os.path.exists(design_file):
            design_current += f"\n--- {design_file} ---\n"
            design_current += _read_text(design_file, max_chars=3000)
    
    return textwrap.dedent(f"""
    CONTEXTO:
    - Proyecto: {title} (sistema RAG para Google Drive)
    - Estado actual: Indexación estable, persistencia idempotente, UI Streamlit funcional
    - Arquitectura: Pipelines de indexación, enriquecimiento, persistencia en Supabase/MongoDB
    - APIs detectadas: {len(apis_md_blocks)} módulos Python con {sum(len(info.get('funcs', [])) for info in [_summarize_py_api(f) for f in py_files[:10]])} funciones
    
    DOCUMENTACIÓN DE DISEÑO ACTUAL:
    {design_current[:5000]}
    
    {_ctx_block(1000)}

    TAREA:
    Escribe un **Roadmap basado ÚNICAMENTE en la documentación de diseño** que:
    
    1. **Si NO hay planes específicos en la documentación de diseño**: 
       - Escribe "No hay planes específicos documentados en docs/design/current"
       - NO inventes ningún roadmap
    
    2. **Si SÍ hay planes en la documentación de diseño**:
       - Lista SOLO los planes que estén explícitamente documentados
       - Para cada plan, indica si se ha cumplido o está pendiente
       - Usa el estado actual del sistema para determinar el cumplimiento
       - NO agregues planes que no estén en la documentación
    
    3. **Si no hay cambios en los planes de diseño**:
       - Escribe "No hay cambios en los planes de diseño desde la última versión"
    
    IMPORTANTE: 
    - NO inventes pasos que no estén en la documentación de diseño
    - NO agregues mejoras o optimizaciones no documentadas
    - Solo reporta lo que esté explícitamente en docs/design/current
    """)

def _mk_prompt_operacion():
    return textwrap.dedent(f"""
    CONTEXTO:
    - Snippets típicos (select_project, ensure_catalog, run_index) y entorno Colab.
    {_ctx_block(1000)}

    TAREA:
    Redacta **Operación / Cómo correr** (pasos claros + bloques de código breves).
    Integra aclaraciones del contexto editorial (p.ej., flags temporales, límites actuales).
    """)

# Archivos a comparar (excluyendo notas-cambio.md)
FILES_TO_COMPARE = [
    'resumen-ejecutivo.md',
    'arquitectura-flujo.md', 
    'arbol-modulos.md',
    'operacion-troubleshooting.md'
]

def compare_file(file_name: str, curr_dir: str, prev_dir: str) -> Dict[str, Any]:
    """
    Compara un archivo específico entre dos directorios.
    
    Returns:
        Dict con:
        - changed: bool - si el archivo cambió
        - diff_text: str - texto del diff generado
        - lines_added: int - líneas añadidas
        - lines_removed: int - líneas eliminadas
        - lines_modified: int - líneas modificadas
    """
    current_file = os.path.join(curr_dir, file_name)
    previous_file = os.path.join(prev_dir, file_name)
    
    if not os.path.exists(current_file) or not os.path.exists(previous_file):
        return {
            "changed": False,
            "diff_text": "",
            "lines_added": 0,
            "lines_removed": 0,
            "lines_modified": 0
        }
    
    current_content = _read_text(current_file, max_chars=5000)
    previous_content = _read_text(previous_file, max_chars=5000)
    
    if current_content == previous_content:
        return {
            "changed": False,
            "diff_text": "",
            "lines_added": 0,
            "lines_removed": 0,
            "lines_modified": 0
        }
    
    # Generar diff simple línea por línea
    current_lines = current_content.split('\n')
    previous_lines = previous_content.split('\n')
    
    diff_lines = []
    lines_added = 0
    lines_removed = 0
    lines_modified = 0
    
    max_lines = max(len(current_lines), len(previous_lines))
    
    for i in range(max_lines):
        current_line = current_lines[i] if i < len(current_lines) else ""
        previous_line = previous_lines[i] if i < len(previous_lines) else ""
        
        if i >= len(previous_lines):
            # Línea nueva
            diff_lines.append(f"+ {current_line}")
            lines_added += 1
        elif i >= len(current_lines):
            # Línea eliminada
            diff_lines.append(f"- {previous_line}")
            lines_removed += 1
        elif current_line != previous_line:
            # Línea modificada
            diff_lines.append(f"- {previous_line}")
            diff_lines.append(f"+ {current_line}")
            lines_modified += 1
    
    diff_text = "\n".join(diff_lines)
    
    return {
        "changed": True,
        "diff_text": diff_text,
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "lines_modified": lines_modified
    }

def _compare_snapshots():
    """Compara archivos entre el snapshot actual y el anterior"""
    snapshots_dir = "docs/kb/snapshots"
    legacy_dir = "docs/kb/snapshots/legacy"
    current_snapshot = SNAPSHOT_TIMESTAMP
    
    # Buscar snapshot anterior (primero en snapshots, luego en legacy)
    previous_snapshot = None
    previous_dir = None
    
    # Buscar en snapshots actuales
    if os.path.exists(snapshots_dir):
        snapshots = []
        for item in os.listdir(snapshots_dir):
            if item != "legacy" and os.path.isdir(os.path.join(snapshots_dir, item)):
                if re.match(r'^\d{4}-\d{2}-\d{2}_\d{6}$', item) and item != current_snapshot:
                    snapshots.append(item)
        
        if snapshots:
            snapshots.sort(reverse=True)
            previous_snapshot = snapshots[0]
            previous_dir = os.path.join(snapshots_dir, previous_snapshot)
    
    # Si no hay en snapshots, buscar en legacy
    if not previous_snapshot and os.path.exists(legacy_dir):
        legacy_snapshots = []
        for item in os.listdir(legacy_dir):
            if os.path.isdir(os.path.join(legacy_dir, item)):
                if re.match(r'^\d{4}-\d{2}-\d{2}_\d{6}$', item):
                    legacy_snapshots.append(item)
        
        if legacy_snapshots:
            legacy_snapshots.sort(reverse=True)
            previous_snapshot = legacy_snapshots[0]
            previous_dir = os.path.join(legacy_dir, previous_snapshot)
    
    if not previous_snapshot:
        return "No hay snapshot anterior para comparar."
    
    # Comparar archivos
    current_dir = os.path.join(snapshots_dir, current_snapshot)
    
    comparison = f"COMPARACIÓN REAL DE ARCHIVOS: {previous_snapshot} → {current_snapshot}\n"
    comparison += "=" * 80 + "\n\n"
    
    for filename in FILES_TO_COMPARE:
        file_comparison = compare_file(filename, current_dir, previous_dir)
        
        if file_comparison["changed"]:
            comparison += f"📄 ARCHIVO: {filename}\n"
            comparison += f"📅 Anterior: {previous_snapshot}\n"
            comparison += f"📅 Actual: {current_snapshot}\n"
            comparison += f"📊 Estado: CAMBIADO\n"
            comparison += f"📈 Líneas: +{file_comparison['lines_added']} -{file_comparison['lines_removed']} ~{file_comparison['lines_modified']}\n\n"
            
            # Mostrar diferencias específicas
            comparison += "🔍 DIFERENCIAS DETECTADAS:\n"
            comparison += "-" * 40 + "\n"
            comparison += file_comparison["diff_text"][:1000]  # Limitar tamaño
            comparison += "\n\n" + "=" * 80 + "\n\n"
        else:
            comparison += f"📄 ARCHIVO: {filename} - SIN CAMBIOS\n\n"
    
    return comparison

def _process_files_individually():
    """
    Procesa archivos individualmente, generando resúmenes por archivo.
    
    Returns:
        Lista de reportes por archivo con resúmenes de cambios
    """
    snapshots_dir = "docs/kb/snapshots"
    legacy_dir = "docs/kb/snapshots/legacy"
    current_snapshot = SNAPSHOT_TIMESTAMP
    
    if VERBOSE:
        print(f"🔍 DEBUG: Buscando snapshot anterior para comparar con {current_snapshot}")
        print(f"🔍 DEBUG: snapshots_dir existe: {os.path.exists(snapshots_dir)}")
        print(f"🔍 DEBUG: legacy_dir existe: {os.path.exists(legacy_dir)}")
    
    # Nueva lógica de comparación:
    # 1. Si existe un snapshot vigente, usarlo para comparar (ya fue movido a legacy por backup_existing)
    # 2. Si no existe snapshot vigente, usar el último en legacy para comparar
    previous_snapshot = None
    previous_dir = None
    
    # Buscar en snapshots actuales (excluyendo el actual)
    current_snapshots = []
    if os.path.exists(snapshots_dir):
        for item in os.listdir(snapshots_dir):
            if item != "legacy" and os.path.isdir(os.path.join(snapshots_dir, item)):
                if re.match(r'^\d{4}-\d{2}-\d{2}_\d{6}$', item) and item != current_snapshot:
                    current_snapshots.append(item)
    
    if VERBOSE:
        print(f"🔍 DEBUG: Snapshots actuales encontrados: {current_snapshots}")
    
    # Si hay snapshots actuales, usar el más reciente para comparar
    if current_snapshots:
        current_snapshots.sort(reverse=True)
        previous_snapshot = current_snapshots[0]
        previous_dir = os.path.join(snapshots_dir, previous_snapshot)
        if VERBOSE:
            print(f"🔍 DEBUG: Usando snapshot actual más reciente: {previous_snapshot}")
    else:
        # Si no hay snapshots actuales, buscar en legacy
        if os.path.exists(legacy_dir):
            legacy_snapshots = []
            for item in os.listdir(legacy_dir):
                if os.path.isdir(os.path.join(legacy_dir, item)):
                    if re.match(r'^\d{4}-\d{2}-\d{2}_\d{6}$', item):
                        legacy_snapshots.append(item)
            
            if VERBOSE:
                print(f"🔍 DEBUG: Snapshots encontrados en legacy/: {legacy_snapshots}")
            
            if legacy_snapshots:
                legacy_snapshots.sort(reverse=True)
                # Usar el snapshot más antiguo de legacy para detectar cambios reales
                previous_snapshot = legacy_snapshots[-1]  # El más antiguo
                previous_dir = os.path.join(legacy_dir, previous_snapshot)
                if VERBOSE:
                    print(f"🔍 DEBUG: Usando snapshot más antiguo de legacy/: {previous_snapshot}")
    
    if not previous_snapshot:
        if VERBOSE:
            print("🔍 DEBUG: No se encontró ningún snapshot anterior")
        return []
    
    # Procesar archivos individualmente
    current_dir = os.path.join(snapshots_dir, current_snapshot)
    per_file_reports = []
    
    for filename in FILES_TO_COMPARE:
        file_comparison = compare_file(filename, current_dir, previous_dir)
        
        if VERBOSE:
            print(f"🔍 DEBUG: Comparando {filename}: changed={file_comparison['changed']}")
            if file_comparison["changed"]:
                print(f"🔍 DEBUG: {filename} - +{file_comparison['lines_added']} -{file_comparison['lines_removed']} ~{file_comparison['lines_modified']}")
                print(f"🔍 DEBUG: {filename} - diff_text preview: {file_comparison['diff_text'][:200]}...")
        
        if file_comparison["changed"]:
            # Generar resumen con LLM
            summary = summarize_change_with_llm(file_comparison["diff_text"], filename)
            
            per_file_reports.append({
                "file_name": filename,
                "changed": True,
                "summary": summary,
                "lines_added": file_comparison["lines_added"],
                "lines_removed": file_comparison["lines_removed"],
                "lines_modified": file_comparison["lines_modified"],
                "diff_text": file_comparison["diff_text"]
            })
        else:
            per_file_reports.append({
                "file_name": filename,
                "changed": False,
                "summary": f"Archivo {filename}: Sin cambios",
                "lines_added": 0,
                "lines_removed": 0,
                "lines_modified": 0,
                "diff_text": ""
            })
    
    return per_file_reports

def _generate_notas_cambio_from_reports(per_file_reports: List[Dict[str, Any]]) -> str:
    """
    Genera las notas de cambio concatenando los resúmenes individuales.
    
    Args:
        per_file_reports: Lista de reportes por archivo
        
    Returns:
        Texto de notas de cambio concatenado
    """
    if not per_file_reports:
        return "No hay snapshot anterior para comparar."
    
    # Filtrar solo archivos que cambiaron
    changed_files = [report for report in per_file_reports if report["changed"]]
    
    if not changed_files:
        return "No se detectaron cambios en los archivos del KB."
    
    # Concatenar resúmenes individuales
    notas = []
    notas.append("## Cambios en el KB\n")
    
    for report in changed_files:
        notas.append(f"### {report['file_name']}")
        notas.append(f"**Resumen:** {report['summary']}")
        notas.append(f"**Estadísticas:** +{report['lines_added']} líneas añadidas, -{report['lines_removed']} líneas eliminadas, ~{report['lines_modified']} líneas modificadas")
        notas.append("")  # Línea en blanco
    
    return "\n".join(notas)

def _generate_resumen_ejecutivo_independiente() -> str:
    """
    Genera el resumen ejecutivo de forma independiente, sin depender de notas_cambio.
    Toma directamente las versiones actuales de los archivos clave.
    """
    # Leer archivos clave actuales
    snapshots_dir = "docs/kb/snapshots"
    current_snapshot = SNAPSHOT_TIMESTAMP
    current_dir = os.path.join(snapshots_dir, current_snapshot)
    
    # Archivos clave para el resumen
    key_files = {
        'description': 'resumen-ejecutivo.md',
        'status': 'operacion-troubleshooting.md',
        'architecture': 'arquitectura-flujo.md'
    }
    
    current_content = {}
    for key, filename in key_files.items():
        file_path = os.path.join(current_dir, filename)
        if os.path.exists(file_path):
            current_content[key] = _read_text(file_path, max_chars=2000)
        else:
            current_content[key] = f"Archivo {filename} no encontrado"
    
    # Crear prompt con contenido actual
    prompt = f"""
    CONTEXTO ACTUAL DEL SISTEMA:
    
    - Descripción actual: {current_content.get('description', 'No disponible')}
    - Estado operacional: {current_content.get('status', 'No disponible')}
    - Arquitectura: {current_content.get('architecture', 'No disponible')}
    
    {_ctx_block(1000)}
    
    TAREA:
    Escribe un **Resumen ejecutivo actualizado** (5–8 viñetas) que explique:
    - Qué es ennui-rag y qué resuelve actualmente
    - Entradas/salidas y persistencia actual
    - Estado actual y cobertura
    - Puntos diferenciales (idempotencia, CSV por proyecto, UI Streamlit opcional)
    - Escollos y límites actuales
    Integra el contexto editorial cuando ayude a precisar el estado actual.
    """
    
    return _llm_call("resumen_independiente", prompt, max_tokens=550)

def _mk_prompt_cambios_kb():
    """Genera prompt para comparación de cambios en KB"""
    comparison = _compare_snapshots()

    return textwrap.dedent(f"""
    CONTEXTO DE COMPARACIÓN REAL:
    {comparison}

    {_ctx_block(2000)}

    TAREA:
    Analiza ÚNICAMENTE la comparación real proporcionada arriba y escribe una **Comparación archivo por archivo** que:

    1. **Para cada archivo que cambió** (según la comparación real):
      - Menciona el nombre específico del archivo
      - Reporta SOLO las diferencias específicas mostradas en la comparación real
      - Usa bullets para cada diferencia específica encontrada
      - NO inventes diferencias que no estén en la comparación real

    2. **Resumen general del estado del sistema**:
      - Describe el estado actual general del proyecto ennui-rag
      - Menciona las mejoras o cambios principales implementados
      - Explica el impacto de los cambios en el sistema

    REGLAS ESTRICTAS:
    - USA EXACTAMENTE la información de la comparación real proporcionada
    - NO inventes cambios que no estén en la comparación real
    - NO menciones timestamps como "181731" - habla de archivos específicos
    - Solo reporta diferencias reales documentadas en la comparación
    - Si un archivo no cambió, NO lo menciones
    - Si no hay diferencias específicas mostradas, NO inventes detalles
    - Usa el contexto editorial para explicar el por qué de los cambios
    - Formato: "Archivo X: [diferencias específicas de la comparación real]"
    """)

# Hacer la comparación ANTES de generar los archivos del snapshot
# Esto asegura que comparamos contra el snapshot anterior, no contra el actual
if not MODO_ORIGINAL:
    per_file_reports = _process_files_individually()
    sec_cambios_kb = _generate_notas_cambio_from_reports(per_file_reports)
    sec_resumen = _generate_resumen_ejecutivo_independiente()
else:
    per_file_reports = []
    sec_cambios_kb = ""
    sec_resumen = ""

# LLM por sección (independientes)
if MODO_ORIGINAL:
    # Lógica original (solo cuando se especifica --modo-original)
    sec_resumen       = _llm_call("resumen", _mk_prompt_resumen(), max_tokens=550)
    sec_arquitectura  = _llm_call("arquitectura", _mk_prompt_arquitectura(), max_tokens=450)
    sec_pipelines     = _llm_call("pipelines", _mk_prompt_pipelines(), max_tokens=450)
    sec_persistencia  = _llm_call("persistencia", _mk_prompt_persistencia(), max_tokens=380)
    sec_adrs          = _llm_call("decisiones", _mk_prompt_adrs(), max_tokens=380)
    sec_riesgos       = _llm_call("riesgos", _mk_prompt_riesgos(), max_tokens=320)
    sec_roadmap       = _llm_call("roadmap", _mk_prompt_roadmap(), max_tokens=260)
    sec_operacion     = _llm_call("operacion", _mk_prompt_operacion(), max_tokens=420)
    sec_cambios_kb    = _llm_call("cambios_kb", _mk_prompt_cambios_kb(), max_tokens=400)
    
    if VERBOSE:
        print("🔧 Modo original activado - usando comparación monolítica")
else:
    # Ya se procesaron los archivos individualmente arriba, solo generar otras secciones
    # Generar otras secciones normalmente
    sec_arquitectura  = _llm_call("arquitectura", _mk_prompt_arquitectura(), max_tokens=450)
    sec_pipelines     = _llm_call("pipelines", _mk_prompt_pipelines(), max_tokens=450)
    sec_persistencia  = _llm_call("persistencia", _mk_prompt_persistencia(), max_tokens=380)
    sec_adrs          = _llm_call("decisiones", _mk_prompt_adrs(), max_tokens=380)
    sec_riesgos       = _llm_call("riesgos", _mk_prompt_riesgos(), max_tokens=320)
    sec_roadmap       = _llm_call("roadmap", _mk_prompt_roadmap(), max_tokens=260)
    sec_operacion     = _llm_call("operacion", _mk_prompt_operacion(), max_tokens=420)
    
    if VERBOSE:
        print("🔧 Modo por archivo (por defecto) - procesando cambios individualmente")

# -------------------- Paso 3: LLM helper y prompts por sección ----------------
def generate_snapshot_files():
    """Genera los archivos especializados del snapshot con front-matter"""
    global title, tree_text, apis_joined, sec_resumen, sec_arquitectura, sec_pipelines, sec_persistencia, sec_adrs, sec_riesgos, sec_roadmap, sec_operacion, sec_cambios_kb, EDITORIAL_CONTEXT, SNAPSHOT_TIMESTAMP, DATE_ES
    
    # Mapeo de contenido para cada archivo
    snapshot_content = {
        'resumen-ejecutivo.md': sec_resumen or "_Sin datos_",
        'arquitectura-flujo.md': sec_arquitectura or "_Sin datos_",
        'arbol-modulos.md': f"# {title} · Estructura de Archivos\n\n## 📁 Estructura Completa del Proyecto\n\n```\n{tree_text}\n```\n\n## 🧩 Módulos y API mínima\n{apis_joined or '_No se detectaron módulos .py_'}\n\n## 🧵 Pipelines clave\n{sec_pipelines or '_Sin datos_'}\n\n## 💾 Persistencia de datos\n{sec_persistencia or '_Sin datos_'}\n\n## 📐 Decisiones (ADR-lite)\n{sec_adrs or '_Sin datos_'}\n\n## ⚠️ Riesgos y mitigaciones\n{sec_riesgos or '_Sin datos_'}\n\n## 🗺️ Roadmap\n{sec_roadmap or '_Sin datos_'}\n\n---\n> Generado con Python a partir del árbol de archivos, parsers AST y extractos de docs/notebooks, con secciones enriquecidas por LLM (OpenAI).",
        'operacion-troubleshooting.md': f"{sec_operacion or '_Sin datos_'}\n\n## 🛠️ Troubleshooting\n- Revisa claves/entorno (`SB_SECRET`, `MONGO_URI`, `OPENAI_API_KEY`).\n- Si falla Drive: re-montar y reintentar.\n- Si hay columnas faltantes en DF: valida `normalize` y utilidades.\n- Conflictos `ON CONFLICT`: alinea índices únicos.\n- UI: si Streamlit no carga, valida versión de `streamlit` y puertos.",
        'notas-cambio.md': f"# Notas de Cambio - {SNAPSHOT_TIMESTAMP}\n\n## Cambios en el KB\n\n{sec_cambios_kb or '_Sin cambios detectados en el KB_'}\n\n## Roadmap\n\n{sec_roadmap or '_Sin roadmap basado en planes de diseño_'}\n\n## Contexto editorial\n\n{EDITORIAL_CONTEXT or '_Sin contexto editorial_'}\n\n---\n> Snapshot generado el {DATE_ES}"
    }
    
    # Generar cada archivo del snapshot
    for filename, title in SNAPSHOT_FILES.items():
        content = snapshot_content.get(filename, "_Sin datos_")
        full_content = _generate_frontmatter(title) + content
        file_path = os.path.join(SNAPSHOT_DIR, filename)
        _write_text(file_path, full_content)
        print(f"📄 Snapshot generado: {filename}")
    
    print(f"✅ Snapshot completo generado en: {SNAPSHOT_DIR}")

# Generar archivos del snapshot
generate_snapshot_files()

# -------------------- Paso 5: README robusto ---------------------------------
def _build_readme() -> str:
    ver  = _bump_version_from_text(readme_prev or "v1.0", fallback="v1.0")
    readme = []
    readme.append("# ennui-rag")
    readme.append("> Sistema RAG para Google Drive (Colab) con persistencia en Supabase/Mongo y CSV por proyecto.")
    readme.append("\n## ✨ Propósito y alcance\n- Indexar carpetas de Drive por proyecto.\n- Normalizar a CSV y preparar registros.\n- Persistir con idempotencia en BD.\n- Enriquecer (descripciones/embeddings) en siguiente fase.")
    readme.append("\n## 📦 Instalación / Setup (Colab)\n1. Monta Google Drive.\n2. Abre `notebooks/ennui-rag-v1.ipynb`.\n3. `pip install -r requirements.txt`.\n4. Variables: `SB_SECRET`, `MONGO_URI`, `OPENAI_API_KEY` (si usarás LLM).")
    readme.append("\n## ⚡️ Uso rápido\n```python\nfrom ennui_rag.pipelines import select_project, ensure_catalog, project_status\nproj = select_project('<folder_id>')\ncsv_path = ensure_catalog(proj['project_id'], force=False, persist=True)\nprint(project_status(proj['project_id']))\n```\n```python\nfrom ennui_rag.pipelines import run_index\ndf = run_index(env='dev', folder_id='<folder_id>', max_items=500)\n```")
    readme.append("\n## 📂 Estructura mínima\n```\nennui-rag-v1/\n├─ notebooks/ennui-rag-v1.ipynb\n├─ src/ennui_rag/{settings.py, pipelines/, indexing/, persistence/, io/, app/}\n├─ configs/{base,dev}.yaml\n├─ data/<project_id>/{catalog_base.csv,sessions.json}\n└─ requirements.txt\n```")
    readme.append("\n## 🔎 Estado actual")
    readme.append("- Indexación estable (DFS con Shortcuts/Shared Drives).")
    readme.append("- CSV por proyecto y sessions.json.")
    readme.append("- Persistencia idempotente en BD.")
    readme.append("- UI Streamlit funcional (secciones: indexing, enrichment, state).")
    # 🔹 Integra el contexto editorial dentro de “Estado actual”, no como sección nueva.
    if EDITORIAL_CONTEXT:
        readme.append("\n**Notas recientes (del autor):**\n")
        readme.append(EDITORIAL_CONTEXT.strip()[:2000])  # limitar para que no sea enorme
    readme.append("\n## 🧭 Roadmap breve\n- Enrichment (descripciones + embeddings).\n- Test suite.\n- Métricas de indexación/persistencia.\n- Vector store opcional.")
    readme.append("\n---\n> Breve descripción de la fuente del contenido: README generado automáticamente desde `KB_ennui_rag_v1.md` y estado del repositorio.\n")
    readme.append(f"{ver} — Generado el {_spanish_date(datetime.datetime.now())}")
    return "\n".join(readme)

if GENERATE_README:
    _write_text(OUT_README, _build_readme())
    print(f"📘 README escrito: {OUT_README}")
else:
    print("ℹ️ README no regenerado (usa --readme para generarlo).")

# -------------------- Paso 6: Limpieza y resumen final -------------------------
def _safe_remove(path: str):
    try:
        if os.path.exists(path):
            os.remove(path); print(f"🧹 Retirado: {path}")
    except Exception as e:
        print(f"ℹ️ No se pudo retirar {path}:", e)

# Limpiar archivos antiguos (opcional)
    if os.getenv("CLEANUP_OLD", "false").lower() == "true":
        _safe_remove(SRC_KB_COLAB)
        _safe_remove(SRC_KB_MIN)

print(f"\n🎉 Generación completada!")
print(f"📁 Snapshot: {SNAPSHOT_DIR}")
print(f"📚 Archivos generados: {len(SNAPSHOT_FILES)}")
print(f"💾 Legacy: docs/kb/snapshots/legacy/")

print("✅ Listo. Snapshot generado con archivos especializados.")
