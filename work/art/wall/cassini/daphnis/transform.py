import os
import glob
import skimage
from skimage import io

raw = 'raw'
raw_format = '.png'
cwd = os.path.dirname(os.path.realpath(__file__))
data = os.path.join(cwd, raw)

for file in os.listdir(data):
    print(file)

filename = os.path.join(skimage.data_dir, 'moon.png')
moon = io.imread(filename)
print(moon.shape)
print(data)