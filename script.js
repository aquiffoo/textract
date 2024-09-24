document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('upload-form');
  const fileInput = document.getElementById('image-upload');
  const extractedText = document.getElementById('extracted-text');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (fileInput.files.length === 0) {
      alert('Please select an image file.');
      return;
    }

    const file = fileInput.files[0];
    extractedText.textContent = 'Processing...';

    try {
      const result = await Tesseract.recognize(file);
      extractedText.textContent = result.data.text;
    } catch (error) {
      extractedText.textContent = `Error: ${error.message}`;
    }
  });

  function cleanupOldFiles() {
    const now = Date.now();
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith('textract_file_')) {
        const timestamp = parseInt(key.split('_')[2]);
        if (now - timestamp > 600000) {
          localStorage.removeItem(key);
        }
      }
    }
  }

  setInterval(cleanupOldFiles, 3600000);
});