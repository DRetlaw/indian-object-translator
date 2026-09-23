from ultralytics import YOLO


class ObjectDetector:
    def __init__(self, model_name="yolo26n.pt", confidence_threshold=0.40):
        self.model = YOLO(model_name)
        self.confidence_threshold = confidence_threshold

    def detect(self, image):
        results = self.model(image, verbose=False)
        result = results[0]

        detections = []

        for box in result.boxes:
            confidence = float(box.conf[0])

            if confidence < self.confidence_threshold:
                continue

            class_id = int(box.cls[0])
            object_name = result.names[class_id]

            detections.append(
                {
                    "object": object_name,
                    "confidence": confidence,
                    "bbox": box.xyxy[0].tolist(),
                }
            )

        detections.sort(key=lambda item: item["confidence"], reverse=True)

        return detections
