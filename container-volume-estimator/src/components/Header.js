import React from 'react';

function Header() {
  return (
    <header className="bg-yellow-400 shadow-md p-4 rounded-lg flex items-center justify-center">
      <img src="/logo.png" alt="Mimware Logo" className="h-10 mr-3" />
      <h1 className="text-2xl font-bold text-gray-900">Konteyner Hacim Hesaplama</h1>
    </header>
  );
}

export default Header;
