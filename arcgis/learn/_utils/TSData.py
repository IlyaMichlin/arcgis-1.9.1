try:
    import fastai
    from fastai.torch_core import *
    from fastai.basic_data import *
    from fastai.data_block import *
    from fastai.core import *
    import torch
except:
    raise Exception("Unable to import")

import arcgis

if getattr(arcgis.env, "_processorType", "") == "GPU" and torch.cuda.is_available():
    device = torch.device("cuda")
elif getattr(arcgis.env, "_processorType", "") == "CPU":
    device = torch.device("cpu")
else:
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


class TSItem(ItemBase):
    "`ItemBase` suitable for time series"

    def __init__(self, item, *args, **kwargs):
        super().__init__(item, *args, **kwargs)
        self.data = item
        self.obj = item
        self.channels = item.shape[-2]
        self.seq_len = item.shape[-1]

    def __str__(self):
        return "TimeSeries(ch={:.0f}, seq_len={:.0f})".format(
            self.channels, self.seq_len
        )

    def clone(self):
        return self.__class__(self.data.clone())

    def apply_tfms(self, tfms=None, **kwargs):
        if tfms is None:
            return self
        x = self.clone()
        for tfm in tfms:
            x.data = tfm(x.data)
        return x

    def reconstruct(self, item):
        return TSItem(item)

    def show(self, ax=None, title=None, **kwargs):
        x = self.clone()
        if ax is None:
            plt.plot(x.data.transpose_(0, 1))
            plt.title(title)
            plt.show()
        else:
            ax.plot(x.data.transpose_(0, 1))
            ax.title.set_text(title)
            ax.tick_params(
                axis="both",
                which="both",
                bottom="off",
                top="off",
                labelbottom="off",
                right="off",
                left="off",
                labelleft="off",
            )
            return ax


class TimeSeriesItem(TSItem):
    pass


class TSDataBunch(DataBunch):
    def scale(
        self,
        scale_type="standardize",
        scale_by_channel=False,
        scale_by_sample=False,
        scale_range=(-1, 1),
    ) -> None:
        self.scale_type = scale_type
        self.scale_by_channel = scale_by_channel
        self.scale_by_sample = scale_by_sample
        self.scale_range = scale_range
        if scale_type is None:
            self.stats = None
            return self
        assert scale_type in ["normalize", "standardize", "robustscale"], print(
            "Select a correct type", scale_type
        )

        train = self.train_ds.x.items.astype(float)
        valid = self.valid_ds.x.items.astype(float)
        if self.test_ds is not None:
            test = self.test_ds.x.items.astype(float)

        if scale_by_channel and scale_by_sample:
            axis = -1  # mean
        elif scale_by_channel:
            axis = (0, 2)  # mean for the entire dataset by channel
        elif scale_by_sample:
            axis = (1, 2)  # mean for each sample
        else:
            axis = None

        if scale_by_sample:
            self.stats = None
            if scale_type == "normalize":
                train_min = np.nanmin(train, axis=axis, keepdims=True)
                train_max = np.nanmax(train, axis=axis, keepdims=True)
                self.train_ds.x.items = (
                    ((train - train_min)) / (train_max - train_min)
                ) * (self.scale_range[1] - self.scale_range[0]) + self.scale_range[0]
                valid_min = np.nanmin(valid, axis=axis, keepdims=True)
                valid_max = np.nanmax(valid, axis=axis, keepdims=True)
                self.valid_ds.x.items = (
                    ((valid - valid_min)) / (valid_max - valid_min)
                ) * (self.scale_range[1] - self.scale_range[0]) + self.scale_range[0]
                if self.test_ds is not None:
                    test_min = np.nanmin(test, axis=axis, keepdims=True)
                    test_max = np.nanmax(test, axis=axis, keepdims=True)
                    self.test_ds.x.items = (
                        ((test - test_min)) / (test_max - test_min)
                    ) * (self.scale_range[1] - self.scale_range[0]) + self.scale_range[
                        0
                    ]
                return self

            elif scale_type == "standardize":
                train_mean = np.nanmean(train, axis=axis, keepdims=True)
                train_std = np.nanstd(train, axis=axis, keepdims=True) + 1e-8
                self.train_ds.x.items = (train - train_mean) / train_std
                valid_mean = np.nanmean(valid, axis=axis, keepdims=True)
                valid_std = np.nanstd(valid, axis=axis, keepdims=True) + 1e-8
                self.valid_ds.x.items = (valid - valid_mean) / valid_std
                if self.test_ds is not None:
                    test_mean = np.nanmean(test, axis=axis, keepdims=True)
                    test_std = np.nanstd(test, axis=axis, keepdims=True) + 1e-8
                    self.test_ds.x.items = (test - test_mean) / test_std
                return self

            elif scale_type == "robustscale":
                train_median = np.nanmedian(train, axis=axis, keepdims=True)
                train_perc_25 = np.nanpercentile(train, 25, axis=axis, keepdims=True)
                train_perc_75 = np.nanpercentile(train, 75, axis=axis, keepdims=True)
                train_scale = train_perc_75 - train_perc_25
                self.train_ds.x.items = (train - train_median) / train_scale

                valid_median = np.nanmedian(valid, axis=axis, keepdims=True)
                valid_perc_25 = np.nanpercentile(valid, 25, axis=axis, keepdims=True)
                valid_perc_75 = np.nanpercentile(valid, 75, axis=axis, keepdims=True)
                valid_scale = valid_perc_75 - valid_perc_25
                self.valid_ds.x.items = (valid - valid_median) / valid_scale

                if self.test_ds is not None:
                    test_median = np.nanmedian(test, axis=axis, keepdims=True)
                    test_perc_25 = np.nanpercentile(test, 25, axis=axis, keepdims=True)
                    test_perc_75 = np.nanpercentile(test, 75, axis=axis, keepdims=True)
                    test_scale = test_perc_75 - test_perc_25
                    self.test_ds.x.items = (test - test_median) / test_scale
                return self

        else:
            if scale_type == "normalize":
                train_min = np.nanmin(train, axis=axis, keepdims=True)
                train_max = np.nanmax(train, axis=axis, keepdims=True)
                self.stats = train_min, train_max
                self.train_ds.x.items = (
                    ((self.train_ds.x.items - train_min)) / (train_max - train_min)
                ) * (self.scale_range[1] - self.scale_range[0]) + self.scale_range[0]
                self.valid_ds.x.items = (
                    ((self.valid_ds.x.items - train_min)) / (train_max - train_min)
                ) * (self.scale_range[1] - self.scale_range[0]) + self.scale_range[0]
                if self.test_ds is not None:
                    self.test_ds.x.items = (
                        ((self.test_ds.x.items - train_min)) / (train_max - train_min)
                    ) * (self.scale_range[1] - self.scale_range[0]) + self.scale_range[
                        0
                    ]
                return self
            elif scale_type == "standardize":
                train_mean = np.nanmean(train, axis=axis, keepdims=True)
                train_std = np.nanstd(train, axis=axis, keepdims=True) + 1e-8
                self.stats = train_mean, train_std
                self.train_ds.x.items = (self.train_ds.x.items - train_mean) / train_std
                self.valid_ds.x.items = (self.valid_ds.x.items - train_mean) / train_std
                if self.test_ds is not None:
                    self.test_ds.x.items = (
                        self.test_ds.x.items - train_mean
                    ) / train_std
                return self
            elif scale_type == "robustscale":
                train_median = np.nanmedian(train, axis=axis, keepdims=True)
                train_perc_25 = np.nanpercentile(train, 25, axis=axis, keepdims=True)
                train_perc_75 = np.nanpercentile(train, 75, axis=axis, keepdims=True)
                train_scale = train_perc_75 - train_perc_25
                self.stats = train_median, train_scale
                self.train_ds.x.items = (train - train_median) / train_scale
                self.valid_ds.x.items = (valid - train_median) / train_scale
                if self.test_ds is not None:
                    self.test_ds.x.items = (test - train_median) / train_scale
                return self

    @property
    def cw(self) -> None:
        return self._get_cw(self.train_dl)

    @property
    def dbtype(self) -> str:
        return "1D"

    def _get_cw(self, train_dl):
        target = torch.Tensor(train_dl.dataset.y.items).to(dtype=torch.int64)
        # Compute samples weight (each sample should get its own weight)
        class_sample_count = torch.tensor(
            [(target == t).sum() for t in torch.unique(target, sorted=True)]
        )
        weights = 1.0 / class_sample_count.float()
        return (weights / weights.sum()).to(device)


def show_counts(databunch):
    labels, counts = np.unique(databunch.train_ds.y.items, return_counts=True)
    plt.bar(labels, counts)
    plt.title("labels")
    plt.xticks(labels)
    plt.show()


DataBunch.show_counts = show_counts


class TSPreProcessor(PreProcessor):
    def __init__(self, ds: ItemList):
        self.ds = ds

    def process(self, ds: ItemList):
        ds.features, ds.seq_len = self.ds.get(0).data.size(-2), self.ds.get(
            0
        ).data.size(-1)
        ds.f = ds.features
        ds.s = ds.seq_len


class TimeSeriesList(ItemList):
    "`ItemList` suitable for time series"
    _bunch = TSDataBunch
    _processor = TSPreProcessor
    _label_cls = None
    _square_show = True

    def __init__(self, items, *args, mask=None, tfms=None, **kwargs):
        items = To3dTensor(items)
        super().__init__(items, *args, **kwargs)
        self.tfms, self.mask = tfms, mask
        self.copy_new.append("tfms")

    def get(self, i):
        item = super().get(i)
        if self.mask is None:
            return TSItem(To2dTensor(item))
        else:
            return [TSItem(To2dTensor(item[m])) for m in self.mask]

    def show_xys(self, xs, ys, figsize=(10, 10), **kwargs):
        "Show the `xs` and `ys` on a figure of `figsize`. `kwargs` are passed to the show method."
        rows = int(math.sqrt(len(xs)))
        fig, axs = plt.subplots(rows, rows, figsize=figsize)
        for x, y, ax in zip(xs, ys, axs.flatten()):
            x.show(ax=ax, title=str(y), **kwargs)
        plt.tight_layout()
        plt.show()

    def show_xyzs(self, xs, ys, zs, figsize=(10, 10), **kwargs):
        if self._square_show_res:
            rows = int(np.ceil(math.sqrt(len(xs))))
            fig, axs = plt.subplots(rows, rows, figsize=figsize)
            fig.suptitle("Ground truth vs Predictions", fontsize=16)
            for x, y, z, ax in zip(xs, ys, zs, axs.flatten()):
                x.show(ax=ax, title=f"{str(y)}\n{str(z)}", **kwargs)
        else:
            fig, axs = plt.subplots(len(xs), 2, figsize=figsize)
            fig.suptitle("Ground truth vs Predictions", fontsize=16)
            for i, (x, y, z) in enumerate(zip(xs, ys, zs)):
                x.show(ax=axs[i, 0], title=str(y), **kwargs)
                x.show(ax=axs[i, 1], title=str(z), **kwargs)
        plt.tight_layout()
        plt.show()

    @classmethod
    def from_array(cls, ts, **kwargs):
        return cls(ts)

    @classmethod
    def from_df(
        cls, df, path=".", cols=None, feat=None, processor=None, **kwargs
    ) -> "ItemList":
        "Create an `ItemList` in `path` from the inputs in the `cols` of `df`."
        if cols is None:
            inputs = df
        else:
            cols = listify(cols)
            if feat is not None and feat not in cols:
                cols = cols + listify(feat)
            col_idxs = df_names_to_idx(list(cols), df)
            inputs = df.iloc[:, col_idxs]
        assert (
            inputs.isna().sum().sum() == 0
        ), f"You have NaN values in column(s) {cols} of your dataframe, please fix it."
        inputs = df2array(inputs, feat)
        res = cls(items=inputs, path=path, inner_df=df, processor=processor, **kwargs)
        return res


class TSList(TimeSeriesList):
    pass


def df2array(df, feat=None):
    if feat is None:
        return df.values[:, None]
    for i, ch in enumerate(df[feat].unique()):
        data_i = df[df[feat] == ch].values[:, None]
        if i == 0:
            data = data_i
        else:
            data = np.concatenate((data, data_i), axis=1)

    return data


def ToTensor(arr, **kwargs):
    if isinstance(arr, np.ndarray):
        arr = torch.from_numpy(arr)
    elif not isinstance(arr, torch.Tensor):
        print(f"Can't convert {type(arr)} to torch.Tensor")
    return arr.float()


def ToArray(arr):
    if isinstance(arr, torch.Tensor):
        arr = np.array(arr)
    elif not isinstance(arr, np.ndarray):
        print(f"Can't convert {type(arr)} to np.array")
    if arr.dtype == "O":
        arr = np.array(arr, dtype=np.float32)
    return arr


def To3dTensor(arr):
    if isinstance(arr, list):
        arr = np.array(arr)
    if arr.dtype == "O":
        arr = np.array(arr, dtype=np.float32)
    arr = ToTensor(arr)
    if arr.ndim == 1:
        arr = arr[None, None]
    elif arr.ndim == 2:
        arr = arr[:, None]
    elif arr.ndim == 4:
        arr = arr[0]
    assert arr.ndim == 3, "Please, review input dimensions"
    return arr


def To2dTensor(arr):
    if arr.dtype == "O":
        arr = np.array(arr, dtype=np.float32)
    arr = ToTensor(arr)
    if arr.ndim == 1:
        arr = arr[None]
    elif arr.ndim == 3:
        arr = torch.squeeze(arr, 0)
    assert arr.ndim == 2, "Please, review input dimensions"
    return arr


def To1dTensor(arr):
    if arr.dtype == "O":
        arr = np.array(arr, dtype=np.float32)
    arr = ToTensor(arr)
    if arr.ndim == 3:
        arr = torch.squeeze(arr, 1)
    if arr.ndim == 2:
        arr = torch.squeeze(arr, 0)
    assert arr.ndim == 1, "Please, review input dimensions"
    return arr


def To3dArray(arr):
    arr = ToArray(arr)
    if arr.ndim == 1:
        arr = arr[None, None]
    elif arr.ndim == 2:
        arr = arr[:, None]
    elif arr.ndim == 4:
        arr = arr[0]
    assert arr.ndim == 3, "Please, review input dimensions"
    return np.array(arr)


def To2dArray(arr):
    arr = ToArray(arr)
    if arr.ndim == 1:
        arr = arr[None]
    if arr.ndim == 3:
        arr = np.squeeze(arr, 0)
    assert arr.ndim == 2, "Please, review input dimensions"
    return np.array(arr)


def To1dArray(arr):
    arr = ToArray(arr)
    if arr.ndim == 3:
        arr = np.squeeze(arr, 1)
    if arr.ndim == 2:
        arr = np.squeeze(arr, 0)
    assert arr.ndim == 1, "Please, review input dimensions"
    return np.array(arr)
