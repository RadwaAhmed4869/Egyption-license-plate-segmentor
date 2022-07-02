import os

output_path = "C:\\Users\\user\\Desktop\\Project\\Egyption-license-plate-segmentor\\outputs_LP7\\"

paths = [output_path]
for path in paths:
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))

# for f in os.listdir(segment_results):
#     os.remove(os.path.join(segment_results, f))