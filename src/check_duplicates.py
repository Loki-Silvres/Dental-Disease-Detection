import os
import os.path as osp

def strip_name(name):
    name = name[ name.find('-') + 1 : ]
    name = name[:name.find('2')-1]
    name = name.lower()
    return name

def is_valid(name):

    if name.find('jpg') != -1:
        return False
    
    if name.isdigit():
        return False
    
    if name == '':
        return False

    return True


train_dir = "/home/loki/DentalObjectDetection/data/v6/train/images"
valid_dir = "/home/loki/DentalObjectDetection/data/v6/valid/images"

files1 = sorted(os.listdir(train_dir))
files2 = sorted(os.listdir(valid_dir))

not_valid_name_count = 0

for f in files2:
    if not is_valid(strip_name(f)):
        not_valid_name_count += 1
        # print(f)
print(f'Number of patients with not valid name in {train_dir} : {not_valid_name_count}')
# breakpoint()

files1 = set([strip_name(f) for f in files1 if is_valid(strip_name(f)) ])
files2 = set([strip_name(f) for f in files2 if is_valid(strip_name(f)) ])

same_file_count = 0
same_files = []

for name1 in files1:
    # name1 = files1[i]
    # name1 = strip_name(files1[i])
    # print(name1)
    # breakpoint()
    for name2 in files2:
        # name2 = strip_name(files2[j])
        if name1 == name2:
            same_file_count += 1
            same_files.append(name1)
            # print(i, j, files1[i], files2[j])
            break
print(f'Number of patients common in {train_dir} and {valid_dir} : {len(same_files)} out of total {len(files1.union(files2))} patients')
print(same_files)