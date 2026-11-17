"""Score an exported Teachable Machine image model on the Task 6 sample.

1. In Teachable Machine: Export Model -> Tensorflow.js -> Download my model, then unzip it.
   The folder holds model.json, weights.bin and metadata.json.
2. Run:

       python score_teachable_machine.py <unzipped model folder> <label of class 1> <label of class 2>

   for example:  python score_teachable_machine.py ~/Downloads/tm-my-image-model FAKE REAL

   The two labels say which folder was uploaded to the first and second class. They can be left
   out if the classes were named REAL and FAKE in Teachable Machine.

It writes results/task_6/predictions/teachable_machine.csv (id,pred), which task_6_offtheshelf.ipynb
scores, and results/task_6/teachable_machine/teachable_machine_probs.csv (raw class probabilities).

How it works: the export describes a small network (a MobileNet feature extractor plus a two-layer
classifier) in model.json and stores its weights in weights.bin. This script rebuilds that network
layer by layer in Keras, copies the weights in, and applies Teachable Machine's own preprocessing
(resize to the model's input size, then scale pixels to the range -1..1).

Requires tensorflow/keras, numpy and Pillow (the same environment as the notebooks).
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
import keras
from keras import layers


def find_project_root():
    here = Path(__file__).resolve().parent
    for d in [here, *here.parents]:
        if (d / "data" / "task_6_sample" / "images").is_dir():
            return d
    sys.exit("Couldn't find data/task_6_sample/images. Run prepare_task_6_sample.py first.")


def make_layer(class_name, c):
    """Build one Keras layer from its entry in model.json."""
    name = c["name"]
    if class_name == "ZeroPadding2D":
        return layers.ZeroPadding2D(padding=c["padding"], name=name)
    if class_name == "Conv2D":
        return layers.Conv2D(c["filters"], c["kernel_size"], strides=c["strides"], padding=c["padding"],
                             dilation_rate=c["dilation_rate"], activation=c["activation"],
                             use_bias=c["use_bias"], name=name)
    if class_name == "DepthwiseConv2D":
        return layers.DepthwiseConv2D(c["kernel_size"], strides=c["strides"], padding=c["padding"],
                                      depth_multiplier=c["depth_multiplier"], dilation_rate=c["dilation_rate"],
                                      activation=c["activation"], use_bias=c["use_bias"], name=name)
    if class_name == "BatchNormalization":
        return layers.BatchNormalization(axis=c["axis"], momentum=c["momentum"], epsilon=c["epsilon"],
                                         center=c["center"], scale=c["scale"], name=name)
    if class_name == "ReLU":
        return layers.ReLU(max_value=c.get("max_value"), name=name)
    if class_name == "Add":
        return layers.Add(name=name)
    if class_name == "GlobalAveragePooling2D":
        return layers.GlobalAveragePooling2D(name=name)
    if class_name == "Dense":
        return layers.Dense(c["units"], activation=c["activation"], use_bias=c["use_bias"], name=name)
    sys.exit(f"This export uses a layer type the script doesn't know: {class_name}")


def build(config, x):
    """Apply a Sequential or functional ('Model') block from model.json to tensor x."""
    if isinstance(config.get("layers"), list) and "input_layers" in config:      # functional graph
        outputs = {}
        for entry in config["layers"]:
            if entry["class_name"] == "InputLayer":
                outputs[entry["name"]] = x
                continue
            inputs = [outputs[node[0]] for node in entry["inbound_nodes"][0]]
            layer = make_layer(entry["class_name"], entry["config"])
            outputs[entry["name"]] = layer(inputs if len(inputs) > 1 else inputs[0])
        return outputs[config["output_layers"][0][0]]
    for entry in config["layers"]:                                              # Sequential
        if entry["class_name"] in ("Sequential", "Model"):
            x = build(entry["config"], x)
        else:
            x = make_layer(entry["class_name"], entry["config"])(x)
    return x


def load_teachable_machine(model_dir):
    spec = json.loads((model_dir / "model.json").read_text())
    meta = json.loads((model_dir / "metadata.json").read_text())
    size = meta.get("imageSize", 224)
    inputs = keras.Input((size, size, 3))
    model = keras.Model(inputs, build(spec["modelTopology"]["config"], inputs))

    # weights.bin is one long run of float32 numbers, in the order listed in model.json
    raw = np.frombuffer((model_dir / "weights.bin").read_bytes(), dtype="<f4")
    by_layer, pos = {}, 0
    for group in spec["weightsManifest"]:
        for w in group["weights"]:
            n = int(np.prod(w["shape"])) if w["shape"] else 1
            layer_name, var = w["name"].rsplit("/", 1)
            by_layer.setdefault(layer_name, {})[var] = raw[pos:pos + n].reshape(w["shape"])
            pos += n
    assert pos == raw.size, "weights.bin doesn't match model.json"
    order = ["kernel", "depthwise_kernel", "bias", "gamma", "beta", "moving_mean", "moving_variance"]
    for layer in model.layers:
        if layer.name in by_layer:
            vals = by_layer[layer.name]
            layer.set_weights([vals[k] for k in order if k in vals])
        elif layer.weights:
            sys.exit(f"No weights found in the export for layer {layer.name}")
    return model, meta, size


def main():
    if len(sys.argv) not in (2, 4):
        sys.exit("usage: python score_teachable_machine.py <model folder> [<class 1 label> <class 2 label>]")
    model_dir = Path(sys.argv[1]).expanduser()
    model, meta, size = load_teachable_machine(model_dir)
    labels = [s.upper() for s in (sys.argv[2:4] if len(sys.argv) == 4 else meta["labels"])]
    if sorted(labels) != ["FAKE", "REAL"]:
        sys.exit(f"The model's classes are {meta['labels']}. Say which is which, for example:\n"
                 f"  python score_teachable_machine.py {sys.argv[1]} FAKE REAL")

    root = find_project_root()
    files = sorted((root / "data" / "task_6_sample" / "images").glob("*.png"))
    x = np.stack([np.asarray(Image.open(f).convert("RGB"), dtype="float32") for f in files])
    x = keras.ops.image.resize(x, (size, size), interpolation="bilinear")
    x = x / 127.0 - 1.0                                   # Teachable Machine's own scaling
    probs = model.predict(x, batch_size=32, verbose=0)

    out = root / "results" / "task_6"
    (out / "teachable_machine").mkdir(parents=True, exist_ok=True)
    (out / "predictions").mkdir(parents=True, exist_ok=True)
    ids = [int(f.stem.split("_")[-1]) for f in files]
    with open(out / "teachable_machine" / "teachable_machine_probs.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "p_class1", "p_class2"])
        w.writerows([i, f"{p[0]:.4f}", f"{p[1]:.4f}"] for i, p in zip(ids, probs))
    with open(out / "predictions" / "teachable_machine.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "pred"])
        w.writerows([i, labels[int(np.argmax(p))]] for i, p in zip(ids, probs))
    print(f"scored {len(files)} images (class 1 = {labels[0]}, class 2 = {labels[1]}) "
          f"-> results/task_6/predictions/teachable_machine.csv")


if __name__ == "__main__":
    main()
