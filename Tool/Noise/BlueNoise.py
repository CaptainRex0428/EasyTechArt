import numpy as np
from matplotlib import image as mpimg  # 用于精确保存图像

def generate_blue_noise(size):
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

    # 生成蓝噪声特性：放大高频部分
    blue_noise_fft = noise_fft * (radius ** 1.5)  # 放大高频部分

    # 反傅里叶变换回到空间域
    blue_noise = np.fft.ifft2(blue_noise_fft).real
    
    # 归一化至0-1
    blue_noise = (blue_noise - np.min(blue_noise)) / (np.max(blue_noise) - np.min(blue_noise))
    
    return blue_noise

# 设定图像大小
size = (512, 512)
blue_noise_image = generate_blue_noise(size)

# 使用 mpimg.imsave 精确保存为 size x size 的 PNG 图像
mpimg.imsave("T_BlueNoise.png", blue_noise_image, cmap='gray')
