#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF 转图片工具 V1.0
支持批量转换 PDF 文件为图片（PNG/JPG）

作者: zhifouli
GitHub: https://github.com/zhifouli?tab=repositories
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import multiprocessing
from multiprocessing import Process, Queue, Event
import fitz  # PyMuPDF

# 版本信息
__version__ = "1.0"
__app_name__ = "PDF 转图片工具"
__author__ = "zhifouli"
__github__ = "https://github.com/zhifouli?tab=repositories"


def convert_pdf_worker(pdf_path, output_dir, output_format, quality, dpi, 
                       progress_queue, pause_event, stop_event):
    """
    独立进程中的 PDF 转换工作函数
    
    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录
        output_format: 输出格式 (png/jpg)
        quality: 图片质量
        dpi: DPI
        progress_queue: 进度消息队列
        pause_event: 暂停事件
        stop_event: 停止事件
    """
    try:
        filename = os.path.basename(pdf_path)
        pdf_name = Path(pdf_path).stem
        pdf_output_dir = os.path.join(output_dir, f"{pdf_name}_imgs")
        os.makedirs(pdf_output_dir, exist_ok=True)
        
        # 发送开始消息
        progress_queue.put({
            "type": "file_start",
            "filename": filename
        })
        
        # 打开 PDF
        pdf_document = fitz.open(pdf_path)
        total_pages = len(pdf_document)
        zoom = dpi / 72
        
        # 发送总页数
        progress_queue.put({
            "type": "file_total_pages",
            "total_pages": total_pages
        })
        
        # 转换每一页
        for page_num in range(total_pages):
            # 检查暂停
            while pause_event.is_set():
                if stop_event.is_set():
                    pdf_document.close()
                    return False
                multiprocessing.Event().wait(0.1)
            
            # 检查停止
            if stop_event.is_set():
                pdf_document.close()
                return False
            
            page = pdf_document[page_num]
            current_page = page_num + 1
            
            # 设置缩放矩阵
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # 生成输出文件名
            output_filename = f"{pdf_name}_{current_page:04d}.{output_format}"
            output_path = os.path.join(pdf_output_dir, output_filename)
            
            # 保存图片
            if output_format == "png":
                pix.save(output_path)
            else:
                pix.save(output_path, jpg_quality=quality)
            
            # 发送进度（每 1 页或最后一页）
            if current_page % 1 == 0 or current_page == total_pages or current_page == 1:
                progress_queue.put({
                    "type": "file_progress",
                    "filename": filename,
                    "current_page": current_page,
                    "total_pages": total_pages
                })
        
        pdf_document.close()
        
        # 发送完成消息
        progress_queue.put({
            "type": "file_complete",
            "filename": filename
        })
        
        return True
        
    except Exception as e:
        progress_queue.put({
            "type": "file_error",
            "filename": os.path.basename(pdf_path),
            "error": str(e)
        })
        return False


def conversion_process_main(pdf_files, output_dir, output_format, quality, dpi,
                            progress_queue, pause_event, stop_event):
    """
    转换进程主函数
    """
    total_files = len(pdf_files)
    success_count = 0
    error_count = 0
    
    for idx, pdf_path in enumerate(pdf_files, 1):
        # 检查停止
        if stop_event.is_set():
            break
        
        # 发送整体进度
        progress_queue.put({
            "type": "overall_progress",
            "current_file": idx,
            "total_files": total_files
        })
        
        # 转换单个 PDF
        result = convert_pdf_worker(
            pdf_path, output_dir, output_format, quality, dpi,
            progress_queue, pause_event, stop_event
        )
        
        if result:
            success_count += 1
        else:
            if stop_event.is_set():
                break
            error_count += 1
    
    # 发送最终完成消息
    progress_queue.put({
        "type": "conversion_complete",
        "success_count": success_count,
        "error_count": error_count,
        "total_files": total_files,
        "stopped": stop_event.is_set()
    })


class PDF2ImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{__app_name__} V{__version__}")
        
        # 设置窗口大小
        window_width = 700
        window_height = 650
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.root.resizable(True, True)
        
        # 设置窗口图标
        try:
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
            else:
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"⚠ 无法加载图标: {e}")
        
        self.pdf_files = []
        self.is_converting = False
        
        # 多进程相关
        self.conversion_process = None
        self.progress_queue = None
        self.pause_event = None
        self.stop_event = None
        self.is_paused = False
        
        self.setup_ui()
        self.check_progress_queue()
    
    def setup_ui(self):
        """设置用户界面"""
        # 底部信息栏（先创建，使用 pack(side="bottom")）
        footer_frame = tk.Frame(self.root, bg="#f0f0f0", pady=8)
        footer_frame.pack(side="bottom", fill="x")
        
        # 作者信息（左侧）
        author_label = tk.Label(
            footer_frame,
            text=f"© 2025 {__author__}",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#666"
        )
        author_label.pack(side="left", padx=10)
        
        # GitHub 链接（右侧）
        github_label = tk.Label(
            footer_frame,
            text="GitHub: zhifouli",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#1976D2",
            cursor="hand2"
        )
        github_label.pack(side="right", padx=10)
        github_label.bind("<Button-1>", lambda e: self.open_github())
        
        # 标题
        title_label = tk.Label(
            self.root, 
            text=f"{__app_name__} V{__version__}", 
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()
        
        # 文件选择区域
        file_frame = tk.LabelFrame(self.root, text="选择 PDF 文件", padx=10, pady=10)
        file_frame.pack(padx=20, pady=(5, 10), fill="both", expand=True)
        
        # 文件列表
        list_frame = tk.Frame(file_frame)
        list_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.file_listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=scrollbar.set,
            selectmode=tk.MULTIPLE,
            height=6
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # 按钮区域
        btn_frame = tk.Frame(file_frame)
        btn_frame.pack(pady=5)
        
        tk.Button(
            btn_frame, 
            text="添加 PDF 文件", 
            command=self.add_files,
            width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame, 
            text="清空列表", 
            command=self.clear_files,
            width=15
        ).pack(side="left", padx=5)
        
        # 设置区域
        settings_frame = tk.LabelFrame(self.root, text="转换设置", padx=10, pady=10)
        settings_frame.pack(padx=20, pady=(0, 10), fill="x")
        
        # 格式选择
        format_frame = tk.Frame(settings_frame)
        format_frame.pack(fill="x", pady=5)
        
        tk.Label(format_frame, text="输出格式:", width=10, anchor="w").pack(side="left")
        self.format_var = tk.StringVar(value="png")
        tk.Radiobutton(
            format_frame, 
            text="PNG", 
            variable=self.format_var, 
            value="png"
        ).pack(side="left", padx=10)
        tk.Radiobutton(
            format_frame, 
            text="JPG", 
            variable=self.format_var, 
            value="jpg"
        ).pack(side="left", padx=10)
        
        # 质量选择
        quality_frame = tk.Frame(settings_frame)
        quality_frame.pack(fill="x", pady=5)
        
        tk.Label(quality_frame, text="图片质量:", width=10, anchor="w").pack(side="left")
        self.quality_var = tk.IntVar(value=95)
        tk.Scale(
            quality_frame,
            from_=50,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.quality_var,
            length=200
        ).pack(side="left", padx=10)
        self.quality_label = tk.Label(quality_frame, text="95%")
        self.quality_label.pack(side="left")
        self.quality_var.trace_add("write", self.update_quality_label)
        
        # DPI 选择
        dpi_frame = tk.Frame(settings_frame)
        dpi_frame.pack(fill="x", pady=5)
        
        tk.Label(dpi_frame, text="分辨率 (DPI):", width=10, anchor="w").pack(side="left")
        self.dpi_var = tk.IntVar(value=150)
        dpi_options = [72, 96, 150, 200, 300]
        dpi_combo = ttk.Combobox(
            dpi_frame,
            textvariable=self.dpi_var,
            values=dpi_options,
            width=10,
            state="readonly"
        )
        dpi_combo.pack(side="left", padx=10)
        
        # 转换按钮和进度区域
        action_frame = tk.Frame(self.root)
        action_frame.pack(padx=20, pady=(5, 10), fill="x")
        
        # 按钮容器
        button_container = tk.Frame(action_frame)
        button_container.pack(pady=(0, 10))
        
        self.convert_btn = tk.Button(
            button_container,
            text="开始转换",
            command=self.start_conversion,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            width=12,
            cursor="hand2"
        )
        self.convert_btn.pack(side="left", padx=5)
        
        self.pause_btn = tk.Button(
            button_container,
            text="暂停",
            command=self.pause_conversion,
            bg="#FF9800",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            width=12,
            cursor="hand2",
            state="disabled"
        )
        self.pause_btn.pack(side="left", padx=5)
        
        self.stop_btn = tk.Button(
            button_container,
            text="停止",
            command=self.stop_conversion,
            bg="#F44336",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            width=12,
            cursor="hand2",
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)
        
        # 整体进度标签
        self.overall_progress_label = tk.Label(
            action_frame,
            text="总进度: 0/0 个文件",
            font=("Arial", 9, "bold")
        )
        self.overall_progress_label.pack(pady=(0, 3))
        
        # 整体进度条
        self.overall_progress = ttk.Progressbar(
            action_frame,
            orient="horizontal",
            mode="determinate"
        )
        self.overall_progress.pack(fill="x", pady=(0, 10))
        
        # 当前文件进度标签
        self.file_progress_label = tk.Label(
            action_frame,
            text="当前文件: --",
            font=("Arial", 9)
        )
        self.file_progress_label.pack(pady=(0, 3))
        
        # 当前文件进度条
        self.file_progress = ttk.Progressbar(
            action_frame,
            orient="horizontal",
            mode="determinate"
        )
        self.file_progress.pack(fill="x", pady=(0, 5))
        
        # 状态标签
        self.status_label = tk.Label(
            action_frame,
            text="准备就绪",
            fg="green",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=(0, 10))
    
    def update_quality_label(self, *args):
        """更新质量标签"""
        self.quality_label.config(text=f"{self.quality_var.get()}%")
    
    def open_github(self):
        """打开 GitHub 链接"""
        import webbrowser
        webbrowser.open(__github__)
    
    def check_progress_queue(self):
        """定时检查进度队列"""
        if self.progress_queue is not None:
            try:
                # 非阻塞获取消息，每次最多处理 5 个
                for _ in range(5):
                    message = self.progress_queue.get_nowait()
                    self.handle_progress_message(message)
            except:
                pass
        
        # 继续定时检查（100ms）
        self.root.after(100, self.check_progress_queue)
    
    def handle_progress_message(self, message):
        """处理进度消息"""
        msg_type = message.get("type")
        
        if msg_type == "overall_progress":
            current = message["current_file"]
            total = message["total_files"]
            self.overall_progress_label.config(text=f"总进度: {current}/{total} 个文件")
            self.overall_progress["value"] = current
            self.overall_progress["maximum"] = total
            
        elif msg_type == "file_start":
            filename = message["filename"]
            self.status_label.config(text=f"正在处理: {filename}", fg="blue")
            self.file_progress["value"] = 0
            
        elif msg_type == "file_total_pages":
            total_pages = message["total_pages"]
            self.file_progress["maximum"] = total_pages
            
        elif msg_type == "file_progress":
            filename = message["filename"]
            current = message["current_page"]
            total = message["total_pages"]
            self.file_progress_label.config(text=f"当前文件: {filename} - {current}/{total} 页")
            self.file_progress["value"] = current
            
        elif msg_type == "file_complete":
            filename = message["filename"]
            self.status_label.config(text=f"完成: {filename}", fg="green")
            
        elif msg_type == "file_error":
            filename = message["filename"]
            error = message["error"]
            print(f"转换 {filename} 失败: {error}")
            
        elif msg_type == "conversion_complete":
            self.handle_conversion_complete(message)
    
    def add_files(self):
        """添加 PDF 文件"""
        files = filedialog.askopenfilenames(
            title="选择 PDF 文件",
            filetypes=[("PDF 文件", "*.pdf"), ("所有文件", "*.*")]
        )
        
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def clear_files(self):
        """清空文件列表"""
        if self.is_converting:
            messagebox.showwarning("警告", "转换进行中，无法清空列表！")
            return
            
        self.pdf_files = []
        self.file_listbox.delete(0, tk.END)
        self.overall_progress["value"] = 0
        self.file_progress["value"] = 0
        self.overall_progress_label.config(text="总进度: 0/0 个文件")
        self.file_progress_label.config(text="当前文件: --")
        self.status_label.config(text="准备就绪", fg="green")
    
    def start_conversion(self):
        """开始转换"""
        if not self.pdf_files:
            messagebox.showwarning("警告", "请先添加 PDF 文件！")
            return
        
        if self.is_converting:
            messagebox.showinfo("提示", "正在转换中，请稍候...")
            return
        
        # 选择输出目录
        output_dir = filedialog.askdirectory(title="选择输出目录")
        if not output_dir:
            return
        
        # 重置状态
        self.is_converting = True
        self.is_paused = False
        
        # 更新按钮状态
        self.convert_btn.config(state="disabled")
        self.pause_btn.config(state="normal", text="暂停", bg="#FF9800")
        self.stop_btn.config(state="normal")
        
        # 创建多进程通信对象
        self.progress_queue = Queue()
        self.pause_event = Event()
        self.stop_event = Event()
        
        # 获取转换参数
        output_format = self.format_var.get()
        quality = self.quality_var.get()
        dpi = self.dpi_var.get()
        
        # 启动转换进程
        self.conversion_process = Process(
            target=conversion_process_main,
            args=(
                self.pdf_files,
                output_dir,
                output_format,
                quality,
                dpi,
                self.progress_queue,
                self.pause_event,
                self.stop_event
            )
        )
        self.conversion_process.start()
    
    def pause_conversion(self):
        """暂停/继续转换"""
        if not self.is_converting or self.pause_event is None:
            return
        
        if self.is_paused:
            # 继续
            self.is_paused = False
            self.pause_event.clear()
            self.pause_btn.config(text="暂停", bg="#FF9800")
            self.status_label.config(text="转换继续...", fg="blue")
        else:
            # 暂停
            self.is_paused = True
            self.pause_event.set()
            self.pause_btn.config(text="继续", bg="#2196F3")
            self.status_label.config(text="已暂停", fg="orange")
    
    def stop_conversion(self):
        """停止转换"""
        if not self.is_converting or self.stop_event is None:
            return
        
        result = messagebox.askyesno(
            "确认停止",
            "确定要停止转换吗？\n当前进度将会丢失。"
        )
        
        if result:
            self.stop_event.set()
            if self.is_paused:
                self.pause_event.clear()  # 如果暂停，先恢复
            self.status_label.config(text="正在停止...", fg="red")
    
    def handle_conversion_complete(self, message):
        """处理转换完成"""
        self.is_converting = False
        self.is_paused = False
        
        # 清理进程资源
        if self.conversion_process and self.conversion_process.is_alive():
            self.conversion_process.terminate()
            self.conversion_process.join(timeout=1)
        
        self.conversion_process = None
        self.progress_queue = None
        self.pause_event = None
        self.stop_event = None
        
        # 恢复按钮状态
        self.convert_btn.config(state="normal")
        self.pause_btn.config(state="disabled", text="暂停", bg="#FF9800")
        self.stop_btn.config(state="disabled")
        
        # 显示完成消息
        stopped = message.get("stopped", False)
        success_count = message.get("success_count", 0)
        error_count = message.get("error_count", 0)
        
        if stopped:
            self.file_progress_label.config(text="当前文件: 已停止")
            self.status_label.config(text=f"⊗ 已停止！已完成: {success_count} 个文件", fg="red")
            messagebox.showinfo("已停止", f"转换已停止\n已完成: {success_count} 个文件")
        elif error_count == 0:
            self.file_progress_label.config(text="当前文件: 已完成")
            self.status_label.config(text=f"✓ 转换完成！成功: {success_count} 个文件", fg="green")
            messagebox.showinfo("完成", f"所有 PDF 文件已成功转换！\n共 {success_count} 个文件")
        else:
            self.file_progress_label.config(text="当前文件: 已完成")
            self.status_label.config(text=f"⚠ 转换完成！成功: {success_count}, 失败: {error_count}", fg="orange")
            messagebox.showwarning("完成", f"转换完成，但有部分失败\n成功: {success_count}\n失败: {error_count}")


def main():
    """主函数"""
    # Windows 多进程必须的设置
    multiprocessing.freeze_support()
    
    root = tk.Tk()
    app = PDF2ImageConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
