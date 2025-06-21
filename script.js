let font = null;

document.getElementById('fontFile').addEventListener('change', function (event) {
  const file = event.target.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      const arrayBuffer = e.target.result;

      font = opentype.parse(arrayBuffer);
      alert('✅ تم تحميل الخط بنجاح!');
    };

    reader.readAsArrayBuffer(file);
  }
});

document.getElementById('previewBtn').addEventListener('click', function () {
  const text = document.getElementById('inputText').value;
  const canvas = document.getElementById('previewCanvas');
  const ctx = canvas.getContext('2d');

  if (!font) {
    alert('⚠️ من فضلك، ارفع ملف الخط أولاً!');
    return;
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height); // مسح المعاينة السابقة

  const fontSize = 48;
  const path = font.getPath(text, 50, 100, fontSize);

  path.draw(ctx);
});

document.getElementById('downloadBtn').addEventListener('click', function () {
  const canvas = document.getElementById('previewCanvas');
  const image = canvas.toDataURL('image/png');

  const link = document.createElement('a');
  link.href = image;
  link.download = 'preview.png';
  link.click();
});