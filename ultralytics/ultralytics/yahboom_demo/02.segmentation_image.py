from ultralytics import YOLO

# Load a model
model = YOLO("/home/pi/ultralytics/ultralytics/yolo11n-seg.pt")  # pretrained yolo11n-seg model
# model = YOLO("/home/pi/ultralytics/ultralytics/yolo11n-seg.onnx")
# model = YOLO("/home/pi/ultralytics/ultralytics/yolo11n-seg_ncnn_model")

# Run batched inference on a list of images
results = model("/home/pi/ultralytics/ultralytics/assets/zidane.jpg")  # return a list of Results objects

# Process results list
for result in results:
    # boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    # keypoints = result.keypoints  # Keypoints object for pose outputs
    # probs = result.probs  # Probs object for classification outputs
    # obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="/home/pi/ultralytics/ultralytics/output/zidane_output.jpg")  # save to disk
