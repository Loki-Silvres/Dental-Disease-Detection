import os
import os.path as osp
import sys
import yaml

def get_labels_list(labels_dir: str) -> list[str]:

    if osp.isdir(labels_dir) == True:
        labels = [osp.join(labels_dir, label) for label in sorted(os.listdir(labels_dir)) if label.endswith('.txt')]
    else:
        assert osp.isfile(labels_dir) == True, "Not found file: {}".format(labels_dir)
        labels = [labels_dir]

    return labels

def remove_label(label_index: str, labels_dir: str, new_labels_dir:str = None) -> None:

    labels = get_labels_list(labels_dir=labels_dir)
    if new_labels_dir is None:
        new_labels_dir = labels_dir
    n_digits = len(label_index)
    success = 0
    
    for label in labels:
        new_label_list = []
        n_labels = 0
        with open(label, 'r') as file:
            lines = file.readlines()
            n_labels = len(lines)
            for line in lines:
                if line[:n_digits] == label_index:
                    n_labels -= 1
                    continue
                new_label_list.append(line)
        file.close()

        if len(new_label_list) == len(lines):
            continue
        
        filename = osp.split(label)[-1]
        new_label = osp.join(new_labels_dir, filename)
        with open(new_label, 'w') as file:
            for itr, line in enumerate(new_label_list):
                file.write(line)
            success += 1
        file.close()

    print(f"Removed label: '{label_index}' from {success} files")

def change_label(changes:dict, labels_dir:str, new_labels_dir:str = None) -> None:

    labels = get_labels_list(labels_dir=labels_dir) 
    if new_labels_dir is None:
        new_labels_dir = labels_dir

    success = 0
    
    for label in labels:
        new_label_list = []
        n_labels = 0
        with open(label, 'r') as file:
            lines = file.readlines()
            n_labels = len(lines)
            for line in lines:
                cls = line.split()[0]
                if cls in changes.keys():
                    line = changes[cls] + ' ' + ' '.join(line.split()[1:]) + '\n'
                new_label_list.append(line)
        file.close()
        
        filename = osp.split(label)[-1]
        if new_labels_dir == labels_dir:
            new_label = label
        else:
            new_label = osp.join(new_labels_dir, filename)
        with open(new_label, 'w') as file:
            for itr, line in enumerate(new_label_list):
                file.write(line)
            success += 1
        file.close()

    print(f"Changed label: '{changes}' in {success} files")


def main():
    
    dir_name = 'temp'
    labels_dirs = [f'/home/loki/DentalObjectDetection/data/{dir_name}/train/labels', 
                   f'/home/loki/DentalObjectDetection/data/{dir_name}/valid/labels',
                #    f'/home/loki/DentalObjectDetection/data/{dir_name}/test/labels',
                   ]
    # labels_dirs = ['/home/loki/DentalObjectDetection/assets/temp.txt']

    datasetv6 = [
        "Caries", "Crown", "Filling", "Implant", "Malaligned", "Mandibular Canal", "Missing teeth", 
        "Periapical lesion", "Retained root", "Root Canal Treatment", "Root Piece", "croen", 
        "impacted tooth", "maxillary sinus"
    ]

    yolo8dental = [
        "Amalgam filling", "Bone Loss", "Caries", "Composite filling", "Crown", "Cyst", "Filling",
        "Fracture teeth", "Implant", "Malaligned", "Missing teeth", "Periapical lesion", "Permanent Teeth", 
        "Primary teeth", "Retained root", "Root Piece", "Root canal filling", "Root canal obturation", 
        "Root resorption", "Supra Eruption", "TAD", "Unhealed socket", "abutment", "attrition", 
        "bone defect", "cavity", "decay", "gingival former", "impacted tooth", "metal band", 
        "orthodontic brackets", "permanentretainer", "plating", "post - core", "rct", 
        "retained deciduous tooth", "spacing", "wire"
    ]

    final = [
        "Caries", "Crown", "Filling", "Implant", "Malaligned", "Mandibular Canal", "Missing teeth", 
        "Periapical lesion", "Retained root", "Root Canal Treatment", "Root Piece", "impacted tooth", 
        "maxillary sinus", "Bone Loss", "Fracture teeth", "Permanent Teeth", "Supra Eruption", "TAD", 
        "abutment", "attrition", "bone defect", "gingival former", "metal band", "orthodontic brackets", 
        "permanent retainer", "post - core", "plating", "wire", "Cyst", "Root resorption"
    ]

    changes = {
        '2': '0', '0':'2', '1':'13', '3': '2', '4': '1', '6': '2', '8': '3', '9': '4', '10': '6', '11': '7', '14': '8',
        '13': '30', '16': '9', '17': '9', '21': '6', '25': '0', '26': '0', '31': '24', '31': '24', '34': '9', '35': '30',
        '15': '10', '28': '11', '1': '13', '7': '14', '12': '15', '19': '16', '20': '17', '36' :'6',
        '22': '18', '23': '19', '24': '20', '27': '21', '29': '22', '30': '23', '33': '25', 
        '32': '26', '37': '27', '5': '28', '18': '29'
    }
    print(len(changes), sorted(changes.keys()))

    for labels_dir in labels_dirs:  
        pass
        # remove_label(label_index='11', labels_dir=labels_dir)
        # change_label(changes=changes, labels_dir=labels_dir)

if __name__ == '__main__':
    main()