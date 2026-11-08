# Audit tiểu luận ctuong smart

Nguồn: `tiểu luận ctuong smart.docx` (476 đoạn có chữ, 21 bảng, 14 hình ảnh nhúng).

## Kết luận nhanh

Tài liệu có đủ vật liệu kỹ thuật nhưng chưa nên phát hành nguyên trạng. Ba lỗi lớn là:

1. Phần 5.3 bị lặp nguyên khối ba lần, gồm các mục 5.3.1–5.3.4 và các đoạn hạn chế/ phạm vi kết luận.
2. Heading dùng nhiều style nội bộ (`Heading11`, `HeadingB`, `Style2smt`, `p3`, `bth`) và có mục cấp 3 bị để style thân bài; số mục bị nhảy hoặc trùng.
3. Phần thuật toán xuất hiện ở Chương 1, Chương 3 và Chương 4 nhưng chưa phân vai rõ: lý thuyết, triển khai và quy trình vận hành đang lẫn nhau.

Tài liệu không có các mục `/exam`, `/logs`, `/evals` dưới dạng phần độc lập. Nội dung tương ứng hiện rải rác ở Chương 5, bảng chỉ số và phần định hướng phát triển.

## Heading cần chuẩn hóa

| Vị trí | Hiện trạng | Đề xuất |
|---|---|---|
| Lời mở đầu | `Heading1`, các tiểu mục `Style2smt` | `Heading 1` cho phần; `Heading 2` cho 6 tiểu mục |
| Chương 1–6 | `Heading11` | `Heading 1`, tiêu đề cùng mẫu `CHƯƠNG N: ...` |
| Chương 2 | Tiêu đề có dấu chấm cuối; tiểu mục “Khái niệm mô hình”, “Cấu trúc logic...” chưa đánh số nhất quán | Đổi thành `2.1`, `2.2` và đánh số các mục con `2.2.1`… |
| Chương 3 | `3.5` có các mục `3.5.1`, `3.5.2`, `3.5.3`, sau đó nhảy tới `3.5.6`; `3.6` nhảy tới `3.6.4`, `3.6.7` | Hoặc bổ sung mục còn thiếu, hoặc đánh lại liên tục; giữ một bộ số duy nhất |
| Chương 4 | “Thiết lập môi trường vận hành”, “Chuẩn hóa và xử lý dữ liệu”, “Cơ chế chống va chạm” chưa có số mục | Đánh số `4.1`, `4.2`, `4.3` và các bước con nếu cần |
| Chương 5 | `5.2.1.Tổng hợp` thiếu khoảng trắng; `5.3.1–5.3.4` lặp ba lần; `5.4.x` dùng style khác | Giữ một bộ `5.1`–`5.4`, đánh số lại và dùng cùng style |
| Chương 6 | “Kết luận” và “Định hướng phát triển” chỉ là tiểu mục không số | Đổi thành `6.1` và `6.2` |
| Tài liệu tham khảo | `Heading11` | `Heading 1`, giữ ngoài đánh số chương |

## Đoạn trùng cần gộp

- Khối bắt đầu ở mục 5.3.1 xuất hiện ba lần gần như nguyên văn. Giữ lần đầu, xóa hai lần lặp; giữ riêng phần “Phạm vi áp dụng kết luận” một lần.
- Các bảng 18, 19 và 20 là cùng một ma trận “Vấn đề / Cơ chế / Bằng chứng”. Giữ một bảng, cập nhật chú thích nếu cần.
- Nội dung A* và tránh va chạm được trình bày ở Chương 1 (cơ sở), Chương 3 (xây dựng) và Chương 4 (vận hành). Không xóa kiến thức, nhưng rút gọn: Chương 1 chỉ định nghĩa; Chương 3 chứa công thức, tham số và giả mã; Chương 4 chỉ mô tả thứ tự thực thi.
- Chương 6 lặp lại nhiều ý đã có trong 5.3 và 5.4. Giữ kết luận ngắn theo kết quả đã đo; chuyển toàn bộ hạn chế/roadmap chi tiết về 5.4 hoặc phụ lục.
- Có lệch cấu hình: nhiều đoạn và bảng ghi “sáu robot”, trong khi mục tiêu hợp nhất hiện tại là năm robot. Cần chọn một cấu hình chính và ghi rõ nếu số liệu V21 cũ vẫn được giữ để đối chiếu.

## Thuật toán cần trình bày lại

Nên gom thành một mục duy nhất ở Chương 3:

1. **Mô hình lưới:** kho 28 × 28 m, ô 0,5 m, lưới 56 × 56, bốn hướng; kệ là ô cấm.
2. **A*:** `f(n)=g(n)+h(n)`, heuristic Manhattan; binary heap; chi phí cơ sở và chi phí mềm tránh robot.
3. **Chu trình nhiệm vụ:** `PICK → DROP → (job queue | RETURN) → DOCK_TURN → CHARGE`.
4. **CPA:** dự đoán trong 2,4 s, ngưỡng `DCPA < SAFE_GAP + 0,16`.
5. **Điều tốc:** `v_safe = sqrt(2 * BRAKE * d_free)`, `MAX_SPEED = 2,3 m/s`, `BRAKE = 2,7 m/s²`.
6. **Bảo vệ bước:** `f5AllowedMove` kiểm tra đoạn quét của mỗi frame; nếu không đạt `SAFE_GAP = 0,98 m` thì hủy bước.
7. **Phục hồi:** replan mỗi 2,6 s, cooperative detour, scan 360° sau 14 s và cooldown 25 s.

Mỗi thuật toán nên có: mục tiêu, đầu vào, đầu ra, giả mã ngắn, tham số, giới hạn và bằng chứng thử nghiệm. Tránh đặt lại cùng một công thức ở nhiều chương.

## `/exam`, `/logs`, `/evals`

Các phần này chưa tồn tại như heading hoặc thư mục trong DOCX. Đề xuất thêm một mục “Hồ sơ kiểm chứng” sau Chương 5 hoặc ở phụ lục:

- **Exam / Test protocol:** cấu hình, seed, phiên bản notebook, số lần lặp, điều kiện pass/fail.
- **Logs:** schema log gồm `timestamp`, `robot_id`, `phase`, `position`, `speed`, `event`, `conflict_count`, `collision_flag`, `distance_to_nearest`; nêu nơi xuất CSV.
- **Evals:** bảng chỉ số và tiêu chí: completion rate, makespan, ETA error, distance, blocked robot·s, replans, rejected moves, dmin, collisions; phân biệt “có cơ chế trong code” với “đã chứng minh bằng thử nghiệm”.

Chỉ số hiện có vẫn có giới hạn: mỗi kịch bản chủ yếu chạy một lần, dmin lấy mẫu theo thời gian chứ chưa phải kiểm tra tiếp xúc liên tục, và chưa có đối chứng bật/tắt từng thuật toán.

## Outline sau khi chỉnh

1. Lời mở đầu
2. Chương 1 – Cơ sở lý luận
3. Chương 2 – Mô hình và kiến trúc hệ thống
4. Chương 3 – Thuật toán và triển khai
5. Chương 4 – Quy trình vận hành
6. Chương 5 – Thực nghiệm, logs và evals
7. Chương 6 – Kết luận và kiến nghị
8. Tài liệu tham khảo
9. Phụ lục: exam/test protocol, schema logs, bảng kết quả đầy đủ, mã giả

## Kiểm tra sau chỉnh sửa

- Heading styles chỉ còn `Title`, `Subtitle`, `Heading 1`–`Heading 4`, `Normal`, `List Paragraph`, `Caption` và style bảng.
- Không còn chuỗi mục `5.3.1` lặp.
- Không còn hai bảng ma trận vấn đề giống nhau.
- TOC, danh mục bảng và danh mục hình được cập nhật.
- Render toàn bộ trang và kiểm tra không có tiêu đề treo, bảng tràn, công thức mất ký tự hoặc hình bị cắt.


## Kết quả sau chỉnh sửa

- Bản đầu ra: `tiểu luận ctuong smart_polished.docx`.
- Đã xóa khối 5.3 lặp và hai bảng ma trận trùng.
- Đã chuẩn hóa heading về `Title`, `Heading 1`–`Heading 3`, `Normal` và `List Paragraph`.
- Đã gộp phần thuật toán của Chương 4 thành quy trình thực thi, giữ công thức và tham số ở Chương 3.
- Đã thêm các mục `/exam`, `/logs`, `/evals` trong Chương 5 và template tương ứng trong repo.
- Kiểm chứng: 41 trang PDF render từ Word, 431 đoạn, 18 bảng, một mục 5.3.1 và một bảng ma trận vấn đề.
