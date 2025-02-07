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
from PIL import Image, UnidentifiedImageError
import logging

from utils import generate_point_cloud, calculate_3d_volume, calculate_fill_percentage, generate_3d_visualization

# Open3D'nin headless modda çalışmasını sağla (Render sorunu önleme)
os.environ["PYOPENGL_PLATFORM"] = "egl"

# FastAPI uygulamasını başlat
app = FastAPI()

# Logger ayarları
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# CORS ayarları (React ile entegrasyon için)
origins = [
    "http://localhost",
    "http://localhost:3000",  # React uygulamasının çalıştığı port
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


def convert_image_to_jpg(image: Image.Image) -> Image.Image:
    """
    Her formatı optimize edilmiş JPG formatına çevirir.
    """
    try:
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        return image
    except Exception as e:
        logging.error(f"🚨 Görsel format dönüşüm hatası: {e}")
        return None

def convert_image_to_base64(image):
    """
    Görseli Base64 formatına çevirerek API'de JSON olarak döndürmeyi sağlar.
    """
    try:
        # Eğer image str (Base64) tipinde ise önce görseli yüklememiz gerekiyor
        if isinstance(image, str):
            image = Image.open(BytesIO(base64.b64decode(image)))

        # Görseli Base64 formatına çevir
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=85, optimize=True)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        logging.error(f"🚨 Görsel Base64 formatına çevrilemedi: {e}")
        return None



@app.post("/calculate")
async def calculate_volume(containerImage: UploadFile = File(...), containerVolume: float = Form(...)):
    """
    Kullanıcının yüklediği konteyner fotoğrafından hacim ve doluluk oranı hesaplar.
    3D nokta bulutu oluşturur ve Base64 formatında optimize edilmiş JPG döndürür.
    """
    try:
        start_time = time.time()
        logging.info(f"✅ Yeni işlem başladı. Konteyner hacmi: {containerVolume} m³")

        # 📸 Görseli oku (PNG, JPG, WEBP destekleniyor)
        image_data = await containerImage.read()
        try:
            image_pil = Image.open(BytesIO(image_data))
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="❌ Geçersiz dosya formatı!")

        # 📌 Eğer desteklenmeyen bir formatsa hata döndür
        if image_pil.format not in ["JPEG", "PNG", "WEBP"]:
            raise HTTPException(status_code=400, detail="❌ Sadece JPG, PNG ve WEBP formatları desteklenmektedir!")

        logging.info(f"📸 Yüklenen görsel formatı: {image_pil.format}")

        # 📌 Görseli optimize edilmiş JPG formatına dönüştür
        optimized_image = convert_image_to_jpg(image_pil)
        if optimized_image is None:
            raise HTTPException(status_code=500, detail="❌ Görsel optimize edilemedi!")

        # OpenCV ile işleme sokmak için numpy array'e çevir
        image_np = np.array(optimized_image)
        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        logging.info("📊 Görsel başarıyla işleme alındı.")

        # 🚀 3D nokta bulutu oluştur
        point_cloud = generate_point_cloud(image_cv)
        if len(point_cloud.points) == 0:
            raise HTTPException(status_code=500, detail="❌ 3D nokta bulutu boş, görselleştirme yapılamıyor!")

        logging.info("📊 3D nokta bulutu oluşturuldu.")

        # 📏 Hacim hesaplama
        volume = calculate_3d_volume(point_cloud)

        # 📊 Doluluk oranı hesaplama
        fill_percentage = calculate_fill_percentage(image_cv)
        filled_volume = (fill_percentage / 100) * containerVolume

        logging.info(f"📏 Hesaplamalar tamamlandı. Doluluk oranı: %{fill_percentage}, Dolu Hacim: {filled_volume} m³")

        # 🖼️ 3D görsel oluştur
        container_image_3d = generate_3d_visualization(point_cloud)
        if container_image_3d is None:
            raise HTTPException(status_code=500, detail="❌ 3D görselleştirme başarısız oldu!")

        # 🖼️ 3D görseli optimize edilmiş JPG Base64 formatına çevir
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
