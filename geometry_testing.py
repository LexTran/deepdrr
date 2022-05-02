import deepdrr
from deepdrr import geo
from deepdrr.utils import test_utils
from deepdrr.utils import image_utils
import numpy as np
import logging
import os
from PIL import Image
import pdb

log = logging.getLogger(__name__)

def test_scatter_geometry():
    file_path = 'G:\CS\DL\datasets\CTPelvic1K_dataset6_data\dataset6_CLINIC_0026_data.nii.gz'
    volume = deepdrr.Volume.from_nifti(file_path, use_thresholding=True)
    volume.faceup()

    carm = deepdrr.MobileCArm(volume.center_in_world)

    print(f"volume center in world: {volume.center_in_world}")
    print(f"volume spacing: {volume.spacing}")
    print(f"volume ijk_from_world\n{volume.ijk_from_world}")

    with deepdrr.Projector(
        volume=volume,
        carm=carm,
        max_block_index=1024,
        photon_count=100000,
        add_noise=True,
        # scatter_num=10e7,
        threads=8,
        neglog=True,
    ) as projector:
        # carm.move_to(alpha=0, beta=15, degrees=True)
        image = projector.project()

    image_utils.save("output/test_multivolume.png", image)
    
    output_dir = test_utils.get_output_dir()

if __name__ == "__main__":
    os.environ['PATH'] += ';'+r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\bin\Hostx64\x64"
    os.environ['PATH'] += ';'+r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include"
    os.environ['PATH'] += ';'+r"D:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt"
    if(os.system("cl.exe")):
        raise RuntimeError("cl.exe still not found, path probably incorrect")
    logging.getLogger("deepdrr").setLevel(logging.DEBUG)
    test_scatter_geometry()
