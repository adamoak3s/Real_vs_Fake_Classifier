| family | config | description | best_val_acc | delta_vs_baseline | best_epoch | final_train_acc | overfit_gap | params | sec_per_epoch |
|---|---|---|---|---|---|---|---|---|---|
| none | baseline | - | 0.9428 | +0.0000 | 10 | 0.9545 | +0.0183 | 1,569,089 | 34 |
| none | baseline_seed7 | - | 0.9473 | +0.0045 | 11 | 0.9589 | +0.0273 | 1,569,089 | 33 |
| batchnorm | batchnorm | BatchNorm after every conv | 0.9475 | +0.0047 | 7 | 0.9576 | +0.0466 | 1,572,065 | 41 |
| dropout_head | dropout_head_0.25 | Dropout(0.25) before Dense | 0.9495 | +0.0067 | 15 | 0.9634 | +0.0156 | 1,569,089 | 33 |
| dropout_head | dropout_head_0.5 | Dropout(0.5) before Dense | 0.9505 | +0.0077 | 18 | 0.9643 | +0.0141 | 1,569,089 | 33 |
| dropout_conv | dropout_conv_0.1 | Dropout(0.1) after every pool | 0.9474 | +0.0046 | 19 | 0.9589 | +0.0223 | 1,569,089 | 34 |
| dropout_conv | dropout_conv_0.25 | Dropout(0.25) after every pool | 0.9245 | -0.0183 | 12 | 0.9368 | +0.0226 | 1,569,089 | 34 |
| l2 | l2_1e-3 | L2(0.001) on all kernels | 0.9082 | -0.0346 | 12 | 0.9026 | -0.0005 | 1,569,089 | 33 |
| l2 | l2_1e-4 | L2(0.0001) on all kernels | 0.9193 | -0.0235 | 5 | 0.9228 | +0.0126 | 1,569,089 | 35 |
| l2 | l2_1e-5 | L2(1e-05) on all kernels | 0.9449 | +0.0021 | 13 | 0.9510 | +0.0154 | 1,569,089 | 34 |
| combo | best_of_combo | BatchNorm after every conv; Dropout(0.1) after every pool; Dropout(0.5) before Dense | 0.9400 | -0.0028 | 7 | 0.9483 | +0.0089 | 1,572,065 | 41 |
| combo | bn+dropout_head_0.5 | BatchNorm after every conv; Dropout(0.5) before Dense | 0.9448 | +0.0020 | 9 | 0.9565 | +0.0755 | 1,572,065 | 41 |
| combo | bn+l2_1e-4 | BatchNorm after every conv; L2(0.0001) on all kernels | 0.9186 | -0.0242 | 3 | 0.9315 | +0.0135 | 1,572,065 | 41 |