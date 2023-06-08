# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Example using PyCoral to detect objects in a given image.
To run this code, you must attach an Edge TPU attached to the host and
install the Edge TPU runtime (`libedgetpu.so`) and `tflite_runtime`. For
device setup instructions, see coral.ai/docs/setup.
Example usage:
```
bash examples/install_requirements.sh detect_image.py
python3 examples/detect_image.py \
  --model test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite \
  --labels test_data/coco_labels.txt \
  --input test_data/grace_hopper.bmp \
  --output ${HOME}/grace_hopper_processed.bmp
```
"""

import argparse
import time

from PIL import Image
from PIL import ImageDraw

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
import json
import os
from os import listdir


def draw_objects(draw, objs, labels):
  """Draws the bounding box and label for each object."""
  count = 0
  for obj in objs:
    bbox = obj.bbox
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                   outline='red')
    print(count)
    draw.text((bbox.xmin + 10, bbox.ymin + 10),
              '%s\n%.2f' % (count, obj.score),
              fill='red')
    count += 1


def ai_model(image_path):

    open(r"model\labelmap.txt")
    labels = r'model\labelmap.txt'
    interpreter = make_interpreter(r'model\edgetpu.tflite')
    interpreter.allocate_tensors()

    image = Image.open(image_path)
    _, scale = common.set_resized_input(
        interpreter, image.size, lambda size: image.resize(size, Image.ANTIALIAS))
    print(scale)

    # print('----INFERENCE TIME----')
    # print('Note: The first inference is slow because it includes', 'loading the model into Edge TPU memory.')
    for _ in range(2):
        start = time.perf_counter()
        interpreter.invoke()
        inference_time = time.perf_counter() - start
        objs = detect.get_objects(interpreter, 0, scale)
        print('%.2f ms' % (inference_time * 1000))

    # print('-------RESULTS--------')
    if not objs:
        print('No objects detected')
    counter_for_ai_output = 0
    ai_output = {}
    for obj in objs:
        #print(labels.get(obj.id, obj.id))
        print('  id:    ', obj.id)
        print('  score: ', obj.score)
        print('  bbox:  ', obj.bbox)

        # obj.bbox needs to be converted into a dictionary
        bbox = obj.bbox
        score = obj.score
        ai_output[counter_for_ai_output] = {}
        ai_output[counter_for_ai_output]['xmin'] = bbox.xmin
        ai_output[counter_for_ai_output]['ymin'] = bbox.ymin
        ai_output[counter_for_ai_output]['xmax'] = bbox.xmax
        ai_output[counter_for_ai_output]['ymax'] = bbox.ymax
        ai_output[counter_for_ai_output]['accuracy'] = score

        counter_for_ai_output += 1
    image = image.convert('RGB')
    draw_objects(ImageDraw.Draw(image), objs, labels)
    image.save('grace_hopper_processed.bmp')
    
        
    # image.show()
    if os.path.exists('meta.jpg') == True:
        os.remove('meta.jpg')
    image.save(r'C:\Users\kiv\Downloads\AstroX/meta/meta_' + images + '.bmp')

    with open('ai_output.json', 'w', encoding='utf-8') as f:
        json.dump(ai_output, f, ensure_ascii=False, indent=4)
    return ai_output


if __name__ == '__main__':
    folder_dir = r"C:\Users\kiv\Downloads\AstroX\data_chops_elected"
    for images in os.listdir(folder_dir):
        data = ai_model(folder_dir + "/" + images)
        print(data)