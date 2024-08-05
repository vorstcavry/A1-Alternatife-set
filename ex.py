# -*- coding: utf-8 -*-
"""ex.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lkvdIOylFQNZoLjdtMHNH2v4EPJ0H45-
"""
%cd /root/vorst-cavry/extensions
import os
from tqdm import tqdm
packages = [
            "git clone https://tinyurl.com/controlnet-s",
            #"git clone https://tinyurl.com/depth-lib-hand",
            #"git clone https://github.com/hnmr293/posex",
            "git clone https://github.com/BlafKing/sd-civitai-browser-plus",
            "git clone https://github.com/vorstcavry/images-browser",
            "git clone https://github.com/Iyashinouta/sd-model-downloader",
            "git clone https://github.com/IDEA-Research/DWPose",
            "git clone https://tinyurl.com/additional-networks-s",
            #"git clone https://github.com/fkunn1326/openpose-editor",
            "git clone https://tinyurl.com/openpose-edit",
            "git clone https://github.com/NoCrypt/inpaint-nav",
            "git clone https://github.com/vorstcavry/tagcomplete",
            "git clone https://tinyurl.com/batchlink-download",
            "git clone https://tinyurl.com/aspect-ratio-v",
            "git clone https://github.com/pantat88/sd-fast-pnginfo",
            "git clone https://github.com/ahgsql/StyleSelectorXL",
            "git clone https://github.com/vorstcavry/static",


]
for install in tqdm(packages, desc=print("Memasang Ekstension...")):
    os.system(install)
