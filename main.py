"""Deterministic renderer entry point for the 20 November 2026 news image."""
from __future__ import annotations
import os, sys, tempfile, zipfile, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
try:
    import PIL  # noqa: F401
except ImportError:
    tag = sys.implementation.cache_tag.rsplit("-", 1)[-1]
    wheel_tag = "cp" + tag.rstrip("t")
    wheels = sorted(p for p in (ROOT / "vendor").glob("*.whl") if f"-{wheel_tag}-" in p.name)
    if not wheels:
        raise RuntimeError(f"No bundled Pillow wheel matches {sys.implementation.cache_tag}")
    extraction = Path(tempfile.mkdtemp(prefix="makefun-pillow-"))
    with zipfile.ZipFile(wheels[0]) as wheel:
        wheel.extractall(extraction)
    sys.path.insert(0, str(extraction))
    import PIL  # noqa: F401
from draw import render

def main() -> None:
    data = json.loads((ROOT / "stories.json").read_text(encoding="utf-8"))
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    render(data, output_dir / "entry.png", ROOT / "assets")

if __name__ == "__main__":
    main()
