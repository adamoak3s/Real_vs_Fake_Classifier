| family | config | description | best_val_acc | delta_vs_baseline | best_epoch | final_train_acc | overfit_gap | params | sec_per_epoch |
|---|---|---|---|---|---|---|---|---|---|
| none | baseline | - | 0.9182 | +0.0000 | 4 | 0.9164 | -0.0018 | 1,569,089 | 37 |
| none | baseline_seed7 | - | 0.9145 | -0.0037 | 3 | 0.9146 | +0.0012 | 1,569,089 | 34 |
| batchnorm | batchnorm | BatchNorm after every conv | 0.9056 | -0.0125 | 2 | 0.9372 | +0.1078 | 1,572,065 | 41 |
| dropout_head | dropout_head_0.25 | Dropout(0.25) before Dense | 0.9215 | +0.0033 | 4 | 0.9128 | -0.0087 | 1,569,089 | 37 |
| dropout_head | dropout_head_0.5 | Dropout(0.5) before Dense | 0.9199 | +0.0017 | 4 | 0.9150 | -0.0049 | 1,569,089 | 34 |
| dropout_conv | dropout_conv_0.1 | Dropout(0.1) after every pool | 0.9153 | -0.0029 | 4 | 0.9138 | -0.0015 | 1,569,089 | 35 |
| dropout_conv | dropout_conv_0.25 | Dropout(0.25) after every pool | 0.9079 | -0.0103 | 4 | 0.9089 | +0.0011 | 1,569,089 | 35 |
| l2 | l2_1e-3 | L2(0.001) on all kernels | 0.5000 | -0.4182 | 1 | 0.4979 | -0.0021 | 1,569,089 | 34 |
| l2 | l2_1e-4 | L2(0.0001) on all kernels | 0.9058 | -0.0123 | 4 | 0.8992 | -0.0066 | 1,569,089 | 34 |
| l2 | l2_1e-5 | L2(1e-05) on all kernels | 0.9182 | +0.0000 | 3 | 0.9148 | -0.0027 | 1,569,089 | 34 |
| combo | bn+dropout_head_0.5 | BatchNorm after every conv; Dropout(0.5) before Dense | 0.9292 | +0.0110 | 4 | 0.9316 | +0.0024 | 1,572,065 | 42 |
| combo | bn+l2_1e-4 | BatchNorm after every conv; L2(0.0001) on all kernels | 0.9181 | -0.0001 | 4 | 0.9243 | +0.0062 | 1,572,065 | 42 |