# Bao_cao_Chuong_5_AGV_V21

> Chuyển tự động từ `Bao_cao_Chuong_5_AGV_V21.docx`. Nội dung được giữ theo thứ tự đoạn và bảng; công thức/hình ảnh được lưu riêng khi DOCX có nhúng.
## BÁO CÁO PHÂN TÍCH KẾT QUẢ KIỂM THỬ

# CHƯƠNG 5

THÍ NGHIỆM VÀ ĐÁNH GIÁ MÔ HÌNH

Đề tài: Tối ưu hóa tuyến đường và giải quyết xung đột trong vận hành robot tự hành (AGV) tại nhà kho thông minh.

### Bảng 1

| THÔNG TIN | NỘI DUNG |
|---|---|
| Mô hình | Kho FEFO 3D – 6 robot AGV, phiên bản V21 |
| Bộ thí nghiệm | TN01–TN07; tổng hợp theo Excel kết quả do nhóm đã tải lên |
| Phương thức thực thi | Node.js, trích hàm điều khiển V21; dựng bản đồ kệ và vị trí SKU giả định |
| Bước thời gian | Δt = 0,1 giây |
| Nguồn số liệu | V21_Ket_qua_7_kich_ban_kiem_thu.xlsx và dữ liệu CSV/JSON cùng bộ kiểm thử |
| Phạm vi kết luận | Kiểm thử hành vi thuật toán; chưa phải chạy toàn ứng dụng Kaggle/Colab/Three.js |

> **Nguồn:** Tài liệu được biên soạn theo bố cục 4 mục của Chương 5 mà nhóm cung cấp. Các số liệu là giá trị đã xuất từ bộ kiểm thử, không được thay thế bằng dữ liệu mô phỏng tự tạo bổ sung.

# CHƯƠNG 5. THÍ NGHIỆM VÀ ĐÁNH GIÁ MÔ HÌNH

Chương này tổng hợp các kết quả kiểm thử TN01–TN07 cho hệ thống kho FEFO 3D và 6 robot AGV V21. Phân tích tập trung vào thời gian thực hiện nhiệm vụ, quãng đường, hành vi nhường đường, khả năng phục hồi khi mất tuyến, quá trình xử lý hàng đợi và trở về trạm sạc. Các số liệu được đối chiếu giữa sổ Excel và CSV của bộ kiểm thử [2]–[4].

Phạm vi dữ liệu: thuật toán được trích từ mã V21 để chạy trong môi trường không đồ họa. Các SKU DEMO và các tình huống đối đầu/đứt tuyến là dữ liệu đầu vào kiểm thử, không phải đơn hàng thực tế trong bộ dữ liệu Kaggle. Vì vậy, kết quả chứng minh hành vi trong các phép thử đã thiết lập chứ không chứng minh hiệu quả hoặc độ an toàn tuyệt đối trong kho thực.

## 5.1. Thiết lập thí nghiệm

### 5.1.1. Mục tiêu và câu hỏi đánh giá

Bộ thí nghiệm được xây dựng để trả lời bốn nhóm câu hỏi: (i) thuật toán có đưa robot đến điểm giao hàng không; (ii) thời gian thực tế chênh lệch bao nhiêu so với thời gian dự tính; (iii) khi có nhiều robot, bộ điều khiển phát hiện và xử lý tình huống cản trở như thế nào; và (iv) robot có thể phục hồi khi mất đường, xử lý hàng đợi và hoàn tất quay về sạc hay không.

### 5.1.2. Cấu hình và phạm vi mô phỏng

### Bảng 2

| Thông số | Giá trị sử dụng | Cơ sở |
|---|---|---|
| Kích thước mặt bằng | 28 × 28 m | Mã V21 |
| Độ phân giải ô lưới | 0,5 × 0,5 m (56 × 56 ô) | Mã V21 |
| Số robot AGV | Tối đa 6 robot | Mã V21 |
| Vận tốc tối đa | 2,3 m/s | MAX_SPEED |
| Gia tốc/phanh | 1,15 / 2,7 m/s² | ACCEL / BRAKE |
| Khoảng cách an toàn | 0,98 m | SAFE_GAP |
| Khoảng dự đoán CPA | 2,4 s | CONFLICT_HORIZON |
| Chu kỳ thử lập tuyến | 2,6 s | REPLAN_INTERVAL |
| Ngưỡng cân nhắc quét | 14 s nếu không có tuyến | BLOCKED_SCAN_AFTER |
| Bước thời gian lấy mẫu | 0,1 s | Bộ kiểm thử |
| Môi trường | Node.js, không hiển thị 3D | Bộ kiểm thử |

> **Nguồn:** Nguồn: mã V21 và mô tả bộ kiểm thử [1], [3]. Các giá trị được giữ nguyên theo điều khiển V21 ngoại trừ đầu vào tình huống thử nghiệm.

### 5.1.3. Thiết kế bảy kịch bản

### Bảng 3

| Mã | Điều kiện thiết lập | Mục tiêu chính |
|---|---|---|
| TN01 | 1 robot – 1 đơn | Kiểm tra hoàn tất nhiệm vụ không có robot cạnh tranh. |
| TN02 | 3 robot – 3 đơn | Kiểm tra điều tốc và xung đột ở mức tải trung bình. |
| TN03 | 6 robot – 6 đơn | Kiểm tra đội robot đầy đủ trong một lượt giao hàng. |
| TN04 | 2 robot đối đầu | Khởi tạo hai robot di chuyển qua nhau tại hành lang z = 21,25 m; trực tiếp giao hàng. |
| TN05 | 1 robot bị đứt tuyến | Tạo vách chắn tạm rồi tháo ở t = 30 s để kiểm tra phục hồi. |
| TN06 | 6 robot – 12 đơn | Mỗi robot nhận 2 nhiệm vụ, có hàng đợi riêng. |
| TN07 | 6 robot về sạc | Dùng cùng 6 đơn TN03, chạy tiếp đến khi về đủ 6 ô sạc và quay 180°. |

### 5.1.4. Phương pháp thu thập dữ liệu

Các nhiệm vụ hoàn thành được lưu trong cấu trúc taskHistory, bao gồm robot, SKU, thời gian dự tính, thời gian thực tế, quãng đường và số lần chuyển sang trạng thái bị robot khác chặn. Bộ kiểm thử bổ sung việc tổng hợp khoảng cách tối thiểu theo mẫu 0,1 s, số lần bị từ chối di chuyển, thời gian không có tuyến, các lần thử lập lại tuyến, vòng tránh và quét 360° [1]–[4].

- Thời gian thực tế của một đơn tính từ khi robot bắt đầu thực hiện đơn đến lúc giao xong; không bao gồm thời gian chờ trong hàng đợi trước khi thực hiện và không bao gồm hành trình RETURN sau giao đơn cuối.

- Thời gian dự tính sử dụng quãng đường kế hoạch chia cho vận tốc tối đa; do đó không mặc định bao gồm tăng tốc, giảm tốc, chờ đường và các thay đổi tuyến sau khi bắt đầu.

- Thời gian bị chặn và thời gian dừng được cộng theo từng robot (robot·giây); không phải thời gian đồng hồ thực tế của toàn kịch bản.

- Khoảng cách nhỏ nhất được đo tại các thời điểm lấy mẫu, không phải phép chứng minh không có tiếp xúc giữa hai mẫu.

- Mỗi kịch bản trong bộ dữ liệu hiện có một lần chạy; chưa có 10 lần lặp hoặc độ lệch chuẩn thí nghiệm.

### 5.1.5. Chỉ số và công thức đánh giá

R = N_hoàn_thành / N_tiếp_nhận × 100%

T_TB = (Σ T_i) / N_hoàn_thành     ;     ΔT = T_TB − T_dự_tính,TB

D_TB = (Σ D_i) / N_hoàn_thành     ;     Q = 3600 × N_hoàn_thành / T_kết_thúc

Chỉ số thông lượng Q ở đây được chuẩn hóa theo thời gian kết thúc kịch bản, đơn vị đơn/giờ. Giá trị này chỉ có ý nghĩa mô tả tốc độ xử lý của đúng kịch bản đang xét; không phải thông lượng ổn định của kho dài hạn. Riêng TN07, có thể tính theo mốc hoàn tất giao đơn cuối hoặc theo mốc cả sáu robot về sạc và phải ghi rõ cách lựa chọn mẫu số.

## 5.2. Đánh giá kết quả thí nghiệm

### 5.2.1. Kết quả tổng hợp

### Bảng 4

| Kịch bản | Đơn xong | Kết thúc (s) | T. gian TB (s) | Đường TB (m) | Xung đột |
|---|---|---|---|---|---|
| TN01 | 1/1 | 35,0 | 35,00 | 26,63 | 0 |
| TN02 | 3/3 | 69,3 | 56,13 | 38,46 | 6 |
| TN03 | 6/6 | 99,3 | 76,30 | 54,17 | 27 |
| TN04 | 2/2 | 18,5 | 12,60 | 7,91 | 3 |
| TN05 | 1/1 | 62,0 | 62,00 | 26,66 | 0 |
| TN06 | 12/12 | 213,4 | 90,77 | 63,25 | 56 |
| TN07 | 6/6 | 164,9 | 76,30 | 54,17 | 27 |

> **Nguồn:** Bảng 5.1. Tổng hợp dữ liệu TN01–TN07; nguồn [2], [4]. Thời gian kết thúc của TN07 bao gồm quay về sạc, khác với mốc kết thúc giao hàng.

Cả bảy kịch bản đều hoàn thành toàn bộ nhiệm vụ được tiếp nhận trong lần thử tương ứng. Tỷ lệ hoàn thành 100% chỉ là kết quả quan sát của các tình huống đã dựng. Nhóm cần thận trọng khi diễn giải, vì TN03 và TN07 dùng cùng sáu nhiệm vụ, còn TN04 bắt đầu trực tiếp ở pha giao hàng, TN05 có vách chắn được can thiệp từ bộ kiểm thử.

**Hình 5.1. So sánh thời gian dự tính và thực tế trung bình (dữ liệu kiểm thử headless).**

### 5.2.2. Kết quả chi tiết của từng kịch bản

### 5.2.2.1. TN01 – Một robot – một đơn

Thiết lập: 1 robot, 1 đơn giao DESPATCH, vị trí lấy hàng mô phỏng.

### Bảng 5

| Chỉ tiêu | Kết quả kiểm thử |
|---|---|
| Số robot tham gia | 1 |
| Nhiệm vụ được tiếp nhận | 1 |
| Nhiệm vụ hoàn thành | 1 |
| Tỷ lệ hoàn thành (%) | 100,00 |
| Thời điểm kết thúc phép thử (s) | 35,0 |
| Thời điểm giao xong đơn cuối (s) | 35,0 |
| Thời gian dự tính TB/đơn (s) | 12,31 |
| Thời gian thực tế TB/đơn (s) | 35,00 |
| Sai lệch thời gian TB/đơn (s) | 22,69 |
| Quãng đường TB/đơn (m) | 26,63 |
| Tổng đường theo nhiệm vụ (m) | 26,63 |
| Tổng đường toàn đội đến lúc dừng (m) | 26,63 |
| Tổng lượt xung đột được ghi nhận | 0 |
| Khoảng cách tâm robot nhỏ nhất (m) | Không áp dụng |
| Số mẫu vi phạm khoảng cách 0,98 m | 0 |
| Thời gian bị robot khác chặn (robot·s) | 0,00 |
| Thời gian dừng khi có hành trình (robot·s) | 3,40 |
| Thời gian không có tuyến (robot·s) | 0,00 |
| Khoảng chặn liên tục dài nhất (s) | 0,00 |
| Số lần thử lập lại tuyến đủ điều kiện | 0 |
| Số lần tìm lại tuyến thành công | 0 |
| Số lần thử tìm đường vòng | 0 |
| Số lần tìm đường vòng thành công | 0 |
| Số lần bắt đầu quét 360° | 0 |
| Số lượt quét trực tiếp tạo tuyến mới | 0 |
| Số bước bị từ chối bởi kiểm tra an toàn | 0 |
| Vận tốc TB khi di chuyển (m/s) | 0,85 |
| Vận tốc lớn nhất ghi nhận (m/s) | 2,00 |
| Độ sâu hàng đợi lớn nhất / robot | 0 |

**Bảng 5.2. Kết quả chi tiết TN01 – kiểm thử không đồ họa.**

Nhận xét: Một robot hoàn tất một nhiệm vụ trong 35,00 s; không ghi nhận sự kiện xung đột với robot khác. Thời gian thực tế lớn hơn ETA lý tưởng vì robot phải tăng tốc, giảm tốc và đổi hướng. Kịch bản không đo đến lúc trở về ô sạc.

### 5.2.2.2. TN02 – Ba robot – ba đơn

Thiết lập: 3 robot, 3 đơn giao DESPATCH, vị trí lấy hàng mô phỏng.

### Bảng 6

| Chỉ tiêu | Kết quả kiểm thử |
|---|---|
| Số robot tham gia | 3 |
| Nhiệm vụ được tiếp nhận | 3 |
| Nhiệm vụ hoàn thành | 3 |
| Tỷ lệ hoàn thành (%) | 100,00 |
| Thời điểm kết thúc phép thử (s) | 69,3 |
| Thời điểm giao xong đơn cuối (s) | 69,3 |
| Thời gian dự tính TB/đơn (s) | 17,20 |
| Thời gian thực tế TB/đơn (s) | 56,13 |
| Sai lệch thời gian TB/đơn (s) | 38,93 |
| Quãng đường TB/đơn (m) | 38,46 |
| Tổng đường theo nhiệm vụ (m) | 115,39 |
| Tổng đường toàn đội đến lúc dừng (m) | 143,02 |
| Tổng lượt xung đột được ghi nhận | 6 |
| Khoảng cách tâm robot nhỏ nhất (m) | 1,0531 |
| Số mẫu vi phạm khoảng cách 0,98 m | 0 |
| Thời gian bị robot khác chặn (robot·s) | 8,70 |
| Thời gian dừng khi có hành trình (robot·s) | 23,70 |
| Thời gian không có tuyến (robot·s) | 0,00 |
| Khoảng chặn liên tục dài nhất (s) | 3,60 |
| Số lần thử lập lại tuyến đủ điều kiện | 2 |
| Số lần tìm lại tuyến thành công | 1 |
| Số lần thử tìm đường vòng | 0 |
| Số lần tìm đường vòng thành công | 0 |
| Số lần bắt đầu quét 360° | 0 |
| Số lượt quét trực tiếp tạo tuyến mới | 0 |
| Số bước bị từ chối bởi kiểm tra an toàn | 0 |
| Vận tốc TB khi di chuyển (m/s) | 0,78 |
| Vận tốc lớn nhất ghi nhận (m/s) | 2,00 |
| Độ sâu hàng đợi lớn nhất / robot | 0 |

**Bảng 5.3. Kết quả chi tiết TN02 – kiểm thử không đồ họa.**

Nhận xét: Ba robot hoàn thành đủ ba đơn; ghi nhận 6 lượt bắt đầu bị robot khác chặn và tổng 8,70 robot·giây bị chặn. Một trong hai lần thử lập lại tuyến đủ điều kiện tạo được tuyến mới. Khoảng cách nhỏ nhất lấy mẫu là 1,0531 m.

### 5.2.2.3. TN03 – Sáu robot – sáu đơn

Thiết lập: 6 robot, 6 đơn giao DESPATCH, vị trí lấy hàng mô phỏng.

### Bảng 7

| Chỉ tiêu | Kết quả kiểm thử |
|---|---|
| Số robot tham gia | 6 |
| Nhiệm vụ được tiếp nhận | 6 |
| Nhiệm vụ hoàn thành | 6 |
| Tỷ lệ hoàn thành (%) | 100,00 |
| Thời điểm kết thúc phép thử (s) | 99,3 |
| Thời điểm giao xong đơn cuối (s) | 99,3 |
| Thời gian dự tính TB/đơn (s) | 22,65 |
| Thời gian thực tế TB/đơn (s) | 76,30 |
| Sai lệch thời gian TB/đơn (s) | 53,65 |
| Quãng đường TB/đơn (m) | 54,17 |
| Tổng đường theo nhiệm vụ (m) | 325,05 |
| Tổng đường toàn đội đến lúc dừng (m) | 408,63 |
| Tổng lượt xung đột được ghi nhận | 27 |
| Khoảng cách tâm robot nhỏ nhất (m) | 1,0012 |
| Số mẫu vi phạm khoảng cách 0,98 m | 0 |
| Thời gian bị robot khác chặn (robot·s) | 25,40 |
| Thời gian dừng khi có hành trình (robot·s) | 56,80 |
| Thời gian không có tuyến (robot·s) | 0,00 |
| Khoảng chặn liên tục dài nhất (s) | 3,80 |
| Số lần thử lập lại tuyến đủ điều kiện | 2 |
| Số lần tìm lại tuyến thành công | 1 |
| Số lần thử tìm đường vòng | 0 |
| Số lần tìm đường vòng thành công | 0 |
| Số lần bắt đầu quét 360° | 0 |
| Số lượt quét trực tiếp tạo tuyến mới | 0 |
| Số bước bị từ chối bởi kiểm tra an toàn | 0 |
| Vận tốc TB khi di chuyển (m/s) | 0,80 |
| Vận tốc lớn nhất ghi nhận (m/s) | 2,00 |
| Độ sâu hàng đợi lớn nhất / robot | 0 |

**Bảng 5.4. Kết quả chi tiết TN03 – kiểm thử không đồ họa.**

Nhận xét: Sáu robot hoàn tất sáu đơn ở t = 99,30 s; ghi nhận 27 lượt xung đột. Tổng thời gian bị robot khác chặn là 25,40 robot·giây. Hai robot đã về ô sạc tại mốc dừng do một số robot hoàn thành sớm, nhưng bốn robot còn lại chưa hoàn tất RETURN.

### 5.2.2.4. TN04 – Hai robot giao cắt/đối đầu

Thiết lập: Hai robot đối đầu dọc hành lang z=21.25; nhiệm vụ DROP trực tiếp đến hai phía đối diện.

### Bảng 8

| Chỉ tiêu | Kết quả kiểm thử |
|---|---|
| Số robot tham gia | 2 |
| Nhiệm vụ được tiếp nhận | 2 |
| Nhiệm vụ hoàn thành | 2 |
| Tỷ lệ hoàn thành (%) | 100,00 |
| Thời điểm kết thúc phép thử (s) | 18,5 |
| Thời điểm giao xong đơn cuối (s) | 18,5 |
| Thời gian dự tính TB/đơn (s) | 3,48 |
| Thời gian thực tế TB/đơn (s) | 12,60 |
| Sai lệch thời gian TB/đơn (s) | 9,12 |
| Quãng đường TB/đơn (m) | 7,91 |
| Tổng đường theo nhiệm vụ (m) | 15,82 |
| Tổng đường toàn đội đến lúc dừng (m) | 24,08 |
| Tổng lượt xung đột được ghi nhận | 3 |
| Khoảng cách tâm robot nhỏ nhất (m) | 1,0002 |
| Số mẫu vi phạm khoảng cách 0,98 m | 0 |
| Thời gian bị robot khác chặn (robot·s) | 2,00 |
| Thời gian dừng khi có hành trình (robot·s) | 5,60 |
| Thời gian không có tuyến (robot·s) | 0,00 |
| Khoảng chặn liên tục dài nhất (s) | 1,60 |
| Số lần thử lập lại tuyến đủ điều kiện | 0 |
| Số lần tìm lại tuyến thành công | 0 |
| Số lần thử tìm đường vòng | 0 |
| Số lần tìm đường vòng thành công | 0 |
| Số lần bắt đầu quét 360° | 0 |
| Số lượt quét trực tiếp tạo tuyến mới | 0 |
| Số bước bị từ chối bởi kiểm tra an toàn | 0 |
| Vận tốc TB khi di chuyển (m/s) | 0,77 |
| Vận tốc lớn nhất ghi nhận (m/s) | 1,96 |
| Độ sâu hàng đợi lớn nhất / robot | 0 |

**Bảng 5.5. Kết quả chi tiết TN04 – kiểm thử không đồ họa.**

Nhận xét: Hai robot được bố trí đối đầu trong một hành lang và chuyển trực tiếp đến pha DROP; không nên so sánh trực tiếp thời gian trung bình của TN04 với TN01–TN03 có đủ pha PICK. Cả hai nhiệm vụ hoàn thành, với 3 lượt xung đột và 2,00 robot·giây bị chặn.

### 5.2.2.5. TN05 – Đứt tuyến 30 giây, khôi phục

Thiết lập: Một robot; dựng vách chắn tạm qua toàn chiều z ngay sau nhận đơn, tháo chắn tại 30 s.

### Bảng 9

| Chỉ tiêu | Kết quả kiểm thử |
|---|---|
| Số robot tham gia | 1 |
| Nhiệm vụ được tiếp nhận | 1 |
| Nhiệm vụ hoàn thành | 1 |
| Tỷ lệ hoàn thành (%) | 100,00 |
| Thời điểm kết thúc phép thử (s) | 62,0 |
| Thời điểm giao xong đơn cuối (s) | 62,0 |
| Thời gian dự tính TB/đơn (s) | 12,31 |
| Thời gian thực tế TB/đơn (s) | 62,00 |
| Sai lệch thời gian TB/đơn (s) | 49,69 |
| Quãng đường TB/đơn (m) | 26,66 |
| Tổng đường theo nhiệm vụ (m) | 26,66 |
| Tổng đường toàn đội đến lúc dừng (m) | 26,66 |
| Tổng lượt xung đột được ghi nhận | 0 |
| Khoảng cách tâm robot nhỏ nhất (m) | Không áp dụng |
| Số mẫu vi phạm khoảng cách 0,98 m | 0 |
| Thời gian bị robot khác chặn (robot·s) | 0,00 |
| Thời gian dừng khi có hành trình (robot·s) | 27,40 |
| Thời gian không có tuyến (robot·s) | 24,30 |
| Khoảng chặn liên tục dài nhất (s) | 0,00 |
| Số lần thử lập lại tuyến đủ điều kiện | 9 |
| Số lần tìm lại tuyến thành công | 1 |
| Số lần thử tìm đường vòng | 4 |
| Số lần tìm đường vòng thành công | 1 |
| Số lần bắt đầu quét 360° | 1 |
| Số lượt quét trực tiếp tạo tuyến mới | 0 |
| Số bước bị từ chối bởi kiểm tra an toàn | 0 |
| Vận tốc TB khi di chuyển (m/s) | 0,82 |
| Vận tốc lớn nhất ghi nhận (m/s) | 1,96 |
| Độ sâu hàng đợi lớn nhất / robot | 0 |

**Bảng 5.6. Kết quả chi tiết TN05 – kiểm thử không đồ họa.**

Nhận xét: Vách chắn tạm được thêm bởi bộ kiểm thử rồi tháo tại t = 30 s. Trong quá trình mất tuyến có 24,30 robot·giây không có đường, 9 lần thử lập lại tuyến đủ điều kiện, 4 lần thử vòng tránh và 1 lượt quét 360°. Quét không trực tiếp tạo được tuyến mới. Robot có thể tiếp tục di chuyển 1,20 s sau khi vách chắn được gỡ.

Giới hạn diễn giải: số xung đột với robot khác bằng 0 vì đây là kịch bản vật cản tĩnh do bộ kiểm thử tạo ra; thời gian không có tuyến không được tính vào chỉ số xung đột giữa các AGV.

### 5.2.2.6. TN06 – Sáu robot – 12 đơn hàng đợi

Thiết lập: 12 đơn: mỗi robot 1 đơn đang chạy + 1 đơn trong hàng đợi; DESPATCH.

### Bảng 10

| Chỉ tiêu | Kết quả kiểm thử |
|---|---|
| Số robot tham gia | 6 |
| Nhiệm vụ được tiếp nhận | 12 |
| Nhiệm vụ hoàn thành | 12 |
| Tỷ lệ hoàn thành (%) | 100,00 |
| Thời điểm kết thúc phép thử (s) | 213,4 |
| Thời điểm giao xong đơn cuối (s) | 213,4 |
| Thời gian dự tính TB/đơn (s) | 24,27 |
| Thời gian thực tế TB/đơn (s) | 90,77 |
| Sai lệch thời gian TB/đơn (s) | 66,51 |
| Quãng đường TB/đơn (m) | 63,25 |
| Tổng đường theo nhiệm vụ (m) | 758,98 |
| Tổng đường toàn đội đến lúc dừng (m) | 877,51 |
| Tổng lượt xung đột được ghi nhận | 56 |
| Khoảng cách tâm robot nhỏ nhất (m) | 0,9810 |
| Số mẫu vi phạm khoảng cách 0,98 m | 0 |
| Thời gian bị robot khác chặn (robot·s) | 74,70 |
| Thời gian dừng khi có hành trình (robot·s) | 148,00 |
| Thời gian không có tuyến (robot·s) | 0,00 |
| Khoảng chặn liên tục dài nhất (s) | 5,40 |
| Số lần thử lập lại tuyến đủ điều kiện | 14 |
| Số lần tìm lại tuyến thành công | 12 |
| Số lần thử tìm đường vòng | 1 |
| Số lần tìm đường vòng thành công | 0 |
| Số lần bắt đầu quét 360° | 0 |
| Số lượt quét trực tiếp tạo tuyến mới | 0 |
| Số bước bị từ chối bởi kiểm tra an toàn | 24 |
| Vận tốc TB khi di chuyển (m/s) | 0,80 |
| Vận tốc lớn nhất ghi nhận (m/s) | 2,18 |
| Độ sâu hàng đợi lớn nhất / robot | 1 |

**Bảng 5.7. Kết quả chi tiết TN06 – kiểm thử không đồ họa.**

Nhận xét: Sáu robot thực hiện 12/12 đơn qua jobQueue riêng; ghi nhận 56 lượt xung đột và 24 bước di chuyển bị lớp kiểm tra an toàn từ chối. Có 14 lần thử lập lại tuyến đủ điều kiện, trong đó 12 lần thành công. Số lượt xung đột tính trên mỗi đơn là 4,67, gần với 4,50 của TN03; các nhiệm vụ khác nhau nên không kết luận tăng tải gây tăng tỷ lệ theo cách tuyến tính.

### 5.2.2.7. TN07 – Sáu robot trở về các ô sạc

Thiết lập: 6 đơn + yêu cầu cả 6 robot vào ô sạc và hoàn thành quay 180°.

### Bảng 11

| Chỉ tiêu | Kết quả kiểm thử |
|---|---|
| Số robot tham gia | 6 |
| Nhiệm vụ được tiếp nhận | 6 |
| Nhiệm vụ hoàn thành | 6 |
| Tỷ lệ hoàn thành (%) | 100,00 |
| Thời điểm kết thúc phép thử (s) | 164,9 |
| Thời điểm giao xong đơn cuối (s) | 99,3 |
| Thời gian dự tính TB/đơn (s) | 22,65 |
| Thời gian thực tế TB/đơn (s) | 76,30 |
| Sai lệch thời gian TB/đơn (s) | 53,65 |
| Quãng đường TB/đơn (m) | 54,17 |
| Tổng đường theo nhiệm vụ (m) | 325,05 |
| Tổng đường toàn đội đến lúc dừng (m) | 516,99 |
| Tổng lượt xung đột được ghi nhận | 27 |
| Khoảng cách tâm robot nhỏ nhất (m) | 0,9804 |
| Số mẫu vi phạm khoảng cách 0,98 m | 0 |
| Thời gian bị robot khác chặn (robot·s) | 35,20 |
| Thời gian dừng khi có hành trình (robot·s) | 74,60 |
| Thời gian không có tuyến (robot·s) | 0,00 |
| Khoảng chặn liên tục dài nhất (s) | 3,80 |
| Số lần thử lập lại tuyến đủ điều kiện | 3 |
| Số lần tìm lại tuyến thành công | 2 |
| Số lần thử tìm đường vòng | 0 |
| Số lần tìm đường vòng thành công | 0 |
| Số lần bắt đầu quét 360° | 0 |
| Số lượt quét trực tiếp tạo tuyến mới | 0 |
| Số bước bị từ chối bởi kiểm tra an toàn | 18 |
| Vận tốc TB khi di chuyển (m/s) | 0,80 |
| Vận tốc lớn nhất ghi nhận (m/s) | 2,02 |
| Độ sâu hàng đợi lớn nhất / robot | 0 |
| Số robot về đúng ô sạc khi dừng | 6 |
| Số robot đang sạc khi dừng | 2 |
| Số robot ở trạng thái IDLE khi dừng | 4 |

**Bảng 5.8. Kết quả chi tiết TN07 – kiểm thử không đồ họa.**

Nhận xét: TN07 dùng lại sáu nhiệm vụ của TN03 nhưng tiếp tục mô phỏng sau thời điểm xong đơn cuối (99,30 s) đến khi toàn đội vào đúng ô sạc và hoàn thành quay đầu (164,90 s). Mốc sau lớn hơn 65,60 s; tại thời điểm đó 6/6 robot ở ô sạc, trong đó 2 robot đang sạc và 4 robot đã trở về IDLE.

Nếu tính thông lượng theo mốc hoàn tất giao hàng: Q = 6 × 3600 / 99,30 = 217,52 đơn/giờ; nếu tính theo mốc cả 6 robot về sạc: Q = 6 × 3600 / 164,90 = 130,99 đơn/giờ. Hai mẫu số đánh giá hai chu kỳ vận hành khác nhau.

### 5.2.3. Đánh giá so sánh các nhóm chỉ số

**Hình 5.2. Tổng lượt bắt đầu bị chặn được ghi nhận qua bảy kịch bản.**

**Hình 5.3. Tổng thời gian bị robot khác chặn (robot·giây).**

TN01 không ghi nhận xung đột do chỉ có một robot. TN02 và TN03 lần lượt ghi nhận 6 và 27 lượt; TN06 ghi nhận 56 lượt ở 12 đơn hàng. Chỉ số số lượt xung đột là số sự kiện bắt đầu bị robot khác chặn theo logic V21, không phải số va chạm. Không nên so sánh trực tiếp tổng số lượt khi số robot, số nhiệm vụ và lộ trình khác nhau; có thể bổ sung chỉ số lượt xung đột trên mỗi đơn để hỗ trợ chuẩn hóa.

**Hình 5.4. Khoảng cách tâm robot nhỏ nhất tại các mốc lấy mẫu so với SAFE_GAP = 0,98 m.**

Các kịch bản đa robot ghi nhận 0 mẫu có khoảng cách nhỏ hơn SAFE_GAP = 0,98 m tại bước kiểm tra 0,1 giây. Khoảng cách thấp nhất đo được là 0,9804 m ở TN07, rất sát ngưỡng. Vì đây là kiểm tra vị trí theo mẫu, không có bộ phát hiện tiếp xúc hình học độc lập, không thể đồng nhất kết quả này với bảo đảm tuyệt đối không va chạm.

**Hình 5.5. TN07: phân biệt mốc giao đơn cuối và mốc về đủ trạm sạc.**

TN03 và TN07 sử dụng cùng tập sáu nhiệm vụ. Trong TN03, kiểm thử dừng tại t = 99,30 s khi hoàn thành đơn cuối. TN07 tiếp tục chạy đến t = 164,90 s để kiểm tra hành vi trở về sạc. Do đó, hai kịch bản không phải hai lần lặp độc lập và phải giữ riêng phạm vi tính thời gian, quãng đường và thông lượng.

### 5.2.4. Kiểm tra độ tin cậy và tính so sánh được của số liệu

- Bộ dữ liệu hiện chỉ có một lần chạy trên mỗi kịch bản. Chưa thể tính độ lệch chuẩn theo lần lặp hoặc khoảng tin cậy thống kê.

- Các vị trí hàng hóa trong TN01–TN03 và TN06 khác nhau; chưa có cặp đối chứng chỉ thay đổi số robot, nên không thể kết luận định lượng mức ảnh hưởng riêng của số lượng robot.

- Chưa có bộ chạy “bật/tắt chi phí tránh robot”, “bật/tắt CPA” hoặc thử nghiệm so sánh Dijkstra–A* với cùng đầu vào để định lượng tỷ lệ cải thiện.

- Cột collisions trong lịch sử được khởi tạo nhưng chưa có bộ đo va chạm độc lập; không dùng giá trị 0 làm chứng cứ về độ an toàn tuyệt đối.

- Không so sánh thời gian chu trình có RETURN (TN07) với thời gian chỉ kết thúc khi giao hàng (TN03) nếu không chuẩn hóa mốc kết thúc.

- Thời gian bị chặn, dừng, không tuyến được tích lũy theo robot·giây. Tổng robot·giây có thể lớn hơn thời gian đồng hồ của kịch bản nhiều robot.

## 5.3. Đánh giá tổng quan mô hình

### 5.3.1. Vấn đề giải quyết được

Dựa trên kết quả kiểm thử trong các tình huống đã thiết lập, có thể xác nhận các năng lực sau ở cấp độ thực thi thuật toán:

- Hoàn thành tác vụ cơ sở: TN01, TN02 và TN03 đều hoàn thành toàn bộ các nhiệm vụ được giao trong lần thử tương ứng.

- Điều phối và nhường đường nhiều robot: TN02, TN03, TN04 và TN06 ghi nhận các sự kiện nhường đường, thời gian bị chặn và thay đổi trạng thái vận tốc.

- Kiểm tra an toàn cho bước di chuyển: TN06 ghi nhận 24 bước bị từ chối và TN07 ghi nhận 18 bước bị từ chối trong quá trình thực hiện.

- Phục hồi khi mất tuyến: TN05 có 9 lần thử lập lại tuyến hợp lệ, 4 lần tìm vòng tránh và hoàn tất nhiệm vụ sau khi vật cản tạm được tháo.

- Xử lý hàng đợi: TN06 thực hiện đủ 12 đơn bằng sáu robot (mỗi robot hai đơn theo thiết lập).

- Trở về trạm sạc: TN07 xác nhận đủ sáu robot vào các ô sạc đã định, sau đó quay đầu 180°.

### 5.3.2. Cách giải quyết vấn đề

### Bảng 12

| Vấn đề vận hành | Cơ chế trong V21 | Bằng chứng kiểm thử |
|---|---|---|
| Tìm tuyến tránh kệ | Bản đồ lưới + A* | TN01–TN03 có nhiệm vụ hoàn thành |
| Đường đi gần robot khác | Chi phí phạt A* + dự đoán vị trí | TN02–TN03 có các lượt thay đổi đường và bị chặn |
| Nguy cơ tiếp cận | CPA, cảm biến ảo, giới hạn phanh | TN04 ghi nhận 3 sự kiện bị chặn |
| Bước di chuyển quá gần | f5AllowedMove() từ chối bước | TN06: 24 lần; TN07: 18 lần |
| Mất tuyến hoặc bế tắc | Thử tuyến mới, detour, quét 360° có điều kiện | TN05: 9 thử lập tuyến, 4 thử detour, 1 quét |
| Nhiều đơn liên tiếp | jobQueue và cơ chế giữ chỗ SKU | TN06: 12/12 nhiệm vụ hoàn thành |
| Dòng robot về sạc | Tuyến RETURN, vùng phạt cửa, lộ trình dock | TN07: 6/6 robot đã về đúng ô sạc |

Kết quả cho thấy bộ điều khiển vận hành dựa trên nhiều lớp hỗ trợ nhau: lập đường trước, điều tốc theo nguy cơ, từ chối bước di chuyển không an toàn và phục hồi khi mất đường. Tuy vậy, một kết quả hoàn thành nhiệm vụ không tự chứng minh từng lớp đã góp bao nhiêu phần trăm vào hiệu quả chung.

### 5.3.3. Vấn đề chưa giải quyết được

- Chưa bảo đảm điều phối đa robot theo thời gian: chưa có bảng đặt chỗ các ô lưới và giao lộ trên trục thời gian (time-expanded reservation).

- Chưa chứng minh tránh khóa chết trong mọi trường hợp: TN05 được giải phóng vật cản ở t = 30 s; không thể coi đây là bằng chứng robot tự thoát khỏi mọi hành lang bị chặn vĩnh viễn.

- Chưa có bằng chứng độc lập về va chạm: chỉ có khoảng cách lấy mẫu và trạng thái bộ điều khiển; chưa kiểm tra tiếp xúc giữa các bước lấy mẫu hoặc hình học thân robot đầy đủ.

- Chưa tối ưu phân công nhiệm vụ trên toàn đội: người dùng vẫn chọn robot/SKU; chưa tối ưu bằng tải công việc, pin và thời gian đến hàng.

- Mô hình pin/động lực học vẫn giản lược: năng lượng và thao tác nâng hạ hàng chưa tính theo tải trọng và lực thực tế.

- Chưa đánh giá tính ổn định thống kê trên nhiều lần lặp, chưa có thí nghiệm đối chứng bật/tắt từng cơ chế.

- Chưa kiểm thử đầy đủ việc tải Kaggle, tương tác Three.js và giao diện Tablet WMS trong bộ headless hiện tại.

- Tính khả chuyển của bộ kiểm thử còn giới hạn ở logic đã trích xuất, cần đối chiếu với phiên bản notebook hiện hành khi mã nguồn thay đổi.

## 5.4. Định hướng phát triển

### 5.4.1. Ưu tiên ngắn hạn – hoàn thiện đo kiểm

- Bổ sung bộ phát hiện tiếp xúc robot độc lập theo hình học và ghi event log tại từng bước mô phỏng, phân biệt “chạm thực tế”, “dưới ngưỡng an toàn”, “bị chặn” và “chỉ giảm tốc”.

- Ghi nhận thời gian chờ trong hàng đợi, thời gian tại kệ, thời gian di chuyển có hàng, thời gian RETURN và tổng thời gian từ lúc phát lệnh đến khi giao xong.

- Xuất dữ liệu đồng bộ từ ứng dụng Colab/Three.js và so sánh với headless ở cùng tập SKU, tọa độ và thời điểm; tối thiểu 10 lần lặp hoặc nhiều bộ kịch bản đa dạng.

- Tạo dữ liệu cấu hình thử nghiệm (seed, danh sách SKU, robot, điểm giao, số đơn) để chạy lại và kiểm tra tính tái lập.

### 5.4.2. Ưu tiên trung hạn – cải thiện thuật toán

- Xây dựng thí nghiệm đối chứng bật/tắt chi phí phạt trong A*, CPA và detour để định lượng vai trò từng cơ chế.

- Nghiên cứu Cooperative A* hoặc Conflict-Based Search với đặt chỗ ô lưới theo thời gian, kết hợp quy tắc cấp quyền qua giao lộ để giảm nguy cơ khóa chết.

- Thiết kế bộ phân công nhiệm vụ tự động theo khoảng cách, độ ưu tiên FEFO, pin và tải công việc; đánh giá trên cùng 12 đơn của TN06.

- Tối ưu ngưỡng SAFE_GAP, SENSOR_RANGE, chi phí tránh robot và chu kỳ replan bằng khảo sát nhiều cấu hình; ghi nhận đường đi – thời gian – an toàn đồng thời.

### 5.4.3. Ưu tiên dài hạn – tiệm cận vận hành thực tế

- Mô phỏng động lực học 2D/3D, cơ cấu nâng hạ và mô hình tiêu hao pin theo quãng đường, tải trọng, gia tốc và thời gian chờ.

- Mô phỏng LiDAR/camera có nhiễu, độ trễ cảm biến và truyền thông, giới hạn phanh khi sàn trơn hoặc tải nặng.

- Lưu kết quả trong cơ sở dữ liệu, phát triển dashboard theo ca vận hành và các chỉ số throughput, thời gian hoàn thành, sử dụng đội robot và sự cố.

- Thử nghiệm trên môi trường robot chuyên dụng hoặc hệ AGV vật lý có giám sát và quy trình an toàn phù hợp.

### 5.4.4. Ma trận ưu tiên thực hiện

### Bảng 13

| Giai đoạn | Hạng mục cần ưu tiên | Tiêu chí nghiệm thu |
|---|---|---|
| 1 – Đo kiểm | Bộ đo va chạm và xuất log sự kiện | Có nhật ký va chạm độc lập, thời điểm và vị trí. |
| 2 – Đối chứng | A* phạt/không phạt; CPA bật/tắt | Có bộ kết quả cùng dữ liệu đầu vào và phép đo chênh lệch. |
| 3 – Điều phối | Đặt chỗ ô lưới theo thời gian | Giảm tình huống hai robot cùng giữ một nút hành lang. |
| 4 – Điều hành | Gán robot tự động + mô hình pin | Phân công theo tải công việc và năng lượng được đo. |
| 5 – Triển khai | Kiểm thử tích hợp Three.js/Kaggle | Chạy toàn notebook và xuất dữ liệu khớp với giao diện. |

## KẾT LUẬN CHƯƠNG 5

Bảy kịch bản kiểm thử headless TN01–TN07 cho thấy các hàm điều phối V21 có thể thực hiện các nhiệm vụ mô phỏng đã thiết lập, kích hoạt cơ chế nhường đường khi có robot khác, tìm lại tuyến trong một số trường hợp và hoàn tất hành trình trở về ô sạc. Điểm nổi bật là khả năng hoàn tất 12/12 đơn của TN06 và 6/6 robot về ô sạc của TN07 trong bộ dữ liệu thử nghiệm.

Các kết quả vẫn có giới hạn rõ ràng: dữ liệu SKU giả định, chưa chạy toàn hệ Colab/Three.js, một lần chạy/kịch bản, không có đối chứng đầy đủ và chưa có bộ đếm va chạm độc lập. Vì vậy, chương này được dùng làm báo cáo kiểm thử chức năng và cơ sở thiết kế thực nghiệm chính thức; mọi tuyên bố về tỷ lệ tối ưu hay độ an toàn tuyệt đối cần đợi kết quả từ chạy tích hợp và kiểm chứng bổ sung.

# PHỤ LỤC A. NHẬT KÝ NHIỆM VỤ ĐÃ HOÀN THÀNH

Bảng dưới đây giữ nguyên toàn bộ nhiệm vụ trong tệp lịch sử tổng hợp của bộ thử nghiệm; các mã DEMO/CROSS là SKU giả định. TN03 và TN07 có các nhiệm vụ giống nhau theo thiết kế. Cột “Xung đột” là số sự kiện chuyển sang bị chặn, không phải va chạm.

### Bảng 14

| TN | Robot | SKU | ETA (s) | Thực (s) | Đường (m) | Xung đột |
|---|---|---|---|---|---|---|
| TN01 | Robot 1 | DEMO-1 | 12,3 | 35,0 | 26,63 | 0 |
| TN02 | Robot 1 | DEMO-1 | 12,3 | 39,9 | 26,63 | 0 |
| TN02 | Robot 2 | DEMO-2 | 18,9 | 59,2 | 41,84 | 4 |
| TN02 | Robot 3 | DEMO-3 | 20,4 | 69,3 | 46,93 | 2 |
| TN03 | Robot 1 | DEMO-1 | 12,3 | 41,1 | 26,61 | 0 |
| TN03 | Robot 2 | DEMO-2 | 18,9 | 65,7 | 48,89 | 3 |
| TN03 | Robot 3 | DEMO-3 | 20,4 | 67,7 | 52,75 | 2 |
| TN03 | Robot 5 | DEMO-5 | 29,0 | 91,7 | 64,92 | 3 |
| TN03 | Robot 4 | DEMO-4 | 25,9 | 92,3 | 63,09 | 7 |
| TN03 | Robot 6 | DEMO-6 | 29,3 | 99,3 | 68,78 | 12 |
| TN04 | Robot 1 | CROSS-1 | 2,2 | 6,7 | 5,00 | 1 |
| TN04 | Robot 2 | CROSS-2 | 4,8 | 18,5 | 10,82 | 2 |
| TN05 | Robot 1 | DEMO-1 | 12,3 | 62,0 | 26,66 | 0 |
| TN06 | Robot 1 | DEMO-1 | 12,3 | 41,1 | 26,61 | 0 |
| TN06 | Robot 2 | DEMO-2 | 18,9 | 65,7 | 48,89 | 3 |
| TN06 | Robot 3 | DEMO-3 | 20,4 | 68,1 | 52,75 | 2 |
| TN06 | Robot 5 | DEMO-5 | 29,0 | 113,6 | 72,28 | 6 |
| TN06 | Robot 6 | DEMO-6 | 29,3 | 115,7 | 73,80 | 15 |
| TN06 | Robot 4 | DEMO-4 | 25,9 | 116,8 | 67,91 | 12 |
| TN06 | Robot 1 | DEMO-7 | 26,6 | 99,5 | 64,29 | 8 |
| TN06 | Robot 6 | DEMO-12 | 13,8 | 53,1 | 44,59 | 0 |
| TN06 | Robot 4 | DEMO-10 | 24,0 | 65,4 | 53,93 | 0 |
| TN06 | Robot 3 | DEMO-9 | 32,2 | 117,6 | 81,45 | 4 |
| TN06 | Robot 2 | DEMO-8 | 22,2 | 132,9 | 89,98 | 5 |
| TN06 | Robot 5 | DEMO-11 | 36,7 | 99,8 | 82,49 | 1 |
| TN07 | Robot 1 | DEMO-1 | 12,3 | 41,1 | 26,61 | 0 |
| TN07 | Robot 2 | DEMO-2 | 18,9 | 65,7 | 48,89 | 3 |
| TN07 | Robot 3 | DEMO-3 | 20,4 | 67,7 | 52,75 | 2 |
| TN07 | Robot 5 | DEMO-5 | 29,0 | 91,7 | 64,92 | 3 |
| TN07 | Robot 4 | DEMO-4 | 25,9 | 92,3 | 63,09 | 7 |
| TN07 | Robot 6 | DEMO-6 | 29,3 | 99,3 | 68,78 | 12 |

> **Nguồn:** Nguồn: v21_seven_scenarios_tasks.csv [4].

# PHỤ LỤC B. NGUỒN DỮ LIỆU VÀ QUY ƯỚC ĐO

Tác giả báo cáo tổng hợp dữ liệu từ mã nguồn V21 do nhóm cung cấp và các tệp kết quả chạy kiểm thử đã có trong cuộc trao đổi. Không bổ sung hoặc thay thế số liệu thử nghiệm bằng ước tính. Khi nhóm có kết quả Colab chính thức, cần gắn mã phiên bản nguồn, môi trường chạy, thời điểm chạy, danh sách SKU thực, cách tạo lệnh và dữ liệu thô cho từng phiên.

### Bảng 15

| Trường | Diễn giải và giới hạn |
|---|---|
| actual | Thời gian bắt đầu nhiệm vụ → giao xong. Không bao gồm chờ nhận việc và RETURN cuối. |
| estimated | Chiều dài đường kế hoạch / MAX_SPEED; không tính đủ hành vi điều tốc và chờ. |
| fleet_distance_m | Quãng đường đội robot tích lũy đến thời điểm kết thúc phép thử. |
| total_distance_tasks_m | Tổng khoảng cách theo các nhiệm vụ giao hàng đã hoàn thành. |
| total_conflicts | Số lần activeTask.conflictCount tăng khi blockedNow chuyển từ false sang true. |
| blocked_seconds_robot_sum | Tổng thời gian theo robot (robot·s) khi bộ đo xác định bị robot khác chặn. |
| min_pair_distance_m | Khoảng cách nhỏ nhất giữa tâm các robot tại các mẫu 0,1 s; không có kiểm chứng giữa mẫu. |
| motion_rejects | Lượt bước di chuyển bị f5AllowedMove() từ chối; khác xung đột. |
| replan_attempts | Lượt thử lập lại tuyến đủ điều kiện REPLAN_INTERVAL; không đồng nghĩa mọi lần gọi hàm. |
| scan_starts | Số lượt bắt đầu quét 360° theo trạng thái, không đồng nghĩa quét tìm được đường. |
| robots_at_dock | Số robot đã về đúng ô sạc tại thời điểm dừng. Chỉ TN07 cố ý chờ đủ cả đội. |

# TÀI LIỆU THAM KHẢO (IEEE)

[1] Nhóm phát triển mô hình AGV V21, “Pasted text(1).txt – Mã nguồn mô hình 3D kho hàng FEFO và điều phối 6 robot,” tài liệu nội bộ do nhóm cung cấp, 2026.

[2] “V21_Ket_qua_7_kich_ban_kiem_thu.xlsx,” Sổ tổng hợp kết quả kiểm thử TN01–TN07, bộ dữ liệu làm việc của báo cáo, 2026.

[3] “V21_7_kich_ban_README.txt” và “v21_seven_scenarios.js,” Mô tả thiết lập, phạm vi và chương trình kiểm thử headless, 2026.

[4] “v21_seven_scenarios_summary.csv” và “v21_seven_scenarios_tasks.csv,” Tệp kết quả tổng hợp và nhật ký theo nhiệm vụ, 2026.

[5] Nhóm 1, “TaskTable_SMART LOGISTICS.docx,” Đề cương và mô tả kỹ thuật của đề tài Smart Logistics, tài liệu nội bộ, 2026.

## Hình ảnh nhúng

Các hình ảnh nhúng trong DOCX được giữ trong thư mục `assets/03-ket-qua-thi-nghiem`.

- `assets/03-ket-qua-thi-nghiem/image1.png`

- `assets/03-ket-qua-thi-nghiem/image2.png`

- `assets/03-ket-qua-thi-nghiem/image3.png`

- `assets/03-ket-qua-thi-nghiem/image4.png`

- `assets/03-ket-qua-thi-nghiem/image5.png`
