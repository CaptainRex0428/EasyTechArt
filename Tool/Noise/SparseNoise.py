import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def generate_star_noise_rgb(
    size=512,
    densities=(0.1, 0.05, 0.02),  # R,G,B 三通道密度
    brightness_ranges=((0.7,1.0), (0.4,0.7), (0.2,0.4)),  # R,G,B 亮度范围
    blur_radius=0.6,
    seed=0
):
    np.random.seed(seed)
    rgb = np.zeros((size, size, 3), dtype=np.float32)

    for c in range(3):  # R,G,B 通道
        density = densities[c]
        b_min, b_max = brightness_ranges[c]
        num_stars = int(size * size * density)

        xs = np.random.randint(0, size, size=num_stars)
        ys = np.random.randint(0, size, size=num_stars)
        brightness = np.random.uniform(b_min, b_max, size=num_stars)

        channel = np.zeros((size, size), dtype=np.float32)

        for x, y, b in zip(xs, ys, brightness):
            channel[y % size, x % size] += b
            # tileable wrap-around 边缘补充
            channel[(y+1)%size, x % size] += b * 0.5
            channel[y % size, (x+1)%size] += b * 0.5
            channel[(y-1)%size, x % size] += b * 0.25
            channel[y % size, (x-1)%size] += b * 0.25

        # 模糊 glow 效果
        channel = gaussian_filter(channel, sigma=blur_radius)
        channel = np.clip(channel, 0, 1)

        rgb[:, :, c] = channel

    return rgb

def save_star_noise_rgb(filename, rgb_img):
    plt.imsave(filename, rgb_img)

if __name__ == "__main__":
    size = 512
    star_noise_rgb = generate_star_noise_rgb(
        size=size,
        densities=(0.01, 0.005, 0.002),
        brightness_ranges=((0.7,1.0), (0.4,0.7), (0.2,0.4)),
        blur_radius=0.6,
        seed=42
    )
    save_star_noise_rgb("T_SparseNoise.png", star_noise_rgb)
    print("已保存 star_noise_rgb.png")
