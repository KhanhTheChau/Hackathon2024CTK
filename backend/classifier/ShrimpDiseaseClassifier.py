import numpy as np
import cv2
from typing import Dict
from PIL import Image
from rembg import remove
from ultralytics import YOLO
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

def remove_background(image_path, output_path):
    try:
        # Đọc ảnh
        input_image = Image.open(image_path)

        # Xóa nền
        output_image = remove(input_image)

        # Lưu ảnh không nền dưới dạng PNG
        output_image.save(output_path, 'PNG')

        print(f"Đã xóa nền: {output_path}")

    except Exception as e:
        print(f"Lỗi khi xử lý {image_path}: {e}")
        return None
    return output_path

class ShrimpDiseaseClassifier:
    """
    Custom CNN model for classifying shrimp disease images.
    This is a placeholder that would be replaced with an actual trained model.
    """
    def __init__(self, model_path: str, yolo_model_path: str):
        self.model_path = model_path
        self.yolo_model_path = yolo_model_path
        self.model = load_model(model_path)
        self.yolo_model = YOLO(yolo_model_path)
        self.class_indices = {'bgd': 0, 'healthy': 1, 'wssv': 2}
        self.labels = {v: k for k, v in self.class_indices.items()}

    def predict(self, image_path: str, threshold: float = 0.5) -> Dict[str, float]:
        """
        Predict disease type from an image.

        Args:
            image_path (str): Path to the input image
            threshold (float): Ngưỡng xác suất để quyết định xem bệnh có được chẩn đoán hay không

        Returns:
            Dict of disease predictions and their probabilities
        """
        # Remove background
        no_bg_path = self.remove_background(image_path)
        if no_bg_path is None:
            return {}

        # Load and preprocess the image before passing it to the model
        img = cv2.imread(image_path)

        # Phát hiện đối tượng bằng YOLO
        results = self.yolo_model(img)

        prediction_dict = {}

        # Lặp qua các hộp giới hạn
        for result in results:
            boxes = result.boxes

            for box in boxes:
                # Lấy tọa độ hộp giới hạn
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

                # Cắt vùng ảnh theo hộp giới hạn
                roi = img[y1:y2, x1:x2]

                # Kiểm tra xem roi có rỗng không
                if roi.size == 0:
                    print("Vùng cắt rỗng, bỏ qua")
                    continue

                try:
                    # Tiền xử lý vùng ảnh cho CNN
                    roi = cv2.resize(roi, (64, 64))
                    roi = image.img_to_array(roi) 
                    roi = np.expand_dims(roi, axis=0)
                    roi /= 255.0

                    # Phân loại bằng CNN
                    prediction = self.model.predict(roi)
                    predicted_class_id = np.argmax(prediction)
                    predicted_class = self.labels[predicted_class_id]
                    probability = prediction[0][predicted_class_id]

                    # In xác suất của từng lớp
                    print(f"Lớp {predicted_class}: {probability:.2f}")

                    # Thêm vào dictionary nếu xác suất vượt ngưỡng
                    if probability >= threshold:
                        prediction_dict[predicted_class] = probability

                except Exception as e:
                    print(f"Lỗi khi phân loại: {e}")

        print(prediction_dict)
        return prediction_dict

    def remove_background(self, image_path: str):
        """
        Removes the background from the image.

        Args:
            image_path (str): Path to the input image

        Returns:
            Path to the image with background removed
        """
        # Tạo đường dẫn ảnh không nền
        filename, file_extension = os.path.splitext(image_path)
        no_bg_path = f"{filename}_no_bg.png"

        # Xóa nền
        return remove_background(image_path, no_bg_path)