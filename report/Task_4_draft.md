# Task 4 Report Draft: Regularization

*Draft for the final report. Source: `notebooks/code/task_4_regularization.ipynb`, results in
`results/task_4/regularization_flip_h_e20.md` and plots in `plots/task_4/`.*

**Setup:** the baseline is Task 3's best pipeline, the Task 2 CNN with horizontal-flip augmentation.
Each regularizer is added on top of it. Every configuration trains a fresh model from the same seed,
with Adam and batch size 64, for up to 20 epochs. Early stopping ends a run after 3 epochs without
a new best validation accuracy and restores the best epoch's weights. The baseline was trained
twice with different seeds to estimate run-to-run noise.

## Discussion

### Summary
Regularization improved validation accuracy slightly, and only one technique did it: dropout before
the classifier. The baseline reached **0.9428** (second seed: 0.9473, so differences under about
0.5 points are treated as noise). Dropout(0.5) on the pooled features reached **0.9505 (+0.8 points)**.

| Group | Configurations | Change vs. baseline |
|---|---|---|
| Helped | Dropout 0.5 before Dense, Dropout 0.25 before Dense | +0.8, +0.7 points |
| Neutral (within or barely above noise) | BatchNorm, Dropout 0.1 after every pool, L2 1e-5, BatchNorm + Dropout 0.5, best-of combination | −0.3 to +0.5 points |
| Harmful | Dropout 0.25 after every pool, L2 1e-4, BatchNorm + L2 1e-4, L2 1e-3 | −1.8 to −3.5 points |

### Dropout before the classifier
The gain is modest (only about 0.3 points above the better of the two baseline runs), but two things
suggest it is real. First, both dropout rates moved accuracy in the same direction by a similar amount.
Second, the training curves show the pattern regularization is supposed to produce. The baseline's
validation accuracy peaked around epoch 10 and then declined while training accuracy kept rising:
overfitting. With Dropout(0.5), validation accuracy stayed near 0.95 from about epoch 14 through the
20-epoch limit, and the run was ended by that limit rather than by early stopping. Dropout did not
raise the ceiling much; it pushed back the point where overfitting begins.

Dropping 50% of the 512 pooled features at every step means the classifier cannot rely on any small
set of features. It has to spread the decision across many of them, which generalizes better.

### Batch normalization
BatchNorm made training much faster (0.88 training accuracy after the first epoch, versus 0.80 for the
baseline), but it did not finish meaningfully higher (+0.5 points, only 0.02 above the noise threshold). Its validation accuracy was also
unstable, dropping to 0.79 at epoch 3. At inference, BatchNorm normalizes with running averages of the
batch statistics; while the weights are changing quickly, those averages lag behind, so the network
behaves differently in evaluation than in training. Its train/validation gap at the end of training
(4.7 points) was the largest of any single technique, so in this setting BatchNorm acted as an
optimization aid, not as a regularizer.

### L2 weight decay
The effect of L2 depended strongly on its strength: neutral at λ = 1e-5, −2.4 points at 1e-4, and
−3.5 points at 1e-3. At 1e-3 the model **underfit**: training and validation accuracy both stalled
near 0.90, with almost no gap between them. The penalty removed the overfitting by also removing the
capacity to learn the task.

### Dropout after every conv block
Dropout(0.1) after each pooling layer was effectively neutral (+0.5 points, barely above the noise threshold); Dropout(0.25) cost 1.8 points, and training accuracy
was also lower. Dropping activations inside every layer throws away part of the signal throughout the
network, which costs more than it gains on a model that overfits only mildly.

### Combinations
Combining techniques did not help:
* **BatchNorm + L2 1e-4 (−2.4 points)** was the most unstable run: validation accuracy fell to 0.66 at
  one epoch. This is a known interaction. BatchNorm makes a layer's output independent of the scale of
  the weights feeding it, so L2 cannot limit what those weights represent. What L2 does instead is
  shrink the weights, which increases the effective learning rate and destabilizes training.
* **BatchNorm + Dropout 0.5 (+0.2 points)** was no better than dropout alone, and its train/validation
  gap at the end of training was the largest of all runs (7.6 points). Dropout and BatchNorm are known
  to interact poorly: dropout changes the variance of activations between training and inference,
  while BatchNorm's running statistics assume it stays the same.
* **The automatic best-of combination** (BatchNorm + Dropout 0.1 after every pool + Dropout 0.5 before
  Dense) scored −0.3 points. Two of its three ingredients, BatchNorm and conv Dropout 0.1, had cleared
  the noise threshold by only 0.01–0.02 points, so the combination was built partly on chance results.

### Limitations
* **One seed per configuration** (apart from the baseline). Differences within about 0.5 points of the
  baseline cannot be told apart from noise.
* **Early stopping cut some runs short.** L2 1e-4 stopped after 8 epochs and BatchNorm + L2 after 6,
  so their harm may be somewhat overstated. Dropout 0.5 reached the 20-epoch limit and might have
  improved slightly with more epochs.
* **"Best validation accuracy" is the best epoch's score**, so runs that train for more epochs get more
  chances at a high score by luck. The dropout runs were among the longest.

### Conclusion
On top of the Task 3 pipeline, **Dropout(0.5) before the classifier** raised validation accuracy to
**0.9505**, mainly by delaying the onset of overfitting. BatchNorm sped up training without improving
the final result, L2 hurt at all but the smallest strength, and combining techniques did not stack.
Flip + Dropout(0.5) before the classifier becomes the baseline pipeline for Task 5.
