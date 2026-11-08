# Tài liệu hợp nhất Smart Logistics AGV

Bộ tài liệu này gom các nguồn DOCX và ba notebook thành một đặc tả dùng cho mô hình nhà kho 3D có đúng **5 robot AGV**. Mục tiêu vận hành là nhận lệnh lấy hàng, đi theo FEFO, giao hàng, tránh vật cản tĩnh, tự nhường đường khi gặp robot khác và quay về trạm sạc sau khi hoàn tất hàng đợi.

## Nguồn đã chuyển sang Markdown

| File Markdown | Nguồn | Nội dung |
|---|---|---|
| [`01-tong-quan-mo-hinh.md`](01-tong-quan-mo-hinh.md) | `Smart_Logistics_AGV.docx` | Cơ sở lý luận, kiến trúc kho, thực thể, quy trình và phạm vi V21 |
| [`02-thuat-toan-va-quy-tac.md`](02-thuat-toan-va-quy-tac.md) | `Chương 3_3.5-3.6-3.7.docx` | Mô hình lưới, A*, chi phí tránh robot, CPA, phanh, điều phối và UI |
| [`03-ket-qua-thi-nghiem.md`](03-ket-qua-thi-nghiem.md) | `Bao_cao_Chuong_5_AGV_V21.docx` | Kịch bản TN01–TN07, số đo và giới hạn kiểm thử |
| [`04-quy-tac-xu-ly-xung-dot.md`](04-quy-tac-xu-ly-xung-dot.md) | `CÁC QUY TẮC XỬ LÝ XUNG ĐỘT TRONG VẬN HÀNH ROBOT.docx` | Bảng QT01–QT24 |
| [`notebook_inventory.md`](notebook_inventory.md) | Ba notebook trong repo | So sánh nguồn và quyết định hợp nhất |
| [`05-mo-hinh-hop-nhat.md`](05-mo-hinh-hop-nhat.md) | Đặc tả sau hợp nhất | Pipeline đích, trạng thái, tham số và tiêu chí nghiệm thu |

Hình ảnh nhúng trong DOCX được giữ tại [`assets/`](assets/), theo từng tài liệu nguồn.

## Notebook đích

[`output/jupyter-notebook/Warehouse_AGV_5Robot_AStar.ipynb`](../output/jupyter-notebook/Warehouse_AGV_5Robot_AStar.ipynb) là bản hợp nhất đã chuẩn hóa:

- Giữ pipeline dữ liệu Kaggle, FEFO, kệ hàng, cửa nhập/xuất, trạm sạc, tablet WMS, mini-map, inspect/relocate và xuất CSV.
- Dùng một đội **5 robot** và 5 ô sạc riêng.
- Dùng A* bốn hướng trên lưới 56×56 (28 m, ô 0,5 m) cho route preview và bộ lập kế hoạch đội.
- Dùng chi phí mềm tránh robot, dự đoán CPA, giới hạn vận tốc theo khoảng cách phanh và kiểm tra swept-gap trước mỗi bước.
- Có replan theo nhịp 2,6 s, detour khi bế tắc, scan 360° có giới hạn, hàng đợi theo robot và chỉ RETURN sau đơn cuối.
- Có ô kiểm tra tĩnh xác nhận fleet size, số ô sạc, A* và bộ bảo vệ va chạm.

## Chạy trên Kaggle hoặc Colab

1. Mở notebook đích.
2. Chạy từ trên xuống dưới.
3. Notebook tải `willianoliveiragibin/grocery-inventory` bằng `kagglehub` và chọn ngày vận hành từ hạn dùng thật trong dữ liệu.
4. Mở tablet WMS để chọn SKU, robot, điểm giao; bấm **XÁC NHẬN CHỌN** rồi **PHÁT LỆNH**.
5. Dùng mini-map và bảng lịch sử để quan sát lộ trình, trạng thái, thời gian, xung đột và va chạm.

Nếu CDN Three.js hoặc Kaggle không truy cập được, notebook vẫn hiển thị lỗi ở panel khởi tạo thay vì để màn hình đen. Cần chạy trong môi trường có `pandas`, `numpy`, `kagglehub` và hỗ trợ HTML/JavaScript.

## Quyết định hợp nhất

- `Warehouse_AGV_3D.ipynb` cung cấp nhà kho 3D/WMS đầy đủ nhưng chỉ có một AGV.
- `Draft_simul.ipynb` cung cấp ý tưởng A* theo thời gian và reservation cho năm AGV nhưng phần kho đơn giản.
- `NHÓM_1_SMART_LOG.ipynb` được dùng làm nền tích hợp vì đã có kho FEFO và bộ điều phối phản ứng; bản đích giảm đội hiện tại từ sáu xuống năm và chuyển route preview từ Dijkstra sang A*.

Các tài liệu V21 gốc mô tả sáu robot ở một số chương. Đây là số liệu của nguồn, không phải cấu hình đích; bản hợp nhất dùng đúng năm robot theo yêu cầu hiện tại. `IDEA.md` không có trong repository tại thời điểm kiểm tra nên nội dung ý tưởng được đối chiếu từ prompt, hai hình ảnh và các DOCX.
