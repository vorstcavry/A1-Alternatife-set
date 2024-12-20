# -*- coding: utf-8 -*-
"""a.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y6IofzwyAJq64pL9FXFK_3nARPIN6l7C
"""
import os
import re
import time
import json
import shutil
import zipfile
import requests
import subprocess
from datetime import timedelta
from subprocess import getoutput
from urllib.parse import unquote
from IPython.utils import capture
from IPython.display import clear_output


#  ================= DETECT ENV =================
import os
import re
import time
import json
import requests
from datetime import timedelta


#  ================= DETECT ENV =================
def detect_environment():
    free_plan = (os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024. ** 3) <= 20)
    environments = {
        'COLAB_GPU': ('Google Colab', "/root" if free_plan else "/content"),
        'KAGGLE_URL_BASE': ('Kaggle', "/kaggle/working/content")
    }

    for env_var, (environment, path) in environments.items():
        if env_var in os.environ:
            return environment, path, free_plan

env, root_path, free_plan = detect_environment()
webui_path = f"{root_path}/vorst-cavry"
flag_file = f"{root_path}/libraries_installed.txt"

if not os.path.exists(flag_file):
    print("💿 Installing the libraries, it's going to take a while:\n")

    install_lib = {
        "gdown": "pip install -U gdown",
        "aria2": "apt-get update && apt -y install aria2",
        "localtunnel": "npm install -g localtunnel &> /dev/null",
        "insightface": "pip install insightface",
    }

    # Dictionary of additional libraries specific to certain environments
    additional_libs = {
        "Google Colab": {
            "xformers": "pip install xformers==0.0.26.dev767 --no-deps",
            "gradio": "pip install gradio_client==0.2.7"
        },
        "Kaggle": {
            "xformers": "pip install -q xformers==0.0.23.post1 triton==2.1.0",
            "torch": "pip install -q torch==2.1.2+cu121 torchvision==0.16.2+cu121 torchaudio==2.1.2 --extra-index-url https://download.pytorch.org/whl/cu121"
        }
    }

    # If the current environment has additional libraries, update the install_lib dictionary
    if env in additional_libs:
        install_lib.update(additional_libs[env])

    # Loop through libraries and execute install commands
    for index, (package, install_cmd) in enumerate(install_lib.items(), start=1):
        print(f"\r[{index}/{len(install_lib)}] \033[32m>>\033[0m Installing \033[33m{package}\033[0m..." + " "*35, end='')
        subprocess.run(install_cmd, shell=True, capture_output=True)

    # Additional manual installation steps for specific packages
    with capture.capture_output() as cap:
        get_ipython().system('curl -s -OL https://github.com/DEX-1101/sd-webui-notebook/raw/main/res/new_tunnel --output-dir {root_path}')
        get_ipython().system('curl -s -Lo /usr/bin/cl https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 && chmod +x /usr/bin/cl')
        get_ipython().system('curl -sLO https://github.com/openziti/zrok/releases/download/v0.4.23/zrok_0.4.23_linux_amd64.tar.gz && tar -xzf zrok_0.4.23_linux_amd64.tar.gz -C /usr/bin && rm -f zrok_0.4.23_linux_amd64.tar.gz')

    del cap

    clear_output()

    # Save file install lib
    with open(flag_file, "w") as f:
        f.write(">W<'")

import os
from tqdm import tqdm
from IPython.utils import capture
from IPython.display import clear_output
packages = [
            "git clone https://github.com/Panchovix/stable-diffusion-webui-reForge /root/vorst-cavry",
]
for install in tqdm(packages, desc=print("Prepare Repo...")):
    os.system(install)
    
    
    print("🍪 Libraries are installed!" + " "*35)
    time.sleep(2)
    clear_output()

