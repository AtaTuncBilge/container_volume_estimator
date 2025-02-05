import React, { useState } from 'react';
import axios from 'axios';
import ResultCard from './ResultCard';

function VolumeForm() {
  const [containerVolume, setContainerVolume] = useState('');
  const [containerImage, setContainerImage] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);

    if (!containerVolume || !containerImage) {
      setError('⚠️ Lütfen tüm alanları doldurun!');
      setLoading(false);
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
    } finally {
      setLoading(false);
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
          disabled={loading}
        >
          {loading ? 'Hesaplanıyor...' : 'Hesapla'}
        </button>
      </form>

      {loading && (
        <div className="mt-4 text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-t-4 border-yellow-400 border-solid mx-auto"></div>
          <p className="text-yellow-400 mt-2">İşleniyor...</p>
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-500 text-white rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <ResultCard fillPercentage={result.fill_percentage} filledVolume={result.filled_volume} />
      )}
    </div>
  );
}

export default VolumeForm;