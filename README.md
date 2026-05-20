# 🎮 Tetris - Xếp Hình (Vibe Coding Using Claude Sonnet 4.6) =)))))

Game xếp hình Tetris cổ điển được xây dựng bằng Python và Pygame.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Cách chơi](#cách-chơi)
- [Điều khiển](#điều-khiển)
- [Hệ thống điểm](#hệ-thống-điểm)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Deploy](#deploy)
- [License](#license)

## 🎯 Giới thiệu

Đây là phiên bản game Tetris (Xếp Hình) cổ điển được phát triển bằng Python sử dụng thư viện Pygame. Game có đầy đủ tính năng bao gồm:

- Gameplay hoàn chỉnh với 7 loại khối Tetromino
- Hệ thống âm thanh được tạo tự động (không cần file âm thanh bên ngoài)
- Điều kiện thắng và thua rõ ràng
- Lưu điểm cao (High Score)
- Ghost piece (hiển thị vị trí rơi)
- Tăng tốc độ theo level

## ✨ Tính năng

| Tính năng | Mô tả |
|-----------|--------|
| 🧱 7 Tetrominos | I, J, L, O, S, T, Z với màu sắc riêng biệt |
| 🔊 Âm thanh | Hiệu ứng âm thanh cho mọi hành động |
| 👻 Ghost Piece | Hiển thị vị trí khối sẽ rơi xuống |
| 📊 Bảng điểm | Score, Level, Lines, High Score |
| 🏆 Điều kiện thắng | Đạt Level 15 để chiến thắng |
| 💀 Điều kiện thua | Khối chạm đỉnh bảng |
| ⏸️ Tạm dừng | Pause/Resume game |
| 💾 Lưu điểm cao | Tự động lưu high score |
| 🎨 Giao diện đẹp | Hiệu ứng 3D cho các khối |

## 💻 Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **Hệ điều hành**: Windows, macOS, Linux
- **RAM**: 256MB trở lên
- **Thư viện**: pygame, numpy

## 🚀 Cài đặt

### Bước 1: Cài đặt Python

Tải Python từ [python.org](https://www.python.org/downloads/) và cài đặt. Đảm bảo tick chọn "Add Python to PATH" khi cài đặt.

### Bước 2: Clone hoặc tải project

```bash
# Clone từ repository (nếu có)
git clone <repository-url>
cd testgame

# Hoặc giải nén file zip vào thư mục
```

### Bước 3: Tạo virtual environment (khuyến nghị)

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (macOS/Linux)
source venv/bin/activate
```

### Bước 4: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 5: Chạy game

```bash
python main.py
```

## 🎮 Cách chơi

### Mục tiêu
Xếp các khối Tetromino rơi xuống sao cho lấp đầy hàng ngang. Khi một hàng được lấp đầy, nó sẽ bị xóa và bạn nhận được điểm.

### Điều kiện thắng
Đạt **Level 15** để chiến thắng game.

### Điều kiện thua
Game kết thúc khi các khối xếp chồng lên nhau chạm đến đỉnh bảng và không còn chỗ cho khối mới.

### Mẹo chơi
1. Luôn giữ bảng phẳng, tránh tạo lỗ trống
2. Cố gắng xóa 4 hàng cùng lúc (Tetris) để được nhiều điểm nhất
3. Sử dụng Ghost Piece để biết khối sẽ rơi ở đâu
4. Hard Drop (Space) giúp đặt khối nhanh hơn
5. Xem trước khối tiếp theo (Next) để lên kế hoạch

## ⌨️ Điều khiển

| Phím | Hành động |
|------|-----------|
| ← (Mũi tên trái) | Di chuyển khối sang trái |
| → (Mũi tên phải) | Di chuyển khối sang phải |
| ↑ (Mũi tên lên) | Xoay khối 90° theo chiều kim đồng hồ |
| ↓ (Mũi tên xuống) | Soft Drop (rơi nhanh hơn) |
| Space (Cách) | Hard Drop (rơi xuống đáy ngay lập tức) |
| P | Tạm dừng / Tiếp tục |
| M | Bật / Tắt âm thanh |
| R | Chơi lại từ đầu |
| ESC | Thoát game |
| Enter | Bắt đầu game (ở màn hình chính) |

## 📊 Hệ thống điểm

### Điểm xóa hàng (nhân với level hiện tại)

| Số hàng xóa | Điểm cơ bản | Ví dụ Level 5 |
|--------------|-------------|----------------|
| 1 hàng (Single) | 100 | 500 |
| 2 hàng (Double) | 300 | 1,500 |
| 3 hàng (Triple) | 500 | 2,500 |
| 4 hàng (Tetris) | 800 | 4,000 |

### Điểm thưởng
- **Soft Drop**: +1 điểm mỗi ô rơi
- **Hard Drop**: +2 điểm mỗi ô rơi

### Level
- Mỗi 10 hàng xóa = tăng 1 level
- Tốc độ rơi tăng theo level
- Đạt Level 15 = Chiến thắng!

## 📁 Cấu trúc dự án

```
testgame/
├── main.py              # Entry point - chạy file này để bắt đầu game
├── requirements.txt     # Danh sách thư viện cần cài
├── highscore.json       # File lưu điểm cao (tự động tạo)
├── README.md            # File hướng dẫn này
├── DOCUMENT.md          # Tài liệu kỹ thuật chi tiết
├── DEPLOY.md            # Hướng dẫn deploy/đóng gói
└── tetris/              # Package chính
    ├── __init__.py      # Package init
    ├── constants.py     # Hằng số và cấu hình game
    ├── piece.py         # Logic khối Tetromino
    ├── board.py         # Logic bảng game
    ├── game.py          # Logic game chính và game loop
    ├── renderer.py      # Module vẽ/render giao diện
    └── sound_manager.py # Quản lý âm thanh
```

## 🖼️ Screenshots

```
┌──────────────────────────────────────────────┐
│  ┌────────────────────┐  NEXT               │
│  │                    │  ┌──────┐            │
│  │    ██              │  │ ████ │            │
│  │    ████            │  └──────┘            │
│  │                    │                      │
│  │                    │  SCORE               │
│  │                    │  1500                │
│  │                    │                      │
│  │                    │  HIGH SCORE          │
│  │                    │  5000                │
│  │                    │                      │
│  │        ░░          │  LEVEL               │
│  │        ░░░░        │  3                   │
│  │                    │                      │
│  │  ████████████████  │  LINES               │
│  │  ██████  ████████  │  25                  │
│  │  ████████████████  │                      │
│  └────────────────────┘  CONTROLS:           │
│                          ← → : Move          │
│                          ↑ : Rotate          │
│                          Space : Hard Drop   │
└──────────────────────────────────────────────┘
```

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 👤 Tác giả

Game được phát triển bằng Python + Pygame.

---

**Chúc bạn chơi vui vẻ! 🎮**
