import numpy as np
from noise import pnoise2  # pip install noise
from matplotlib import image as mpimg  # 用于精确保存图像

def generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity, seed=0):
    noise = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            val = pnoise2(x / scale,
                          y / scale,
                          octaves=octaves,
                          persistence=persistence,
                          lacunarity=lacunarity,
                          repeatx=width,
                          repeaty=height,
                          base=seed)
            noise[y][x] = val * 0.5 + 0.5  # Normalize to [0,1]
    return noise

def generate_color_cloud(size_power_of_two=512, noisescale = 100):
    if (size_power_of_two & (size_power_of_two - 1)) != 0:
        raise ValueError("输入的尺寸必须是2的幂次方，例如256、512、1024等。")

    width = height = size_power_of_two
    r = generate_perlin_noise(width, height, scale=noisescale, octaves=6, persistence=0.5, lacunarity=2.0, seed=1)
    g = generate_perlin_noise(width, height, scale=noisescale, octaves=6, persistence=0.5, lacunarity=2.0, seed=5)
    b = generate_perlin_noise(width, height, scale=noisescale, octaves=6, persistence=0.5, lacunarity=2.0, seed=9)

    rgb = np.stack([r, g, b], axis=2)
    rgb = np.clip(rgb, 0, 1)
    return rgb

# 设置尺寸（必须是2的幂）
size = 512
cloud_rgb = generate_color_cloud(size_power_of_two=size,noisescale = 100)

# 精确保存为 size x size 的 PNG 图像
mpimg.imsave("cloud_noise.png", cloud_rgb)
