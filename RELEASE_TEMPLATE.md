# Release v1.0 - PDF 转图片工具

## 📦 下载

### Windows 用户（推荐）

下载下方的 `PDF转图片工具_v1.0.exe` 文件，双击即可运行，无需安装 Python。

**文件列表：**
- `PDF转图片工具_v1.0.exe` - Windows 可执行文件（约 XX MB）
- `Source code (zip)` - 完整源代码压缩包
- `Source code (tar.gz)` - 完整源代码压缩包

### 从源码运行

```bash
git clone https://github.com/zhifouli/pdf2img.git
cd pdf2img
pip install -r requirements.txt
python pdf2img_converter.py
```

## ✨ 功能特点

- 📁 批量转换多个 PDF 文件
- 🖼️ 支持 PNG/JPG 格式输出
- ⚙️ 可调节质量和分辨率
- 🚀 多进程加速转换
- ⏸️ 支持暂停/继续/停止
- 📊 实时进度显示

## 🆕 本版本更新

- ✨ 首次发布
- ✅ 完整的 GUI 界面
- ✅ 支持批量转换
- ✅ 多进程优化
- ✅ 实时进度显示

## 📋 系统要求

- Windows 7/8/10/11 (64-bit)
- 无需安装 Python（exe 版本）

## ⚙️ 使用说明

1. 下载并运行 `PDF转图片工具_v1.0.exe`
2. 点击"添加 PDF 文件"选择要转换的文件
3. 选择输出格式（PNG/JPG）和质量设置
4. 点击"开始转换"，选择输出目录
5. 等待转换完成

详细说明请查看 [README.md](https://github.com/zhifouli/pdf2img/blob/master/README.md)

## 📄 许可证

本项目采用 **AGPL-3.0** 许可证。

⚠️ **重要提示：** 本软件使用 PyMuPDF 库（AGPL-3.0 许可）。

- ✅ 个人使用：无限制
- ✅ 开源项目：需保持 AGPL-3.0 许可
- ⚠️ 商业闭源：需购买 PyMuPDF 商业许可

详情请阅读 [COMPLIANCE.md](https://github.com/zhifouli/pdf2img/blob/master/COMPLIANCE.md)

## 🐛 已知问题

无

## 📧 反馈

如有问题或建议，请提交 [Issue](https://github.com/zhifouli/pdf2img/issues)

---

**SHA256 校验和：**
```
PDF转图片工具_v1.0.exe: [打包后在此填写 SHA256]
```

**如何验证（可选）：**
```powershell
# Windows PowerShell
Get-FileHash .\PDF转图片工具_v1.0.exe -Algorithm SHA256
```

---

© 2025 zhifouli | Licensed under AGPL-3.0
