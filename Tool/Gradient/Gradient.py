from PIL import Image
import math
import os

def generate_id_strip_image(width=128, output_path=None, max_n=8, mode='RGB'):
    """
    生成一张 ID 图像，左到右排列，支持 RGB、RGBA、灰度、单通道写入等格式

    参数:
    - width: 图像宽度（像素）
    - output_path: 保存路径（若为 None 则自动命名）
    - max_n: 最大颜色数量为 2^max_n
    - mode: 图像模式 ('RGB', 'RGBA', 'L', 'R', 'G', 'B')
    """
    assert mode in ['RGB', 'RGBA', 'L', 'R', 'G', 'B'], "mode 仅支持 'RGB'、'RGBA'、'L'、'R'、'G'、'B'"

    # 自动选择合适的 n
    n = min(max_n, int(math.floor(math.log2(width))))
    num_ids = 2 ** n
    pixels_per_id = width // num_ids
    real_width = pixels_per_id * num_ids

    print(f"使用 n={n}，生成 {num_ids} 个颜色，每种宽度 {pixels_per_id}px，总宽度={real_width}px，模式={mode}")

    # 确定 PIL 允许的图像模式
    pil_mode = 'L' if mode == 'L' else ('RGBA' if mode == 'RGBA' else 'RGB')

    # 颜色值生成
    def get_color(i):
        value = i * (256 // num_ids)
        if mode == 'L':
            return value
        elif mode == 'RGB':
            return (value, value, value)
        elif mode == 'R':
            return (value, 0, 0)
        elif mode == 'G':
            return (0, value, 0)
        elif mode == 'B':
            return (0, 0, value)
        elif mode == 'RGBA':
            return (value, 0, 0, 255)

    # 创建图像
    img = Image.new(pil_mode, (real_width, 1))

    # 写入颜色条
    for idx in range(num_ids):
        color = get_color(idx)
        for x in range(idx * pixels_per_id, (idx + 1) * pixels_per_id):
            img.putpixel((x, 0), color)

        # 打印每个块的精确RGB值
        print(f"Block {idx + 1} (x={idx * pixels_per_id} to {(idx + 1) * pixels_per_id - 1}): {color}")

    # 自动生成输出文件名
    if output_path is None:
        output_path = f"T_Gradient_Strip_{real_width}px_{mode}.png"

    img.save(output_path)
    print(f"图像保存至: {output_path}")

# ✅ 示例调用
if __name__ == "__main__":
    generate_id_strip_image(width=32, mode='G')
