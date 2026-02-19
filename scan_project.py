# scan_project.py
import os
import re
import json
import ast
import sys
import subprocess
from pathlib import Path
from datetime import datetime

IGNORE_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build"}
IGNORE_EXTS = {".pyc", ".pyo", ".log", ".tmp"}
MAX_FILE_BYTES = 300_000  # 300 KB (big files skip to keep fast)

def safe_read_text(p: Path) -> str:
    try:
        data = p.read_bytes()
        if len(data) > MAX_FILE_BYTES:
            return ""
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""

def is_ignored(path: Path) -> bool:
    parts = set(path.parts)
    if parts & IGNORE_DIRS:
        return True
    if path.suffix in IGNORE_EXTS:
        return True
    return False

def find_files(root: Path):
    files = []
    for p in root.rglob("*"):
        if p.is_file() and not is_ignored(p):
            files.append(p)
    return files

def parse_imports_py(code: str):
    imports = set()
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.add(n.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
    except Exception:
        pass
    return sorted(imports)

def guess_entrypoints(files):
    names = {"main.py", "app.py", "run.py", "server.py", "bot.py", "__main__.py"}
    eps = []
    for f in files:
        if f.name in names:
            eps.append(str(f))
    return eps

def module_name_from_path(root: Path, p: Path):
    rel = p.relative_to(root)
    if rel.suffix != ".py":
        return None
    parts = list(rel.parts)
    parts[-1] = parts[-1].replace(".py", "")
    return ".".join(parts)

def build_py_index(root: Path, files):
    mod_to_path = {}
    path_to_mod = {}
    for f in files:
        if f.suffix == ".py":
            mn = module_name_from_path(root, f)
            if mn:
                mod_to_path[mn] = str(f)
                path_to_mod[str(f)] = mn
    return mod_to_path, path_to_mod

def find_local_import_edges(root: Path, files, mod_to_path):
    edges = []  # (src_file, imported_module, type)
    file_imports = {}
    for f in files:
        if f.suffix != ".py":
            continue
        code = safe_read_text(f)
        imps = parse_imports_py(code)
        file_imports[str(f)] = imps
        for m in imps:
            # local module heuristic: matches top-level folder/module in project
            # Example: scripts.core.edit_video => imports "scripts"
            if m in mod_to_path or (root / m).exists():
                edges.append((str(f), m, "local_or_project"))
            else:
                edges.append((str(f), m, "external_or_std"))
    return edges, file_imports

def read_requirements(root: Path):
    req = root / "requirements.txt"
    if not req.exists():
        return []
    lines = safe_read_text(req).splitlines()
    out = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out

def check_env(root: Path):
    envf = root / ".env"
    keys = []
    if envf.exists():
        txt = safe_read_text(envf)
        for line in txt.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k = line.split("=", 1)[0].strip()
            keys.append(k)
    return {"env_exists": envf.exists(), "keys_found": keys}

def run_smoke(root: Path):
    main = root / "main.py"
    if not main.exists():
        return {"ran": False, "error": "main.py not found"}
    try:
        # run with same python
        proc = subprocess.run(
            [sys.executable, str(main)],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "ran": True,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-5000:],
            "stderr": proc.stderr[-5000:]
        }
    except subprocess.TimeoutExpired:
        return {"ran": True, "returncode": None, "stdout": "", "stderr": "TIMEOUT (30s) - main.py kept running"}
    except Exception as e:
        return {"ran": False, "error": str(e)}

def top_used_modules(file_imports):
    freq = {}
    for f, imps in file_imports.items():
        for m in imps:
            freq[m] = freq.get(m, 0) + 1
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)

def guess_dead_files(root: Path, files, edges, entrypoints):
    # heuristic:
    # - if a .py file is never imported by any other .py and not an entrypoint, mark as maybe-dead
    imported_toplevel = set()
    for src, mod, typ in edges:
        if typ == "local_or_project":
            imported_toplevel.add(mod)

    maybe_dead = []
    for f in files:
        if f.suffix != ".py":
            continue
        fp = str(f)
        if fp in entrypoints:
            continue
        # top-level module name (first segment)
        rel = f.relative_to(root)
        top = rel.parts[0] if len(rel.parts) > 1 else rel.stem
        if top not in imported_toplevel:
            maybe_dead.append(fp)

    return sorted(set(maybe_dead))

def write_report(root: Path, summary: dict):
    md = []
    md.append(f"# SCAN REPORT\n")
    md.append(f"- Generated: {summary['meta']['generated_at']}\n")
    md.append(f"- Root: `{summary['meta']['root']}`\n")
    md.append(f"- Total files: {summary['counts']['total_files']}\n")
    md.append(f"- Python files: {summary['counts']['py_files']}\n")
    md.append(f"- Entrypoints: {', '.join(summary['entrypoints']) if summary['entrypoints'] else 'None'}\n")

    md.append("\n## .env\n")
    md.append(f"- Exists: {summary['env']['env_exists']}\n")
    md.append(f"- Keys found: {', '.join(summary['env']['keys_found']) if summary['env']['keys_found'] else 'None'}\n")

    md.append("\n## requirements.txt\n")
    if summary["requirements"]:
        for r in summary["requirements"][:200]:
            md.append(f"- {r}\n")
    else:
        md.append("- Not found or empty\n")

    md.append("\n## Top Imports (by frequency)\n")
    for m, c in summary["top_imports"][:40]:
        md.append(f"- `{m}` : {c}\n")

    md.append("\n## Suspected Dead/Unused Python Files (heuristic)\n")
    if summary["maybe_dead_files"]:
        for f in summary["maybe_dead_files"][:200]:
            md.append(f"- {f}\n")
    else:
        md.append("- None detected\n")

    md.append("\n## Smoke Test (run main.py)\n")
    smoke = summary["smoke_test"]
    md.append(f"- Ran: {smoke.get('ran')}\n")
    if "returncode" in smoke:
        md.append(f"- Return code: {smoke.get('returncode')}\n")
    if smoke.get("stdout"):
        md.append("\n### STDOUT (last part)\n")
        md.append("```\n" + smoke["stdout"] + "\n```\n")
    if smoke.get("stderr"):
        md.append("\n### STDERR (last part)\n")
        md.append("```\n" + smoke["stderr"] + "\n```\n")

    md.append("\n## Python Files Map (first ~200)\n")
    for f in summary["py_files"][:200]:
        md.append(f"- {f}\n")

    (root / "SCAN_REPORT.md").write_text("".join(md), encoding="utf-8")
    (root / "SCAN_SUMMARY.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

def main():
    root = Path(os.getcwd())
    files = find_files(root)
    py_files = [str(f) for f in files if f.suffix == ".py"]
    entrypoints = guess_entrypoints(files)
    mod_to_path, _ = build_py_index(root, files)
    edges, file_imports = find_local_import_edges(root, files, mod_to_path)

    summary = {
        "meta": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "root": str(root),
        },
        "counts": {
            "total_files": len(files),
            "py_files": len(py_files),
        },
        "entrypoints": entrypoints,
        "env": check_env(root),
        "requirements": read_requirements(root),
        "top_imports": top_used_modules(file_imports),
        "maybe_dead_files": guess_dead_files(root, files, edges, entrypoints),
        "py_files": sorted(py_files),
        "imports_by_file": file_imports,
        "edges": edges,
        "smoke_test": run_smoke(root),
    }

    write_report(root, summary)
    print("✅ Scan complete!")
    print("📄 Generated: SCAN_REPORT.md")
    print("🧾 Generated: SCAN_SUMMARY.json")

if __name__ == "__main__":
    main()
