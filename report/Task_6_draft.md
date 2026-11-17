# Task 6 Report Draft: Off-the-shelf Tools

*Draft for the final report. Source: `notebooks/code/task_6_offtheshelf.ipynb`, results in
`results/task_6/tool_comparison.md`, plots in `plots/task_6/`, method details in `report/Task_6_notes.md`.*

## Setup
Every tool was scored on the same sample: 200 images drawn at random from the **test** set (100 real,
100 fake), shuffled and renamed so file names reveal nothing. For the chat tools, the 32×32 images were
enlarged 8× without smoothing and arranged on 8 numbered contact sheets, and each tool received the same
prompt with no examples and no hint about the share of fakes.

| Tool | What it is | How it was used |
|---|---|---|
| My model | ImageNet-pre-trained ResNet50, fine-tuned (Task 5's best, with flip + dropout) | Trained on 80,000 labeled images |
| Teachable Machine | Google's browser tool; trains a small classifier on a frozen pre-trained network | Trained on 1,000 labeled images (500 per class), default settings |
| Claude (Fable 5.2) | General-purpose AI assistant | Zero-shot, from the contact sheets |
| Gemini (Pro) | General-purpose AI assistant | Zero-shot, all 8 sheets in one message |
| ChatGPT | General-purpose AI assistant | Not completed: upload limit reached |

**Metrics:** accuracy, plus precision, recall and F1 with FAKE as the positive class, and confusion
matrices. Accuracy alone cannot show whether a tool misses fakes or falsely accuses real photos, and those
are different failures. With 200 images, each accuracy carries a 95% confidence interval of roughly ±5
points, which is reported alongside it.

## Results

| Tool | Accuracy (95% CI) | Precision (FAKE) | Recall (FAKE) | F1 (FAKE) |
|---|---|---|---|---|
| **My model** | **0.990** (0.964–0.997) | 1.000 | 0.980 | 0.990 |
| Teachable Machine | 0.865 (0.811–0.906) | 0.854 | 0.880 | 0.867 |
| Claude | 0.765 (0.702–0.818) | 0.873 | 0.620 | 0.725 |
| Gemini | 0.395 (0.330–0.464) | 0.200 | 0.070 | 0.104 |

Confusion matrices (counts out of 100 per row):

| | My model | Teachable Machine | Claude | Gemini |
|---|---|---|---|---|
| Fake called fake | 98 | 88 | 62 | 7 |
| Fake called real | 2 | 12 | 38 | 93 |
| Real called fake | 0 | 15 | 9 | 28 |
| Real called real | 100 | 85 | 91 | 72 |

On the **full 20,000-image test set**, which no earlier task used, my model reached **0.975** accuracy
(precision 0.976, recall 0.975, F1 0.975), in line with its validation accuracy of 0.978. Its 0.990 on the
200-image sample is consistent with that, given the sample's confidence interval.

## Discussion

### Accuracy follows how much each tool learned from this data
The ranking matches the amount of task-specific training. My model was fine-tuned on 80,000 labeled images.
Teachable Machine trained on 1,000. The chat tools had none: they could only apply general visual judgment
about what AI-generated images look like.

The confidence intervals of neighboring tools do not overlap, except that Teachable Machine (0.811–0.906)
and Claude (0.702–0.818) overlap slightly, so the gap between those two is the least certain.

### Teachable Machine: a quick, decent baseline
With a few minutes of work and 1,000 images, Teachable Machine reached 86.5%, with balanced errors (12% of
fakes missed, 15% of real photos flagged). It works the same way as the "frozen base" models in Task 5: a
pre-trained network (MobileNet) whose features are kept fixed, with only a small classifier trained on top.
Task 5 showed the limit of that approach for this problem. Frozen ImageNet features describe objects, not
the pixel-level traces of how an image was made, and the largest gains came from fine-tuning the deep
layers, which Teachable Machine does not do.

### Claude: reasonable precision, poor recall
Claude scored 76.5%. When it called an image fake it was usually right (precision 0.873), and it recognized
91% of real photos, but it missed 38% of the fakes. It judged by visible style: images that looked
unusually clean, saturated and neatly composed were called fake. Generated images without that look gave
it nothing to go on, so they passed as real.

### Gemini: worse than guessing
Gemini scored 39.5%, and its confidence interval (0.330–0.464) lies entirely below 50%. It called only 35
images fake, and 28 of those were real photos; it caught 7 of the 100 fakes (recall 0.07). Its notion of
"looks fake" pointed the wrong way for this dataset. A likely explanation is that the real photos here are
noisy and low quality while the generated ones are clean, so a judgment that treats visual defects as a
sign of AI generation flags the wrong class. Gemini also received all 200 images in one message, which may
have reduced its accuracy compared with one sheet at a time.

This result shows why accuracy alone is not enough: a recall of 0.07 says more about the failure than the
accuracy does.

### Challenges in using off-the-shelf tools
* **No training signal (chat tools).** They cannot learn what distinguishes the classes in *this* dataset.
* **Image handling.** The images are 32×32. Chat tools and Teachable Machine resize uploads, and chat tools
  re-encode them, which can alter the pixel-level texture that Tasks 3–5 showed trained models rely on.
* **Volume limits.** ChatGPT's upload limit stopped the test before the 8 sheets were submitted. A
  200-image evaluation was already at the edge of what a chat interface allows.
* **Manual effort and throughput.** Chat tools need uploads and copying of answers; Teachable Machine needs
  1,000 manual uploads and offers no batch testing (its preview takes one image at a time), so its model had
  to be exported and run in code. My model labeled the 20,000-image test set in about 15 seconds.
* **Free-text output.** Replies must be parsed, and a tool may skip images or decline to commit. (Both chat
  tools that completed the test answered all 200 in the requested format.)
* **Reproducibility.** Hosted models change over time and can answer differently on a second run, and the
  exact model version is not always shown.
* **No control.** Teachable Machine fixes the architecture and most training settings; chat tools expose
  none.

### Limitations of this comparison
* One run per tool on 200 images.
* Claude designed the sample and knew it was balanced; the other tools were not told. It did not use that to
  adjust its answers, but the conditions were not identical.
* Gemini received all sheets in one message; Claude viewed them in two batches of four.
* The Teachable Machine model was run in code with its own preprocessing; resizing may differ slightly from
  its browser preview.
* The chat tools were tested zero-shot. Giving them labeled examples in the prompt might improve them.

### Conclusion
For this problem, a model trained on the task far outperformed off-the-shelf tools: 99.0% on the shared
sample (97.5% on the full test set), against 86.5% for Teachable Machine, 76.5% for Claude and 39.5% for
Gemini. Detecting AI-generated images at 32×32 depends on pixel-level patterns that have to be learned from
labeled examples of this specific data; general visual judgment is unreliable and, in Gemini's case,
systematically wrong. Teachable Machine is a useful quick baseline when some labeled data is available, but
it cannot fine-tune the deep features that mattered most here.
