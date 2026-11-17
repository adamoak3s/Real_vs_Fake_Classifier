# Task 5 Report Draft: Stronger Architectures and Pre-trained Models

*Draft for the final report. Source: `notebooks/code/task_5_architectures.ipynb`, results in
`results/task_5/architectures_flip_drop05_e20.md` and plots in `plots/task_5/`.*

**Setup:** every model uses the best pipeline from Tasks 3 and 4: horizontal-flip augmentation at the
input and Dropout(0.5) before the final Dense layer. The only thing that changes between models is the
architecture and its starting weights. Images are upsampled from 32×32 to 180×180 inside each model.
From-scratch models train for up to 20 epochs. Pre-trained models train in two phases of up to 10 epochs
each: first with the pre-trained base frozen (only the new classifier head learns), then with the top
block of the base unfrozen at a 100× lower learning rate (1e-5). Early stopping ends a run after 3 epochs
without a new best validation accuracy. All models were trained in one run on the same machine, so their
training times are directly comparable.

## Results

| Model | Parameters (trainable) | Best val. acc. | Δ vs. baseline | Training time | s/epoch | Inference (20k images) |
|---|---|---|---|---|---|---|
| Task 2 CNN (baseline) | 1.57M | 0.9492 | — | 12.3 min | 36 | 2.0 s |
| Mini ResNet (scratch) | 2.41M | 0.9378 | −1.1 | 16.3 min | 135 | 7.7 s |
| Mini DenseNet (scratch) | 0.98M | 0.9596 | +1.0 | 10.3 min | 46 | 2.8 s |
| ResNet50 (scratch) | 23.6M | 0.9613 | +1.2 | 50.0 min | 210 | 8.4 s |
| VGG16, ImageNet, frozen | 14.7M (513) | 0.8635 | −8.6 | 10.5 min | 87 | 17.3 s |
| VGG16, ImageNet, fine-tuned | 14.7M (7.08M) | 0.9729 | +2.4 | 26.2 min* | 94 | 16.7 s |
| ResNet50, ImageNet, frozen | 23.6M (2,049) | 0.9260 | −2.3 | 5.1 min | 42 | 8.6 s |
| ResNet50, ImageNet, fine-tuned | 23.6M (15.0M) | **0.9778** | **+2.9** | 13.9 min* | 51 | 8.6 s |

\* Cumulative time of both phases (frozen + fine-tuning).

## Discussion

### (a) Stronger architectures trained from scratch
More powerful architectures helped only modestly. ResNet50 trained from random weights reached
0.9613 (+1.2 points), but with 15× the parameters of the baseline it took 50 minutes, about 4× as long.
The mini DenseNet reached 0.9596 (+1.0) with *fewer* parameters than the baseline (0.98M vs. 1.57M)
and less total training time. Its dense connections let every layer reuse all earlier features instead of
re-learning them, which makes it the most efficient from-scratch architecture here. The mini ResNet scored
0.9378 (−1.1).

All three from-scratch architectures use BatchNorm, and all three had unstable validation accuracy:
ResNet50 dropped to 0.73 at epoch 2, and the mini ResNet to 0.81 at epoch 3, even though training accuracy
rose smoothly. This matches the BatchNorm behavior in Task 4. At inference, BatchNorm normalizes with running
averages of batch statistics, and while the weights are changing quickly those averages lag behind, so the
network behaves differently in evaluation than in training. The instability also interacted with early
stopping: the mini ResNet was stopped after only 7 epochs, so its result likely understates what the
architecture can do.

### (b) Pre-trained models: feature extraction vs. fine-tuning
With the pre-trained base **frozen**, both models did worse than the baseline: VGG16 reached only 0.8635
and ResNet50 0.9260, and both plateaued after the first epoch. Training accuracy even stayed *below*
validation accuracy (VGG16: 0.81 vs. 0.86), a sign of underfitting: a single Dense layer on top of
frozen features cannot learn the task, and the dropout and flip are active only during training.

The reason is what ImageNet features encode. A network pre-trained on ImageNet learns to tell objects
apart: its early layers detect edges and textures, and its deep layers detect object parts and categories.
Real and AI-generated images in this dataset contain the same kinds of objects; they differ in fine,
pixel-level statistics. Frozen deep features carry little of that information.

**Fine-tuning** the top block changed this completely: VGG16 rose by 10.9 points to 0.9729 and ResNet50 by
5.2 points to **0.9778**, the best result of the whole project. Unfreezing the deepest layers, at a learning
rate low enough not to destroy the pre-trained features, let them re-tune from object detection to this
task while keeping the general low-level filters learned from ImageNet.

The fine-tuned models also trained smoothly, unlike the from-scratch BatchNorm models. The pre-trained base
runs in inference mode, so ResNet50's BatchNorm layers use their fixed ImageNet statistics instead of
updating running averages, and the lag that destabilized the from-scratch models does not occur.

### What pre-training is worth
ResNet50 was trained both ways with an identical architecture, input processing and classifier head, so
the comparison isolates the effect of the starting weights. Starting from ImageNet weights gave **1.7 points
higher** accuracy (0.9778 vs. 0.9613) in **less than a third of the training time** (14 vs. 50 minutes).
Pre-training was both more accurate and much cheaper.

### Training and running time
* **Fine-tuned ResNet50 is the best accuracy-for-time trade-off:** +2.9 points for only about 1.7 minutes more
  training than the baseline (835 s vs. 735 s).
* **VGG16** took about twice as long to train as ResNet50 (26 vs. 14 minutes) and is about twice as slow at
  inference (17 s vs. 8.6 s for the 20,000 validation images), for slightly lower accuracy. VGG16 has fewer
  parameters than ResNet50 but needs more computation per image, because its convolutions operate on large
  feature maps with many channels.
* The **baseline CNN** remains the fastest at inference (2.0 s), about 4× faster than ResNet50.

### Limitations
* **One seed per model.** Task 4 measured run-to-run noise of about ±0.5 points on this pipeline. The
  pre-trained gains (+2.4 and +2.9) are far beyond that; the ±1-point differences among the from-scratch
  models are only about twice the noise.
* **Early stopping** cut the unstable from-scratch runs short, especially the mini ResNet (7 epochs).
* **Both fine-tuning phases reached their 10-epoch limit**, but validation accuracy had been flat (about
  0.976 for ResNet50) since about the fifth fine-tuning epoch, so more epochs would likely change little.
  The fine-tuned ResNet50 also overfits (0.998 training vs. 0.975 validation accuracy at the end), yet it
  still generalizes best.

### Conclusion
Fine-tuning a pre-trained ResNet50 gave the highest validation accuracy, **0.9778** (+2.9 points over the
baseline), at little extra training cost. Larger architectures trained from scratch helped only modestly and
were much slower, and frozen pre-trained features underperformed even the baseline. The value of
pre-training here comes almost entirely from fine-tuning: ImageNet's low-level filters transfer, but its
deep, object-level features must be re-tuned to detect how an image was made.
