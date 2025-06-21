const renderBtn = document.getElementById("renderBtn");
const fileInput = document.getElementById("fontFile");
const textInput = document.getElementById("textInput");
const preview = document.getElementById("preview");
const glyphsContainer = document.getElementById("glyphs");
const featuresList = document.getElementById("featuresList");
const downloadBtn = document.getElementById("downloadBtn");

renderBtn.addEventListener("click", () => {
  if (fileInput.files.length === 0) {
    alert("من فضلك اختر ملف خط أولاً");
    return;
  }

  const reader = new FileReader();

  reader.onload = function (e) {
    const fontData = e.target.result;
    const fontName = "UploadedFont";

    // معاينة النص باستخدام FontFace
    const font = new FontFace(fontName, fontData);
    font.load().then((loadedFont) => {
      document.fonts.add(loadedFont);
      preview.style.fontFamily = fontName;
      preview.textContent = textInput.value;
    });

    // تحليل الخط باستخدام opentype.js
    const fontParsed = opentype.parse(fontData);

    // 🧩 عرض الجليفات
    glyphsContainer.innerHTML = "";
    fontParsed.glyphs.forEach((glyph) => {
      const path = glyph.getPath(0, 0, 72);
      if (path.commands.length === 0) return;

      const canvas = document.createElement("canvas");
      canvas.width = 80;
      canvas.height = 80;
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#fff";
      ctx.translate(40, 60);
      path.draw(ctx);
      glyphsContainer.appendChild(canvas);
    });

    // 🎛️ عرض خصائص OpenType
    const tables = fontParsed.tables;
    if (tables.gsub && tables.gsub.features.length > 0) {
      featuresList.innerHTML = '';
      tables.gsub.features.forEach((feature) => {
        const tag = document.createElement('div');
        tag.className = 'feature-tag';
        tag.textContent = feature.tag;
        featuresList.appendChild(tag);
      });
    } else {
      featuresList.innerHTML = 'لم يتم العثور على خصائص OpenType في هذا الخط.';
    }
  };

  reader.readAsArrayBuffer(fileInput.files[0]);
});

// 📷 تحميل المعاينة كصورة
downloadBtn.addEventListener("click", () => {
  html2canvas(preview).then((canvas) => {
    const link = document.createElement("a");
    link.download = "preview.png";
    link.href = canvas.toDataURL();
    link.click();
  });
});
