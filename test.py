# -*- coding: utf-8 -*-
"""test.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13zeNKG7vvxEI0vw1URyzv4aKBFO4z82W
"""

# @title ## **Install Environment**
import sys
import subprocess
import os
import time
import json
import shutil
import random
import string
from pathlib import Path
from tqdm import tqdm
from pydantic import BaseModel

python_version  = ".".join(sys.version.split(".")[:2])
python_path     = Path(f"/usr/local/lib/python{python_version}/dist-packages/")
colablib_path   = python_path / "colablib"
if not colablib_path.exists():
    subprocess.run(['pip', 'install', '--upgrade', 'git+https://github.com/Linaqruf/colablib'], check=True)

from colablib.colored_print import cprint, print_line
from colablib.utils import py_utils, package_utils, config_utils
from colablib.sd_models.downloader import aria2_download, download
from colablib.utils.git_utils import update_repo, reset_repo, validate_repo, batch_update
from colablib.utils.py_utils import get_filename

################################
# COLAB ARGUMENTS GOES HERE
################################

# It ain't much, but it's honest work.
class CustomDirs(BaseModel):
    url: str
    dst: str

# @markdown ### **Drive Config**
mount_drive          = False  # @param {type: 'boolean'}
output_drive_folder  = "cagliostro-colab-forge"  # @param {type: 'string'}

# @markdown ### **Repo Config**
update_webui         = True  # @param {type: 'boolean'}
update_extensions    = True  # @param {type: 'boolean'}
commit_hash          = ""  # @param {type: 'string'}

# @markdown ### **Download Config**
# @markdown > Check only the options you need
animagine_xl_3_1     = False  # @param {type: 'boolean'}
rae_diffusion_xl_v2  = False  # @param {type: 'boolean'}
kivotos_xl_v2_0      = False  # @param {type: 'boolean'}
urangdiffusion_1_4   = False  # @param {type: 'boolean'}

# @markdown > **Note:**
# @markdown - For multiple URLs, use comma separation (e.g. `url1, url2, url3`)
# @markdown - Forge supports FLUX, SD, and SDXL, but this notebook focuses only on SDXL
# @markdown - **Highly Recommended:** Use Hugging Face links whenever possible
custom_model_url     = ""  # @param {'type': 'string'}
custom_vae_url       = "https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl.vae.safetensors"  # @param {'type': 'string'}
custom_lora_url      = ""  # @param {'type': 'string'}

# @markdown Set `use_preset` for using default prompt, resolution, sampler, and other settings
use_presets          = True  # @param {type: 'boolean'}

# @markdown ### **Launch Arguments**

auto_select_model    = False  # @param {type: 'boolean'}
auto_select_vae      = True  # @param {type: 'boolean'}
additional_arguments = "--lowram --theme dark --no-half-vae --opt-sdp-attention"  # @param {type: 'string'}

################################
# GLOBAL VARIABLES GOES HERE
################################

# ROOT DIR
root_dir        = Path("/content")
drive_dir       = root_dir / "drive" / "MyDrive"
repo_dir        = root_dir / "stable-diffusion-webui-forge"
tmp_dir         = root_dir / "tmp"

models_dir      = repo_dir / "models"
extensions_dir  = repo_dir / "extensions"
ckpt_dir        = models_dir / "Stable-diffusion"
vae_dir         = models_dir / "VAE"
lora_dir        = models_dir / "Lora"
output_subdir   = ["txt2img-samples", "img2img-samples", "extras-samples", "txt2img-grids", "img2img-grids"]

config_file_path    = repo_dir / "config.json"
ui_config_file_path = repo_dir / "ui-config.json"

package_url = [
    "https://huggingface.co/Linaqruf/fast-repo/resolve/main/webui-forge.tar.lz4",
    "https://huggingface.co/Linaqruf/fast-repo/resolve/main/webui-forge-deps.tar.lz4",
]

custom_dirs = {
    "model" : CustomDirs(url=custom_model_url, dst=str(ckpt_dir)),
    "vae"   : CustomDirs(url=custom_vae_url, dst=str(vae_dir)),
    "lora"  : CustomDirs(url=custom_lora_url, dst=str(lora_dir)),
}

default_model_urls = {
    "animagine_xl_3_1"      : "https://huggingface.co/cagliostrolab/animagine-xl-3.1/resolve/main/animagine-xl-3.1.safetensors",
    "rae_diffusion_xl_v2"   : "https://huggingface.co/Raelina/Rae-Diffusion-XL-V2/resolve/main/RaeDiffusion-XL-v2.safetensors",
    "kivotos_xl_v2_0"       : "https://huggingface.co/yodayo-ai/kivotos-xl-2.0/resolve/main/kivotos-xl-2.0.safetensors",
    "urangdiffusion_1_4"    : "https://huggingface.co/kayfahaarukku/UrangDiffusion-1.4/resolve/main/UrangDiffusion-1.4.safetensors",
}

################################
# HELPER FUNCTIONS STARTS HERE
################################

def mount_drive_function(directory):
    output_dir = repo_dir / "outputs"

    if mount_drive:
        print_line(80, color="green")
        if not directory.exists():
            from google.colab import drive
            cprint("Mounting google drive...", color="green", reset=False)
            drive.mount(str(directory.parent))
        output_dir = directory / output_drive_folder
        cprint("Set default output path to:", output_dir, color="green")

    return output_dir

def setup_directories():
    for dir in [ckpt_dir, vae_dir, lora_dir]:
        dir.mkdir(parents=True, exist_ok=True)

def pre_download(dir, urls, desc, overwrite=False):
    ffmpy_path = python_path / "ffmpy-0.3.0.dist-info"

    for url in tqdm(urls, desc=desc):
        filename = Path(url).name
        aria2_download(dir, filename, url, quiet=True)
        if filename == "webui-forge-deps.tar.lz4":
            package_utils.extract_package(filename, python_path, overwrite=True)
        else:
            package_utils.extract_package(filename, "/", overwrite=overwrite)
        os.remove(dir / filename)

    subprocess.run(["rm", "-rf", str(ffmpy_path)])
    subprocess.run(["pip", "install", "--force-reinstall", "ffmpy"], check=True)

def install_dependencies():
    ubuntu_deps = ["aria2", "lz4"]
    cprint("Installing ubuntu dependencies", color="green")
    subprocess.run(["apt", "install", "-y"] + ubuntu_deps, check=True)

def install_webui(repo_dir, desc):
    if not repo_dir.exists():
        pre_download(root_dir, package_url, desc, overwrite=False)
    else:
        cprint("Stable Diffusion Web UI Forge already installed, skipping...", color="green")

def configure_output_path(config_path, output_dir, output_subdir):
    try:
        config = config_utils.read_config(str(config_path))
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}

    config_updates = {
        f"outdir_{subdir.split('-')[0]}_{'_'.join(subdir.split('-')[1:])}": str(output_dir / subdir)
        for subdir in output_subdir
    }
    config.update(config_updates)

    config_path.parent.mkdir(parents=True, exist_ok=True)

    config_utils.write_config(str(config_path), config)

    for dir in output_subdir:
        (output_dir / dir).mkdir(parents=True, exist_ok=True)

def prepare_environment():
    cprint("Preparing environment...", color="green")
    os.environ['PYTORCH_CUDA_ALLOC_CONF']   = "garbage_collection_threshold:0.9,max_split_size_mb:512"
    os.environ["TF_CPP_MIN_LOG_LEVEL"]      = "3"
    os.environ["PYTHONWARNINGS"]            = "ignore"

def custom_download(custom_dirs):
    filtered_urls = filter_dict_items(default_model_urls)

    for key, value in custom_dirs.items():
        urls = value.url.split(",")
        dst = value.dst

        if key == "model":
            urls.extend(filtered_urls)

        if urls[0]:
            print_line(80, color="green")
            cprint(f" [-] Downloading Custom {key}...", color="flat_yellow")

        for url in urls:
            url = url.strip()
            if url != "":
                print_line(80, color="green")
                if "|" in url:
                    url, filename = map(str.strip, url.split("|"))
                    if not filename.endswith((".safetensors", ".ckpt", ".pt", "pth")):
                        filename = filename + Path(get_filename(url)).suffix
                else:
                    filename = get_filename(url)

                download(url=url, filename=filename, dst=dst, quiet=False)

def filter_dict_items(dict_items):
    result_list = []
    for key, url in dict_items.items():
        if globals().get(key):
            result_list.append(url)
    return result_list

def auto_select_file(target_dir, config_key, file_types):
    valid_files = [f for f in os.listdir(target_dir) if f.endswith(file_types)]
    if valid_files:
        file_path = random.choice(valid_files)

        if Path(target_dir).joinpath(file_path).exists():
            config = config_utils.read_config(str(config_file_path))
            config[config_key] = file_path
            config_utils.write_config(str(config_file_path), config)
        return file_path
    else:
        return None

def ui_config_presets():
    preset_prompt = "masterpiece, best quality, very aesthetic, absurdres"
    preset_negative_prompt = "nsfw, lowres, (bad), text, error, fewer, extra, missing, worst quality, jpeg artifacts, low quality, watermark, unfinished, displeasing, oldest, early, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract]"

    return {
        "txt2img/Prompt/value"              : preset_prompt,
        "txt2img/Negative prompt/value"     : preset_negative_prompt,
        "img2img/Prompt/value"              : preset_prompt,
        "img2img/Negative prompt/value"     : preset_negative_prompt,
        "customscript/sampler.py/txt2img/Sampling method/value" : "Euler a",
        "customscript/sampler.py/txt2img/Sampling steps/value"  : 28,
        "customscript/sampler.py/txt2img/Scheduler/value"       : "Automatic",
    }

def ui_config_settings(ui_config_file: str):
    config = config_utils.read_config(str(ui_config_file))
    preset_config = ui_config_presets()

    for key, value in preset_config.items():
        config[key] = value

    config_utils.write_config(str(ui_config_file), config)

def general_config_presets(config_file: str, lora_dir: str, use_presets: bool, ui_config_file: str):
    config = config_utils.read_config(str(config_file))

    config.update({
        "CLIP_stop_at_last_layers"      : 2,
        "show_progress_every_n_steps"   : 10,
        "show_progressbar"              : True,
        "samples_filename_pattern"      : "[model_name]_[seed]",
        "show_progress_type"            : "Approx NN",
        "live_preview_content"          : "Prompt",
        "forge_preset"                  : "xl",
        "xl_t2i_width"                  : 832,
        "xl_t2i_height"                 : 1216,
        "xl_t2i_cfg"                    : 7,
        "xl_t2i_hr_cfg"                 : 7,
        "xl_t2i_sampler"                : "Euler a",
        "xl_t2i_scheduler"              : "Automatic",
        "gradio_theme"                  : gradio_theme,
    })

    config_utils.write_config(str(config_file), config)

    if use_presets:
        ui_config_settings(ui_config_file)

def is_valid(target_dir, file_types):
    return any(f.endswith(file_types) for f in os.listdir(target_dir))

def parse_args(config):
    args = []
    for k, v in config.items():
        if k.startswith("_"):
            args.append(f'"{v}"')
        elif isinstance(v, str):
            args.append(f'--{k}="{v}"')
        elif isinstance(v, bool) and v:
            args.append(f"--{k}")
        elif isinstance(v, (float, int)) and not isinstance(v, bool):
            args.append(f"--{k}={v}")
    return " ".join(args)

def main():
    global output_dir, auto_select_model, auto_select_vae

    ################################
    # MAIN EXECUTION
    ################################

    os.chdir(root_dir)
    start_time = time.time()
    output_dir = mount_drive_function(drive_dir)

    gpu_info    = py_utils.get_gpu_info(get_gpu_name=True)
    python_info = py_utils.get_python_version()
    torch_info  = py_utils.get_torch_version()

    print_line(80, color="green")
    cprint(f" [-] Current GPU: {gpu_info}", color="flat_yellow")
    cprint(f" [-] Python {python_info}", color="flat_yellow")
    cprint(f" [-] Torch {torch_info}", color="flat_yellow")
    print_line(80, color="green")

    try:
        install_dependencies()

        print_line(80, color="green")
        install_webui(repo_dir, cprint("Unpacking Web UI Forge", color="green", tqdm_desc=True))
        prepare_environment()

        configure_output_path(config_file_path, output_dir, output_subdir)

        print_line(80, color="green")
        if update_webui and not commit_hash:
            update_repo(cwd=repo_dir, args="-X theirs --rebase --autostash")
        elif commit_hash:
            reset_repo(repo_dir, commit_hash)

        setup_directories()

        repo_name, current_commit_hash, current_branch = validate_repo(repo_dir)
        cprint(f"Using '{repo_name}' repository...", color="green")
        cprint(f"Branch: {current_branch}, Commit hash: {current_commit_hash}", color="green")

        if update_extensions:
            print_line(80, color="green")
            batch_update(fetch=True, directory=extensions_dir, desc=cprint("Updating extensions", color="green", tqdm_desc=True))

        elapsed_time = py_utils.calculate_elapsed_time(start_time)
        print_line(80, color="green")
        cprint(f"Finished installation. Took {elapsed_time}.", color="flat_yellow")
    except Exception as e:
        cprint(f"An error occurred: {str(e)}", color="red")
        print_line(80, color="red")
        cprint("Setup failed. Please check the error message above and try again.", color="red")
        print_line(80, color="red")
        return

    start_time = time.time()

    custom_download(custom_dirs)

    elapsed_time = py_utils.calculate_elapsed_time(start_time)
    print_line(80, color="green")
    cprint(f"Download finished. Took {elapsed_time}.", color="flat_yellow")
    print_line(80, color="green")
    cprint(f"Launching '{repo_name}'", color="flat_yellow")
    print_line(80, color="green")

    if not is_valid(ckpt_dir, ('.ckpt', '.safetensors')):
        cprint(f"No checkpoints were found in the directory '{ckpt_dir}'.", color="yellow")
        url = "https://huggingface.co/cagliostrolab/animagine-xl-3.1/blob/main/animagine-xl-3.1.safetensors"
        filename = get_filename(url)
        aria2_download(url=url, download_dir=ckpt_dir, filename=filename)
        print_line(80, color="green")
        auto_select_model = True

    if not is_valid(vae_dir, ('.vae.pt', '.vae.safetensors', '.pt', '.ckpt')):
        cprint(f"No VAEs were found in the directory '{vae_dir}'.", color="yellow")
        url = "https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/blob/main/sdxl.vae.safetensors"
        filename = get_filename(url)
        aria2_download(url=url, download_dir=vae_dir, filename=filename)
        print_line(80, color="green")
        auto_select_vae = True

    if auto_select_model:
        selected_model  = auto_select_file(ckpt_dir, "sd_model_checkpoint", ('.ckpt', '.safetensors'))
        cprint(f"Selected Model: {selected_model}", color="green")

    if auto_select_vae:
        selected_vae    = auto_select_file(vae_dir, "sd_vae", ('.vae.pt', '.vae.safetensors', '.pt', '.ckpt'))
        cprint(f"Selected VAE: {selected_vae}", color="green")


if __name__ == "__main__":
    main()