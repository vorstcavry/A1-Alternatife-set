# -*- coding: utf-8 -*-
"""ex-lite.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YzShFqX1aXFWOduhNiGWXL3P7VF_6M-p
"""

import os
from tqdm import tqdm
packages = [
            "git clone https://github.com/BlafKing/sd-civitai-browser-plus",
            "git clone https://github.com/vorstcavry/images-browser",
            "git clone https://github.com/Iyashinouta/sd-model-downloader",
            "git clone https://github.com/kohya-ss/sd-webui-additional-networks /root/vorst-cavry/extensions/Additional-Networks",
            "git clone https://github.com/DominikDoom/a1111-sd-webui-tagcomplete",
            "git clone https://github.com/gutris1/sd-hub",
            "git clone https://github.com/thomasasfk/sd-webui-aspect-ratio-helper",
            "git clone https://github.com/ahgsql/StyleSelectorXL",
            "git clone https://github.com/vorstcavry/static",

]
for install in tqdm(packages, desc=print("Memasang Ekstension...")):
    os.system(install)