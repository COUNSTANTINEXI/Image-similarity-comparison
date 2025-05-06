from flask import Flask, request, jsonify, send_from_directory, render_template
from image_similarity import similarity
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # 启用跨域支持

# 提供静态文件（HTML 页面）
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'ISC.html')

@app.route('/compare', methods=['POST'])
def compare_images():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"error": "请上传两张图片"}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    # 保存临时文件
    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)  # 确保临时目录存在
    img1_path = os.path.join(temp_dir, image1.filename)
    img2_path = os.path.join(temp_dir, image2.filename)
    image1.save(img1_path)
    image2.save(img2_path)

    try:
        # 调用 similarity 函数计算相似度
        result = similarity(img1_path, img2_path)
        return jsonify({"similarity": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # 删除临时文件
        os.remove(img1_path)
        os.remove(img2_path)

if __name__ == "__main__":
    app.run(debug=True)