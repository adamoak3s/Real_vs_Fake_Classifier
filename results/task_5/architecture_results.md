| part | config | method | total_params | trainable_params | best_val_acc | delta_vs_task2 | cumulative_epochs | sec_per_epoch | cumulative_train_sec | val_inference_sec |
|---|---|---|---|---|---|---|---|---|---|---|
| a | task2_cnn | baseline (Task 2 CNN) | 1,569,089 | 1,569,089 | 0.9244 | +0.0000 | 4 | 36 | 160 | 2.2 |
| a | mini_resnet | from scratch | 2,410,945 | 2,407,937 | 0.9428 | +0.0184 | 4 | 131 | 560 | 7.0 |
| a | mini_densenet | from scratch | 983,383 | 969,019 | 0.9418 | +0.0174 | 4 | 45 | 240 | 3.6 |
| a | resnet50_scratch | from scratch (random weights) | 23,589,761 | 23,536,641 | 0.9169 | -0.0075 | 4 | 121 | 535 | 8.5 |
| b | vgg16_imagenet_feature_extract | pre-trained, frozen base (feature extraction) | 14,715,201 | 513 | 0.8623 | -0.0621 | 4 | 84 | 344 | 15.8 |
| b | vgg16_imagenet_fine_tune | pre-trained, fine-tune top block (block5_*), lr=1e-05 | 14,715,201 | 7,079,937 | 0.9659 | +0.0415 | 8 | 92 | 719 | 15.9 |
| b | resnet50_imagenet_feature_extract | pre-trained, frozen base (feature extraction) | 23,589,761 | 2,049 | 0.9218 | -0.0027 | 4 | 41 | 173 | 8.4 |
| b | resnet50_imagenet_fine_tune | pre-trained, fine-tune top block (conv5_*), lr=1e-05 | 23,589,761 | 14,978,049 | 0.9733 | +0.0488 | 8 | 51 | 392 | 7.1 |