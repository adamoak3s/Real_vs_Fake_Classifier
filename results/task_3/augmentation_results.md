| family | config | idg_equivalent | best_val_acc | delta_vs_baseline | best_epoch | final_train_acc | overfit_gap | sec_per_epoch |
|---|---|---|---|---|---|---|---|---|
| none | baseline | - | 0.9390 | +0.0000 | 10 | 0.9573 | +0.0270 | 37 |
| none | baseline_seed7 | - (noise-floor rerun) | 0.9420 | +0.0030 | 9 | 0.9560 | +0.0157 | 36 |
| flip | flip_h | horizontal_flip=True | 0.9507 | +0.0117 | 12 | 0.9610 | +0.0138 | 38 |
| flip | flip_hv | horizontal_flip=True, vertical_flip=True | 0.9429 | +0.0039 | 11 | 0.9479 | +0.0085 | 36 |
| rotation | rot_0.05 | rotation_range=18 | 0.9303 | -0.0087 | 7 | 0.9351 | +0.0200 | 46 |
| rotation | rot_0.10 | rotation_range=36 | 0.8906 | -0.0483 | 5 | 0.9183 | +0.0279 | 46 |
| rotation | rot_0.20 | rotation_range=72 | 0.8732 | -0.0658 | 5 | 0.9092 | +0.0624 | 46 |
| zoom | zoom_0.1 | zoom_range=0.1 | 0.9218 | -0.0171 | 5 | 0.9200 | +0.0432 | 50 |
| zoom | zoom_0.2 | zoom_range=0.2 | 0.9229 | -0.0161 | 6 | 0.9168 | +0.0035 | 45 |
| zoom | zoom_0.3 | zoom_range=0.3 | 0.9280 | -0.0109 | 8 | 0.9190 | +0.0181 | 45 |
| translation | shift_0.1 | width_shift_range=0.1, height_shift_range=0.1 | 0.9108 | -0.0281 | 13 | 0.9332 | +0.0276 | 45 |
| translation | shift_0.2 | width_shift_range=0.2, height_shift_range=0.2 | 0.8383 | -0.1007 | 2 | 0.8820 | +0.0563 | 46 |
| brightness | brightness_0.2 | brightness_range=[0.8, 1.2] | 0.9385 | -0.0005 | 12 | 0.9438 | +0.0057 | 36 |
| contrast | contrast_0.2 | - (no direct equivalent) | 0.9362 | -0.0028 | 6 | 0.9499 | +0.0378 | 37 |
| noise | noise_0.02 | - (no direct equivalent) | 0.9469 | +0.0080 | 16 | 0.9737 | +0.0358 | 36 |
| combo | best_of_combo | horizontal_flip=True + - (no direct equivalent) | 0.9406 | +0.0016 | 7 | 0.9458 | +0.0069 | 37 |
| combo | book_combo | horizontal_flip=True, rotation_range=36, zoom_range=0.2 | 0.8510 | -0.0880 | 4 | 0.8811 | +0.0424 | 47 |