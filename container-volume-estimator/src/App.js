import React, { useState } from 'react';
import Header from './components/Header';
import VolumeForm from './components/VolumeForm';
import ResultCard from './components/ResultCard';
import './index.css';

function App() {
  const [containerVolume, setContainerVolume] = useState("");
  const [containerImage, setContainerImage] = useState(null);
  const [fillPercentage, setFillPercentage] = useState(null);
  const [filledVolume, setFilledVolume] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setContainerImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setFillPercentage(null);
    setFilledVolume(null);

    if (!containerVolume || !containerImage) {
      setError("Lütfen tüm alanları doldurun!");
      return;
    }

    const formData = new FormData();
    formData.append("containerImage", containerImage);
    formData.append("containerVolume", containerVolume);

    try {
      const response = await fetch("http://127.0.0.1:8000/calculate", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setFillPercentage(data.fill_percentage);
      setFilledVolume(data.filled_volume);
    } catch (err) {
      setError("Bir hata oluştu. Lütfen tekrar deneyin.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-700 text-white flex flex-col items-center p-6 relative">
      <Header />
      <img
        src="/assets/images/image (1).png"
        alt="Decorative"
        className="absolute top-0 left-0 w-40 opacity-20"
      />
      <img
        src="/assets/images/image (2).png"
        alt="Decorative"
        className="absolute bottom-0 right-0 w-40 opacity-20"
      />
      <main className="w-full max-w-4xl mt-8 bg-gray-800 p-10 rounded-xl shadow-3xl border border-gray-600">
        <VolumeForm
          containerVolume={containerVolume}
          setContainerVolume={setContainerVolume}
          handleFileChange={handleFileChange}
          handleSubmit={handleSubmit}
        />
        {fillPercentage !== null && (
          <ResultCard
            fillPercentage={fillPercentage}
            filledVolume={filledVolume}
          />
        )}
        {error && <p className="text-red-500">{error}</p>}
      </main>
    </div>
  );
}

export default App;
