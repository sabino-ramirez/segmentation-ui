# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# import os
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import dicom2nifti
import torch

# import monai
from monai.config.deviceconfig import print_config

from monai.apps.deepedit.transforms import (
    AddGuidanceSignalDeepEditd,
    AddGuidanceFromPointsDeepEditd,
    ResizeGuidanceMultipleLabelDeepEditd,
)

from monai.transforms import (
    Activationsd,
    AsDiscreted,
    EnsureChannelFirstd,
    EnsureTyped,
    LoadImaged,
    Orientationd,
    Resized,
    ScaleIntensityRanged,
    SqueezeDimd,
    ToNumpyd,
    ToTensord,
)

from monai.networks.nets.dynunet import DynUNet

# print_config()

def dicomHTing():
    dicom2nifti.dicom_series_to_nifti("/home/sabino/repos/segmentation-ui/api/dicoms/", "/home/sabino/repos/segmentation-ui/api/static/dicom.nii.gz", reorient_nifti=True)


def doTheThing(img: str):
    labels = {"vagina": 1, "background": 0}

    # target_spacing = [1.0, 1.0, 1.0]
    spatial_size = [128, 128, 128]

    model = DynUNet(
        spatial_dims=3,
        in_channels=len(labels) + 1,
        out_channels=len(labels),
        kernel_size=[3, 3, 3, 3, 3, 3],
        strides=[1, 2, 2, 2, 2, [2, 2, 1]],
        upsample_kernel_size=[2, 2, 2, 2, [2, 2, 1]],
        norm_name="instance",
        deep_supervision=False,
        res_block=True,
        dropout=0.2,
    )

    # spleen label points are demoed:     'spleen': [[66, 180, 105], [66, 180, 145]].
    data = {
        # "image": "ai/patient001.nii.gz",
        "image": img,
        "vagina": [[162, 159, 12], [163, 159, 18]],
        "background": [],
    }

    # Pre Processing

    pre_transforms = [
        # Loading the image
        LoadImaged(keys="image", reader="ITKReader"),
        # Ensure channel first
        EnsureChannelFirstd(keys="image"),
        # Change image orientation
        Orientationd(keys="image", axcodes="RAS"),
        # Scaling image intensity - works well for CT images
        ScaleIntensityRanged(
            keys="image", a_min=-175, a_max=250, b_min=0.0, b_max=1.0, clip=True
        ),
        # DeepEdit Tranforms for Inference
        # Add guidance (points) in the form of tensors based on the user input
        AddGuidanceFromPointsDeepEditd(
            ref_image="image", guidance="guidance", label_names=labels
        ),
        # Resize the image
        Resized(keys="image", spatial_size=spatial_size, mode="area"),
        # Resize the guidance based on the image resizing
        ResizeGuidanceMultipleLabelDeepEditd(guidance="guidance", ref_image="image"),
        # Add the guidance to the input image
        AddGuidanceSignalDeepEditd(keys="image", guidance="guidance"),
        # Convert image to tensor
        ToTensord(keys="image"),
    ]

    # Going through each of the pre_transforms
    for t in pre_transforms:
        tname = type(t).__name__
        test_img = data["image"]
        data = t(data)
        image = data["image"]
        # adds label to data dict
        label = data.get("label")
        # adds guidance to data dict
        guidance = data.get("guidance")

    transformed_image = data["image"]
    guidance = data.get("guidance")

    # Evaluation
    model_path = "ai/deepedit_dynunet.pt"
    model.load_state_dict(torch.load(model_path))
    model.cuda()
    model.eval()

    inputs = data["image"][None].cuda()
    with torch.no_grad():
        outputs = model(inputs)
    outputs = outputs[0]
    data["pred"] = outputs

    post_transforms = [
        EnsureTyped(keys="pred"),
        Activationsd(keys="pred", softmax=True),
        AsDiscreted(keys="pred", argmax=True),
        SqueezeDimd(keys="pred", dim=0),
        ToNumpyd(keys="pred"),
    ]

    pred = None
    for t in post_transforms:
        tname = type(t).__name__
        data = t(data)
        image = data["image"]
        label = data["pred"]

    nib.save(nib.Nifti1Image(data["pred"], np.eye(4)), "pred_" + img)
