# Copyright 2018-2019 Open-MMLab.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# detectors_cascade_rcnn_r50_1x_coco.py, box AP=47.4

_base_ = "./_base_/models/cascade_rcnn_r50_fpn.py"

model = dict(
    backbone=dict(
        type="DetectoRS_ResNet",
        conv_cfg=dict(type="ConvAWS"),
        sac=dict(type="SAC", use_deform=True),
        stage_with_sac=(False, True, True, True),
        output_img=True,
    ),
    neck=dict(
        type="RFP",
        rfp_steps=2,
        aspp_out_channels=64,
        aspp_dilations=(1, 3, 6, 1),
        rfp_backbone=dict(
            rfp_inplanes=256,
            type="DetectoRS_ResNet",
            depth=50,
            in_channels=3,
            num_stages=4,
            out_indices=(0, 1, 2, 3),
            frozen_stages=1,
            norm_cfg=dict(type="BN", requires_grad=True),
            norm_eval=True,
            conv_cfg=dict(type="ConvAWS"),
            sac=dict(type="SAC", use_deform=True),
            stage_with_sac=(False, True, True, True),
            pretrained="torchvision://resnet50",
            style="pytorch",
        ),
    ),
)

checkpoint = "http://download.openmmlab.com/mmdetection/v2.0/detectors/detectors_cascade_rcnn_r50_1x_coco/detectors_cascade_rcnn_r50_1x_coco-32a10ba0.pth"
