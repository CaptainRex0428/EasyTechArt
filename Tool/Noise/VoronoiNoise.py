import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

def generate_voronoi_noise(width, height, num_points=50, seed=42):
    np.random.seed(seed)
    
    # 生成随机种子点坐标
    points = np.random.rand(num_points, 2) * np.array([[width, height]])
    
    # 构建空图
    voronoi = np.zeros((height, width), dtype=np.float32)

    for y in range(height):
        for x in range(width):
            pos = np.array([x, y])
            # 计算当前位置到所有种子点的欧氏距离
            dists = np.linalg.norm(points - pos, axis=1)
            min_dist = np.min(dists)
            voronoi[y, x] = min_dist

    # 归一化为 [0, 1] 灰度
    voronoi -= voronoi.min()
    voronoi /= voronoi.max()
    return voronoi

# 参数设置
size = 256  # 图像大小为 size x size
num_seeds = 64  # 控制细胞数量
voronoi_noise = generate_voronoi_noise(size, size, num_points=num_seeds)

# 保存图像
plt.imsave("T_VoronoiNoise.png", voronoi_noise, cmap='gray')

# （可选）显示图像
plt.imshow(voronoi_noise, cmap='gray')
plt.axis('off')
plt.show()
