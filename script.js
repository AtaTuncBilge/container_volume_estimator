function calculateVolume() {
    const containerVolume = document.getElementById('containerVolume').value;
    const containerImage = document.getElementById('containerImage').files[0];
    const resultDiv = document.getElementById('result');

    if (!containerVolume || !containerImage) {
        resultDiv.innerHTML = "⚠️ Lütfen tüm alanları doldurun!";
        resultDiv.style.backgroundColor = "#FFC0C0";
        resultDiv.style.color = "#B00000";
        return;
    }

    const formData = new FormData();
    formData.append('containerVolume', containerVolume);
    formData.append('containerImage', containerImage);


    fetch('http://127.0.0.1:5000/calculate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerHTML = `❌ Hata: ${data.error}`;
            resultDiv.style.backgroundColor = "#FFC0C0";
            resultDiv.style.color = "#B00000";
        } else {
            resultDiv.innerHTML = `
                📦 Doluluk Oranı: %${data.fill_percentage} <br>
                🧮 Dolu Hacim: ${data.filled_volume} m³
            `;
            resultDiv.style.backgroundColor = "#CFFFCF";
            resultDiv.style.color = "#006600";
        }
    })
    .catch(error => {
        resultDiv.innerHTML = `❌ Hata: ${error}`;
        resultDiv.style.backgroundColor = "#FFC0C0";
        resultDiv.style.color = "#B00000";
    });
}
