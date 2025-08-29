#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import base64
import json
from PIL import Image, ImageDraw, ImageFont
import io

def create_test_image():
    """إنشاء صورة اختبار بسيطة"""
    # إنشاء صورة بيضاء
    img = Image.new('RGB', (400, 200), 'white')
    draw = ImageDraw.Draw(img)
    
    # رسم مربع أسود
    draw.rectangle([50, 50, 150, 150], fill='black')
    
    # رسم دائرة سوداء
    draw.ellipse([200, 50, 300, 150], fill='black')
    
    # رسم نص أسود
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 170), "Test", fill='black', font=font)
    
    # تحويل إلى base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def test_potrace_service():
    """اختبار خدمة Potrace"""
    print("🧪 اختبار خدمة Potrace...")
    
    # إنشاء صورة اختبار
    print("📝 إنشاء صورة اختبار...")
    test_image = create_test_image()
    
    # إعداد البيانات
    data = {
        'image': test_image,
        'options': {
            'smoothness': 'high',
            'threshold': 0.5
        }
    }
    
    try:
        # إرسال الطلب
        print("📤 إرسال الطلب للخدمة...")
        response = requests.post('http://127.0.0.1:5000/convert', 
                               json=data, 
                               timeout=30)
        
        print(f"📊 كود الاستجابة: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                svg_content = result.get('svg')
                print(f"✅ نجح التحويل! طول SVG: {len(svg_content)} حرف")
                
                # عرض بداية المحتوى
                print(f"📄 بداية SVG: {svg_content[:200]}...")
                
                # حفظ النتيجة
                with open('test_result.svg', 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                print("💾 تم حفظ النتيجة في test_result.svg")
                
                return True
            else:
                print(f"❌ فشل التحويل: {result.get('error')}")
                return False
        else:
            print(f"❌ خطأ HTTP: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📄 تفاصيل الخطأ: {error_data}")
            except:
                print(f"📄 الرد: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخدمة!")
        print("💡 تأكد من تشغيل: python potrace_converter.py")
        return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

if __name__ == "__main__":
    success = test_potrace_service()
    if success:
        print("\n🎉 الاختبار نجح! النظام يعمل بشكل صحيح")
    else:
        print("\n💥 الاختبار فشل! يرجى مراجعة الأخطاء أعلاه")