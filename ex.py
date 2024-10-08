# -*- coding: utf-8 -*-
"""ex.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lkvdIOylFQNZoLjdtMHNH2v4EPJ0H45-
"""

import os
from tqdm import tqdm
packages = [
            "git clone https://github.com/Mikubill/sd-webui-controlnet",
            #"git clone https://tinyurl.com/depth-lib-hand",
            #"git clone https://github.com/hnmr293/posex",
            #"git clone https://github.com/Klokinator/Umi-AI-Wildcards",
            #"git clone https://github.com/BlafKing/sd-civitai-browser-plus",
            #"git clone https://github.com/viyiviyi/sd-encrypt-image /root/vorst-cavry/extensions/Encrypt-Image", 
            #"git clone https://github.com/animerl/novelai-2-local-prompt",
            "git clone https://github.com/vorstcavry/images-browser",
            #"git clone https://github.com/Iyashinouta/sd-model-downloader",
            "git clone https://github.com/IDEA-Research/DWPose",
            "git clone https://github.com/kohya-ss/sd-webui-additional-networks",
            #"git clone https://github.com/fkunn1326/openpose-editor",
            "git clone https://github.com/huchenlei/sd-webui-openpose-editor",
            "git clone https://github.com/NoCrypt/inpaint-nav",
            "git clone https://github.com/DominikDoom/a1111-sd-webui-tagcomplete",
            #"git clone https://github.com/gutris1/sd-hub",
            "git clone https://github.com/thomasasfk/sd-webui-aspect-ratio-helper",
            "git clone https://github.com/pantat88/sd-fast-pnginfo",
            "git clone https://github.com/ahgsql/StyleSelectorXL",
            "git clone https://github.com/vorstcavry/static",
            "git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards",
            #"git clone https://github.com/new-sankaku/stable-diffusion-webui-simple-manga-maker",
            "git clone https://github.com/hnmr293/sd-webui-llul",

]
for install in tqdm(packages, desc=print("Memasang Ekstension...")):
    os.system(install)
