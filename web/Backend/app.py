from flask import Flask
import cv2
import base64
from ultralytics import YOLO
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask import request

app = Flask(__name__)

detect_model = YOLO('best.pt')

classnames = ['fruit-bores', 'grasshopper', 'leafroller', 'maybug', 'moth', 'red-spider', 'mealybug-disease', 'snail', 'stag-beetle', 'stinkbug'] 

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def crop_image(image, coordinates):
    # coordinates of bounding box yolo x1, y1, x2, y2
    x1, y1, x2, y2 = map(int, coordinates)

    cropped_image = image[y1:y2, x1:x2]
    return cropped_image

@app.route('/api/predict', methods=['POST'])
@cross_origin(origins='*')
def predict():
    global detect_model
    global classnames

    uploaded_file = request.files['file']
    uploaded_file = cv2.imread(uploaded_file)
    result = detect_model.predict(uploaded_file, save=False)
    
    boxes = result[0].boxes.xyxy.tolist()
    detected_cls_idx = result[0].boxes.cls.tolist()
    detected_confidences = result[0].boxes.conf.tolist()

    detected_images = []

    for index, (box, cls) in enumerate(zip(boxes, detected_cls_idx)):
        cropped_image = crop_image(uploaded_file, box)

        _, encoded_image = cv2.imencode('.jpg', cropped_image)
        encoded_image = base64.b64encode(encoded_image).decode('utf-8')
        detected_images.append(encoded_image)

    rounded_numbers = []
    for number in detected_confidences:
        rounded_numbers.append(round(number, 3))
    
    # detected_results = []
    # for index in detected_cls_idx:
    #     detected_cls = classnames[int(index)]
    #     detected_results.append(detected_cls)
    return jsonify({
        'detected_images': detected_images,
        'detected_classes': detected_cls_idx,
        'confidences': rounded_numbers
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2409')