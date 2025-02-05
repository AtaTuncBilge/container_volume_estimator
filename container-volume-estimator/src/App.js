import React from 'react';
import Header from './components/Header';
import VolumeForm from './components/VolumeForm';
import ResultCard from './components/ResultCard';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-4">
      <Header />
      <main className="w-full max-w-2xl mt-6">
        <VolumeForm />
        <ResultCard />
      </main>
    </div>
  );
}

export default App;
