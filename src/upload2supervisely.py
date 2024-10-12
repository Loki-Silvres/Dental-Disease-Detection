import supervisely as sly
import os
import numpy as np
from supervisely.io.fs import get_file_name, get_file_ext
import imagesize as imgsz
from tqdm import tqdm
from multiprocessing import Pool

"""
REQUIREMENTS:

pip install supervisely imagesize tqdm

"""

"""
Create a file named supervisely_env.env with Supervisely credentials:

SERVER_ADDRESS="https://app.supervise.ly"
API_TOKEN="your_api_token"

"""

"""
PARAMETERS:

env_file_path: Path to your supervisely_env.env file.
workspace_id: Your workspace ID on Supervisely.
project_name: Name of your Supervisely project (fill if you want to create new project).
project_id: Set None if you’re creating a new project (fill if you want to upload to an existing project).
dataset_name: The dataset name within the project (fill if you want to create new dataset).
dataset_id: Set None if you’re creating a new dataset (fill if you want to upload to an existing dataset).
images_dir and labels_dir: Path to local directories containing your YOLO-format dataset.
labels_dict: Dictionary that maps class ID to class name.
"""

env_file_path = 'config/supervisely_env.env'

workspace_id = 105867  # Replace with your workspace ID

project_name = "Panoramic Dental X-Ray Segmentation Project"
project_id = 321470

dataset_name = f"Combined train Dataset"
dataset_id = None

# YOLO Dataset folder paths
images_dir = f"/home/loki/DentalObjectDetection/data/YOLO/train/images"
labels_dir = f"/home/loki/DentalObjectDetection/data/YOLO/train/labels"

labels_dict = {
    0: "Caries",
    1: "Crown",
    2: "Filling",
    3: "Implant",
    4: "Malaligned",
    5: "Mandibular Canal",
    6: "Missing teeth",
    7: "Periapical lesion",
    8: "Retained root",
    9: "Root Canal Treatment",
    10: "Root Piece",
    11: "impacted tooth",
    12: "maxillary sinus",
    13: "Bone Loss",
    14: "Fracture teeth",
    15: "Permanent Teeth",
    16: "Supra Eruption",
    17: "TAD",
    18: "abutment",
    19: "attrition",
    20: "bone defect",
    21: "gingival former",
    22: "metal band",
    23: "orthodontic brackets",
    24: "permanent retainer",
    25: "post - core",
    26: "plating",
    27: "wire",
    28: "Cyst",
    29: "Root resorption",
    30: "Primary teeth"
}

api = sly.Api.from_env(env_file=env_file_path)

if project_id is None:
    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    project_id = project.id
if dataset_id is None:
    dataset = api.dataset.create(project_id, dataset_name, change_name_if_conflict=True)
    dataset_id = dataset.id

obj_classes = []
for class_name in labels_dict.values():
    obj_class = sly.ObjClass(name=class_name, geometry_type=sly.Polygon) 
    obj_classes.append(obj_class)

meta = sly.ProjectMeta(obj_classes=obj_classes)
api.project.update_meta(project_id, meta.to_json())

def convert_yolo_segmentation_to_polygon(yolo_data, img_width, img_height):
    """
    yolo_data: list of (x, y) coordinates from YOLO format (either normalized or pixel values)
    img_width: width of the image
    img_height: height of the image
    """
    points = []
    for x, y in yolo_data:
        abs_x = x * img_width
        abs_y = y * img_height
        points.append(sly.PointLocation(abs_y, abs_x)) 

    return sly.Polygon(points)

def upload_image_and_annotations(img_filename):
    if get_file_ext(img_filename) not in [".jpg", ".png"]:
        return None
    img_path = os.path.join(images_dir, img_filename)
    label_path = os.path.join(labels_dir, f"{get_file_name(img_filename)}.txt")
    img_width, img_height = imgsz.get(img_path)
    img_info = api.image.upload_path(dataset_id, img_filename, img_path)
    labels = []
    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            for line in f.readlines():
                values = line.strip().split()

                class_id = int(values[0])
                class_name = labels_dict[class_id]

                yolo_polygon = [(float(values[i]), float(values[i + 1])) for i in range(1, len(values), 2)]
                polygon = convert_yolo_segmentation_to_polygon(yolo_polygon, img_width, img_height)

                label = sly.Label(polygon, meta.get_obj_class(class_name))
                labels.append(label)

    ann = sly.Annotation(img_size=(img_height, img_width), labels=labels)
    api.annotation.upload_ann(img_info.id, ann)

    return img_filename

def process_images():
    with Pool() as pool:
        img_filenames = os.listdir(images_dir)
        for result in tqdm(pool.imap_unordered(upload_image_and_annotations, img_filenames), total=len(img_filenames)):
            if result:
                print(f"Processed {result}")

if __name__ == "__main__":
    process_images()

print("Segmentation dataset uploaded successfully!")
