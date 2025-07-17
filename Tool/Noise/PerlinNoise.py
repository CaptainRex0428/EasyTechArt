import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2

def generate_seamless_perlin(width, height, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=0):
    """
    生成无缝的Perlin噪声
    
    参数:
    - width, height: 图像尺寸
    - scale: 噪声的缩放因子（越大，噪声越平滑）
    - octaves: 噪声的层数
    - persistence: 每层振幅的衰减率
    - lacunarity: 每层频率的增长率
    - seed: 随机种子
    """
    noise = np.zeros((height, width))
    
    # 计算噪声空间中的重复周期
    # 这是关键：repeatx和repeaty应该是噪声坐标系中的值，而不是像素值
    repeat_x = width / scale
    repeat_y = height / scale
    
    for y in range(height):
        for x in range(width):
            # 计算噪声坐标
            nx = x / scale
            ny = y / scale
            
            # 生成Perlin噪声，使用正确的重复周期
            val = pnoise2(nx, ny,
                         octaves=octaves,
                         persistence=persistence,
                         lacunarity=lacunarity,
                         repeatx=repeat_x,
                         repeaty=repeat_y,
                         base=seed)
            
            # 归一化到 [0, 1]
            noise[y][x] = val * 0.5 + 0.5
    
    return noise

def generate_seamless_perlin_optimized(width, height, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=0):
    """
    优化版本：使用numpy向量化操作提高性能
    """
    # 创建坐标网格
    x_coords = np.arange(width)
    y_coords = np.arange(height)
    xx, yy = np.meshgrid(x_coords, y_coords)
    
    # 转换到噪声坐标系
    nx = xx / scale
    ny = yy / scale
    
    # 计算重复周期
    repeat_x = width / scale
    repeat_y = height / scale
    
    # 向量化的pnoise2函数
    vectorized_pnoise2 = np.vectorize(lambda x, y: pnoise2(x, y, 
                                                           octaves=octaves,
                                                           persistence=persistence,
                                                           lacunarity=lacunarity,
                                                           repeatx=repeat_x,
                                                           repeaty=repeat_y,
                                                           base=seed))
    
    # 生成噪声
    noise = vectorized_pnoise2(nx, ny)
    
    # 归一化到 [0, 1]
    noise = noise * 0.5 + 0.5
    
    return noise

def visualize_seamless_test(noise):
    """
    可视化测试无缝性：显示2x2平铺的效果
    """
    # 创建2x2平铺
    tiled = np.tile(noise, (2, 2))
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    # 显示原始噪声
    axes[0].imshow(noise, cmap='gray', vmin=0, vmax=1)
    axes[0].set_title('Original Perlin Noise')
    axes[0].axis('off')
    
    # 显示平铺效果
    axes[1].imshow(tiled, cmap='gray', vmin=0, vmax=1)
    axes[1].set_title('2x2 Tiled (Test Seamlessness)')
    axes[1].axis('off')
    
    # 在平铺图上画线显示边界
    h, w = noise.shape
    axes[1].axhline(y=h, color='red', linewidth=1, alpha=0.5)
    axes[1].axvline(x=w, color='red', linewidth=1, alpha=0.5)
    
    plt.tight_layout()
    return fig

# 主程序
if __name__ == "__main__":
    # 设置参数
    size = 256  # 图像大小
    scale = 50.0  # 噪声缩放（调整这个值来改变噪声的"粗细"）
    
    # 生成无缝Perlin噪声
    print("生成无缝Perlin噪声...")
    perlin_noise = generate_seamless_perlin(size, size, scale=scale, octaves=6, 
                                           persistence=0.5, lacunarity=2.0, seed=42)
    
    # 保存图像
    plt.imsave("T_PerlinNoise_Seamless.png", perlin_noise, cmap='gray')
    print("已保存: T_PerlinNoise_Seamless.png")
    
    # 可视化测试无缝性
    fig = visualize_seamless_test(perlin_noise)
    plt.savefig("T_PerlinNoise_Seamless_Test.png", dpi=150, bbox_inches='tight')
    print("已保存测试图: T_PerlinNoise_Seamless_Test.png")
    plt.show()
    
    # 验证无缝性（检查边缘像素）
    print("\n验证无缝性:")
    print(f"左边缘第一个像素: {perlin_noise[0, 0]:.6f}")
    print(f"右边缘最后像素: {perlin_noise[0, -1]:.6f}")
    print(f"上边缘第一个像素: {perlin_noise[0, 0]:.6f}")
    print(f"下边缘最后像素: {perlin_noise[-1, 0]:.6f}")
    
    # 检查对角
    print(f"\n左上角: {perlin_noise[0, 0]:.6f}")
    print(f"右下角: {perlin_noise[-1, -1]:.6f}")
    
    # 边缘连续性测试
    left_edge = perlin_noise[:, 0]
    right_edge = perlin_noise[:, -1]
    top_edge = perlin_noise[0, :]
    bottom_edge = perlin_noise[-1, :]
    
    print(f"\n边缘差异:")
    print(f"左右边缘最大差异: {np.max(np.abs(left_edge - right_edge)):.6f}")
    print(f"上下边缘最大差异: {np.max(np.abs(top_edge - bottom_edge)):.6f}")