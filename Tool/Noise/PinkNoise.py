import numpy as np
from matplotlib import image as mpimg  # 用于精确保存图像

def generate_pink_noise(size):
    # 生成随机噪声
    noise = np.random.normal(0, 1, size)
    
    # 对噪声进行傅里叶变换
    noise_fft = np.fft.fft2(noise)
    
    # 频率坐标
    rows, cols = size
    x = np.fft.fftfreq(cols)
    y = np.fft.fftfreq(rows)

    # 生成频率网格
    X, Y = np.meshgrid(x, y)
    radius = np.sqrt(X**2 + Y**2)

    # 生成粉噪声特性：增强低频部分
    pink_noise_fft = noise_fft / (radius + 1e-10)  # 防止除零
    pink_noise_fft[0, 0] = 0  # 去掉直流分量

    # 反傅里叶变换回到空间域
    pink_noise = np.fft.ifft2(pink_noise_fft).real
    
    # 归一化至0-1
    pink_noise = (pink_noise - np.min(pink_noise)) / (np.max(pink_noise) - np.min(pink_noise))
    
    return pink_noise

# 设置尺寸
size = (512, 512)
pink_noise_image = generate_pink_noise(size)

# 使用 mpimg.imsave 精确保存为 size x size 的 PNG 图像
mpimg.imsave("T_PinkNoise.png", pink_noise_image, cmap='gray')
