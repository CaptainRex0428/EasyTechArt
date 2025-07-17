from PIL import Image
import numpy as np
import math

class NoiseGenerator:
    def __init__(self, width=512, height=512, seed=None):
        """
        初始化噪声生成器
        
        Args:
            width: 图像宽度
            height: 图像高度
            seed: 随机种子，用于重现结果
        """
        self.width = width
        self.height = height
        if seed is not None:
            np.random.seed(seed)
    
    def generate_perlin_like_noise(self, octaves=4, persistence=0.5, scale=1.0):
        """
        生成类似Perlin噪声的自然分布噪声
        
        Args:
            octaves: 噪声层数，越多越复杂
            persistence: 持续性，控制高频噪声的衰减
            scale: 整体缩放因子
        
        Returns:
            numpy array: 单通道噪声数据 [0, 1]
        """
        noise = np.zeros((self.height, self.width))
        amplitude = 1.0
        frequency = scale
        max_value = 0.0
        
        for i in range(octaves):
            # 生成当前频率的噪声
            octave_noise = self.generate_smooth_noise(frequency)
            noise += octave_noise * amplitude
            
            max_value += amplitude
            amplitude *= persistence
            frequency *= 2.0
        
        # 归一化到 [0, 1]
        noise = noise / max_value
        return np.clip(noise, 0, 1)
    
    def generate_smooth_noise(self, frequency):
        """
        生成平滑的噪声层
        
        Args:
            frequency: 噪声频率
        
        Returns:
            numpy array: 平滑噪声
        """
        # 生成网格坐标
        x = np.linspace(0, frequency, self.width)
        y = np.linspace(0, frequency, self.height)
        X, Y = np.meshgrid(x, y)
        
        # 使用多个正弦波叠加创建更自然的噪声
        noise = np.zeros((self.height, self.width))
        
        # 添加多个方向的波形
        for angle in [0, np.pi/4, np.pi/2, 3*np.pi/4]:
            wave_x = X * np.cos(angle) + Y * np.sin(angle)
            wave_y = -X * np.sin(angle) + Y * np.cos(angle)
            
            # 组合不同频率的噪声
            noise += (np.sin(wave_x * 2 * np.pi) * np.cos(wave_y * 2 * np.pi) +
                     np.sin(wave_x * 4 * np.pi) * np.cos(wave_y * 4 * np.pi) * 0.5)
        
        # 添加随机扰动使其更自然
        random_noise = np.random.normal(0, 0.1, (self.height, self.width))
        noise += random_noise
        
        return noise
    
    def generate_fractal_noise(self, octaves=6, lacunarity=2.0, gain=0.5):
        """
        生成分形噪声（更自然的分布）
        
        Args:
            octaves: 噪声层数
            lacunarity: 频率倍数
            gain: 振幅衰减
        
        Returns:
            numpy array: 分形噪声 [0, 1]
        """
        noise = np.zeros((self.height, self.width))
        amplitude = 1.0
        frequency = 1.0
        max_value = 0.0
        
        for i in range(octaves):
            # 生成当前层的噪声
            layer_noise = self.generate_noise_layer(frequency)
            noise += layer_noise * amplitude
            
            max_value += amplitude
            amplitude *= gain
            frequency *= lacunarity
        
        # 归一化并应用更自然的分布曲线
        noise = noise / max_value
        noise = np.clip(noise, 0, 1)
        
        # 应用幂函数使分布更自然
        noise = np.power(noise, 1.2)
        
        return noise
    
    def generate_noise_layer(self, frequency):
        """
        生成单层噪声
        """
        # 使用正态分布作为基础
        base_noise = np.random.normal(0, 1, (self.height, self.width))
        
        # 应用频率调制
        x = np.arange(self.width) * frequency / self.width
        y = np.arange(self.height) * frequency / self.height
        X, Y = np.meshgrid(x, y)
        
        # 使用正弦调制创建周期性变化
        modulation = np.sin(X * 2 * np.pi) * np.cos(Y * 2 * np.pi)
        
        # 组合基础噪声和调制
        noise = base_noise * (1 + modulation * 0.3)
        
        return noise
    
    def generate_rgba_noise(self, channel_configs):
        """
        生成RGBA四通道噪声
        
        Args:
            channel_configs: 字典，包含每个通道的配置
                例如: {
                    'R': {'type': 'perlin', 'octaves': 4, 'scale': 1.0},
                    'G': {'type': 'fractal', 'octaves': 6, 'lacunarity': 2.0},
                    'B': {'type': 'perlin', 'octaves': 2, 'scale': 2.0},
                    'A': {'type': 'fractal', 'octaves': 8, 'gain': 0.3}
                }
        
        Returns:
            numpy array: RGBA噪声数据 [0, 255]
        """
        channels = []
        
        for channel_name in ['R', 'G', 'B', 'A']:
            config = channel_configs.get(channel_name, {})
            noise_type = config.get('type', 'perlin')
            
            if noise_type == 'perlin':
                octaves = config.get('octaves', 4)
                persistence = config.get('persistence', 0.5)
                scale = config.get('scale', 1.0)
                channel_noise = self.generate_perlin_like_noise(octaves, persistence, scale)
            
            elif noise_type == 'fractal':
                octaves = config.get('octaves', 6)
                lacunarity = config.get('lacunarity', 2.0)
                gain = config.get('gain', 0.5)
                channel_noise = self.generate_fractal_noise(octaves, lacunarity, gain)
            
            elif noise_type == 'smooth':
                frequency = config.get('frequency', 1.0)
                channel_noise = self.generate_smooth_noise(frequency)
                channel_noise = (channel_noise - channel_noise.min()) / (channel_noise.max() - channel_noise.min())
            
            else:  # 默认使用简单随机噪声
                channel_noise = np.random.random((self.height, self.width))
            
            # 应用后处理
            contrast = config.get('contrast', 1.0)
            brightness = config.get('brightness', 0.0)
            gamma = config.get('gamma', 1.0)
            
            # 对比度和亮度调整
            channel_noise = np.clip(channel_noise * contrast + brightness, 0, 1)
            
            # 伽马校正
            channel_noise = np.power(channel_noise, gamma)
            
            # 转换到 [0, 255] 范围
            channel_noise = (channel_noise * 255).astype(np.uint8)
            channels.append(channel_noise)
        
        # 合并通道
        rgba_array = np.stack(channels, axis=-1)
        return rgba_array

# 使用示例和预设配置
def create_sand_effect_noise():
    """
    创建适合沙化效果的噪声配置
    """
    generator = NoiseGenerator(width=512, height=512, seed=42)
    
    # 沙化效果的通道配置
    sand_config = {
        'R': {
            'type': 'fractal',
            'octaves': 6,
            'lacunarity': 2.0,
            'gain': 0.6,
            'contrast': 1.2,
            'brightness': 0.1,
            'gamma': 1.1
        },
        'G': {
            'type': 'perlin',
            'octaves': 4,
            'persistence': 0.4,
            'scale': 1.5,
            'contrast': 1.0,
            'brightness': 0.15,
            'gamma': 1.0
        },
        'B': {
            'type': 'fractal',
            'octaves': 8,
            'lacunarity': 1.8,
            'gain': 0.4,
            'contrast': 0.8,
            'brightness': 0.2,
            'gamma': 0.9
        },
        'A': {
            'type': 'perlin',
            'octaves': 3,
            'persistence': 0.7,
            'scale': 0.8,
            'contrast': 1.5,
            'brightness': 0.0,
            'gamma': 1.2
        }
    }
    
    return generator.generate_rgba_noise(sand_config)

def create_custom_noise():
    """
    创建自定义配置的噪声
    """
    generator = NoiseGenerator(width=512, height=512, seed=123)
    
    # 自定义配置示例
    custom_config = {
        'R': {
            'type': 'fractal',
            'octaves': 1,
            'lacunarity': 1.0,
            'gain': 1.5,
            'contrast': 2,
            'brightness': 0.1,
            'gamma': 1.1
        },
        'G': {
            'type': 'fractal',
            'octaves': 6,
            'lacunarity': 4.0,
            'gain': 1,
            'contrast': 1.2,
            'brightness': 0.1,
            'gamma': 1.1
        },
        'B': {
            'type': 'fractal',
            'octaves': 3,
            'lacunarity': 2.0,
            'gain': 0.6,
            'contrast': 1,
            'brightness': 0.1,
            'gamma': 1.1
            
        },
        'A': {
            'type': 'smooth',
            'frequency': 1.5,
            'contrast': 1.3,
            'gamma': 0.8
        }
    }
    
    return generator.generate_rgba_noise(custom_config)

# 主程序
if __name__ == "__main__":
    # 生成沙化效果噪声
    # print("生成沙化效果噪声...")
    # sand_noise = create_sand_effect_noise()
    # sand_image = Image.fromarray(sand_noise, 'RGBA')
    # sand_image.save("T_SandNoise.png")
    # print("沙化效果噪声已保存为 sand_effect_noise.png")
    
    # 生成自定义噪声
    print("生成自定义噪声...")
    custom_noise = create_custom_noise()
    custom_image = Image.fromarray(custom_noise, 'RGBA')
    custom_image.save("T_CustomNoise.png")
    print("自定义噪声已保存为 custom_noise.png")
    
    # 显示各通道信息
    print("\n各通道统计信息:")
    channels = ['R', 'G', 'B', 'A']
    for i, channel in enumerate(channels):
        channel_data = custom_noise[:, :, i]
        print(f"{channel}通道 - 最小值: {channel_data.min()}, 最大值: {channel_data.max()}, 平均值: {channel_data.mean():.2f}")