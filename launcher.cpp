#include <graphics.h>
#include <iostream>
#include <cstdlib>
#include <thread>
#include <chrono>
#include <string>

// Function declarations
void installDependencies();
void runApp();
void openBrowser();
void closeAll();
void drawUI();
void showMessage(const std::wstring& message);

// Function to display a message on the UI
void showMessage(const std::wstring& message) {
    setfillcolor(WHITE);
    solidrectangle(50, 500, 750, 550); // 清除之前的消息
    outtextxy(60, 510, _T(message.c_str()));
}

void installDependencies() {
    showMessage(L"正在安装依赖...");
    int result = std::system("pip install -r requirements.txt");
    if (result != 0) {
        showMessage(L"依赖安装失败！");
        return;
    }
    showMessage(L"依赖安装成功！");
}

void runApp() {
    showMessage(L"正在启动 Flask 应用...");
    std::thread([]() {
        std::system("start cmd /k python app.py");
        }).detach(); // 在单独的线程中运行
    std::this_thread::sleep_for(std::chrono::seconds(5)); // 模拟延迟
    showMessage(L"Flask 应用已启动！");
}

void openBrowser() {
    showMessage(L"正在打开浏览器...");
    std::system("start http://127.0.0.1:5000");
    showMessage(L"浏览器已打开！");
}

void closeAll() {
    showMessage(L"正在关闭所有进程...");
    std::system("taskkill /IM python.exe /F");
    std::system("taskkill /IM cmd.exe /F");
    showMessage(L"所有进程已关闭！");
}

void drawUI() {
    // 初始化 EasyX 图形窗口
    initgraph(800, 600); // 创建窗口大小为 800x600
    setbkcolor(WHITE);   // 设置背景颜色为白色
    cleardevice();       // 清除背景
    settextcolor(BLACK); // 设置文字颜色为黑色
    settextstyle(20, 0, _T("宋体")); // 设置字体样式和大小

    // 绘制标题
    outtextxy(200, 30, _T("图像相似度比较工具启动器"));

    // 绘制按钮并设置背景颜色
    setfillcolor(LIGHTBLUE); // 设置按钮背景颜色为浅蓝色

    // 安装依赖按钮
    solidrectangle(100, 100, 300, 150); // 填充按钮背景
    rectangle(100, 100, 300, 150);      // 绘制按钮边框
    outtextxy(120, 115, _T("安装依赖"));

    // 启动应用按钮
    setfillcolor(LIGHTGREEN);
    solidrectangle(100, 180, 300, 230);
    rectangle(100, 180, 300, 230);
    outtextxy(120, 195, _T("启动 Flask 应用"));

    // 打开浏览器按钮
    setfillcolor(LIGHTCYAN);
    solidrectangle(100, 260, 300, 310);
    rectangle(100, 260, 300, 310);
    outtextxy(120, 275, _T("打开浏览器"));

    // 关闭进程按钮
    setfillcolor(LIGHTRED);
    solidrectangle(100, 340, 300, 390);
    rectangle(100, 340, 300, 390);
    outtextxy(120, 355, _T("关闭所有进程"));

    // 退出按钮
    setfillcolor(LIGHTGRAY);
    solidrectangle(100, 420, 300, 470);
    rectangle(100, 420, 300, 470);
    outtextxy(120, 435, _T("退出程序"));
}

int main() {
    drawUI();

    while (true) {
        // 检测鼠标点击事件
        ExMessage msg = getmessage(EM_MOUSE);
        if (msg.message == WM_LBUTTONDOWN) {
            int x = msg.x, y = msg.y;

            // 判断点击的区域
            if (x >= 100 && x <= 300 && y >= 100 && y <= 150) {
                installDependencies();
            }
            else if (x >= 100 && x <= 300 && y >= 180 && y <= 230) {
                runApp();
            }
            else if (x >= 100 && x <= 300 && y >= 260 && y <= 310) {
                openBrowser();
            }
            else if (x >= 100 && x <= 300 && y >= 340 && y <= 390) {
                closeAll();
            }
            else if (x >= 100 && x <= 300 && y >= 420 && y <= 470) {
                closegraph(); // 关闭图形窗口
                break;
            }
        }
    }

    return 0;
}
