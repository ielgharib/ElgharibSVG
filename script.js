// معاينة الخط
document.getElementById("renderBtn").addEventListener("click", () => {
  const fileInput = document.getElementById("fontFile");
  const textInput = document.getElementById("textInput").value;
  const preview = document.getElementById("preview");
  const glyphsContainer = document.getElementById("glyphs");

  if (fileInput.files.length === 0) {
    alert("من فضلك اختر ملف خط أولاً");
    return;
  }

  const reader = new FileReader();

  reader.onload = function (e) {
    const fontData = e.target.result;
    const fontName = "UploadedFont";

    // معاينة الخط بالنص
    const font = new FontFace(fontName, fontData);
    font.load().then((loadedFont) => {
      document.fonts.add(loadedFont);
      preview.style.fontFamily = fontName;
      preview.textContent = textInput;
    });

    // قراءة الجليفات من opentype.js
    const fontParsed = opentype.parse(fontData);
    glyphsContainer.innerHTML = ''; // تصفير القائمة القديمة

    fontParsed.glyphs.forEach((glyph) => {
      if (glyph.unicode) {
        const char = String.fromCharCode(glyph.unicode);
        const div = document.createElement("div");
        div.textContent = char;
        glyphsContainer.appendChild(div);
      }
    });
  };

  reader.readAsArrayBuffer(fileInput.files[0]);
});

// تحميل المعاينة كصورة
document.getElementById("downloadBtn").addEventListener("click", () => {
  const preview = document.getElementById("preview");

  html2canvas(preview).then((canvas) => {
    const link = document.createElement("a");
    link.download = "preview.png";
    link.href = canvas.toDataURL();
    link.click();
  });
});
