#! python3

import logging
import os
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from rich.logging import RichHandler         # 终端美化工具
from time import time

import deepdrr
from deepdrr import geo
from deepdrr.utils import test_utils, image_utils
from deepdrr.projector import Projector

# set up fancy logging
log = logging.getLogger().handlers.clear()
log = logging.getLogger('deepdrr')
log.addHandler(RichHandler())
log.setLevel(logging.INFO)

def main():
    output_dir = Path.cwd() / "output"                                # 输出文件夹
    # data_dir = test_utils.download_sampledata("CTPelvic1K_sample")
    i = 1
    for data in os.listdir('G:\CS\DL\datasets\CTPelvic1K_dataset6_data'):
        patient = deepdrr.Volume.from_nifti(
            # data_dir / "dataset6_CLINIC_0001_data.nii.gz", use_thresholding=True       
            r'G:\CS\DL\datasets\CTPelvic1K_dataset6_data\\'+data, use_thresholding=True
        )                                                                       # 指定输入图像，读取CT容积
        patient.faceup()

        # define the simulated C-arm
        carm = deepdrr.MobileCArm(patient.center_in_world)
        # deepdrr.vis.show(patient, carm, full=[False, True])

        # project in the AP view
        with Projector(patient, 
            carm=carm,
            photon_count=100000,
            add_noise=True,
            # scatter_num=10,
            threads=8,
            neglog=True,
        ) as projector:
            #carm.move_to(alpha=0, beta=-15)
            image = projector()

        path = output_dir / f'example_projector_{i}.png'
        image_utils.save(path, image)
        i += 1
        log.info(f"saved example projection image to {path.absolute()}")

if __name__ == "__main__":
# if(os.system("cl.exe")):
    os.environ['PATH'] += ';'+r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\bin\Hostx64\x64"
    os.environ['PATH'] += ';'+r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include"
    os.environ['PATH'] += ';'+r"D:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt"
    if(os.system("cl.exe")):
        raise RuntimeError("cl.exe still not found, path probably incorrect")
    main()
