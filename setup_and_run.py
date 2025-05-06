# -*- coding: utf-8 -*-
import os
import subprocess
import webbrowser
import sys
import tkinter as tk
from tkinter import messagebox
import socket
import time  # 添加用于延时的模块

app_started = False  # 全局变量，标记是否已经启动

def is_port_in_use(port):
    """检查指定端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def install_dependencies(progress_label):
    """检查并安装必要的依赖项"""
    required_packages = [
        "flask",
        "flask-cors",
        "tensorflow",
        "numpy",
        "opencv-python"
    ]
    for i, package in enumerate(required_packages, start=1):
        progress_label.config(text=f"正在安装依赖项：{package} ({i}/{len(required_packages)})")
        progress_label.update_idletasks()
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def run_app(progress_label):
    global app_started
    if app_started:
        messagebox.showinfo("提示", "程序已启动，请勿重复操作！")
        return

    progress_label.config(text="正在检查端口占用...")
    progress_label.update_idletasks()
    if is_port_in_use(5000):  # 检查端口是否被占用
        webbrowser.open("http://127.0.0.1:5000")
        messagebox.showinfo("提示", "Flask 应用已在运行，浏览器已打开 http://127.0.0.1:5000")
        app_started = True  # 标记为已启动，避免重复操作
        return

    app_started = True  # 标记为已启动

    if getattr(sys, 'frozen', False):  # 检查是否为 PyInstaller 打包的可执行文件
        base_path = sys._MEIPASS  # PyInstaller 解压后的临时目录
    else:
        base_path = os.getcwd()

    app_path = os.path.join(base_path, "app.py")
    if not os.path.exists(app_path):
        messagebox.showerror("错误", "找不到 app.py 文件，请确保脚本在正确的目录中运行。")
        app_started = False  # 重置标记
        return

    progress_label.config(text="正在启动 Flask 应用...")
    progress_label.update_idletasks()

    # 启动 app.py 并捕获输出
    process = subprocess.Popen(
        [sys.executable, app_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(3)  # 等待 Flask 应用启动

    if process.poll() is None:  # 检查 Flask 应用是否成功启动
        webbrowser.open("http://127.0.0.1:5000")
        messagebox.showinfo("提示", "程序已启动，浏览器已打开 http://127.0.0.1:5000")
    else:
        stdout, stderr = process.communicate()
        messagebox.showerror("错误", f"程序启动失败：\n{stderr}")
        progress_label.config(text="启动失败！")
        app_started = False  # 重置标记

def start_gui():
    """启动图形界面"""
    def on_start():
        try:
            progress_label.config(text="正在安装依赖项...", font=("Arial", 12, "italic"))
            progress_label.update_idletasks()
            install_dependencies(progress_label)
            run_app(progress_label)
            progress_label.config(text="启动完成！", font=("Arial", 12, "bold"), fg="green")
        except Exception as e:
            messagebox.showerror("错误", f"运行失败：{e}")
            progress_label.config(text="启动失败！", font=("Arial", 12, "bold"), fg="red")

    root = tk.Tk()
    root.title("智能图片比对系统")
    root.geometry("500x300")  # 调整窗口分辨率
    root.resizable(False, False)  # 禁止调整窗口大小

    # 标题标签
    label = tk.Label(
        root,
        text="欢迎使用智能图片比对系统",
        font=("Arial", 18, "bold"),
        fg="#333333"
    )
    label.pack(pady=20)

    # 进度标签
    progress_label = tk.Label(
        root,
        text="",
        font=("Arial", 12, "italic"),
        fg="#007BFF"
    )
    progress_label.pack(pady=10)

    # 按钮容器
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    # 启动按钮
    start_button = tk.Button(
        button_frame,
        text="启动应用",
        font=("Arial", 14, "bold"),
        bg="#4CAF50",
        fg="white",
        width=12,
        height=2,
        command=on_start
    )
    start_button.grid(row=0, column=0, padx=10)

    # 退出按钮
    exit_button = tk.Button(
        button_frame,
        text="退出",
        font=("Arial", 14, "bold"),
        bg="#f44336",
        fg="white",
        width=12,
        height=2,
        command=root.quit
    )
    exit_button.grid(row=0, column=1, padx=10)

    # 底部版权信息
    footer_label = tk.Label(
        root,
        text="© 电子科技大学2023080901025周子谷 课程设计",
        font=("Arial", 10, "italic"),
        fg="#888888"
    )
    footer_label.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    # 检查是否通过 PyInstaller 打包运行
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)  # 切换到 PyInstaller 解压目录
    start_gui()
