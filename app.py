from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import os
import uvicorn
import base64
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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


def generate_matplotlib_3d(point_cloud):
    """
    Eğer Open3D başarısız olursa, Matplotlib ile 3D nokta bulutu görselleştirmesi oluştur.
    """
    try:
        logging.info("Matplotlib ile 3D görselleştirme başlatılıyor...")
        
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Nokta bulutundaki X, Y, Z değerlerini al
        xyz = np.asarray(point_cloud.points)
        ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], c='b', marker='o', s=1)

        ax.set_xlabel('X Ekseni')
        ax.set_ylabel('Y Ekseni')
        ax.set_zlabel('Z Ekseni')

        # Görseli kaydet
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        
        logging.info("Matplotlib 3D görsel başarıyla oluşturuldu.")
        return Image.open(buf)
    
    except Exception as e:
        logging.error(f"Matplotlib ile 3D görselleştirme başarısız oldu: {e}")
        return None


def convert_image_to_base64(image):
    """
    PIL.Image nesnesini Base64 string formatına çevirir.
    """
    try:
        if isinstance(image, np.ndarray):
            logging.warning("Gelen görsel numpy array formatında! PIL.Image formatına dönüştürülüyor...")
            image = Image.fromarray(image)

        elif not isinstance(image, Image.Image):
            logging.error(f"Geçersiz görsel formatı: {type(image)}")
            return None

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    except Exception as e:
        logging.error(f"Görsel Base64 formatına çevrilemedi: {e}")
        return None


@app.post("/calculate")
async def calculate_volume(containerImage: UploadFile = File(...), containerVolume: float = Form(...)):
    """
    Kullanıcının yüklediği konteyner fotoğrafından hacim ve doluluk oranı hesaplar.
    3D nokta bulutu oluşturur ve Base64 formatında bir görsel döndürür.
    """
    try:
        logging.info(f"Yeni işlem başladı. Konteyner hacmi: {containerVolume} m³")

        # Görseli oku ve OpenCV ile işleme al
        image_data = await containerImage.read()
        npimg = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="❌ Yüklenen görüntü geçersiz!")

        logging.info("Görsel başarıyla okundu ve işleniyor...")

        # 3D nokta bulutu oluştur
        point_cloud = generate_point_cloud(image)
        if len(point_cloud.points) == 0:
            raise HTTPException(status_code=500, detail="❌ 3D nokta bulutu boş, görselleştirme yapılamıyor!")

        logging.info("3D nokta bulutu oluşturuldu.")

        # Hacim hesaplama
        volume = calculate_3d_volume(point_cloud)

        # Doluluk oranı hesaplama
        fill_percentage = calculate_fill_percentage(image)
        filled_volume = (fill_percentage / 100) * containerVolume

        logging.info(f"Hesaplamalar tamamlandı. Doluluk oranı: %{fill_percentage}, Dolu Hacim: {filled_volume} m³")

        # 3D görsel oluştur
        container_image_3d = generate_3d_visualization(point_cloud)

        # Eğer Open3D başarısız olursa, Matplotlib kullan
        if container_image_3d is None or isinstance(container_image_3d, str):
            logging.warning("[WARNING] Open3D başarısız oldu, Matplotlib kullanılıyor...")
            container_image_3d = generate_matplotlib_3d(point_cloud)

        if container_image_3d is None:
            raise HTTPException(status_code=500, detail="❌ 3D görselleştirme başarısız oldu!")

        # Görseli Base64 formatına çevir
        img_str = convert_image_to_base64(container_image_3d)
        if img_str is None:
            raise HTTPException(status_code=500, detail="❌ Görseli Base64 formatına çevirme başarısız oldu!")

        logging.info("3D görselleştirme başarıyla tamamlandı!")

        return JSONResponse(content={
            "fill_percentage": round(fill_percentage, 2),
            "filled_volume": round(filled_volume, 2),
            "3d_volume": round(volume, 2),
            "3d_image": f"data:image/png;base64,{img_str}"
        })

    except HTTPException as http_err:
        logging.error(f"API Hatası: {http_err.detail}")
        return JSONResponse(content={"error": http_err.detail}, status_code=http_err.status_code)

    except Exception as e:
        logging.error(f"Beklenmeyen bir hata oluştu: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
