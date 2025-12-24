# PDF 转图片工具

一个简单易用的 PDF 批量转图片工具，支持将 PDF 文件转换为 PNG 或 JPG 格式的图片。
![](https://upyuncdn.zhifouli.top/weblog/uploads/2025/12/974968320.png)

## ✨ 功能特点

- 📁 **批量转换** - 支持一次选择多个 PDF 文件进行批量转换
- 🖼️ **多格式支持** - 支持输出 PNG 和 JPG 两种图片格式
- ⚙️ **自定义设置** - 可调节图片质量（50-100%）和分辨率（72-300 DPI）
- ⏸️ **暂停/继续** - 转换过程中可以暂停和继续
- 🛑 **随时停止** - 可以随时停止转换任务
- 📊 **实时进度** - 显示整体进度和当前文件的详细转换进度
- 🎨 **友好界面** - 简洁直观的图形用户界面

## 📦 依赖库

- Python 3.7+
- PyMuPDF >= 1.24.11

## 🔧 安装

1. 克隆或下载本项目
2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 📥 下载

### 预编译版本（推荐）

前往 [Releases](https://github.com/zhifouli/pdf2img/releases) 页面下载最新版本的 exe 文件。

下载后直接双击运行即可，无需安装 Python 环境。

### 从源码运行

如果您想从源码运行或进行二次开发：

```bash
# 克隆仓库
git clone https://github.com/zhifouli/pdf2img.git
cd pdf2img

# 安装依赖
pip install -r requirements.txt

# 运行
python pdf2img_converter.py
```

## 🚀 使用方法

### 操作步骤

1. 点击"添加 PDF 文件"选择要转换的 PDF 文件
2. 设置输出格式（PNG/JPG）
3. 调整图片质量和分辨率（DPI）
4. 点击"开始转换"并选择输出目录
5. 等待转换完成

转换后的图片会保存在输出目录中，每个 PDF 文件会创建一个单独的文件夹。

## ⚙️ 参数说明

- **输出格式**
  - PNG: 无损格式，文件较大，适合需要高质量的场景
  - JPG: 有损压缩，文件较小，适合一般使用

- **图片质量** (50-100%)
  - 仅对 JPG 格式有效
  - 推荐值：95%

- **分辨率 DPI** (72/96/150/200/300)
  - 72: 屏幕显示质量
  - 150: 推荐值，平衡质量和文件大小
  - 300: 打印质量，文件较大

## 📄 许可证

本项目采用 **GNU Affero General Public License v3.0 (AGPL-3.0)** 许可证。

### ⚠️ 重要许可说明

本软件使用 **PyMuPDF** 库，该库基于 MuPDF，采用 **AGPL-3.0 和商业双重许可**。

#### AGPL-3.0 许可要求

如果您使用 AGPL-3.0 许可，您需要：

1. ✅ 保持源代码开放
2. ✅ 使用相同的 AGPL-3.0 许可证
3. ✅ 如果通过网络提供服务，必须向用户提供源代码
4. ✅ 标注您所做的任何修改

#### 需要商业许可的场景

如果您的使用场景包括以下情况，您需要联系 Artifex 获取商业许可：

- ❌ 集成到闭源商业软件中
- ❌ 修改后不愿公开源代码
- ❌ 提供 SaaS 服务但不开源
- ❌ 其他不符合 AGPL-3.0 的使用场景

**商业许可咨询:**
- 网址: https://artifex.com/
- 邮箱: sales@artifex.com

### 许可证文件

- `LICENSE` - AGPL-3.0 许可证文本
- `NOTICE` - 第三方软件声明
- `COMPLIANCE.md` - 合规使用指南

**请务必仔细阅读 AGPL-3.0 许可证全文，确保您的使用方式符合许可要求。**

完整许可证: https://www.gnu.org/licenses/agpl-3.0.html

## 👨‍💻 作者

**zhifouli**

- GitHub: https://github.com/zhifouli?tab=repositories

## 🔨 从源码构建 exe

如果您想自己构建 exe 文件：

```bash
# 安装 PyInstaller
pip install pyinstaller

# 运行打包脚本
虚拟环境打包_简化版.bat
```

或手动打包：

```bash
pyinstaller pdf2img_optimized.spec
```

生成的 exe 文件位于 `dist` 目录。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

由于本项目采用 AGPL-3.0 许可证，您的贡献也将自动采用相同许可证。

### 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📧 联系方式

如有问题或建议，请通过 GitHub Issues 联系。

## ⚖️ 免责声明

本软件按"原样"提供，不提供任何形式的明示或暗示担保。使用本软件产生的任何后果由使用者自行承担。

使用者有责任确保自己的使用方式符合 PyMuPDF/MuPDF 的许可证要求。如果您不确定是否符合 AGPL-3.0 要求，请咨询法律专业人士或联系 Artifex 获取商业许可。

---

© 2025 zhifouli | Licensed under AGPL-3.0

