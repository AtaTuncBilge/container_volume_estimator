import React, { useState, useEffect } from "react";

const Container3DImage = ({ apiUrl }) => {
  const [imageSrc, setImageSrc] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        if (data["3d_image"]) {
          setImageSrc(data["3d_image"]);
        } else {
          setError("❌ 3D Görsel yüklenemedi.");
        }
        setLoading(false);
      })
      .catch((err) => {
        setError("❌ API Hatası: " + err.message);
        setLoading(false);
      });
  }, [apiUrl]);

  return (
    <div>
      <h3>3D Görsel:</h3>
      {loading ? (
        <p>⏳ Yükleniyor...</p>
      ) : error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : (
        <img src={imageSrc} alt="3D Container" style={{ maxWidth: "100%" }} />
      )}
    </div>
  );
};

export default Container3DImage;
