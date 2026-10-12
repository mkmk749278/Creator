import subprocess, os, glob, time
def sh(c, tail=3000):
    print(">>", c[:300], flush=True); t=time.time()
    r = subprocess.run(c, shell=True, text=True, capture_output=True, executable="/bin/bash")
    print(r.stdout[-tail:], r.stderr[-tail:], f"[{time.time()-t:.0f}s rc={r.returncode}]", flush=True)
    if r.returncode: raise SystemExit(f"failed: {c[:200]}")
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
inp = glob.glob("/kaggle/input/**/base.mp4", recursive=True)[0]; d = os.path.dirname(inp)
LS="/kaggle/temp/LS"; PY=f"{LS}/.venv/bin/python"
sh(f"git clone -q https://github.com/bytedance/LatentSync.git {LS} && cd {LS} && git log -1 --oneline && cat requirements.txt")
sh(f"pip install -q uv && cd {LS} && uv venv -q -p 3.10 .venv && uv pip install -q -p .venv/bin/python -r requirements.txt huggingface_hub", tail=4000)
sh(f"cd {LS} && {PY} -c \"from huggingface_hub import hf_hub_download as h; [h('ByteDance/LatentSync-1.5', f, local_dir='checkpoints') for f in ['latentsync_unet.pt','whisper/tiny.pt']]\" && ls -R checkpoints | head")
sh(f"cd {LS} && {PY} -m scripts.inference --help", tail=3000)
sh(f"cd {LS} && {PY} -m scripts.inference --unet_config_path configs/unet/stage2.yaml --inference_ckpt_path checkpoints/latentsync_unet.pt --inference_steps 25 --guidance_scale 1.5 --video_path {inp} --audio_path {d}/vo.wav --video_out_path /kaggle/working/latentsync.mp4", tail=6000)
sh("ls -la /kaggle/working")
