import React, { useState, useEffect } from "react";

function ResultCard({ fillPercentage, filledVolume, container3DImage }) {
  const [isLoading, setIsLoading] = useState(true);
  const [imageError, setImageError] = useState(false);
  const [validImage, setValidImage] = useState(false);

  useEffect(() => {
    if (container3DImage) {
      if (
        container3DImage.startsWith("data:image/jpeg;base64,") ||
        container3DImage.startsWith("data:image/png;base64,")
      ) {
        setValidImage(true);
        setIsLoading(false);
      } else {
        console.warn("⚠️ Geçersiz 3D Görsel URL’si:", container3DImage);
        setImageError(true);
        setIsLoading(false);
      }
    }
  }, [container3DImage]);

  if (fillPercentage === undefined || filledVolume === undefined) return null;

  return (
    <div className="bg-green-500 text-white p-6 mt-4 rounded-xl shadow-lg">
      <h2 className="text-xl font-bold mb-2">📊 Hesaplama Sonuçları</h2>
      <div className="space-y-2">
        <p>✅ <strong>Doluluk Oranı:</strong> %{fillPercentage}</p>
        <p>🧮 <strong>Dolu Hacim:</strong> {filledVolume} m³</p>
      </div>

      <div className="mt-4">
        <p className="text-lg font-medium">3D Görsel:</p>
        <div className="w-[300px] h-[300px] flex items-center justify-center bg-gray-700 rounded-lg overflow-hidden">
          {isLoading ? (
            <p className="text-gray-300 animate-pulse">⏳ Görsel Yükleniyor...</p>
          ) : imageError || !validImage ? (
            <p className="text-red-400">❌ 3D Görsel yüklenemedi.</p>
          ) : (
            <img
              src={container3DImage}
              alt="3D Görsel"
              className="w-full h-full object-contain"
              onError={() => {
                console.error("🚨 3D Görsel yüklenirken hata oluştu!");
                setImageError(true);
              }}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default ResultCard;
