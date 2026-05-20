# 🚀 Hướng dẫn Deploy - Tetris Game

## Mục lục

- [Chạy trực tiếp (Development)](#1-chạy-trực-tiếp-development)
- [Đóng gói thành EXE (Windows)](#2-đóng-gói-thành-exe-windows)
- [Đóng gói cho macOS](#3-đóng-gói-cho-macos)
- [Đóng gói cho Linux](#4-đóng-gói-cho-linux)
- [Docker](#5-docker)
- [Phân phối](#6-phân-phối)

---

## 1. Chạy trực tiếp (Development)

### Yêu cầu
- Python 3.8+
- pip (Python package manager)

### Các bước

```bash
# 1. Mở terminal/command prompt tại thư mục project
cd path/to/testgame

# 2. (Khuyến nghị) Tạo virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Chạy game
python main.py
```

### Xử lý lỗi thường gặp

| Lỗi | Giải pháp |
|-----|-----------|
| `python` không nhận | Thử `python3` hoặc `py` |
| `pip` không nhận | Thử `pip3` hoặc `python -m pip` |
| `pygame` lỗi display | Cài driver đồ họa mới nhất |
| `numpy` lỗi import | `pip install --upgrade numpy` |

---

## 2. Đóng gói thành EXE (Windows)

### Sử dụng PyInstaller

```bash
# Cài PyInstaller
pip install pyinstaller

# Đóng gói thành 1 file EXE
pyinstaller --onefile --windowed --name "Tetris" main.py

# Hoặc đóng gói thành thư mục (khởi động nhanh hơn)
pyinstaller --onedir --windowed --name "Tetris" main.py
```

### Tùy chọn nâng cao

```bash
# Với icon tùy chỉnh
pyinstaller --onefile --windowed --name "Tetris" --icon=icon.ico main.py

# Spec file cho cấu hình chi tiết
pyinstaller Tetris.spec
```

### File spec mẫu (Tetris.spec)

```python
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['numpy', 'pygame'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Tetris',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

### Kết quả
- File EXE nằm trong thư mục `dist/`
- Có thể chạy trực tiếp mà không cần cài Python
- Kích thước khoảng 30-50MB (bao gồm Python runtime)

---

## 3. Đóng gói cho macOS

### Sử dụng PyInstaller

```bash
# Cài PyInstaller
pip install pyinstaller

# Tạo .app bundle
pyinstaller --onefile --windowed --name "Tetris" main.py

# Với icon
pyinstaller --onefile --windowed --name "Tetris" --icon=icon.icns main.py
```

### Sử dụng py2app (macOS native)

```bash
# Cài py2app
pip install py2app

# Tạo setup.py
```

File `setup_mac.py`:
```python
from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame', 'numpy'],
    'iconfile': 'icon.icns',  # Optional
}

setup(
    app=APP,
    name='Tetris',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

```bash
# Build
python setup_mac.py py2app
```

---

## 4. Đóng gói cho Linux

### Sử dụng PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile --name "tetris" main.py
```

### Tạo AppImage

```bash
# Cài appimage-builder
pip install appimage-builder

# Tạo AppImageBuilder.yml (xem mẫu bên dưới)
appimage-builder --recipe AppImageBuilder.yml
```

### Tạo .deb package

```bash
# Cấu trúc thư mục
mkdir -p tetris-game/DEBIAN
mkdir -p tetris-game/usr/local/bin
mkdir -p tetris-game/usr/share/applications

# Copy binary
cp dist/tetris tetris-game/usr/local/bin/

# Tạo control file
cat > tetris-game/DEBIAN/control << EOF
Package: tetris-game
Version: 1.0.0
Section: games
Priority: optional
Architecture: amd64
Depends: python3
Maintainer: Developer
Description: Classic Tetris puzzle game
EOF

# Build .deb
dpkg-deb --build tetris-game
```

---

## 5. Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Install system dependencies for pygame
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# For running with display (requires X11 forwarding)
ENV DISPLAY=:0
CMD ["python", "main.py"]
```

### Chạy với Docker

```bash
# Build image
docker build -t tetris-game .

# Chạy (Linux với X11)
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix tetris-game

# Chạy (Windows với VcXsrv)
# 1. Cài và chạy VcXsrv
# 2. docker run -e DISPLAY=host.docker.internal:0 tetris-game
```

---

## 6. Phân phối

### Tạo Release trên GitHub

```bash
# Tag version
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Upload EXE/binary lên GitHub Releases
```

### Cấu trúc release khuyến nghị

```
Tetris-v1.0.0-Windows.zip
├── Tetris.exe
└── README.txt

Tetris-v1.0.0-macOS.zip
├── Tetris.app
└── README.txt

Tetris-v1.0.0-Linux.tar.gz
├── tetris
└── README.txt
```

### Checklist trước khi release

- [ ] Test trên Windows 10/11
- [ ] Test trên macOS (nếu có)
- [ ] Test trên Linux (nếu có)
- [ ] High score hoạt động đúng
- [ ] Âm thanh hoạt động
- [ ] Không có crash/bug nghiêm trọng
- [ ] README cập nhật
- [ ] Version number đúng

---

## 7. CI/CD với GitHub Actions (Tùy chọn)

File `.github/workflows/build.yml`:

```yaml
name: Build Game

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pyinstaller
      - run: pyinstaller --onefile --windowed --name "Tetris" main.py
      - uses: actions/upload-artifact@v4
        with:
          name: Tetris-Windows
          path: dist/Tetris.exe

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          sudo apt-get update
          sudo apt-get install -y libsdl2-dev libsdl2-mixer-dev
      - run: pip install -r requirements.txt pyinstaller
      - run: pyinstaller --onefile --name "tetris" main.py
      - uses: actions/upload-artifact@v4
        with:
          name: Tetris-Linux
          path: dist/tetris
```

---

## Tóm tắt nhanh

| Mục đích | Lệnh |
|----------|-------|
| Chạy dev | `python main.py` |
| Build EXE | `pyinstaller --onefile --windowed --name "Tetris" main.py` |
| Build macOS | `pyinstaller --onefile --windowed --name "Tetris" main.py` |
| Build Linux | `pyinstaller --onefile --name "tetris" main.py` |

**Lưu ý**: Game tạo âm thanh bằng code nên KHÔNG cần đính kèm file âm thanh khi deploy. Chỉ cần code Python là đủ.
