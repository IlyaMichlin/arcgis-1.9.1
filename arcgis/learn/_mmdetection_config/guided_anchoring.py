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

# error in show results
# ga_faster_x101_64x4d_fpn_1x_coco.py, box AP=43.9

_base_ = "./_base_/models/faster_rcnn_r50_fpn.py"
model = dict(
    pretrained="open-mmlab://resnext101_64x4d",
    backbone=dict(
        type="ResNeXt",
        depth=101,
        groups=64,
        base_width=4,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type="BN", requires_grad=True),
        style="pytorch",
    ),
    rpn_head=dict(
        _delete_=True,
        type="GARPNHead",
        in_channels=256,
        feat_channels=256,
        approx_anchor_generator=dict(
            type="AnchorGenerator",
            octave_base_scale=8,
            scales_per_octave=3,
            ratios=[0.5, 1.0, 2.0],
            strides=[4, 8, 16, 32, 64],
        ),
        square_anchor_generator=dict(
            type="AnchorGenerator", ratios=[1.0], scales=[8], strides=[4, 8, 16, 32, 64]
        ),
        anchor_coder=dict(
            type="DeltaXYWHBBoxCoder",
            target_means=[0.0, 0.0, 0.0, 0.0],
            target_stds=[0.07, 0.07, 0.14, 0.14],
        ),
        bbox_coder=dict(
            type="DeltaXYWHBBoxCoder",
            target_means=[0.0, 0.0, 0.0, 0.0],
            target_stds=[0.07, 0.07, 0.11, 0.11],
        ),
        loc_filter_thr=0.01,
        loss_loc=dict(
            type="FocalLoss", use_sigmoid=True, gamma=2.0, alpha=0.25, loss_weight=1.0
        ),
        loss_shape=dict(type="BoundedIoULoss", beta=0.2, loss_weight=1.0),
        loss_cls=dict(type="CrossEntropyLoss", use_sigmoid=True, loss_weight=1.0),
        loss_bbox=dict(type="SmoothL1Loss", beta=1.0, loss_weight=1.0),
    ),
    roi_head=dict(bbox_head=dict(bbox_coder=dict(target_stds=[0.05, 0.05, 0.1, 0.1]))),
    # model training and testing settings
    train_cfg=dict(
        rpn=dict(
            ga_assigner=dict(
                type="ApproxMaxIoUAssigner",
                pos_iou_thr=0.7,
                neg_iou_thr=0.3,
                min_pos_iou=0.3,
                ignore_iof_thr=-1,
            ),
            ga_sampler=dict(
                type="RandomSampler",
                num=256,
                pos_fraction=0.5,
                neg_pos_ub=-1,
                add_gt_as_proposals=False,
            ),
            allowed_border=-1,
            center_ratio=0.2,
            ignore_ratio=0.5,
        ),
        rpn_proposal=dict(max_num=300),
        rcnn=dict(
            assigner=dict(pos_iou_thr=0.6, neg_iou_thr=0.6, min_pos_iou=0.6),
            sampler=dict(type="RandomSampler", num=256),
        ),
    ),
    test_cfg=dict(rpn=dict(max_num=300), rcnn=dict(score_thr=1e-3)),
)

checkpoint = "http://download.openmmlab.com/mmdetection/v2.0/guided_anchoring/ga_faster_x101_64x4d_fpn_1x_coco/ga_faster_x101_64x4d_fpn_1x_coco_20200215-0fa7bde7.pth"
