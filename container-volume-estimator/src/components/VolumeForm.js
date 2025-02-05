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
    <div className="bg-gray-800 p-8 rounded-xl shadow-xl transition-transform transform hover:scale-105">
      <form onSubmit={handleSubmit} className="space-y-6">
        <label className="block text-yellow-400 font-bold text-lg">📦 Konteyner Hacmi (m³):</label>
        <input
          type="number"
          value={containerVolume}
          onChange={(e) => setContainerVolume(e.target.value)}
          className="w-full p-3 rounded-lg bg-gray-700 text-white focus:ring-4 focus:ring-yellow-400 border-2 border-transparent focus:border-yellow-400 transition"
          placeholder="Örn: 20"
          required
        />

        <label className="block text-yellow-400 font-bold text-lg">📷 Konteyner Fotoğrafı Yükleyin:</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setContainerImage(e.target.files[0])}
          className="w-full p-3 rounded-lg bg-gray-700 text-white border-2 border-transparent focus:border-yellow-400 transition"
          required
        />

        <button
          type="submit"
          className="w-full bg-yellow-400 text-black font-bold py-3 rounded-lg shadow-md hover:bg-yellow-500 hover:shadow-lg transition duration-300 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? '⏳ Hesaplanıyor...' : '🚀 Hesapla'}
        </button>
      </form>

      {loading && (
        <div className="mt-6 text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-yellow-400 border-solid mx-auto"></div>
          <p className="text-yellow-400 mt-3 font-semibold">İşleniyor...</p>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-500 text-white rounded-lg shadow-md">
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