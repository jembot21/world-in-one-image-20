from pathlib import Path
import os
import shutil
import sys


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    shutil.copyfile(source, destination)
    print(f"Copied {destination.stat().st_size} image bytes to {destination}", file=sys.stderr)


if __name__ == "__main__":
    main()
