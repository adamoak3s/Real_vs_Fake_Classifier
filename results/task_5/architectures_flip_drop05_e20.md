| part | config | method | total_params | trainable_params | best_val_acc | delta_vs_baseline | cumulative_epochs | sec_per_epoch | cumulative_train_sec | val_inference_sec |
|---|---|---|---|---|---|---|---|---|---|---|
| a | task2_cnn | baseline (Task 2 CNN + flip + dropout) | 1,569,089 | 1,569,089 | 0.9492 | +0.0000 | 20 | 36 | 735 | 2.0 |
| a | mini_resnet | from scratch | 2,410,945 | 2,407,937 | 0.9378 | -0.0114 | 7 | 135 | 979 | 7.7 |
| a | mini_densenet | from scratch | 983,383 | 969,019 | 0.9596 | +0.0104 | 12 | 46 | 615 | 2.8 |
| a | resnet50_scratch | from scratch (random weights) | 23,589,761 | 23,536,641 | 0.9613 | +0.0121 | 14 | 210 | 3000 | 8.4 |
| b | vgg16_imagenet_feature_extract | pre-trained, frozen base (feature extraction) | 14,715,201 | 513 | 0.8635 | -0.0857 | 7 | 87 | 628 | 17.3 |
| b | vgg16_imagenet_fine_tune | pre-trained, fine-tune top block (block5_*), lr=1e-05 | 14,715,201 | 7,079,937 | 0.9729 | +0.0236 | 17 | 94 | 1574 | 16.7 |
| b | resnet50_imagenet_feature_extract | pre-trained, frozen base (feature extraction) | 23,589,761 | 2,049 | 0.9260 | -0.0232 | 7 | 42 | 305 | 8.6 |
| b | resnet50_imagenet_fine_tune | pre-trained, fine-tune top block (conv5_*), lr=1e-05 | 23,589,761 | 14,978,049 | 0.9778 | +0.0285 | 17 | 51 | 835 | 8.6 |