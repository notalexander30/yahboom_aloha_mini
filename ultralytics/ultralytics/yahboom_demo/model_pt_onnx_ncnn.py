from ultralytics import YOLO

# Load a YOLO11n PyTorch model
model = YOLO("/home/pi/ultralytics/ultralytics/yolo11n.pt")
# model = YOLO("/home/pi/ultralytics/ultralytics/yolo11n-seg.pt")
# model = YOLO("/home/pi/ultralytics/ultralytics/yolo11n-pose.pt")
# model = YOLO("/home/pi/ultralytics/ultralytics/yolo11n-cls.pt")
# model = YOLO("/home/pi/ultralytics/ultralytics/yolo11n-obb.pt")

# Export the model to ONNX format
model.export(format="onnx")  # This will create 'yolo11n.onnx' in the same directory

# Export the model to NCNN format
model.export(format="ncnn")  # creates 'yolo11n_ncnn_model'

