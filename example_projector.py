#! python3

from genericpath import isfile
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
    output_dir = input("请输入输出路径：")                                # 输出文件夹
    output_dir = Path(output_dir)
    data_dir = input("请输入数据路径：")
    i = 1
    if os.path.isdir(data_dir):
        outputname = input("请输入输出序列前缀：")
        for data in os.listdir(data_dir):
            patient = deepdrr.Volume.from_nifti(     
                data_dir + "\\" + data, use_thresholding=True
            )                                                                       # 指定输入图像，读取CT容积
            patient.faceup()

            # define the simulated C-arm
            carm = deepdrr.MobileCArm(
                patient.center_in_world,
                source_to_detector_distance = 400,
                source_to_isocenter_vertical_distance = 320,
                source_to_isocenter_horizontal_offset = 0,
                free_space = 820,
                sensor_height = 1536*1.5,
                sensor_width = 1536*1.5,
                pixel_size = 0.5,
            )
            # deepdrr.vis.show(patient, carm, full=[False, True])

            # project in the AP view
            with Projector(patient, 
                carm=carm,
                step=0.01,
                spectrum='60KV_AL35', # Options are `'60KV_AL35'`, `'90KV_AL40'`, and `'120KV_AL43'`
                photon_count=100000,
                add_noise=True,
                threads=8,
            ) as projector:
                #carm.move_to(alpha=0, beta=-15)
                image = projector()

            path = output_dir / f'{outputname}_{i}.png'
            image_utils.save(path, image)
            i += 1
            log.info(f"saved example projection image to {path.absolute()}")
    elif os.path.isfile(data_dir):
        outputname = input("请输入输出名称：")
        patient = deepdrr.Volume.from_nifti(     
            data_dir, use_thresholding=True
        )                                                                       # 指定输入图像，读取CT容积
        patient.faceup()

        # define the simulated C-arm
        carm = deepdrr.MobileCArm(
            patient.center_in_world,
            source_to_detector_distance = 300,
            source_to_isocenter_vertical_distance = 240,
            source_to_isocenter_horizontal_offset = 0,
            free_space = 820,
            sensor_height = 1536*1.5,
            sensor_width = 1536*1.5,
            pixel_size = 0.5,
        )

        # project in the AP view
        with Projector(patient, 
            carm=carm,
            step=0.01,
            spectrum='60KV_AL35', # Options are `'60KV_AL35'`, `'90KV_AL40'`, and `'120KV_AL43'`
            photon_count=100000,
            add_noise=True,
            threads=8,
        ) as projector:
            #carm.move_to(alpha=0, beta=-15)
            image = projector()

        path = output_dir / f'{outputname}.png'
        image_utils.save(path, image)
        log.info(f"saved example projection image to {path.absolute()}")
    else:
        raise RuntimeError("Path is not correct!")


if __name__ == "__main__":
# if(os.system("cl.exe")):
    os.environ['PATH'] += ';'+r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\bin\Hostx64\x64"
    os.environ['PATH'] += ';'+r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include"
    os.environ['PATH'] += ';'+r"D:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt"
    if(os.system("cl.exe")):
        raise RuntimeError("cl.exe still not found, path probably incorrect")
    main()
