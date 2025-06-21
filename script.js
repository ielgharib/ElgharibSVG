document.getElementById("renderBtn").addEventListener("click", () => {
  const fileInput = document.getElementById("fontFile");
  const textInput = document.getElementById("textInput").value;
  const preview = document.getElementById("preview");

  if (fileInput.files.length === 0) {
    alert("من فضلك اختر ملف خط أولاً");
    return;
  }

  const reader = new FileReader();

  reader.onload = function (e) {
    const fontData = e.target.result;
    const fontName = "UploadedFont";

    const font = new FontFace(fontName, fontData);
    font.load().then((loadedFont) => {
      document.fonts.add(loadedFont);
      preview.style.fontFamily = fontName;
      preview.textContent = textInput;
    });
  };

  reader.readAsArrayBuffer(fileInput.files[0]);
});
