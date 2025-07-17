from PIL import Image
import numpy as np

array = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
image = Image.fromarray(array)
image.save("T_WhiteNoise.png")