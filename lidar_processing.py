import open3d as o3d
import numpy as np

def load_lidar_data(file_path):
    """LiDAR nokta bulutu verisini yükle ve görselleştir."""
    pcd = o3d.io.read_point_cloud(file_path)
    o3d.visualization.draw_geometries([pcd])  # 3D Görselleştir

    return np.asarray(pcd.points)

def estimate_volume(point_cloud):
    """Nokta bulutu verisinden hacim hesapla."""
    min_bound = np.min(point_cloud, axis=0)
    max_bound = np.max(point_cloud, axis=0)

    volume = np.prod(max_bound - min_bound)  # Hacim = En * Boy * Yükseklik
    return volume

# 📌 Test etmek için örnek bir nokta bulutu dosyası kullan!
point_cloud_data = load_lidar_data("container_scan.pcd")
calculated_volume = estimate_volume(point_cloud_data)

print(f"📦 Konteynerin dolu hacmi: {calculated_volume:.2f} m³")
