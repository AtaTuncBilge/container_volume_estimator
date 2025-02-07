import cv2
import numpy as np
import open3d as o3d
import base64
import matplotlib.pyplot as plt
from io import BytesIO

def generate_point_cloud(image):
    """Örnek nokta bulutu üretme (şu an rastgele değerler kullanıyor)."""
    pcd = o3d.geometry.PointCloud()
    points = np.random.rand(1000, 3)  # Daha fazla nokta üret
    pcd.points = o3d.utility.Vector3dVector(points)

    print(f"[DEBUG] Nokta Bulutu Oluşturuldu. Toplam Nokta Sayısı: {len(points)}")
    
    return pcd

def calculate_3d_volume(point_cloud):
    """3D nokta bulutundan hacim hesapla."""
    try:
        bounding_box = point_cloud.get_axis_aligned_bounding_box()
        volume = np.prod(bounding_box.get_max_bound() - bounding_box.get_min_bound())
        print(f"[DEBUG] Hacim Hesaplandı: {volume} m³")
        return volume
    except Exception as e:
        print(f"[ERROR] Hacim hesaplanırken hata oluştu: {str(e)}")
        return 0

def calculate_fill_percentage(image):
    """Görsel üzerinden doluluk oranı hesapla."""
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        filled_pixels = np.sum(thresh == 255)
        total_pixels = image.shape[0] * image.shape[1]
        fill_percentage = (filled_pixels / total_pixels) * 100
        print(f"[DEBUG] Doluluk Oranı: %{fill_percentage:.2f}")
        return fill_percentage
    except Exception as e:
        print(f"[ERROR] Doluluk oranı hesaplanırken hata oluştu: {str(e)}")
        return 0

def generate_3d_visualization(point_cloud):
    """3D nokta bulutunun görselini oluştur ve base64 formatına dönüştür."""
    try:
        print("[INFO] 3D Görselleştirme başlatıldı...")

        vis = o3d.visualization.Visualizer()
        vis.create_window(visible=False)  # Headless mod
        vis.add_geometry(point_cloud)
        vis.poll_events()
        vis.update_renderer()

        # Open3D ekran görüntüsü al
        image = vis.capture_screen_float_buffer(True)
        vis.destroy_window()

        if image is None:
            print("[ERROR] 3D Görsel oluşturulamadı, Open3D ekran görüntüsü boş.")
            return generate_matplotlib_3d(point_cloud)

        # Open3D görüntüsünü numpy formatına çevir
        image = np.asarray(image) * 255
        image = image.astype(np.uint8)

        print(f"[DEBUG] Open3D Görüntü Boyutu: {image.shape}")

        # Görseli Base64 formatına çevir
        _, buffer = cv2.imencode('.png', image)
        img_str = base64.b64encode(buffer).decode("utf-8")

        print(f"[SUCCESS] 3D Görsel oluşturuldu! Base64 Uzunluk: {len(img_str)}")
        return f"data:image/png;base64,{img_str}"

    except Exception as e:
        print(f"[EXCEPTION] 3D Görsel oluşturulurken hata oluştu: {str(e)}")
        return generate_matplotlib_3d(point_cloud)

def generate_matplotlib_3d(point_cloud):
    """Eğer Open3D çalışmazsa, Matplotlib ile 3D görsel oluştur."""
    try:
        print("[INFO] Matplotlib ile 3D görsel oluşturuluyor...")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        points = np.asarray(point_cloud.points)
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='r', marker='o')

        plt.axis('off')
        
        # Görseli kaydet
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        # Base64 formatına çevir
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        print(f"[SUCCESS] Matplotlib görseli oluşturuldu! Base64 Uzunluk: {len(img_str)}")
        return f"data:image/png;base64,{img_str}"

    except Exception as e:
        print(f"[EXCEPTION] Matplotlib ile görsel oluşturulurken hata oluştu: {str(e)}")
        return None
