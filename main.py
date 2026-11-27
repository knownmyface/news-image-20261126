import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
shutil.copyfile(os.path.join(HERE, "entry.png"), out)
print(f"copied entry.png -> {out}")
