import React, { useState } from 'react';
import axios from 'axios';

function VolumeForm() {
  const [containerVolume, setContainerVolume] = useState('');
  const [containerImage, setContainerImage] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    if (!containerVolume || !containerImage) {
      setError('⚠️ Lütfen tüm alanları doldurun!');
      return;
    }

    const formData = new FormData();
    formData.append('containerVolume', containerVolume);
    formData.append('containerImage', containerImage);

    try {
      const response = await axios.post('http://127.0.0.1:5000/calculate', formData);
      setResult(response.data);
    } catch (err) {
      setError('❌ Hata oluştu: ' + (err.response?.data?.error || err.message));
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-md">
      <form onSubmit={handleSubmit} className="space-y-4">
        <label className="block text-yellow-400 font-semibold">📦 Konteyner Hacmi (m³):</label>
        <input
          type="number"
          value={containerVolume}
          onChange={(e) => setContainerVolume(e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white focus:ring-2 focus:ring-yellow-400"
          placeholder="Örn: 20"
          required
        />

        <label className="block text-yellow-400 font-semibold">📷 Konteyner Fotoğrafı Yükleyin:</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setContainerImage(e.target.files[0])}
          className="w-full p-2 rounded bg-gray-700 text-white"
          required
        />

        <button
          type="submit"
          className="w-full bg-yellow-400 text-black font-bold py-2 rounded-lg hover:bg-yellow-500 transition"
        >
          Hesapla
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 bg-red-500 text-white rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4 p-4 bg-green-500 text-white rounded-lg shadow">
          <p>📊 Doluluk Oranı: %{result.fill_percentage}</p>
          <p>🧮 Dolu Hacim: {result.filled_volume} m³</p>
        </div>
      )}
    </div>
  );
}

export default VolumeForm;
