from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from ultralytics import YOLO
import open3d as o3d
import uvicorn

app = FastAPI()

# YOLOv8 Modelini Yükle
model = YOLO("yolov8n.pt")

@app.get("/")
def home():
    return {"message": "🚀 Konteyner Doluluk API'si Çalışıyor!"}

@app.post("/calculate")
async def calculate_volume(containerImage: UploadFile = File(...)):
    try:
        # Görseli oku
        image_data = await containerImage.read()
        image_np = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # YOLOv8 ile nesne tanıma
        results = model(image)
        detected_objects = len(results[0].boxes)

        return {
            "message": "📦 Konteyner Doluluk Tahmini",
            "detected_objects": detected_objects
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
