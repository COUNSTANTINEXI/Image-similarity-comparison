import cv2
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input                            # type: ignore
from tensorflow.keras.preprocessing import image                                                        # type: ignore

# 加载预训练模型（去顶层+全局池化）
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

def preprocess_img(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    return preprocess_input(x)

def similarity(img1_path, img2_path):
    # 特征提取
    feat1 = model.predict(preprocess_img(img1_path)).flatten()
    feat2 = model.predict(preprocess_img(img2_path)).flatten()
    
    # 余弦相似度计算
    cosine_sim = np.dot(feat1, feat2) / (np.linalg.norm(feat1)*np.linalg.norm(feat2))
    return f"{cosine_sim*100:.2f}%"

# 示例调用
if __name__ == "__main__":
    img1_path = "images/1.png"
    img2_path = "images/2.png"
    print(img1_path,"和",img2_path,"图片相似度：")
    print(similarity(img1_path, img2_path)) 