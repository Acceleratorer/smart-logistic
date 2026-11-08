# Mô hình kho 3D hợp nhất với 5 robot AGV

## Mục tiêu

Mô hình đích kết hợp hai lớp: (1) robot nhận lệnh lấy hàng theo dữ liệu FEFO và (2) năm robot cùng chạy trong một kho có kệ, cửa nhập/xuất, trạm sạc và các vùng giao thông hẹp. Mọi lệnh đi qua cùng một bộ điều phối để tránh trùng hàng, tránh vật cản, giảm tốc trước xung đột và ngăn hai robot đi vào cùng vùng an toàn.

## Pipeline vận hành

```text
Kaggle inventory
  -> chuẩn hóa SKU / ngày hết hạn / số lượng
  -> chọn ngày vận hành và phân nhóm FEFO
  -> ánh xạ SKU vào ô kệ 3D
  -> WMS tạo lệnh (robot, SKU, điểm giao)
  -> giữ chỗ slot và xếp hàng đợi theo robot
  -> A* tìm đường trên lưới kho
  -> PICK -> DROP -> (đơn tiếp theo | RETURN)
  -> DOCK_TURN -> CHARGE -> IDLE
  -> task history / speed CSV / mini-map
```

Lệnh từ tablet, tìm SKU, ưu tiên FEFO, click mini-map và nút điều phối đều đi vào `f5Assign`/hàng đợi đội; không dùng một đường điều khiển riêng cho robot đơn lẻ trong bản đích.

## Không gian và A*

- Mặt bằng: 28 × 28 m.
- Lưới: 0,5 m/ô, 56 × 56 ô, bốn hướng trái/phải/trước/sau.
- Kệ và vật cản tĩnh là ô không đi được; điểm bắt đầu/đích được kéo về ô đi được gần nhất.
- Heuristic: `h(n) = |x - x_goal| + |z - z_goal|`.
- Chi phí cơ sở mỗi bước là 1. A* dùng `f(n)=g(n)+h(n)` và binary min-heap.
- Khi lập đường cho đội, robot khác là chi phí mềm: phạt lớn trong vùng dưới `SAFE_GAP + 0,12`, phạt vừa ở vùng giữa và phạt nhỏ ở vùng xa hơn. Vị trí dự đoán của robot đang chạy được cộng thêm phạt.
- Dải phía sau trạm sạc bị loại khỏi giao thông xuyên kho. Tuyến RETURN thêm phạt gần cửa nhập/xuất và đi vào ô sạc theo đường tiếp cận riêng.

Chi phí mềm giúp robot ưu tiên lối ít ùn tắc mà không biến robot đang đỗ thành vật cản vĩnh viễn. A* chỉ tạo ứng viên; bộ điều khiển thời gian thực vẫn phải kiểm tra CPA và bước quét trước khi di chuyển.

## Bộ điều khiển đa robot

| Thành phần | Giá trị đích | Vai trò |
|---|---:|---|
| `ROBOT_COUNT` | 5 | Số robot và số ô sạc duy nhất |
| `SAFE_GAP` | 0,98 m | Khoảng cách tối thiểu giữa hai robot |
| `MAX_SPEED` | 2,3 m/s | Giới hạn tốc độ |
| `ACCEL` / `BRAKE` | 1,15 / 2,7 m/s² | Tăng tốc và phanh có giới hạn |
| `CONFLICT_HORIZON` | 2,4 s | Cửa sổ dự đoán CPA |
| `REPLAN_INTERVAL` | 2,6 s | Nhịp thử lập đường lại |
| `BLOCKED_SCAN_AFTER` | 14 s | Ngưỡng bế tắc mới xét quét 360° |
| `SCAN_COOLDOWN` | 25 s | Khoảng nghỉ giữa hai lần quét |
| ưu tiên cập nhật | 4 s | Xoay robot được cập nhật đầu tiên |

Mỗi frame chạy theo thứ tự:

1. Lấy waypoint kế tiếp từ route A*.
2. Tính hướng, khoảng cách, góc cua và giới hạn tốc độ phía trước/bên cạnh.
3. Tính CPA với các robot đang chạy trong 2,4 giây.
4. Giảm tốc theo khoảng cách phanh và trước/sau góc cua.
5. Kiểm tra `f5AllowedMove` trên toàn đoạn quét của frame; nếu không đủ `SAFE_GAP`, hủy bước.
6. Nếu bị chặn đủ lâu, thử A* lại, sau đó thử cooperative detour, cuối cùng mới scan 360° có cooldown.
7. Ghi nhận conflict/blocked vào task history và cập nhật mini-map/HUD.

## Trạng thái robot

```text
IDLE
  -> PICK        đi tới ô hàng
  -> DROP        chở hàng tới cửa/ô giao
  -> DONE        ghi metrics, lấy đơn kế tiếp nếu còn
  -> RETURN      về đúng ô sạc của robot
  -> DOCK_TURN   quay 180° sau khi đã vào ô
  -> CHARGE      sạc 10 giây
  -> IDLE
```

`WAIT_NEXT` dùng khi robot có hàng đợi nhưng lối đến đơn kế tiếp chưa an toàn. `SCAN_360` chỉ là trạng thái chẩn đoán sau bế tắc kéo dài; nó không thay thế kiểm tra khoảng cách.

## WMS và FEFO

Dữ liệu hàng được tải từ Kaggle, chuẩn hóa theo SKU/Product ID/tên/nhóm/số lượng/ngày hết hạn, sau đó chọn ngày vận hành dựa trên các hạn dùng thật. Các ô kệ 3D là bố trí mô phỏng và mang mã location. Tablet hỗ trợ:

- tìm SKU, Product ID, tên hoặc location;
- chọn hàng gần hết hạn nhất;
- tạo hàng đợi theo robot và điểm giao;
- inspect ô kệ, relocate sang ô trống;
- xem pin, bước, thời gian, trạng thái, task history;
- tải lịch sử vận tốc đội dưới dạng CSV.

Một `slotId` chỉ được giữ chỗ một lần trong các tập active, queued hoặc pending; robot chỉ RETURN sau khi xử lý hết hàng đợi.

## Tiêu chí nghiệm thu

- Notebook tạo đúng 5 robot và 5 ô sạc, không còn robot thứ sáu trong UI.
- Route preview dùng A*; bộ điều phối đội dùng A* có phạt tránh robot.
- Không có bước di chuyển vượt qua kệ hoặc đi qua robot khác trong `SAFE_GAP`.
- Hai robot gặp nhau phải giảm tốc, chờ hoặc replan; conflict được ghi nhận.
- Bế tắc có detour có giới hạn và scan 360° có cooldown.
- Chu kỳ PICK → DROP → RETURN → CHARGE chạy được cho từng robot.
- FEFO, inspect, relocate, task history, speed CSV và mini-map vẫn hoạt động.
- Ô kiểm tra cuối notebook phải pass trước khi dùng trong Kaggle/Colab.

## Giới hạn hiện tại

Đây là mô phỏng 3D chạy trong trình duyệt, không phải bộ điều khiển phần cứng. Đoạn quét va chạm kiểm tra khoảng cách trên bước thời gian mô phỏng; nó không chứng minh an toàn liên tục theo mô hình hình học thân robot. Reservation theo thời gian từ `Draft_simul.ipynb` được giữ như hướng benchmark, còn live controller dùng A* phản ứng + CPA + swept-gap để tránh duy trì hai planner cạnh tranh.
