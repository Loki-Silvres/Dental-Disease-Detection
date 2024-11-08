# Dental Disease Detection

This project aims to detect various dental diseases from panoramic images using object detection and segmentation models. The Flask API allows for image input, processing, and visualization of the results in the browser.

## Installation

Follow the steps below to set up the project on your local machine.

### 1. Clone the repository

```bash
cd
git clone https://github.com/Loki-Silvres/Dental-Disease-Detection.git
cd Dental-Disease-Detection/
git checkout Flask
```

### 2. Install the required dependencies

Ensure you have Python 3.7+ installed on your system. Then, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### 3. Download the Pretrained Model

Download the model weights from [Kaggle](https://www.kaggle.com/datasets/lokisilvres/dental-disease-panoramic-detection-dataset) and place the files in the root of the `Dental-Disease-Detection` directory.

### 4. Running the Flask API

Once the model is downloaded and placed correctly, you can run the Flask server:

```bash
python app.py
```

The server will run locally on port `5000` by default. You can test the API by uploading images for detection and viewing the results.

## Usage

- Access the API at `http://localhost:5000/`.
- Use the `/coordinates` endpoint to send an image file for detection and segmentation.
- The response will be an image with bounding boxes and segmentation masks for detected dental diseases, along with a color-coded palette for easy interpretation.
- Via Terminal:
  ```bash
  curl -X POST http://localhost:5000/coordinates -F "image=@sample_img.jpg" --output output.jpg
  ```

## Segmentation Classes

The detection model is trained to detect the following dental conditions:

```
0: Caries
1: Crown
2: Filling
3: Implant
4: Malaligned
5: Mandibular Canal
6: Missing teeth
7: Periapical lesion
8: Retained root
9: Root Canal Treatment
10: Root Piece
11: Impacted tooth
12: Maxillary sinus
13: Bone Loss
14: Fracture teeth
15: Permanent Teeth
16: Supra Eruption
17: TAD
18: Abutment
19: Attrition
20: Bone defect
21: Gingival former
22: Metal band
23: Orthodontic brackets
24: Permanent retainer
25: Post-core
26: Plating
27: Wire
28: Cyst
29: Root resorption
30: Primary teeth
```

## Sample Input and Output

Here is an example of a panoramic dental X-ray image being processed by the model.

### Input

The sample panoramic dental X-ray image that was uploaded for analysis.

![Sample Input](https://github.com/Loki-Silvres/Dental-Disease-Detection/blob/Flask/sample_img.jpg)

### Output

The same image after processing, with bounding boxes and segmentation masks applied. The palette on the right indicates which color corresponds to each detected condition.

![Sample Output](https://github.com/Loki-Silvres/Dental-Disease-Detection/blob/Flask/output.jpg)

### Sample Video
[X-Ray_Disease_Detection_Sample_Video.webm](https://github.com/user-attachments/assets/601c36ed-fd09-4d2c-9768-59b1112058b6)

## Acknowledgments

- Model trained using the dataset available on [Kaggle](https://www.kaggle.com/datasets/lokisilvres/dental-disease-panoramic-detection-dataset).

