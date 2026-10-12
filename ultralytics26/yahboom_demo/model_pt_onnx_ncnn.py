from ultralytics import YOLO

# Load a YOLo PyTorch model
model = YOLO("/home/pi/ultralytics26/yolo26n.pt")
# model = YOLO("/home/pi/ultralytics26/yolo26n-seg.pt")
# model = YOLO("/home/pi/ultralytics26/yolo26n-pose.pt")
# model = YOLO("/home/pi/ultralytics26/yolo26n-cls.pt")
# model = YOLO("/home/pi/ultralytics26/yolo26n-obb.pt")

# Export the model to ONNX format
model.export(format="onnx")  # This will create 'yolo11n.onnx' in the same directory

# Export the model to NCNN format
model.export(format="ncnn")  # creates 'yolo11n_ncnn_model'

