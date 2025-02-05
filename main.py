def get_container_volume():
    try:
        volume = float(input("Konteynerin hacmini (m³ cinsinden) girin: "))
        return volume
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
        return get_container_volume()
    
from image_processing import load_image, process_image
from utils import calculate_fill_percentage

def main():
    container_volume = get_container_volume()
    image_path = input("Konteyner fotoğrafının yolunu girin: ")

    try:
        image = load_image(image_path)
        processed_image = process_image(image)
        fill_percentage = calculate_fill_percentage(processed_image)
        
        filled_volume = (fill_percentage / 100) * container_volume

        print(f"Konteynerin doluluk oranı: %{fill_percentage:.2f}")
        print(f"Konteynerin dolu hacmi: {filled_volume:.2f} m³")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    main()
