import os
import glob
from pathlib import Path
import re

def rename_all_files(root_folder):
    # 获取所有图片文件路径（包括子文件夹）
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.tga', '*.bmp', '*.tif', '*.exr', '*.gif']
    all_files = []
    
    # 递归收集所有符合条件的图片文件
    for ext in image_extensions:
        all_files.extend(glob.glob(os.path.join(root_folder, '**', ext), recursive=True))
    
    # 按文件路径排序（确保连续编号）
    all_files.sort()
    
    # 确定总文件数，计算需要的位数（至少3位）
    total_files = len(all_files)
    num_digits = max(3, len(str(total_files)))
    
    print(f"Found {total_files} files. Using {num_digits}-digit numbering...")
    
    # 重命名所有文件（全局连续编号）
    for index, file_path in enumerate(all_files, start=1):
        folder = os.path.dirname(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # 格式化序号为三位数（或更多位），前面补零
        formatted_index = str(index).zfill(num_digits)
        
        # 构建新文件名
        new_name = f"T_MatCap_{formatted_index}{file_ext}"
        new_path = os.path.join(folder, new_name)
        
        # 避免覆盖冲突（如果目标文件已存在）
        if os.path.exists(new_path):
            base_name = f"T_MatCap_{formatted_index}"
            counter = 1
            while os.path.exists(new_path):
                new_name = f"{base_name}_{counter}{file_ext}"
                new_path = os.path.join(folder, new_name)
                counter += 1
        
        # 重命名文件
        os.rename(file_path, new_path)
        print(f"Renamed: {Path(file_path).relative_to(root_folder)} -> {new_name}")
    
    print(f"\nSuccessfully renamed {total_files} files with continuous numbering.")

if __name__ == "__main__":
    # 替换为你的根目录路径
    root_path = r"D:/BaiduNetdiskDownload/MatCap球ZBrush材质球映射材质球各种材质Mapcap算法材质使用贴图/Matcap512"  # Windows路径示例
    # root_path = "/home/user/your/folder"  # Linux/macOS路径示例
    
    # 安全验证
    if not os.path.exists(root_path):
        print(f"Error: Path '{root_path}' does not exist!")
    elif not os.path.isdir(root_path):
        print(f"Error: '{root_path}' is not a directory!")
    else:
        # 确认操作
        confirm = input(f"About to rename ALL files in {root_path} and its subfolders. Continue? (y/n): ")
        if confirm.lower() == 'y':
            rename_all_files(root_path)
            print("Operation completed.")
        else:
            print("Operation canceled.")
