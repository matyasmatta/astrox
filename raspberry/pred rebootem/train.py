"""
Retrain a classification model on-device with weight imprinting

Resources:
- https://coral.ai/docs/edgetpu/retrain-classification-ondevice/#overview
- https://github.com/google-coral/pycoral/blob/master/examples/imprinting_learning.py
- https://github.com/CodeNextAdmin/edge_ml_club/blob/solutions/train_images.py
"""

from pathlib import Path
from PIL import Image

from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.dataset import read_label_file
from pycoral.learn.imprinting.engine import ImprintingEngine

def contents(folder):
    """
    Iterate over the contents of `folder`
    """
    for filename in folder.iterdir():
        yield folder/filename

# the absolute path for the directory where this Python script is stored
script_dir = Path(__file__).parent.resolve()
# specify the input and output (retrained) model
model_path = script_dir/'models'/'mobilenet_v1_1.0_224_l2norm_quant_edgetpu.tflite'
out_model_path = script_dir/'models'/'astropi-day-vs-nite.tflite'
#  specify where the labels and labelled training data are
data_dir = script_dir/'data'
labels_path = data_dir/'day-vs-night.txt'

'''
Create an instance of `ImprintingEngine` by specifying a compatible 
TensorFlow Lite model. We use a compatible pre-trained model here:
https://github.com/google-coral/test_data/raw/master/mobilenet_v1_1.0_224_l2norm_quant_edgetpu.tflite
The initialization function allows you to specify whether to keep the
classifications from the pre-trained model or abandon them and use only
the classes you're about to add.
'''
engine = ImprintingEngine(f"{model_path}", keep_classes=False)

'''
Create an instance of `Interpreter` for the Edge TPU, using the 
`ImprintingEngine` model, provided by `serialize_extractor_model()`.
'''
extractor_interpreter = make_interpreter(engine.serialize_extractor_model())
extractor_interpreter.allocate_tensors()
size = common.input_size(extractor_interpreter)

'''
Parse the file containing the labels and create a mapping from 
label id's to label names, e.g. {0: 'day', 1: 'night', 2: 'twilight'}
'''
labels = read_label_file(labels_path)

'''
For each training image, run an inference with the Interpreter and collect 
the output (which is the image embedding). Then train a new class or continue 
training an existing class by calling train(), which takes the image embedding
and a label ID.
'''
# for each class
for class_id, class_name in labels.items():
    print(f"Class {class_id}: {class_name}")
    # for each training image for the current class
    for image_path in contents(data_dir/class_name):
        image = Image.open(image_path).convert('RGB').resize(size, Image.Resampling.NEAREST)
        # run an inference with the `Interpreter`
        common.set_input(extractor_interpreter, image)
        extractor_interpreter.invoke()
        # collect the output (which is the image embedding).
        embedding = classify.get_scores(extractor_interpreter)
        print(f"{image_path.name} scores: {embedding}")
        # continue training the current class by calling `train()`
        engine.train(embedding, class_id)

'''
Save the retrained model using `serialize_model()`
'''
with open(out_model_path, 'wb') as f:
    f.write(engine.serialize_model())
