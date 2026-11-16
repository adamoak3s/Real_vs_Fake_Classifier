| family | config | idg_equivalent | best_val_acc | delta_vs_baseline | best_epoch | final_train_acc | overfit_gap | sec_per_epoch |
|---|---|---|---|---|---|---|---|---|
| none | baseline | - | 0.9252 | +0.0000 | 4 | 0.9176 | -0.0076 | 41 |
| none | baseline_seed7 | - (noise-floor rerun) | 0.9138 | -0.0114 | 3 | 0.9201 | +0.0085 | 38 |
| flip | flip_h | horizontal_flip=True | 0.9268 | +0.0016 | 4 | 0.9178 | -0.0089 | 41 |
| flip | flip_hv | horizontal_flip=True, vertical_flip=True | 0.9151 | -0.0100 | 4 | 0.9068 | -0.0083 | 41 |
| rotation | rot_0.05 | rotation_range=18 | 0.8528 | -0.0724 | 3 | 0.9010 | +0.0789 | 55 |
| rotation | rot_0.10 | rotation_range=36 | 0.8424 | -0.0828 | 4 | 0.8981 | +0.0557 | 46 |
| rotation | rot_0.20 | rotation_range=72 | 0.8073 | -0.1179 | 3 | 0.8921 | +0.0889 | 45 |
| zoom | zoom_0.1 | zoom_range=0.1 | 0.8852 | -0.0400 | 3 | 0.8963 | +0.0552 | 45 |
| zoom | zoom_0.2 | zoom_range=0.2 | 0.8476 | -0.0776 | 3 | 0.8852 | +0.0561 | 44 |
| zoom | zoom_0.3 | zoom_range=0.3 | 0.8769 | -0.0483 | 3 | 0.8756 | +0.0297 | 47 |
| translation | shift_0.1 | width_shift_range=0.1, height_shift_range=0.1 | 0.8459 | -0.0793 | 3 | 0.8867 | +0.0635 | 53 |
| translation | shift_0.2 | width_shift_range=0.2, height_shift_range=0.2 | 0.9003 | -0.0249 | 4 | 0.8749 | -0.0254 | 45 |
| brightness | brightness_0.2 | brightness_range=[0.8, 1.2] | 0.9100 | -0.0152 | 4 | 0.8996 | -0.0104 | 36 |
| contrast | contrast_0.2 | - (no direct equivalent) | 0.9230 | -0.0022 | 4 | 0.9151 | -0.0079 | 37 |
| noise | noise_0.02 | - (no direct equivalent) | 0.9208 | -0.0044 | 4 | 0.9155 | -0.0052 | 37 |
| combo | book_combo | horizontal_flip=True, rotation_range=36, zoom_range=0.2 | 0.7466 | -0.1786 | 1 | 0.8482 | +0.1456 | 47 |