import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageCompressor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("图片压缩工具")
        self.window.geometry("800x600")
        
        # 创建左右框架
        self.left_frame = tk.Frame(self.window)
        self.left_frame.pack(side=tk.LEFT, padx=20, pady=20, expand=True, fill=tk.BOTH)
        
        self.right_frame = tk.Frame(self.window)
        self.right_frame.pack(side=tk.RIGHT, padx=20, pady=20, expand=True, fill=tk.BOTH)
        
        # 左侧 - 控制面板
        self.create_control_panel()
        
        # 右侧 - 图片预览
        self.create_preview_panel()
        
        self.selected_file = None
        self.image_preview = None
        
    def create_control_panel(self):
        # 选择图片按钮
        self.select_btn = tk.Button(self.left_frame, text="选择图片", command=self.select_file)
        self.select_btn.pack(pady=10)
        
        # 原图信息显示
        self.info_frame = tk.LabelFrame(self.left_frame, text="图片信息", padx=10, pady=10)
        self.info_frame.pack(fill=tk.X, pady=10)
        
        self.filename_label = tk.Label(self.info_frame, text="文件名: ")
        self.filename_label.pack(anchor=tk.W)
        
        self.size_label = tk.Label(self.info_frame, text="文件大小: ")
        self.size_label.pack(anchor=tk.W)
        
        self.dimensions_label = tk.Label(self.info_frame, text="图片尺寸: ")
        self.dimensions_label.pack(anchor=tk.W)
        
        # 目标大小设置
        self.target_frame = tk.LabelFrame(self.left_frame, text="压缩设置", padx=10, pady=10)
        self.target_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(self.target_frame, text="目标文件大小(KB):").pack(anchor=tk.W)
        self.target_size_var = tk.StringVar(value="500")
        self.target_size_entry = tk.Entry(self.target_frame, textvariable=self.target_size_var)
        self.target_size_entry.pack(fill=tk.X, pady=5)
        
        # 保存路径设置
        self.save_path_frame = tk.LabelFrame(self.left_frame, text="保存设置", padx=10, pady=10)
        self.save_path_frame.pack(fill=tk.X, pady=10)
        
        self.save_path_btn = tk.Button(self.save_path_frame, text="选择保存位置", command=self.select_save_path)
        self.save_path_btn.pack(fill=tk.X, pady=5)
        
        self.save_path_label = tk.Label(self.save_path_frame, text="保存位置: 未选择", wraplength=300)
        self.save_path_label.pack(anchor=tk.W)
        
        # 压缩按钮
        self.compress_btn = tk.Button(self.left_frame, text="开始压缩", command=self.compress_image)
        self.compress_btn.pack(pady=20)
        
    def create_preview_panel(self):
        self.preview_label = tk.Label(self.right_frame, text="图片预览")
        self.preview_label.pack()
        
        self.canvas = tk.Canvas(self.right_frame, width=400, height=400)
        self.canvas.pack(expand=True)
        
    def select_file(self):
        filetypes = (
            ('图片文件', '*.jpg *.jpeg *.png'),
            ('所有文件', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='选择图片',
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file = filename
            self.update_image_info()
            self.show_preview()
            
    def select_save_path(self):
        save_path = filedialog.askdirectory(title='选择保存位置')
        if save_path:
            self.save_path_label.config(text=f"保存位置: {save_path}")
            
    def update_image_info(self):
        # 更新文件信息
        filename = os.path.basename(self.selected_file)
        size = os.path.getsize(self.selected_file) / 1024  # KB
        
        image = Image.open(self.selected_file)
        width, height = image.size
        
        self.filename_label.config(text=f"文件名: {filename}")
        self.size_label.config(text=f"文件大小: {size:.1f}KB")
        self.dimensions_label.config(text=f"图片尺寸: {width}x{height}")
        
    def show_preview(self):
        # 显示图片预览
        image = Image.open(self.selected_file)
        
        # 计算缩放比例以适应预览区域
        canvas_width = 400
        canvas_height = 400
        
        # 计算缩放比例
        ratio = min(canvas_width/image.width, canvas_height/image.height)
        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)
        
        # 调整图片大小用于预览
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 将图片转换为PhotoImage对象
        self.image_preview = ImageTk.PhotoImage(image)
        
        # 在画布上显示图片
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width/2, 
            canvas_height/2, 
            image=self.image_preview,
            anchor=tk.CENTER
        )
        
    def compress_image(self):
        if not self.selected_file:
            messagebox.showerror("错误", "请先选择图片文件!")
            return
            
        try:
            target_size = float(self.target_size_var.get())
            if target_size <= 0:
                messagebox.showerror("错误", "目标文件大小必须大于0!")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的目标文件大小!")
            return
            
        # 获取保存路径
        save_path = self.save_path_label.cget("text").replace("保存位置: ", "")
        if save_path == "未选择":
            messagebox.showerror("错误", "请选择保存位置!")
            return
            
        # 获取原文件大小
        original_size = os.path.getsize(self.selected_file) / 1024  # KB
        
        # 打开图片
        image = Image.open(self.selected_file)
        
        # 生成输出文件名
        filename = os.path.basename(self.selected_file)
        name, ext = os.path.splitext(filename)
        output_filename = os.path.join(save_path, f"{name}_compressed{ext}")
        
        if ext.lower() in ['.png', '.PNG']:
            self.compress_png(image, output_filename, target_size)
        else:  # JPEG和其他格式
            self.compress_jpeg(image, output_filename, target_size)
            
        final_size = os.path.getsize(output_filename) / 1024
        
        # 显示结果
        result_message = f"压缩完成!\n原始大小: {original_size:.1f}KB\n压缩后大小: {final_size:.1f}KB\n压缩率: {((original_size-final_size)/original_size*100):.1f}%"
        messagebox.showinfo("完成", result_message)

    def compress_png(self, image, output_filename, target_size):
        """PNG特定的压缩方法"""
        current_size = os.path.getsize(self.selected_file) / 1024
        
        # 如果原图大小已经小于目标大小，直接复制
        if current_size <= target_size:
            image.save(output_filename, format='PNG', optimize=True)
            return
            
        # 保存原始尺寸和模式
        original_size = image.size
        original_mode = image.mode
        
        # 步骤1：如果图片是RGBA模式且没有实际的透明度，转换为RGB
        if original_mode == 'RGBA':
            # 检查是否有实际的透明度
            alpha = image.getchannel('A')
            if all(pixel == 255 for pixel in alpha.getdata()):
                image = image.convert('RGB')
        
        # 步骤2：尝试不同的优化方法直到达到目标大小
        methods = [
            # 方法1：仅优化
            lambda img: img.save(output_filename, format='PNG', optimize=True),
            
            # 方法2：减少颜色 (如果不是1位或P模式)
            lambda img: (img.quantize(colors=256) if img.mode not in ['1', 'P'] 
                        else img).save(output_filename, format='PNG', optimize=True),
            
            # 方法3：开始逐步缩小尺寸
            lambda img: self.scale_image(img, 0.9).save(output_filename, format='PNG', optimize=True),
            lambda img: self.scale_image(img, 0.8).save(output_filename, format='PNG', optimize=True),
            lambda img: self.scale_image(img, 0.7).save(output_filename, format='PNG', optimize=True),
            lambda img: self.scale_image(img, 0.6).save(output_filename, format='PNG', optimize=True),
            lambda img: self.scale_image(img, 0.5).save(output_filename, format='PNG', optimize=True),
        ]
        
        for method in methods:
            try:
                method(image)
                current_size = os.path.getsize(output_filename) / 1024
                if current_size <= target_size:
                    break
            except Exception as e:
                continue
                
    def compress_jpeg(self, image, output_filename, target_size):
        """JPEG特定的压缩方法"""
        # 二分法查找合适的质量参数
        quality_low = 1
        quality_high = 100
        best_quality = 0
        best_size = 0
        
        while quality_low <= quality_high:
            quality = (quality_low + quality_high) // 2
            # 临时保存压缩文件
            image.save(output_filename, format='JPEG', quality=quality, optimize=True)
            current_size = os.path.getsize(output_filename) / 1024
            
            if abs(current_size - target_size) < 100:  # 允许100KB的误差
                break
            elif current_size > target_size:
                quality_high = quality - 1
            else:
                quality_low = quality + 1
                if abs(current_size - target_size) < abs(best_size - target_size):
                    best_quality = quality
                    best_size = current_size
        
        # 如果没有找到完全符合的质量参数，使用最接近的结果
        if best_quality > 0:
            image.save(output_filename, format='JPEG', quality=best_quality, optimize=True)
    
    def scale_image(self, image, scale_factor):
        """按比例缩放图片"""
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageCompressor()
    app.run()