from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import os
import uvicorn
import base64
import time
from io import BytesIO
import logging

from utils import generate_point_cloud, calculate_3d_volume, calculate_fill_percentage, generate_3d_visualization

os.environ["PYOPENGL_PLATFORM"] = "egl"

app = FastAPI()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

origins = [
    "http://localhost",
    "http://localhost:3000",  
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "🚀 Konteyner Hacim Hesaplama API'si Çalışıyor!"}

def convert_image_to_base64(image_np: np.ndarray) -> str:
    try:
        _, buffer = cv2.imencode('.jpg', image_np)  # JPEG formatında encode et
        return base64.b64encode(buffer).decode("utf-8")
    except Exception as e:
        logging.error(f"🚨 Görsel Base64 formatına çevrilemedi: {e}")
        return None

@app.post("/calculate")
async def calculate_volume(containerImage: UploadFile = File(...), containerVolume: float = Form(...)):
    try:
        start_time = time.time()
        logging.info(f"✅ Yeni işlem başladı. Konteyner hacmi: {containerVolume} m³")

        image_data = await containerImage.read()
        try:
            image_pil = Image.open(BytesIO(image_data))
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="❌ Geçersiz dosya formatı!")

        if image_pil.format not in ["JPEG", "PNG", "WEBP"]:
            raise HTTPException(status_code=400, detail="❌ Sadece JPG, PNG ve WEBP formatları desteklenmektedir!")

        optimized_image = np.array(image_pil)
        image_cv = cv2.cvtColor(optimized_image, cv2.COLOR_RGB2BGR)

        logging.info("📊 Görsel başarıyla işleme alındı.")

        point_cloud = generate_point_cloud(image_cv)
        if len(point_cloud.points) == 0:
            raise HTTPException(status_code=500, detail="❌ 3D nokta bulutu boş, görselleştirme yapılamıyor!")

        volume = calculate_3d_volume(point_cloud)

        fill_percentage = calculate_fill_percentage(image_cv)
        filled_volume = (fill_percentage / 100) * containerVolume

        container_image_3d = generate_3d_visualization(point_cloud)
        if container_image_3d is None:
            raise HTTPException(status_code=500, detail="❌ 3D görselleştirme başarısız oldu!")

        # NumPy dizisini Base64'e dönüştür
        img_str = convert_image_to_base64(container_image_3d)
        if img_str is None:
            raise HTTPException(status_code=500, detail="❌ Görseli Base64 formatına çevirme başarısız oldu!")

        processing_time = round(time.time() - start_time, 2)
        logging.info(f"✅ 3D görselleştirme tamamlandı! İşlem süresi: {processing_time} saniye")

        return JSONResponse(content={
            "fill_percentage": round(fill_percentage, 2),
            "filled_volume": round(filled_volume, 2),
            "3d_volume": round(volume, 2),
            "3d_image": f"data:image/jpeg;base64,{img_str}",
            "processing_time": processing_time
        })

    except HTTPException as e:
        logging.error(f"🔥 API Hatası: {e.detail}")
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)

    except Exception as e:
        logging.error(f"🔥 Beklenmeyen bir hata oluştu: {e}")
        return JSONResponse(content={"error": "❌ Sunucu iç hatası!"}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
