import base64
from io import BytesIO
import numpy as np
import open3d as o3d
import cv2
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS ayarları
origins = [
    "http://localhost",
    "http://localhost:3000",  # React app'inizin çalıştığı port
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
    return {"message": "Konteyner Hacim Hesaplama API'si Çalışıyor!"}

@app.post("/calculate")
async def calculate_volume(containerImage: UploadFile = File(...), containerVolume: float = Form(...)):
    try:
        # Görseli oku
        image_data = await containerImage.read()
        npimg = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # 3D hacim hesaplama
        point_cloud = generate_point_cloud(image)
        volume = calculate_3d_volume(point_cloud)

        # Doluluk oranı hesaplama
        fill_percentage = calculate_fill_percentage(image)

        # Hacim ve doluluk oranını döndür
        filled_volume = (fill_percentage / 100) * containerVolume

        # 3D görseli oluştur ve base64 formatında döndür
        container_image_3d = generate_3d_visualization(point_cloud)

        return JSONResponse(content={
            "fill_percentage": round(fill_percentage, 2),
            "filled_volume": round(filled_volume, 2),
            "3d_volume": round(volume, 2),
            "3d_image": container_image_3d
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def generate_point_cloud(image):
    pcd = o3d.geometry.PointCloud()
    points = np.random.rand(100, 3)  # 100 rastgele 3D nokta
    pcd.points = o3d.utility.Vector3dVector(points)
    return pcd

def calculate_3d_volume(point_cloud):
    bounding_box = point_cloud.get_axis_aligned_bounding_box()
    volume = np.prod(bounding_box.get_max_bound() - bounding_box.get_min_bound())
    return volume

def calculate_fill_percentage(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    filled_pixels = np.sum(thresh == 255)
    total_pixels = image.shape[0] * image.shape[1]
    return (filled_pixels / total_pixels) * 100

def generate_3d_visualization(point_cloud):
    """3D görseli oluştur ve base64 formatına dönüştür."""
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(point_cloud)

    # Görseli kaydetmek
    image = vis.capture_screen_float_buffer(True)
    
    # Görseli numpy dizisine dönüştür
    image = np.asarray(image)

    # Görseli base64 formatına dönüştür
    _, buffer = cv2.imencode('.png', (image * 255).astype(np.uint8))
    img_str = base64.b64encode(buffer).decode("utf-8")

    # Debug: Base64 görseli kontrol edelim
    print(f"Base64 Görsel: {img_str[:100]}...")  # İlk 100 karakteri yazdıralım

    vis.destroy_window()
    return f"data:image/png;base64,{img_str}"

