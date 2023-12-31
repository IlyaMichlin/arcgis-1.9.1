from ._multi_task_road_extractor import MultiTaskRoadExtractor


class ConnectNet(MultiTaskRoadExtractor):
    """
    Creates a ConnectNet model for binary segmentation of linear features. Supports RGB
    and Multispectral Imagery.
    Implementation based on https://doi.org/10.1109/CVPR.2019.01063 .

    =====================   ===========================================
    **Argument**            **Description**
    ---------------------   -------------------------------------------
    data                    Required fastai Databunch. Returned data object from
                            ``prepare_data`` function.
    ---------------------   -------------------------------------------
    backbone                Optional String. Backbone CNN model to be used for
                            creating the base. If hourglass is chosen as
                            the mtl_model (Architecture),then this parameter is
                            ignored as hourglass uses a special customised
                            architecture.
                            This parameter is used with `linknet` model.
                            Default: 'resnet34'

                            Supported backbones: 'resnet18', 'resnet34',
                            'resnet50', 'resnet101', 'resnet152'
    ---------------------   -------------------------------------------
    mtl_model               Optional String. It is used to create model
                            from linknet or hourglass based neural architectures.
                            Supported: 'linknet', 'hourglass'.
                            Default: 'hourglass'
    ---------------------   -------------------------------------------
    pretrained_path         Optional String. Path where a compatible pre-trained
                            model is saved. Accepts a Deep Learning Package
                            (DLPK) or Esri Model Definition(EMD) file.
    =====================   ===========================================

    **kwargs**

    =============================   =============================================
    **Argument**                    **Description**
    -----------------------------   ---------------------------------------------
    gaussian_thresh                 Optional float. Sets the gaussian threshold
                                    which allows to set the required width of the
                                    linear feature.
                                    Range: 0.0 to 1.0
                                    Default:0.76
    -----------------------------   ---------------------------------------------
    orient_bin_size                 Optional Int. Sets the bin size for
                                    orientation angles.
                                    Default:20
    -----------------------------   ---------------------------------------------
    orient_theta                    Optional Int. Sets the width of orientation
                                    mask.
                                    Default:8
    =============================   =============================================

    :return: `ConnectNet` Object
    """

    pass
    # This is a dummy class just to hold the doc strings of the model ConnectNet
    # This model is a clone of MultiTaskRoadExtractor and hence not reimplemented.
