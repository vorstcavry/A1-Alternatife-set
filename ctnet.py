# -*- coding: utf-8 -*-
"""ctnet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lkvdIOylFQNZoLjdtMHNH2v4EPJ0H45-
"""

import os
from tqdm import tqdm

packages = [
            "aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_canny_fp16.safetensors -d /root/vorst-cavry/models/ControlNet -o control_v11p_sd15_canny.safetensors",
            "aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_inpaint_fp16.safetensors -d /root/vorst-cavry/models/ControlNet -o control_v11p_sd15_inpaint.safetensors",
            "aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_lineart_fp16.safetensors -d /root/vorst-cavry/models/ControlNet -o control_v11f1p_sd15_depth.safetensors",
            "aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_openpose_fp16.safetensors -d /root/vorst-cavry/models/ControlNet -o control_v11p_sd15_openpose.safetensors",
            "aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15s2_lineart_anime_fp16.safetensors -d /root/vorst-cavry/models/ControlNet -o control_v11p_sd15s2_lineart_anime.safetensors"
]
for install in tqdm(packages, desc=print("Install controlnet...")):
    os.system(install)