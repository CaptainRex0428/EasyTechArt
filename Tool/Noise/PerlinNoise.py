import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2  # pip install noise

def generate_perlin_grayscale(width, height, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=0):
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
            noise[y][x] = val * 0.5 + 0.5  # 归一化到 [0, 1]
    return noise

# 设置图像大小（必须是2的幂次方）
size = 256
perlin_noise = generate_perlin_grayscale(size, size)

# 保存为纯灰度图
plt.imsave("perlin_noise.png", perlin_noise, cmap='gray')
