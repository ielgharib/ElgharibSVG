#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import base64
import io
import tempfile
import subprocess
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# مسار Potrace
POTRACE_PATH = os.path.join(os.path.dirname(__file__), 'potrace.exe')

def convert_image_to_svg(image_data, options=None):
    """
    تحويل صورة إلى SVG باستخدام Potrace
    """
    if options is None:
        options = {}
    
    try:
        # فك تشفير الصورة من base64
        try:
            if ',' in image_data:
                image_bytes = base64.b64decode(image_data.split(',')[1])
            else:
                image_bytes = base64.b64decode(image_data)
        except Exception as e:
            raise Exception(f"فشل في فك تشفير الصورة: {e}")
            
        image = Image.open(io.BytesIO(image_bytes))
        
        # التحقق من حجم الصورة
        if image.width < 10 or image.height < 10:
            raise Exception("الصورة صغيرة جداً")
            
        if image.width > 3000 or image.height > 3000:
            # تصغير الصورة إذا كانت كبيرة جداً
            image.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
        
        # تحويل إلى أبيض وأسود (مثل الكود الأصلي)
        threshold = int(options.get('threshold', 0.5) * 255)
        img_bw = image.convert("L").point(lambda x: 0 if x < threshold else 255, "1")
        
        # إنشاء ملفات مؤقتة
        with tempfile.NamedTemporaryFile(suffix='.pbm', delete=False) as temp_pbm:
            with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp_svg:
                
                # حفظ الصورة كـ PBM (مثل الكود الأصلي)
                img_bw.save(temp_pbm.name)
                
                # إعداد خيارات Potrace (مثل الكود الأصلي)
                potrace_args = [POTRACE_PATH, temp_pbm.name, "-s", "-o", temp_svg.name]
                
                # إضافة خيارات إضافية حسب الحاجة
                smoothness = options.get('smoothness', 'medium')
                if smoothness == 'ultra':
                    potrace_args.extend(['-a', '0.0'])
                elif smoothness == 'high':
                    potrace_args.extend(['-a', '0.5'])
                elif smoothness == 'medium':
                    potrace_args.extend(['-a', '1.0'])
                else:  # low
                    potrace_args.extend(['-a', '1.5'])
                
                # تشغيل Potrace
                print(f"تشغيل Potrace: {' '.join(potrace_args)}")
                result = subprocess.run(potrace_args, capture_output=True, text=True, check=True)
                
                # التحقق من وجود ملف SVG
                if not os.path.exists(temp_svg.name):
                    raise Exception("لم يتم إنشاء ملف SVG")
                
                # قراءة ملف SVG
                with open(temp_svg.name, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                
                # التحقق من محتوى SVG
                if not svg_content or len(svg_content) < 100:
                    raise Exception("محتوى SVG فارغ أو قصير جداً")
                
                if '<svg' not in svg_content:
                    raise Exception("محتوى SVG غير صالح")
                
                # تنظيف الملفات المؤقتة
                try:
                    os.unlink(temp_pbm.name)
                    os.unlink(temp_svg.name)
                except:
                    pass  # تجاهل أخطاء التنظيف
                
                return svg_content
                
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr or e.stdout or "خطأ في تشغيل Potrace"
        print(f"خطأ Potrace: {error_msg}")
        return None
    except Exception as e:
        print(f"خطأ في التحويل: {e}")
        return None

@app.route('/convert', methods=['POST'])
def convert_endpoint():
    """
    نقطة النهاية لتحويل الصور
    """
    try:
        data = request.json
        image_data = data.get('image')
        options = data.get('options', {})
        
        if not image_data:
            return jsonify({
                'success': False,
                'error': 'No image data provided'
            }), 400
        
        svg_content = convert_image_to_svg(image_data, options)
        
        if svg_content and len(svg_content) > 100:
            return jsonify({
                'success': True,
                'svg': svg_content
            })
        else:
            return jsonify({
                'success': False,
                'error': 'SVG content is invalid or too short'
            }), 500
            
    except Exception as e:
        print(f"خطأ في endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    فحص حالة الخدمة
    """
    potrace_available = os.path.exists(POTRACE_PATH)
    return jsonify({
        'status': 'healthy',
        'potrace_available': potrace_available,
        'potrace_path': POTRACE_PATH
    })

if __name__ == '__main__':
    print("🚀 بدء خدمة تحويل Potrace...")
    print(f"📁 مسار Potrace: {POTRACE_PATH}")
    print(f"✅ Potrace متوفر: {os.path.exists(POTRACE_PATH)}")
    
    app.run(host='127.0.0.1', port=5000, debug=False)