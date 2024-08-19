# -*- coding: utf-8 -*-
"""miku.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uTztL4JLXCaKSKodCf6KOUlMhwfWeQRK
"""

!rm -r /root/vorst-cavry
!wget https://huggingface.co/NoCrypt/fast-repo/resolve/main/ubuntu_deps.zip ; unzip ubuntu_deps.zip -d /root/deps ; dpkg -i /root/deps/* ; rm -rf ubuntu_deps.zip /root/deps/
!echo -e "https://huggingface.co/NoCrypt/fast-repo/resolve/main/dep.tar.lz4\n\tout=dep.tar.lz4\nhttps://huggingface.co/NoCrypt/fast-repo/resolve/main/repo.tar.lz4\n\tout=repo.tar.lz4\nhttps://huggingface.co/NoCrypt/fast-repo/resolve/main/cache.tar.lz4\n\tout=cache.tar.lz4\n" \
  | aria2c -i- -j5 -x16 -s16 -k1M -c
import os
from tqdm import tqdm
packages = [
"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/NoCrypt/fast-repo/resolve/main/dep.tar.lz4 -d /root -o dep.tar.lz4",
"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/NoCrypt/fast-repo/resolve/main/repo.tar.lz4 -d /root -o repo.tar.lz4",
"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/NoCrypt/fast-repo/resolve/main/cache.tar.lz4 -d /root -o cache.tar.lz4"
]
for install in tqdm(packages, desc=print("Install Miku...")):
    os.system(install)
!tar -xI lz4 -f dep.tar.lz4 --overwrite-dir --directory=/usr/local/lib/python3.10/dist-packages/ #(manual dir)
!tar -xI lz4 -f repo.tar.lz4 --directory=/ #/root/vorst-cavry/ (auto dir)
!tar -xI lz4 -f cache.tar.lz4 --directory=/ #/root/.cache/huggingface (auto dir)

!rm -rf /root/dep.tar.lz4 /root/repo.tar.lz4 /root/cache.tar.lz4
!mv /content/sdw /root/vorst-cavry
!sed -i 's@"gradio_theme":.*@"gradio_theme": "NoCrypt/miku",@' {config_dir}