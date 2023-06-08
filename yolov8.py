from ultralytics import YOLO

# Load a model
model = YOLO("yolov8_latest.pt")  # load a pretrained model (recommended for training)

# Use the model
results = model(r"C:\Users\kiv\Downloads\AstroX\data_chops_elected\img_0_x1515_y505.jpg")  # predict on an image
path = model.export(format="tflite")  # export the model to ONNX format