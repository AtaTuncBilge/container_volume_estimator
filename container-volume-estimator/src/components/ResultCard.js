import React from 'react';

function ResultCard({ fillPercentage, filledVolume, container3DImage }) {
  if (fillPercentage === undefined || filledVolume === undefined) return null;

  return (
    <div className="bg-green-500 text-white p-6 mt-4 rounded-xl shadow-lg transform hover:scale-105 transition-transform">
      <h2 className="text-xl font-bold mb-2">📊 Hesaplama Sonuçları</h2>
      <div className="space-y-2">
        <p>✅ <strong>Doluluk Oranı:</strong> %{fillPercentage}</p>
        <p>🧮 <strong>Dolu Hacim:</strong> {filledVolume} m³</p>
      </div>

      {/* 3D Görseli Göster */}
      <div className="mt-4">
        <p className="text-lg font-medium">3D Görsel:</p>
        <div style={{ width: '300px', height: '300px', backgroundColor: 'gray' }}>
          {/* Görsel Base64 olarak dönecek */}
          {container3DImage ? (
            <img src={container3DImage} alt="3D Görsel" className="w-full h-full object-cover rounded-lg" />
          ) : (
            <p>3D Görsel yüklenemedi.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ResultCard;
