from PIL import Image
import os

def generate_icons():
    img_path = "logo.JPG"
    if not os.path.exists(img_path):
        print(f"找不到文件: {img_path}，请确认已放进当前目录！")
        return

    img = Image.open(img_path)
    width, height = img.size

    # 核心修改：同时裁掉左侧的留白和右侧的文字
    # 左边切掉约 20% 的高度（去掉多余白边）
    # 右边保留到 1.15 倍高度（刚好避开文字）
    left_edge = int(height * 0.20)
    right_edge = int(height * 1.15)
    
    crop_box = (left_edge, 0, right_edge, height)
    icon_img = img.crop(crop_box)

    # 计算等比例缩放，确保它能完美放进 512x512 的方框里
    icon_width, icon_height = icon_img.size
    scale = 512 / max(icon_width, icon_height)
    new_w = int(icon_width * scale)
    new_h = int(icon_height * scale)
    icon_img = icon_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # 创建一块 512x512 的纯白正方形底板
    square_img = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
    
    # 把“贴边裁剪”后的 logo 绝对居中贴上去
    offset_x = (512 - new_w) // 2
    offset_y = (512 - new_h) // 2
    square_img.paste(icon_img, (offset_x, offset_y))

    # 保存文件
    square_img.save("icon.png")
    print("✅ 成功生成 icon.png (完美去白边且居中)")

    square_img.save("icon.ico", format="ICO", sizes=[(256, 256)])
    print("✅ 成功生成 icon.ico (完美去白边且居中)")

if __name__ == "__main__":
    generate_icons()