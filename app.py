import os
import numpy as np
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import io
from ultralytics import YOLO

HOME = os.getcwd()
model = YOLO(f'{HOME}/best.pt')

PALETTE = [
    (220, 20, 60), (119, 11, 32), (0, 0, 142), (0, 0, 230), (106, 0, 228),
    (0, 60, 100), (0, 80, 100), (0, 0, 70), (0, 0, 192), (250, 170, 30),
    (100, 170, 30), (220, 220, 0), (175, 116, 175), (250, 0, 30),
    (30, 144, 255), (0, 191, 255), (135, 206, 250), (70, 130, 180), (123, 104, 238),
    (72, 61, 139), (138, 43, 226), (148, 0, 211), (186, 85, 211), (255, 20, 147),
    (255, 105, 180), (255, 160, 122), (255, 69, 0), (255, 99, 71), (218, 112, 214),
    (238, 130, 238), (255, 222, 173)
]

CLASS_NAMES = [
    "Caries", "Crown", "Filling", "Implant", "Malaligned", "Mandibular Canal", "Missing teeth",
    "Periapical lesion", "Retained root", "Root Canal Treatment", "Root Piece", "Impacted tooth",
    "Maxillary sinus", "Bone Loss", "Fractured teeth", "Permanent Teeth", "Supra Eruption", "TAD",
    "Abutment", "Attrition", "Bone defect", "Gingival former", "Metal band", "Orthodontic brackets",
    "Permanent retainer", "Post-core", "Plating", "Wire", "Cyst", "Root resorption", "Primary teeth"
]

app = Flask(__name__)
CORS(app, resources={r"/coordinates": {"origins": "*"}})

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    return response

@app.route('/')
def hello_world():
    return "<p>Hello world</p>"

@app.route('/coordinates', methods=['POST'])
def get_coordinates():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    file = request.files['image']
    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        annotated_img = img.copy()
        draw = ImageDraw.Draw(annotated_img)
    except Exception as e:
        return jsonify({"error": f"Failed to process the image: {str(e)}"}), 400

    results = model(img)
    annotations = []

    for detection, class_id in zip(results[0].boxes, results[0].boxes.cls):
        x1, y1, x2, y2 = detection.xyxy[0].tolist()
        class_name = results[0].names[int(class_id.item())]
        color = PALETTE[int(class_id.item()) % len(PALETTE)]
        draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=3)
        annotation = {
            "label": class_name,
            "bounding_box": {
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2
            }
        }
        annotations.append(annotation)

    if hasattr(results[0], 'masks'):
        for i, seg in enumerate(results[0].masks.xy):
            polygon_vertices = [(float(x), float(y)) for x, y in seg]
            color = PALETTE[int(results[0].boxes.cls[i].item()) % len(PALETTE)]
            draw.polygon(polygon_vertices, outline=color, fill=None)
            annotation = {
                "label": results[0].names[int(results[0].boxes.cls[i].item())],
                "segmentation": [{"x": float(x), "y": float(y)} for x, y in seg]
            }
            annotations.append(annotation)

    concatenated_img = Image.new('RGB', (img.width * 2 + 200, img.height))
    concatenated_img.paste(img, (0, 0))
    concatenated_img.paste(annotated_img, (img.width, 0))

    palette_img = Image.new('RGB', (200, len(CLASS_NAMES) * 20))
    draw_palette = ImageDraw.Draw(palette_img)

    for i, (color, name) in enumerate(zip(PALETTE, CLASS_NAMES)):
        draw_palette.rectangle([0, i * 20, 200, (i + 1) * 20], fill=color)
        draw_palette.text((5, i * 20), name, fill=(255, 255, 255))  # White text

    concatenated_img.paste(palette_img, (img.width * 2, 0))

    img_io = io.BytesIO()
    concatenated_img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
