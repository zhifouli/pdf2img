@echo off
chcp 65001 >nul
echo ========================================
echo PDF 转图片工具 V1.0 - 虚拟环境打包
echo 使用预编译包，无需 Visual Studio
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.7 或更高版本
    pause
    exit /b 1
)

echo [1/7] 创建虚拟环境...
if exist venv_build (
    echo 检测到已存在的虚拟环境，正在删除...
    rmdir /s /q venv_build
)
python -m venv venv_build
if errorlevel 1 (
    echo [错误] 虚拟环境创建失败
    pause
    exit /b 1
)
echo ✓ 虚拟环境创建成功

echo.
echo [2/7] 激活虚拟环境...
call venv_build\Scripts\activate.bat
if errorlevel 1 (
    echo [错误] 虚拟环境激活失败
    pause
    exit /b 1
)
echo ✓ 虚拟环境已激活

echo.
echo [3/7] 升级 pip...
python -m pip install --upgrade pip --quiet
echo ✓ pip 升级完成

echo.
echo [4/7] 安装打包依赖（使用预编译包）...
echo 提示: 使用 --only-binary 确保不从源码编译
echo.
echo 正在安装 PyMuPDF...
pip install "PyMuPDF>=1.24.11" --only-binary :all:
if errorlevel 1 (
    echo [错误] PyMuPDF 安装失败
    call deactivate
    pause
    exit /b 1
)
echo ✓ PyMuPDF 安装成功

echo.
echo 正在安装 PyInstaller...
pip install "pyinstaller>=6.3.0" --quiet
if errorlevel 1 (
    echo [错误] PyInstaller 安装失败
    call deactivate
    pause
    exit /b 1
)
echo ✓ PyInstaller 安装成功

echo.
echo [6/7] 清理旧的打包文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo ✓ 清理完成

echo.
echo [7/7] 开始打包（这可能需要几分钟）...
echo.
pyinstaller pdf2img_optimized.spec --clean
if errorlevel 1 (
    echo.
    echo [错误] 打包失败，请查看上面的错误信息
    call deactivate
    pause
    exit /b 1
)

echo.
echo ========================================
call deactivate
echo ✓ 虚拟环境已退出

REM 显示文件大小
for %%A in ("dist\PDF转图片工具_V1.0.exe") do (
    set size=%%~zA
    set /a sizeMB=%%~zA/1048576
)

echo.
echo ========================================
echo ✓✓✓ 打包成功！✓✓✓
echo ========================================
echo.
echo 可执行文件位置:
echo   %CD%\dist\PDF转图片工具_V1.0.exe
echo.
echo 文件大小: %sizeMB% MB
echo.
echo 优化说明:
echo - 使用虚拟环境确保环境纯净
echo - 使用预编译包，无需 Visual Studio
echo - 仅安装必需的依赖包
echo - 启用了代码压缩和优化
echo.

REM 询问是否删除虚拟环境
set /p clean="是否删除虚拟环境文件夹？(Y/N): "
if /i "%clean%"=="Y" (
    echo 正在删除虚拟环境...
    rmdir /s /q venv_build
    echo ✓ 虚拟环境已删除
)

echo.
REM 询问是否打开文件夹
set /p open="是否打开 dist 文件夹？(Y/N): "
if /i "%open%"=="Y" (
    explorer dist
)

pause
