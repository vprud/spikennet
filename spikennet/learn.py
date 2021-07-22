import numpy as np

from typing import Union
from sklearn.metrics import (mean_squared_error, mean_absolute_error,
                             r2_score)

from .models import SpikeDNNet, SigmaDNNet


def dnn_validate(dnn: Union[SpikeDNNet, SigmaDNNet],
                 folds: list) -> tuple:

    mse_res = np.ones((len(folds), 2))
    mae_res = np.ones((len(folds), 2))
    r2_res = np.ones((len(folds), 2))
    norms_W_1 = []
    norms_W_2 = []
    tr_res = {}
    vl_res = {}

    for i, fold in enumerate(folds):
        tr_target = fold[0][0]
        tr_control = fold[0][1]

        vl_target = fold[1][0]
        vl_control = fold[1][1]

        snn = dnn
        target_est = snn.fit(tr_target, tr_control)
        vl_pred = snn.predict(target_est[-1][0], vl_control)

        mse_res[i][0] = mean_squared_error(tr_target[:, 0], target_est[:, 0])
        mse_res[i][1] = mean_squared_error(vl_target[:, 0], vl_pred[:, 0])

        mae_res[i][0] = mean_absolute_error(tr_target[:, 0], target_est[:, 0])
        mae_res[i][1] = mean_absolute_error(vl_target[:, 0], vl_pred[:, 0])

        r2_res[i][0] = r2_score(tr_target[:, 0], target_est[:, 0])
        r2_res[i][1] = r2_score(vl_target[:, 0], vl_pred[:, 0])

        tr_res[i] = target_est
        vl_res[i] = vl_pred

        norms_W_1.append(np.linalg.norm(snn.array_hist_W_1[:-1], axis=2)[:, 0])
        norms_W_2.append(np.linalg.norm(snn.array_hist_W_2[:-1], axis=2)[:, 0])

    return (tr_res, vl_res, mse_res, mae_res, r2_res, norms_W_1, norms_W_2)
