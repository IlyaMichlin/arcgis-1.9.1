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

# cascade_rcnn_hrnetv2p_w40_20e_coco.py, box AP=43.8
_base_ = "./_base_/models/cascade_rcnn_r50_fpn.py"
model = dict(
    pretrained="open-mmlab://msra/hrnetv2_w40",
    backbone=dict(
        _delete_=True,
        type="HRNet",
        extra=dict(
            stage1=dict(
                num_modules=1,
                num_branches=1,
                block="BOTTLENECK",
                num_blocks=(4,),
                num_channels=(64,),
            ),
            stage2=dict(
                num_modules=1,
                num_branches=2,
                block="BASIC",
                num_blocks=(4, 4),
                num_channels=(40, 80),
            ),
            stage3=dict(
                num_modules=4,
                num_branches=3,
                block="BASIC",
                num_blocks=(4, 4, 4),
                num_channels=(40, 80, 160),
            ),
            stage4=dict(
                num_modules=3,
                num_branches=4,
                block="BASIC",
                num_blocks=(4, 4, 4, 4),
                num_channels=(40, 80, 160, 320),
            ),
        ),
    ),
    neck=dict(
        _delete_=True, type="HRFPN", in_channels=[40, 80, 160, 320], out_channels=256
    ),
)

checkpoint = "http://download.openmmlab.com/mmdetection/v2.0/hrnet/cascade_rcnn_hrnetv2p_w40_20e_coco/cascade_rcnn_hrnetv2p_w40_20e_coco_20200512_161112-75e47b04.pth"
