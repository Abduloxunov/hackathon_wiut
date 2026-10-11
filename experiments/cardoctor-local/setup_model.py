"""Explicit one-time model download. Destination is checked by core.py."""
import core
import torch
if __name__=='__main__':
    core.MODEL_FILE.parent.mkdir(parents=True,exist_ok=True)
    if not core.MODEL_FILE.exists():
        torch.hub.download_url_to_file(core.MODEL_URL,str(core.MODEL_FILE),hash_prefix='f37072fd',progress=True)
    core.model()
    print('Model ready:',core.MODEL_FILE)
    print('Bytes:',core.MODEL_FILE.stat().st_size)
