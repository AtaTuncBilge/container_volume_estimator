import React, { useState } from 'react';
import axios from 'axios';
import ResultCard from './ResultCard';

function VolumeForm() {
  const [containerVolume, setContainerVolume] = useState('');
  const [containerImage, setContainerImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [imageName, setImageName] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setContainerImage(file);
    setImageName(file ? file.name : '');
    setImagePreview(file ? URL.createObjectURL(file) : null);
  };

  const calculateVolume = async (e) => {
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
      const response = await axios.post('http://127.0.0.1:8000/calculate', formData);
      setResult(response.data);
    } catch (err) {
      setError(`❌ API Hatası: ${err.response ? err.response.data.error : err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 bg-gray-800 text-white rounded-lg shadow-2xl border border-gray-600">
      <h1 className="text-2xl font-bold mb-6">Konteyner Hacim Hesaplama</h1>
      <form onSubmit={calculateVolume} className="space-y-4">
        <label className="block text-lg font-medium">Konteyner Hacmi (m³):</label>
        <input
          type="number"
          value={containerVolume}
          onChange={(e) => setContainerVolume(e.target.value)}
          className="w-full p-3 bg-gray-700 rounded focus:outline-none focus:ring-2 focus:ring-yellow-400"
          required
        />

        <label className="block text-lg font-medium">Konteyner Fotoğrafı:</label>
        <div className="flex items-center space-x-4">
          <input type="file" onChange={handleFileChange} className="hidden" id="fileInput" required />
          <label
            htmlFor="fileInput"
            className="cursor-pointer bg-yellow-400 text-black p-2 rounded hover:bg-yellow-500 transition text-center"
          >
            Dosya Seçin
          </label>
          {imageName && <span className="text-sm text-gray-300">{imageName}</span>}
        </div>

        {imagePreview && (
          <div className="mt-4">
            <p className="text-sm text-gray-300 mb-2">📷 Yüklenen Resim:</p>
            <img src={imagePreview} alt="Konteyner Önizleme" className="w-32 h-32 object-cover rounded-lg border" />
          </div>
        )}

        <button
          type="submit"
          className="bg-yellow-400 text-black p-2 mt-4 rounded hover:bg-yellow-500 transition"
        >
          {loading ? '⏳ Hesaplanıyor...' : 'Hesapla'}
        </button>
      </form>

      {error && <div className="mt-4 text-red-500 font-semibold">{error}</div>}

      {result && (
        <ResultCard
          fillPercentage={result.fill_percentage}
          filledVolume={result.filled_volume}
          volume3D={result["3d_volume"]}
          image3D={result["3d_image"]}
        />
      )}
    </div>
  );
}

export default VolumeForm;
