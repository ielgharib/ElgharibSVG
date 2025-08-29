
import os
import subprocess
from PIL import Image

# إعدادات المجلدات
current_dir = os.getcwd()
output_dir = os.path.join(current_dir, "svg_output")
os.makedirs(output_dir, exist_ok=True)

# الصيغ المدعومة
supported_formats = [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"]

# التأكد من وجود Potrace
def check_potrace():
    try:
        result = subprocess.run(["potrace", "-v"], capture_output=True, text=True)
        return "potrace" in result.stdout.lower()
    except Exception:
        return False

if not check_potrace():
    print("❌ لم يتم العثور على 'potrace.exe' أو لم يتم إضافته للمسار.")
    print("📌 تأكد أن 'potrace.exe' في نفس المجلد أو أضفه إلى PATH.")
    exit()

# بدء التحويل
converted = 0
skipped = 0

for filename in os.listdir(current_dir):
    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in supported_formats:
        continue

    try:
        image_path = os.path.join(current_dir, filename)
        pbm_path = os.path.join(current_dir, f"{name}.pbm")
        svg_path = os.path.join(output_dir, f"{name}.svg")

        # تحويل للصورة بالأبيض والأسود
        img = Image.open(image_path).convert("L").point(lambda x: 0 if x < 128 else 255, "1")
        img.save(pbm_path)  # حفظ بدون تحديد الصيغة

        # تحويل باستخدام Potrace
        subprocess.run(["potrace", pbm_path, "-s", "-o", svg_path], check=True)

        os.remove(pbm_path)
        converted += 1
        print(f"✅ تم تحويل: {filename} → {name}.svg")

    except Exception as e:
        skipped += 1
        print(f"❌ فشل تحويل {filename} - الخطأ: {e}")

# النتائج النهائية
print(f"\n📦 تم تحويل {converted} صورة.")
if skipped > 0:
    print(f"⚠️ تم تخطي {skipped} صورة بسبب أخطاء.")
