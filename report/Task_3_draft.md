# Task 3 Report Draft: Data Augmentation

*Draft for the final report. Source: `../notebooks/code`, results in
`results/task_3/augmentation_results.md` and plots in `plots/task_3/`.*

**Setup:** the Task 2 CNN, trained from the same seed for every configuration, with the same
optimizer (Adam) and batch size (64). Each model trains for up to 20 epochs; early stopping ends a
run after 3 epochs without a new best validation accuracy. Augmentation is applied with Keras
preprocessing layers (the Keras 3 replacement for `ImageDataGenerator`).

## Discussion

### Summary
Data augmentation **can** improve validation accuracy on this task, but only one kind did.
The baseline (no augmentation) reached **0.9390**. The best configuration, **horizontal flip**,
reached **0.9507 (+1.2 points)**. Every geometric transform that resamples pixels (rotation, zoom,
translation) lowered accuracy, and the damage grew with the strength of the transform.

| Group | Configurations | Change vs. baseline |
|---|---|---|
| Helped | horizontal flip | +1.2 points |
| Possibly helped (uncertain, see below) | Gaussian noise 0.02 | +0.8 points |
| Neutral | horizontal + vertical flip, brightness 0.2, contrast 0.2, flip + noise combination | −0.3 to +0.4 points |
| Mildly harmful | rotation 0.05, zoom 0.1 / 0.2 / 0.3 | −0.9 to −1.7 points |
| Clearly harmful | translation 0.1, rotation 0.1, rotation 0.2, flip + rotation + zoom combination, translation 0.2 | −2.8 to −10.1 points |

**How much of a difference is real?** The baseline was trained twice with different seeds, and the
two runs differed by 0.3 points. Two runs is a very small sample, so that 0.3-point gap should be read
as a *lower bound* on run-to-run noise; differences of under roughly one point are treated with caution
below.

### Why horizontal flip helped
Given enough epochs, the baseline **overfits**. Its best validation accuracy came at epoch 10. After
that, training accuracy kept rising (0.945 → 0.957) while validation accuracy fell (0.939 → 0.930).
That is the situation data augmentation is designed for.

A horizontal flip is an *exact* transform: it rearranges pixels without creating any new pixel values.
A mirrored real photo is still a real photo, and its pixel-level statistics are unchanged. So the
flip gives the network more varied training images without changing what distinguishes the two
classes. With the flip, the final train/validation gap shrank from 2.7 points (baseline) to 1.4 points,
and validation accuracy kept improving until epoch 12.

Adding a vertical flip as well brought no further gain (+0.4 points, within noise). Upside-down scenes
are rare in real photos, so the extra variety is less useful.

### Why the geometric transforms hurt
Rotation, zoom and sub-pixel translation all **resample** the image: each output pixel is interpolated
from several input pixels, which smooths fine texture. That is exactly where the difference between the
classes lives. Real and AI-generated images in this dataset show the same kinds of subjects, so what the
network can exploit is pixel-level texture and local statistics. To a person, a rotated real photo is
still a photo. At the pixel level, its texture has been changed by interpolation. In other words, these
transforms are **not label-preserving for this task**, and label preservation is the assumption data
augmentation depends on. (Rotating a cat still gives a cat. Rotating a real photo does not necessarily
still give "real" pixel statistics.)

The results support this explanation in two ways:

1. **The harm grows with the amount of interpolation.** Rotation, the clearest case, went from −0.9 points
   (rotation 0.05) to −4.8 (rotation 0.1) to −6.6 (rotation 0.2). The three zoom settings all landed
   within about 0.6 points of each other (−1.1 to −1.7), too close to rank by strength.
2. **Validation accuracy became unstable.** The baseline's validation accuracy changed by about one point
   from epoch to epoch. With rotation 0.05, it swung between 0.76 and 0.93, even though training accuracy
   rose smoothly. The model was learning from interpolated images and being evaluated on clean ones, so
   small changes in what it learned produced large changes on the validation set.

Photometric transforms (brightness, contrast) change pixel values but not their spatial arrangement, and
they were neutral. Additive Gaussian noise did not hurt either, which suggests the network is not relying
on a faint noise pattern that low-amplitude noise could mask.

### Combinations
The standard flip + rotation 0.1 + zoom 0.2 combination scored −8.8 points: the harm from rotation and zoom
outweighed the benefit of the flip. The automatically built **flip + noise** combination (the two settings
that beat the baseline on their own) scored only +0.2 points, *below* flip alone. The two benefits did not
add up, which suggests the noise result was at least partly chance (see limitations).

### Limitations
* **Early stopping cut runs short.** Training was allowed up to 20 epochs, with early stopping after
  3 epochs without a new best validation accuracy. No run reached 20 epochs. The geometric runs, whose
  validation accuracy swung the most, were among the earliest to stop (5–11 epochs, except translation 0.1, which ran 16).
  Translation 0.2 stopped after only 5 epochs, so its −10.1-point result likely overstates its harm. The
  harm from the other geometric transforms may also be somewhat overstated.
* **One seed per configuration.** Apart from the baseline, each configuration was trained once. Results
  within about one point of the baseline cannot be told apart from noise.
* **"Best validation accuracy" is the best epoch's score.** Runs that train for more epochs get more
  chances at a high score by luck. The Gaussian noise run trained for 19 epochs, the most of any
  configuration, which is one more reason to treat its +0.8 points as unconfirmed.

### Conclusion
Data augmentation increased validation accuracy from 0.9390 to **0.9507** with a horizontal flip. Whether
an augmentation helps depends on whether it preserves the label. For a classifier that detects how an
image was made, transforms that leave pixel values intact (flip) or only shift them slightly (brightness,
contrast, light noise) are safe. Transforms that interpolate pixels (rotation, zoom, translation) are not:
they reduced accuracy by up to about 10 points, and more the stronger they were.

**Practical note:** moving the augmentation from the CPU data pipeline into the model (where it runs on the
GPU), and loading images at their native 32×32, cut training time from about 1,400 s to about 36–50 s per
epoch.
