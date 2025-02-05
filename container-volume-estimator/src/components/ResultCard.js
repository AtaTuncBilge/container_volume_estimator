import React from 'react';

function ResultCard({ fillPercentage, filledVolume }) {
  if (fillPercentage === undefined || filledVolume === undefined) return null;

  return (
    <div className="bg-green-500 text-white p-6 mt-4 rounded-xl shadow-lg transform hover:scale-105 transition-transform">
      <h2 className="text-xl font-bold mb-2">📊 Hesaplama Sonuçları</h2>
      <div className="space-y-2">
        <p>✅ <strong>Doluluk Oranı:</strong> %{fillPercentage}</p>
        <p>🧮 <strong>Dolu Hacim:</strong> {filledVolume} m³</p>
      </div>
    </div>
  );
}

export default ResultCard;