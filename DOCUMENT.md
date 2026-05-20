# 📖 Tài liệu kỹ thuật - Tetris Game

## 1. Tổng quan kiến trúc

Game Tetris được xây dựng theo mô hình **modular**, chia thành các module độc lập với trách nhiệm rõ ràng:

```
main.py (Entry Point)
    └── Game (game.py) - Điều phối chính
            ├── Board (board.py) - Quản lý lưới
            ├── Piece (piece.py) - Logic khối
            ├── Renderer (renderer.py) - Vẽ giao diện
            └── SoundManager (sound_manager.py) - Âm thanh
```

## 2. Chi tiết các Module

### 2.1 constants.py - Hằng số và cấu hình

Chứa tất cả các hằng số cấu hình game:

- **Kích thước màn hình**: 500x620 pixels
- **Lưới game**: 10 cột x 20 hàng, mỗi ô 30x30 pixels
- **Màu sắc**: Định nghĩa RGB cho tất cả màu sử dụng
- **Hình dạng Tetromino**: Ma trận 2D cho 7 loại khối
- **Tốc độ**: Tốc độ ban đầu, tăng tốc, tốc độ tối thiểu
- **Điểm số**: Điểm cho từng loại xóa hàng
- **Font**: Kích thước font cho các loại text

### 2.2 piece.py - Class Piece

Quản lý logic của một khối Tetromino:

| Method | Mô tả |
|--------|--------|
| `__init__(shape_index)` | Tạo khối mới, random nếu không chỉ định |
| `rotate_clockwise()` | Xoay 90° theo chiều kim đồng hồ |
| `rotate_counterclockwise()` | Xoay 90° ngược chiều kim đồng hồ |
| `get_cells()` | Trả về danh sách tọa độ các ô chiếm |
| `clone()` | Tạo bản sao của khối |

**Thuật toán xoay**: Transpose ma trận + đảo ngược hàng (cho clockwise).

### 2.3 board.py - Class Board

Quản lý lưới game 10x20:

| Method | Mô tả |
|--------|--------|
| `is_valid_position(piece)` | Kiểm tra vị trí hợp lệ |
| `lock_piece(piece)` | Khóa khối vào lưới |
| `clear_lines()` | Xóa hàng đầy, trả về số hàng xóa |
| `is_game_over(piece)` | Kiểm tra game over |
| `get_ghost_position(piece)` | Tính vị trí ghost piece |
| `reset()` | Reset lưới về trống |

**Thuật toán xóa hàng**: Lọc các hàng chưa đầy, thêm hàng trống ở trên.

### 2.4 game.py - Class Game

Module điều phối chính, quản lý game loop và state:

**Game States:**
- `start` - Màn hình bắt đầu
- `playing` - Đang chơi
- `paused` - Tạm dừng
- `game_over` - Thua
- `win` - Thắng (đạt Level 15)

**Game Loop:**
```
while running:
    1. Xử lý events (input)
    2. Update logic (drop timer, collision)
    3. Render (vẽ frame)
    4. Clock tick (60 FPS)
```

**Hệ thống Wall Kick**: Khi xoay khối, nếu vị trí mới không hợp lệ, thử dịch chuyển ±1, ±2 ô để tìm vị trí hợp lệ.

### 2.5 renderer.py - Class Renderer

Xử lý toàn bộ việc vẽ giao diện:

| Method | Mô tả |
|--------|--------|
| `draw_block()` | Vẽ 1 ô với hiệu ứng 3D |
| `draw_grid()` | Vẽ lưới và các khối đã khóa |
| `draw_piece()` | Vẽ khối đang rơi |
| `draw_ghost()` | Vẽ ghost piece (bán trong suốt) |
| `draw_next_piece()` | Vẽ preview khối tiếp theo |
| `draw_info_panel()` | Vẽ bảng thông tin |
| `draw_game_over()` | Vẽ overlay game over |
| `draw_pause()` | Vẽ overlay pause |
| `draw_start_screen()` | Vẽ màn hình bắt đầu |
| `draw_win_screen()` | Vẽ màn hình chiến thắng |

**Hiệu ứng 3D**: Mỗi block có highlight (sáng hơn) ở cạnh trên-trái và shadow (tối hơn) ở cạnh dưới-phải.

### 2.6 sound_manager.py - Class SoundManager

Tạo và phát âm thanh hoàn toàn bằng code (không cần file âm thanh):

| Sound | Mô tả | Kỹ thuật |
|-------|--------|----------|
| `move` | Di chuyển khối | Sine wave 200Hz, 50ms |
| `rotate` | Xoay khối | Sine wave 400Hz, 80ms |
| `drop` | Khối chạm đáy | Square wave 100Hz, 150ms |
| `line_clear` | Xóa hàng | Melody ascending C-E-G-C |
| `tetris` | Xóa 4 hàng | Melody triumphant 8 notes |
| `level_up` | Lên level | Melody 6 notes ascending |
| `game_over` | Thua | Melody descending 8 notes |
| `win` | Thắng | Melody celebratory |
| `hard_drop` | Hard drop | Square wave 80Hz, 200ms |
| `pause` | Pause/Resume | Sine wave 300Hz, 200ms |

**Kỹ thuật tạo âm thanh**: Sử dụng numpy để tạo waveform, áp dụng envelope (fade in/out), chuyển đổi sang 16-bit stereo PCM.

## 3. Luồng xử lý chính

### 3.1 Khối rơi xuống
```
Drop Timer tích lũy → Đủ thời gian → Move piece down
    → Hợp lệ: Tiếp tục
    → Không hợp lệ: Lock piece → Clear lines → Spawn new piece
```

### 3.2 Xóa hàng
```
Lock piece → Kiểm tra từng hàng
    → Hàng đầy: Xóa, tăng điểm
    → Cập nhật level nếu đủ lines
    → Kiểm tra win condition
```

### 3.3 Game Over
```
Spawn new piece → Kiểm tra valid position
    → Không hợp lệ (chồng lên khối cũ): GAME OVER
```

## 4. Hệ thống điểm chi tiết

```
Base Score = {1 line: 100, 2 lines: 300, 3 lines: 500, 4 lines: 800}
Final Score = Base Score × Current Level
Soft Drop Bonus = 1 point per cell
Hard Drop Bonus = 2 points per cell
```

## 5. Hệ thống tốc độ

```
Speed (ms) = max(100, 500 - (level - 1) × 25)

Level 1:  500ms
Level 5:  400ms
Level 10: 275ms
Level 15: 150ms (win condition)
```

## 6. Lưu trữ dữ liệu

High score được lưu trong file `highscore.json`:
```json
{
    "high_score": 12500
}
```

## 7. Xử lý lỗi

- File high score bị hỏng: Reset về 0
- Pygame init thất bại: Exception tự nhiên
- Âm thanh không khả dụng: Game vẫn chạy bình thường

## 8. Performance

- **FPS**: Cố định 60 FPS
- **Memory**: Tối thiểu, chỉ lưu grid 10x20 và 2 pieces
- **CPU**: Rất nhẹ, chủ yếu là render 2D đơn giản
- **Âm thanh**: Tạo 1 lần khi khởi động, cache trong memory

## 9. Mở rộng

Có thể mở rộng game với:
- Hold piece (giữ khối)
- T-Spin detection
- Combo system
- Multiplayer
- Leaderboard online
- Themes/skins
- Background music
