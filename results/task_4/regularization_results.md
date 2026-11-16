| family | config | description | best_val_acc | delta_vs_baseline | best_epoch | final_train_acc | overfit_gap | params | sec_per_epoch |
|---|---|---|---|---|---|---|---|---|---|
| none | baseline | - | 0.9403 | +0.0000 | 10 | 0.9583 | +0.0186 | 1,569,089 | 34 |
| none | baseline_seed7 | - | 0.9473 | +0.0070 | 14 | 0.9741 | +0.0403 | 1,569,089 | 33 |
| batchnorm | batchnorm | BatchNorm after every conv | 0.9169 | -0.0234 | 3 | 0.9475 | +0.0667 | 1,572,065 | 40 |
| dropout_head | dropout_head_0.25 | Dropout(0.25) before Dense | 0.9485 | +0.0081 | 16 | 0.9772 | +0.0319 | 1,569,089 | 34 |
| dropout_head | dropout_head_0.5 | Dropout(0.5) before Dense | 0.9449 | +0.0046 | 10 | 0.9560 | +0.0140 | 1,569,089 | 33 |
| dropout_conv | dropout_conv_0.1 | Dropout(0.1) after every pool | 0.9406 | +0.0002 | 11 | 0.9504 | +0.0164 | 1,569,089 | 34 |
| dropout_conv | dropout_conv_0.25 | Dropout(0.25) after every pool | 0.9280 | -0.0123 | 13 | 0.9452 | +0.0535 | 1,569,089 | 34 |
| l2 | l2_1e-3 | L2(0.001) on all kernels | 0.8925 | -0.0479 | 20 | 0.8960 | +0.0035 | 1,569,089 | 33 |
| l2 | l2_1e-4 | L2(0.0001) on all kernels | 0.9341 | -0.0063 | 11 | 0.9357 | +0.0245 | 1,569,089 | 34 |
| l2 | l2_1e-5 | L2(1e-05) on all kernels | 0.9187 | -0.0217 | 4 | 0.9291 | +0.0197 | 1,569,089 | 35 |
| combo | bn+dropout_head_0.5 | BatchNorm after every conv; Dropout(0.5) before Dense | 0.9488 | +0.0084 | 13 | 0.9723 | +0.1981 | 1,572,065 | 40 |
| combo | bn+l2_1e-4 | BatchNorm after every conv; L2(0.0001) on all kernels | 0.8975 | -0.0429 | 2 | 0.9290 | +0.0573 | 1,572,065 | 41 |