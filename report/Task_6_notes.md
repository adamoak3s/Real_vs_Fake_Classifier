# Task 6 Notes: Off-the-shelf Tools

*Working notes for the final report. Scoring notebook: `notebooks/code/task_6_offtheshelf.ipynb`.*

## The shared test sample
* 200 images from the **test** set: 100 REAL, 100 FAKE, drawn at random (fixed seed), shuffled and
  renamed `img_001` … `img_200`. Answer key: `results/task_6/answer_key.csv`.
* `data/task_6_sample/images/`: each image enlarged 8× (32×32 → 256×256, nearest-neighbor, no blending).
* `data/task_6_sample/sheets/`: 8 contact sheets of 25 numbered images, for the chat tools.
* `data/task_6_sample/PROMPT.txt`: the prompt every chat tool gets (no examples, no hint about the
  share of fakes).
* `data/task_6_sample/teachable_machine_train/`: 500 REAL + 500 FAKE *training* images (enlarged the
  same way) for training a Teachable Machine model. None of them are in the test sample.

## Claude (done)
* **Model and method:** Claude (Fable 5.2) in the Claude app, November 16, 2026. It viewed the 8
  contact sheets and labeled all 200 images zero-shot, before the answer key was read. Predictions:
  `results/task_6/predictions/claude.csv`.
* **Result:** accuracy **0.765** (153 of 200). Precision (FAKE) 0.873, recall (FAKE) 0.620, F1 0.725.

  | | called FAKE | called REAL |
  |---|---|---|
  | is FAKE (100) | 62 | 38 |
  | is REAL (100) | 9 | 91 |

* **How it decided:** by visible style only: generated images tended to look cleaner, more saturated
  and more "composed" (centered subject, smooth blurred background, vignette); real ones noisier, with
  awkward crops and cluttered backgrounds.
* **How it failed:** it called 71 images FAKE, although 100 were. Real photos were almost always
  recognized (91%), but 38% of the fakes passed as real. When a generated image doesn't have the
  "too clean" look, there is nothing left for a person-style visual judgment to go on.
* **Caveats:** Claude designed the sample, so it knew the sample was balanced (the other tools aren't
  told). It did not use that to adjust its answers. One run, 200 images: the 95% confidence interval
  for its accuracy is roughly 0.70–0.82.

## Gemini (done)
* **Model and method:** Gemini Pro (the "Pro" model in the Gemini app; version number not recorded), November 16, 2026, same 8 contact sheets
  and the prompt in `PROMPT.txt`, zero-shot. All 8 sheets were uploaded in a single message, and it
  replied with all 200 answers at once. Predictions: `results/task_6/predictions/gemini.csv`.
* **Result:** accuracy **0.395** (79 of 200; 95% CI 0.33–0.46), which is *below* guessing.
  Precision (FAKE) 0.200, recall (FAKE) 0.070, F1 0.104.

  | | called FAKE | called REAL |
  |---|---|---|
  | is FAKE (100) | 7 | 93 |
  | is REAL (100) | 28 | 72 |

* **How it failed:** it called only 35 images FAKE, and 28 of those 35 were real photos. It caught 7
  of the 100 fakes. Its sense of "looks fake" pointed the wrong way on this dataset: the low-quality,
  noisy real photos were the ones it flagged, and the clean generated images passed as real.
* **Answered all 200** in the requested format, with no refusals.

## Teachable Machine (done)
* **Model and method:** Google Teachable Machine, Standard image model, default settings, trained in
  the browser on 500 REAL + 500 FAKE *training* images (enlarged to 256×256), November 16, 2026. No
  account needed. The trained model was exported (TensorFlow.js format) and run in code on the 200
  sample images with Teachable Machine's own preprocessing (resize to 224×224, scale to −1…1).
  Class probabilities: `results/task_6/teachable_machine/teachable_machine_probs.csv`.
* **Result:** accuracy **0.865** (173 of 200; 95% CI about 0.81–0.91). Precision (FAKE) 0.854,
  recall (FAKE) 0.880, F1 0.867.

  | | called FAKE | called REAL |
  |---|---|---|
  | is FAKE (100) | 88 | 12 |
  | is REAL (100) | 15 | 85 |

* **Class mapping:** the classes were left as "Class 1" and "Class 2"; the FAKE folder was uploaded
  to Class 1 and the REAL folder to Class 2.
* **Challenges:** uploading 1,000 images by hand; no built-in way to test a batch of images (the
  preview takes one at a time), so the model had to be exported and run in code; training settings
  and the base network (MobileNet) are fixed; it rescales every image to 224×224.

## ChatGPT (not completed)
* Hit an upload limit before the 8 sheets could be submitted. This is itself a finding for the
  "challenges" section: usage limits can block even a 200-image evaluation.

## Still to run (needs your accounts)
* **ChatGPT (if retried):** new chat; upload one sheet at a time with the text of `PROMPT.txt`;
  paste all 8 replies into `save_predictions("chatgpt", '''…''')` in the notebook (same for "gemini").
  Write down the model name and date for the report.

## Challenges observed so far (for the report)
* **No training signal.** A chat tool gets no labeled examples from this dataset; it can only apply
  general visual judgment. My model learned from 80,000 labeled examples.
* **Image size.** The images are 32×32. Chat tools resize and re-encode uploads, which can alter the
  pixel-level texture that Tasks 3–5 showed the trained models rely on.
* **Throughput and cost.** 200 images took 8 uploads and manual copying of answers; my model labels
  20,000 images in seconds. Chat tools also have upload and message limits.
* **Output format.** Free-text replies must be parsed, and a tool may skip images or refuse to commit.
  The scoring notebook counts an unanswered image as wrong.
* **Reproducibility.** Chat models change over time and can answer differently on a second try.
* **Small sample.** With 200 images, accuracy is uncertain by about ±6 points.
