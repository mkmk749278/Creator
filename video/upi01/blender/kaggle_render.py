# Builds a Kaggle GPU kernel that renders world.py (PLAYBOOK §4a-9: Blender hero shots on Kaggle GPU).
# Usage: python3 kaggle_render.py <outdir> -- <world.py args...> [--env KEY=VAL ...]
#   writes <outdir>/runner.py + kernel-metadata.json; then: kaggle kernels push -p <outdir>
import base64, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
outdir = sys.argv[1]; rest = sys.argv[sys.argv.index("--") + 1:]
env = dict(a.split("=", 1) for a in rest[rest.index("--env") + 1:]) if "--env" in rest else {}
wargs = rest[:rest.index("--env")] if "--env" in rest else rest
src = base64.b64encode(open(os.path.join(here, "world.py"), "rb").read()).decode()
font = base64.b64encode(open("/usr/share/fonts/opentype/inter/Inter-Bold.otf", "rb").read()).decode()  # OFL
runner = f'''import base64, os, subprocess, sys, time
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "bpy==5.2.2"], check=True)
open("world.py", "wb").write(base64.b64decode("{src}"))
open("Inter-Bold.otf", "wb").write(base64.b64decode("{font}"))
env = dict(os.environ, UPI_DEVICE="GPU", UPI_FONT=os.path.abspath("Inter-Bold.otf"), **{env!r})
os.makedirs("/kaggle/working/out", exist_ok=True)
t0 = time.time()
r = subprocess.run([sys.executable, "-I", "world.py", "--", *{wargs!r}], env=env, capture_output=True, text=True)
print(r.stdout[-6000:]); print(r.stderr[-3000:]); print(f"TOTAL {{time.time() - t0:.1f}}s")
'''
os.makedirs(outdir, exist_ok=True)
open(os.path.join(outdir, "runner.py"), "w").write(runner)
json.dump({"id": "kishoremulakapati/upi01-blender-render", "title": "upi01-blender-render", "code_file": "runner.py",
           "language": "python", "kernel_type": "script", "is_private": True, "enable_gpu": True,
           "enable_internet": True, "dataset_sources": [], "competition_sources": [], "kernel_sources": []},
          open(os.path.join(outdir, "kernel-metadata.json"), "w"), indent=1)
print("ready:", outdir)
