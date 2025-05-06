import os
import numpy as np
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template

from werkzeug.utils import secure_filename
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms, models
from torchvision.models import ResNet50_Weights

app = Flask(__name__)
CORS(app)

# 初始化ResNet50模型
from torchvision.models import ResNet50_Weights
model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
model = nn.Sequential(*list(model.children())[:-1])  # 移除最后一层
model.eval()

# 图像预处理
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_features(image_path):
    img = Image.open(image_path).convert('RGB')
    img_t = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        features = model(img_t)
    return features.squeeze().numpy()

@app.route('/api/compare', methods=['POST'])
def compare_images():
    if 'main_image' not in request.files or 'comparison_images' not in request.files:
        return jsonify({'error': 'Missing files'}), 400

    main_file = request.files['main_image']
    comp_files = request.files.getlist('comparison_images')

    # 保存主图
    main_path = os.path.join(UPLOAD_FOLDER, secure_filename(main_file.filename))
    main_file.save(main_path)

    # 处理比对图片
    similarities = []
    for file in comp_files[:5]:  # 最多处理5张
        if file.filename == '': continue
        comp_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(comp_path)
        
        # 提取特征
        main_feat = extract_features(main_path)
        comp_feat = extract_features(comp_path)
        
        # 计算余弦相似度
        cos_sim = np.dot(main_feat, comp_feat) / (np.linalg.norm(main_feat) * np.linalg.norm(comp_feat))
        similarities.append((file.filename, float(cos_sim)))

    # 清理临时文件
    for f in [main_path] + [os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)) for f in comp_files]:
        if os.path.exists(f):
            os.remove(f)

    if not similarities:
        return jsonify({'error': 'No valid comparison images'}), 400

    # 找到最相似的图片
    most_similar = max(similarities, key=lambda x: x[1])
    return jsonify({
        'most_similar': most_similar[0],
        'similarity': most_similar[1],
        'all_results': similarities
    })

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)

