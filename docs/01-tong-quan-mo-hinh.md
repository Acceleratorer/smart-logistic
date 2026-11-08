# Smart_Logistics_AGV

> Chuyển tự động từ `Smart_Logistics_AGV.docx`. Nội dung được giữ theo thứ tự đoạn và bảng; công thức/hình ảnh được lưu riêng khi DOCX có nhúng.
BÀI TIỂU LUẬN HỌC PHẦN

SMART LOGISTICS

TỐI ƯU HÓA TUYẾN ĐƯỜNG VÀ GIẢI QUYẾT XUNG ĐỘT TRONG VẬN HÀNH ROBOT TỰ HÀNH (AGV) TẠI NHÀ KHO THÔNG MINH

Bài nghiên cứu mô hình: Kho FEFO 3D – sáu robot AGV – phiên bản V21

Nhóm thực hiện: NHÓM 1

Giảng viên hướng dẫn: ..........................................................

Lớp/Học phần: ......................................................................

TP. Hồ Chí Minh, tháng 11 năm 2026

LỜI CAM KẾT VỀ PHẠM VI VÀ NGUỒN DỮ LIỆU

Tiểu luận được xây dựng từ khung phân công và phần mô tả kỹ thuật V21 trong tài liệu “TaskTable_SMART LOGISTICS.docx” do nhóm cung cấp; đồng thời tham khảo tài liệu khoa học, tiêu chuẩn kỹ thuật và tài liệu công nghệ được trích dẫn theo chuẩn APA. Thông tin về cơ chế đã triển khai được phân biệt với giải pháp đề xuất. Các bảng kết quả thí nghiệm chưa có dữ liệu đo được đều ghi rõ “Chưa đo”, không sử dụng số liệu giả định như số liệu thực nghiệm.

Đường dẫn notebook Colab của nhóm được ghi trong danh mục nguồn nội bộ. Tại thời điểm biên soạn, quyền truy cập trực tiếp nội dung notebook qua liên kết chưa được xác thực, vì vậy các mô tả về phiên bản V21 trong tiểu luận được đối chiếu theo phần phân tích kỹ thuật đính kèm, không được trình bày như kết quả kiểm thử độc lập trên notebook gốc.

TÓM TẮT

Trong quá trình chuyển đổi số logistics, năng lực xử lý đơn hàng của kho phụ thuộc không chỉ vào bố trí lưu trữ mà còn vào khả năng phối hợp phương tiện vận chuyển tự hành. Bài tiểu luận nghiên cứu một mô hình kho thông minh ba chiều có sáu robot AGV, hướng đến hai yêu cầu cốt lõi: xác lập hành trình lấy hàng – giao hàng – quay về trạm sạc và giảm xung đột trong không gian vận hành chung. Sản phẩm tham chiếu là mô hình V21 được mô tả trong tài liệu nhóm, sử dụng dữ liệu Grocery Inventory từ Kaggle, Python để tiền xử lý, JavaScript để điều phối và Three.js để mô phỏng hình học ba chiều.

Phương pháp được sử dụng gồm tổng hợp lý thuyết quản trị kho và tìm đường trên đồ thị; mô tả kiến trúc, dữ liệu và thuật toán; xây dựng quy trình vận hành; đề xuất các kịch bản thí nghiệm có khả năng lặp lại. Trên bản đồ lưới 28 × 28 m với bước lưới 0,5 m, hệ thống áp dụng A* kết hợp hàm chi phí hạn chế đi gần robot khác; lớp kiểm soát xung đột sử dụng dự đoán điểm tiếp cận gần nhất (CPA), giới hạn tốc độ theo khoảng cách phanh, kiểm tra chuyển động và cơ chế tìm đường lại. Ngoài ra, FEFO hỗ trợ ưu tiên quản lý hàng sắp hết hạn, hệ thống hàng đợi quản lý nhiều lệnh cho từng robot, và máy trạng thái điều khiển chu trình nhiệm vụ.

Kết quả phân tích cho thấy V21 đã có thiết kế hỗ trợ những chức năng điều hướng, điều tốc và giám sát quan trọng trong môi trường mô phỏng. Tuy nhiên, việc cài đặt cơ chế chưa đủ để khẳng định an toàn tuyệt đối hay tối ưu toàn cục, vì hệ thống chưa có cơ chế đặt chỗ không–thời gian hoàn chỉnh, điều phối đơn tự động và bộ số liệu thử nghiệm độc lập. Tiểu luận đề xuất chuẩn hóa định danh kệ, tích hợp giải thuật tìm đường đa tác tử, bổ sung cơ chế đánh giá an toàn và phát triển khả năng lưu dữ liệu bền vững.

Từ khóa: Smart Logistics; nhà kho thông minh; AGV; A*; Dijkstra; CPA; FEFO; mô phỏng 3D; điều phối đa robot.

DANH MỤC TỪ VIẾT TẮT

**Bảng 1. Danh mục chữ viết tắt dùng trong báo cáo**

### Bảng 1

| Viết tắt | Thuật ngữ tiếng Anh | Diễn giải tiếng Việt |
|---|---|---|
| AGV | Automated Guided Vehicle | Robot/phương tiện dẫn hướng tự động |
| AMR | Autonomous Mobile Robot | Robot di động tự chủ |
| WMS | Warehouse Management System | Hệ thống quản lý kho |
| FEFO | First Expired, First Out | Ưu tiên xuất hàng hết hạn trước |
| FIFO | First In, First Out | Nhập trước – xuất trước |
| A* | A-star Search | Thuật toán tìm đường có hàm ước lượng |
| CPA | Closest Point of Approach | Điểm/thời điểm tiếp cận gần nhất |
| MAPF | Multi-Agent Path Finding | Tìm đường đồng thời cho nhiều tác tử |
| CBS | Conflict-Based Search | Tìm kiếm dựa trên xung đột |
| SKU | Stock Keeping Unit | Mã nhận diện đơn vị hàng hóa |
| FPS | First-Person View | Chế độ quan sát góc nhìn thứ nhất |
| CSV | Comma-Separated Values | Tệp dữ liệu dạng giá trị phân cách bởi dấu phẩy |
| JSON | JavaScript Object Notation | Định dạng trao đổi dữ liệu |
| KPI | Key Performance Indicator | Chỉ số đánh giá hiệu quả |
| CDN | Content Delivery Network | Mạng phân phối nội dung |
| LiDAR | Light Detection and Ranging | Cảm biến đo khoảng cách bằng ánh sáng |

MỤC LỤC

LỜI MỞ ĐẦU

#### 1. Tính cấp thiết của đề tài  |  2. Tổng quan nghiên cứu  |  3. Mục tiêu

#### 4. Đối tượng và phạm vi  |  5. Phương pháp  |  6. Ý nghĩa  |  7. Kết cấu

# CHƯƠNG 1. CƠ SỞ LÝ LUẬN

1.1. Nhà kho và các mô hình tổ chức; 1.2. Số hóa và tự động hóa kho; 1.3. Robot AGV; 1.4. FEFO; 1.5. Biểu diễn không gian và khoảng cách; 1.6. Dijkstra và A*; 1.7. Xung đột và an toàn; 1.8. Chỉ số đánh giá

# CHƯƠNG 2. GIỚI THIỆU MÔ HÌNH

#### 2.1. Khái niệm và bài toán; 2.2. Cấu trúc logic; 2.3. Chức năng và đối tượng; 2.4. Ràng buộc và tiêu chí tối ưu

# CHƯƠNG 3. XÂY DỰNG MÔ HÌNH

3.1. Mục tiêu; 3.2. Kiến trúc tổng thể; 3.3. Công cụ và thư viện; 3.4. Dữ liệu đầu vào; 3.5. Thuật toán tìm đường; 3.6. Chống va chạm; 3.7. Điều phối nhiệm vụ; 3.8. Thiết kế giao diện

# CHƯƠNG 4. QUY TRÌNH VẬN HÀNH

4.1. Thiết lập môi trường; 4.2. Chuẩn hóa dữ liệu; 4.3. Tính khoảng cách; 4.4. Chống xung đột; 4.5. Chu trình tác nghiệp; 4.6. Giao diện và ghi nhận dữ liệu; 4.7. Các tình huống ngoại lệ

# CHƯƠNG 5. THÍ NGHIỆM VÀ ĐÁNH GIÁ

#### 5.1. Thiết lập thí nghiệm; 5.2. Chỉ số và phương pháp đo; 5.3. Biểu mẫu kết quả; 5.4. Đánh giá chức năng; 5.5. Hạn chế; 5.6. Định hướng phát triển

# CHƯƠNG 6. KẾT LUẬN VÀ KIẾN NGHỊ

TÀI LIỆU THAM KHẢO  |  PHỤ LỤC A–D

Mục lục được đánh số theo đúng 6 chương trong khung phân công của nhóm; số trang xem ở chân trang và có thể cập nhật bằng chức năng mục lục tự động trong Microsoft Word.

# LỜI MỞ ĐẦU

## 1. Tính cấp thiết của đề tài

Kho hàng đóng vai trò kết nối giữa cung ứng và phân phối: vừa tiếp nhận và bảo quản hàng hóa, vừa tổ chức lấy hàng để đáp ứng nhu cầu khách hàng. Trong điều kiện danh mục sản phẩm ngày càng đa dạng và yêu cầu giao nhận ngày càng nhanh, chi phí di chuyển nội bộ, độ chính xác của vị trí lưu trữ và khả năng tránh ùn tắc ở các tuyến giao cắt trở thành những nhân tố quan trọng đối với hiệu quả khai thác. Theo de Koster, Le-Duc và Roodbergen (2007), bài toán lấy hàng liên quan đồng thời đến thiết kế mặt bằng, bố trí sản phẩm, chọn tuyến và tổ chức thực hiện; tối ưu riêng một khâu khó có thể thay thế cho quản trị tổng thể.

Việc đưa robot AGV vào kho có thể giảm thao tác di chuyển lặp lại và giúp điều phối nhiệm vụ một cách có hệ thống. Tuy nhiên, khi nhiều robot cùng khai thác một hành lang hẹp hoặc cùng tiếp cận khu giao nhận, đường đi ngắn nhất của từng robot chưa chắc tạo thành phương án tốt cho cả đội. Hai AGV có thể đối đầu, giao cắt, bám đuôi hoặc cùng đợi một đoạn đường, khiến thời gian hoàn thành đơn tăng lên. Công trình về điều phối hàng trăm phương tiện tại kho của Wurman, D’Andrea và Mountz (2008) cho thấy vấn đề phối hợp đa robot là nền tảng quan trọng của kho tự động hóa quy mô lớn.

Từ thực tiễn đó, nhóm lựa chọn đề tài “Tối ưu hóa tuyến đường và giải quyết xung đột trong vận hành robot tự hành (AGV) tại nhà kho thông minh”, sử dụng mô hình mô phỏng V21 làm trường hợp nghiên cứu. Đề tài vừa thể hiện mối liên hệ giữa quản trị logistics và kỹ thuật thuật toán, vừa tạo điều kiện đánh giá rõ tính khả thi và những giới hạn chưa được kiểm chứng của một nguyên mẫu phần mềm.

## 2. Tổng quan về tình hình nghiên cứu

Ở bình diện tổ chức kho, de Koster và cộng sự (2007) hệ thống hóa các quyết định thiết kế mặt bằng, lưu trữ, phân vùng và định tuyến lấy hàng. Ở bình diện triển khai tự động hóa, Wurman và cộng sự (2008) giới thiệu những thách thức vận hành đội robot quy mô lớn. Những nền tảng này chỉ ra hai hướng nghiên cứu có quan hệ chặt chẽ: lựa chọn đường đi hiệu quả và phối hợp nhiều phương tiện để tránh cản trở lẫn nhau.

Về thuật toán, Dijkstra (1959) giải quyết bài toán đường đi ngắn nhất trên đồ thị có trọng số không âm; Hart, Nilsson và Raphael (1968) phát triển A* kết hợp chi phí đã đi và chi phí ước lượng tới đích nhằm tăng hiệu quả tìm kiếm. Đối với môi trường nhiều phương tiện, Silver (2005) đề xuất Cooperative A* cùng các biến thể tìm kiếm không–thời gian, còn Sharon và cộng sự (2015) nghiên cứu Conflict-Based Search cho bài toán tìm đường đa tác tử. Những nghiên cứu này là cơ sở để đối chiếu cơ chế tìm đường có trọng số né robot của V21 với hướng phối hợp lộ trình ở cấp đội robot.

Đối với hàng hóa có hạn sử dụng, chính sách FEFO ưu tiên đơn vị gần tới ngày hết hạn; nguyên tắc này không đồng nhất với FIFO dựa vào thời gian nhập kho. Các nghiên cứu về quản trị hạn sử dụng cho thấy yêu cầu thông tin về tuổi sản phẩm và trạng thái chất lượng là một thành phần thiết yếu của quản trị tồn kho dễ hỏng (Hertog et al., 2014).

Từ những cơ sở trên, khoảng trống của nguyên mẫu nghiên cứu không nằm ở việc chỉ thêm một thuật toán tìm đường, mà ở khả năng tích hợp dữ liệu hàng tồn, lập kế hoạch đường đi, điều khiển thời gian thực và kiểm chứng khách quan tính an toàn trong cùng một mô hình mô phỏng.

## 3. Mục tiêu nghiên cứu

Mục tiêu tổng quát là phân tích và hệ thống hóa phương pháp xây dựng mô hình kho thông minh ứng dụng AGV, hướng tới tối ưu hành trình xử lý đơn và hạn chế các tình huống xung đột khi sáu robot hoạt động đồng thời.

- Hệ thống hóa lý thuyết về nhà kho, tự động hóa, FEFO, đồ thị và thuật toán tìm đường Dijkstra – A*.

- Mô tả đúng kiến trúc V21, nguồn dữ liệu, cách biểu diễn kho và vòng đời của một nhiệm vụ lấy hàng.

- Phân tích cơ chế dự đoán xung đột, điều tốc, kiểm tra bước đi, tìm đường lại và hàng đợi nhiệm vụ.

- Đề xuất thiết kế thí nghiệm có chỉ tiêu rõ ràng để kiểm chứng mức độ hoàn thành, năng suất và an toàn.

- Nhận diện giới hạn hiện tại và định hướng mở rộng theo thuật toán tìm đường đa robot có ràng buộc thời gian.

## 4. Đối tượng và phạm vi nghiên cứu

Đối tượng nghiên cứu là mô hình điều phối sáu AGV trong kho FEFO 3D, tập trung vào quãng đường, thời gian thực hiện, xung đột giao thông nội bộ và cơ chế hỗ trợ người vận hành. Không gian mô phỏng theo tài liệu nhóm có kích thước 28 × 28 m, được chia thành các ô lưới cạnh 0,5 m. Tác nghiệp quan sát gồm lựa chọn SKU, xác định robot, đặt điểm giao, phát lệnh, di chuyển đến kệ, giao hàng, thực hiện các đơn chờ và trở về trạm sạc.

Phạm vi là nghiên cứu thuật toán và phần mềm mô phỏng trong trình duyệt; không bao gồm chế tạo AGV vật lý, đo cảm biến thực, kiểm định thiết bị theo tiêu chuẩn an toàn hoặc triển khai quản lý tồn kho tại doanh nghiệp. Dijkstra được sử dụng làm thuật toán đối chứng về lý thuyết, không trình bày như một chức năng đã tích hợp trong V21. Những số liệu định lượng không có trong tài liệu sẽ được để trống để nhóm chạy thực nghiệm bổ sung.

## 5. Phương pháp nghiên cứu

Tiểu luận sử dụng phương pháp nghiên cứu tài liệu và so sánh để hình thành khung lý thuyết; phương pháp phân tích hệ thống để tách các lớp dữ liệu, điều phối và trình diễn; phương pháp mô hình hóa bằng đồ thị để mô tả không gian di chuyển; phương pháp phân tích thuật toán để giải thích A*, CPA và điều tốc; cuối cùng là phương pháp thực nghiệm có đối chứng nhằm xây dựng quy trình kiểm tra cho một, ba và sáu robot. Việc đối chiếu mô tả mã nguồn dựa trên tài liệu kỹ thuật V21 do nhóm cung cấp.

## 6. Ý nghĩa khoa học và thực tiễn

Về khoa học, đề tài minh họa cách biến một bài toán logistics thành bài toán tối ưu đường đi có ràng buộc động, đồng thời làm rõ sự khác nhau giữa đường đi ngắn nhất của một robot và tính khả thi khi nhiều robot hoạt động đồng thời. Về thực tiễn, mô hình giúp thử nghiệm cách tổ chức lấy hàng, quan sát điểm nghẽn, đào tạo người vận hành và xác lập các chỉ số đánh giá trước khi đầu tư thiết bị thực. Giá trị của mô phỏng nằm ở hỗ trợ ra quyết định và kiểm chứng giả thuyết, không nằm ở việc thay thế các thử nghiệm an toàn khi triển khai thực tế.

## 7. Kết cấu tiểu luận

Ngoài phần mở đầu, tài liệu tham khảo và phụ lục, tiểu luận gồm sáu chương theo đúng phân công: Chương 1 trình bày cơ sở lý luận; Chương 2 giới thiệu bài toán và cấu trúc logic của mô hình; Chương 3 phân tích việc xây dựng dữ liệu, thuật toán và giao diện; Chương 4 mô tả quy trình vận hành; Chương 5 thiết kế thí nghiệm, đánh giá và đề xuất phát triển; Chương 6 tổng hợp kết luận và kiến nghị.

# CHƯƠNG 1. CƠ SỞ LÝ LUẬN

## 1.1. Khái niệm và vai trò của nhà kho

Nhà kho là một mắt xích của hệ thống logistics, nơi diễn ra các hoạt động tiếp nhận, kiểm tra, định vị, lưu trữ, bảo quản, lấy hàng, tập kết và xuất hàng. Mục tiêu quản trị không đơn thuần là tối đa lượng hàng lưu trữ mà phải cân bằng công suất phục vụ, độ chính xác, chi phí và an toàn. Đối với kho có lưu lượng đơn lớn, thời gian di chuyển để tiếp cận đúng vị trí lưu trữ thường làm tăng đáng kể thời gian hoàn thành một đơn; vì vậy bố trí luồng giao thông nội bộ và tổ chức đơn hàng phải được nghiên cứu song song.

Một chu trình kho có thể khái quát thành: Inbound (tiếp nhận) → kiểm đếm/kiểm tra → put-away (đưa vào vị trí) → bảo quản và quản lý tồn → picking (lấy hàng) → staging (tập kết) → Despatch (xuất/giao). Ở từng bước, WMS cung cấp mã vị trí, mã SKU và trạng thái đơn để bảo đảm dòng hàng hóa phù hợp với dòng thông tin. Nếu thiếu đồng bộ giữa vị trí vật lý và dữ liệu số, thuật toán định tuyến dù tốt cũng có thể đưa robot đến sai kệ.

## 1.2. Các mô hình nhà kho và quá trình chuyển đổi số

**Bảng 2. So sánh các mức độ phát triển nhà kho**

### Bảng 2

| Mô hình kho | Đặc trưng vận hành | Lợi thế | Hạn chế chính |
|---|---|---|---|
| Thủ công | Nhân viên sử dụng giấy tờ, xe đẩy, xe nâng | Chi phí đầu tư ban đầu thấp | Phụ thuộc lao động; khó theo dõi thời gian thực |
| Bán tự động | WMS kết hợp barcode/RFID và một phần cơ giới hóa | Tăng độ chính xác và truy xuất | Dữ liệu và thiết bị có thể thiếu đồng bộ |
| Tự động hóa | Băng chuyền, hệ thống lấy hàng và AGV/AMR | Giảm thao tác lặp và tăng tính nhất quán | Đòi hỏi vốn, bảo trì, điều phối phức tạp |
| Kho thông minh | Dữ liệu, thuật toán, cảm biến và trực quan hóa phối hợp | Hỗ trợ tối ưu và giám sát tức thời | Phụ thuộc chất lượng dữ liệu và bảo mật |

Tự động hóa tập trung thay thế hoặc hỗ trợ thao tác vật lý; số hóa tập trung biến trạng thái hàng hóa, tuyến đường và nhiệm vụ thành dữ liệu có thể phân tích. Một nhà kho thông minh cần đồng thời có (i) lớp đối tượng vật lý như kệ, hàng, xe, cửa; (ii) lớp thu nhận dữ liệu như barcode, RFID hoặc cảm biến; (iii) lớp xử lý như WMS, tối ưu và điều phối; (iv) lớp giao diện phục vụ thao tác và theo dõi. Trong V21, phần thu nhận dữ liệu cảm biến thực chưa tồn tại; các vị trí và va chạm được tính từ mô hình toán học.

## 1.3. Robot AGV trong logistics

AGV là phương tiện vận chuyển tự động theo tuyến hoặc quy tắc điều hướng đã xác lập. Một hệ AGV hoàn chỉnh thường có bộ điều khiển chuyển động, cơ cấu truyền động, năng lượng, phương tiện xác định vị trí, cơ chế phát hiện vật cản, bộ điều phối và giao diện giám sát. Khác với AGV vận hành vật lý, robot 3D trong V21 là đối tượng phần mềm được cập nhật tọa độ theo từng khung hình. Vì thế các tham số như tốc độ, gia tốc hay bán kính an toàn là tham số mô phỏng và không phải thông số được chứng nhận của một phương tiện thương mại.

Vận hành đồng thời nhiều AGV đem lại lợi ích tiềm năng về thông lượng nhưng nảy sinh các xung đột: đối đầu trong hành lang chỉ đủ một xe, hai xe cắt nhau ở ngã giao, một xe phía sau bị chặn bởi xe phía trước và nhiều xe cùng đi vào khu vực nhận/trả hàng. Một cơ chế hiệu quả cần không chỉ phát hiện giao cắt, mà còn quyết định xe nào được quyền đi trước và tránh tình trạng cả hai cùng chờ.

## 1.4. Nguyên tắc FEFO và quản trị hàng có hạn sử dụng

FEFO (First Expired, First Out) ưu tiên xuất đơn vị sản phẩm có ngày hết hạn sớm hơn, với điều kiện hàng còn phù hợp để sử dụng. FEFO khác FIFO: một lô nhập kho muộn hơn vẫn có thể cần xuất trước nếu ngày hết hạn đến sớm. Trong hệ thống mô phỏng, số ngày còn hạn được tính bằng chênh lệch giữa ngày hết hạn và ngày vận hành. Mục tiêu chính là làm rõ thứ tự ưu tiên, chưa phải tối ưu toàn bộ vòng đời tồn kho theo thời gian và điều kiện bảo quản.

Dᵢ = Eᵢ − T   (đơn vị: ngày)

Trong đó Dᵢ là số ngày còn hạn của sản phẩm i; Eᵢ là ngày hết hạn; T là ngày vận hành mô phỏng. Theo tài liệu V21, hàng hợp lệ được phân thành ba nhóm: 0–15 ngày (đỏ, ưu tiên cao), 16–45 ngày (vàng, mức trung bình), trên 45 ngày (xanh, chưa gấp). Hàng đã quá hạn hoặc không còn tồn kho được loại khỏi danh sách hoạt động. Đây là ngưỡng dùng cho sản phẩm của nhóm, không mặc nhiên là quy chuẩn nghiệp vụ cho mọi loại hàng.

Điểm cần phân biệt là V21 sắp xếp và biểu diễn trực quan theo FEFO, nhưng người vận hành vẫn có thể chủ động chọn SKU. Bởi vậy chưa thể kết luận rằng mọi lệnh xuất trong hệ thống đều bị ràng buộc bởi chính sách FEFO bắt buộc. Nếu muốn chuyển thành chức năng kiểm soát nghiệp vụ, cần xét hạn dùng theo từng lô, số lượng tồn khả dụng, đơn hàng khách và quy tắc ngoại lệ.

## 1.5. Biểu diễn không gian và lý thuyết khoảng cách

Để robot tìm đường, mặt bằng kho được biểu diễn thành một đồ thị G=(V,E), trong đó V là tập các vị trí robot có thể đứng và E là tập các cặp vị trí có thể di chuyển trực tiếp. Mỗi cạnh mang chi phí c(u,v) không âm, có thể đại diện cho độ dài, thời gian hoặc mức phạt rủi ro. Tại V21, kho dài 28 m và rộng 28 m, bước lưới 0,5 m tạo thành 56 × 56 = 3.136 ô. Các vùng kệ, tường và vật cản cố định được gắn nhãn không thể đi qua; robot được phép chuyển sang bốn ô kề theo phương ngang/dọc.

dₑ(A,B) = √[(x₂−x₁)² + (z₂−z₁)²]

dₘ(A,B) = |x₂−x₁| + |z₂−z₁|

Khoảng cách Euclid dₑ phản ánh chiều dài đoạn thẳng giữa hai điểm trong mặt phẳng, còn Manhattan dₘ phản ánh tổng độ lệch theo hai trục vuông góc. Với quy tắc di chuyển bốn hướng và chi phí mỗi ô ngang bằng nhau, Manhattan là hàm ước lượng thích hợp cho A* vì không vượt quá chi phí đường đi ngắn nhất khi không có chi phí cạnh thấp hơn bước lưới tương ứng; vì thế là một heuristic chấp nhận được trong giả thiết thông thường. Khi vật cản xuất hiện, tuyến đi thực tế dài hơn hoặc bằng đường không vật cản.

Ví dụ về chuyển đổi lưới: nếu hai ô cách nhau 12 bước theo x và 8 bước theo z thì độ dài Manhattan trên mặt bằng là (12+8)×0,5 = 10 m khi không có vật cản. Đây chỉ là ví dụ lý thuyết; tuyến đường trong kho phải được tính sau khi loại các ô không đi được và có thể thay đổi theo vị trí những robot khác.

## 1.6. Cơ sở của thuật toán Dijkstra và A*

Dijkstra lựa chọn nút có tổng chi phí tạm thời thấp nhất từ nguồn, sau đó cập nhật chi phí tới các nút kề. Với trọng số cạnh không âm, thuật toán tìm đường tối ưu theo tổng trọng số; tuy nhiên nó không sử dụng thông tin về hướng đích để ưu tiên mở rộng. Đối với bài toán chỉ một điểm nguồn–đích trên lưới lớn, Dijkstra có thể duyệt nhiều vị trí không cần thiết.

A* bổ sung hàm ước lượng h(n) từ vị trí hiện tại đến đích. Một nút được đánh giá bằng f(n)=g(n)+h(n), trong đó g(n) là chi phí đã tích lũy từ nguồn. Khi h không vượt quá chi phí thực còn lại và cách cài đặt phù hợp, A* có cơ sở tìm được đường đi tối ưu theo hàm chi phí đã định nghĩa (Hart et al., 1968). Nếu chuyển sang chi phí gồm rủi ro giao thông, “tối ưu” phải hiểu là tối thiểu hàm chi phí tổng hợp, không đồng nghĩa quãng đường hình học luôn ngắn nhất.

f(n) = g(n) + h(n)

h(n) = |xₙ − xg| + |zₙ − zg|

**Bảng 3. Đối chiếu Dijkstra và A* trong phạm vi đề tài**

### Bảng 3

| Tiêu chí | Dijkstra | A* trong V21 |
|---|---|---|
| Thông tin sử dụng | Chi phí từ nguồn g(n) | g(n) cộng ước lượng h(n) |
| Khả năng định hướng tới đích | Không trực tiếp | Có, nhờ Manhattan |
| Ràng buộc vật cản | Loại bỏ ô không đi được | Loại bỏ ô không đi được |
| Robot khác | Cần mô hình thêm | Cộng phạt khi đi gần robot khác |
| Vai trò trong đề tài | Mốc đối chiếu lý thuyết | Thuật toán triển khai được tài liệu mô tả |

## 1.7. Xung đột, va chạm và nguyên tắc an toàn

Xung đột giao thông trong mô phỏng là tình huống các nhiệm vụ hoặc chuyển động yêu cầu dùng chung một không gian theo cách không tương thích. Va chạm là trường hợp có sự chồng lấn hình học vượt ngưỡng cho phép trong mô hình va chạm. Việc robot dừng hoặc giảm tốc do một robot khác cản đường không tự động đồng nghĩa đã xảy ra va chạm. Phân biệt hai khái niệm là yêu cầu cơ bản khi thiết kế chỉ số và trình bày kết quả.

CPA dùng vị trí tương đối r⃗ và vận tốc tương đối v⃗r để tính thời điểm hai robot đến gần nhau nhất trong một cửa sổ dự đoán T. Nếu hai robot không đổi vận tốc trong khoảng dự đoán, khoảng cách tại thời điểm CPA có thể được dùng như cảnh báo sớm. V21 sử dụng T = 2,4 giây và kết hợp kết quả đó với ngưỡng khoảng cách an toàn. Phép dự đoán này vẫn có sai số nếu robot bất ngờ rẽ, tăng tốc hoặc xuất hiện vật cản mới.

tCPA = clamp[ −(r⃗ · v⃗r)/‖v⃗r‖², 0, T ]

dCPA = ‖r⃗ + v⃗r·tCPA‖

Từ lý thuyết động học v² = 2as (đối với giảm tốc đều đến khi dừng), có thể tính vận tốc trần theo khoảng trống phía trước: v_safe = √(2a_brake·d_free). Dù hữu ích cho mô phỏng, biểu thức này chưa bao gồm độ trễ cảm biến, thời gian phản hồi, độ bám sàn, kích thước thực, tải trọng hay sai số định vị. ISO 3691-4:2023 quy định các yêu cầu an toàn và kiểm chứng đối với phương tiện công nghiệp không người lái; nguyên mẫu phần mềm V21 chưa phải đối tượng đã được chứng nhận theo tiêu chuẩn này.

v_safe = √(2 a_brake · d_free)

## 1.8. Hệ thống chỉ số đánh giá vận hành AGV

Một mô hình đánh giá hợp lý phải ghi nhận cả hiệu suất và an toàn. Nhóm hiệu suất gồm tỷ lệ hoàn thành đơn, thời gian trung bình, độ dài hành trình, thông lượng và thời gian chờ. Nhóm an toàn gồm số lần xung đột, số lần vi phạm khoảng cách tối thiểu và va chạm được đo độc lập. Nhóm tin cậy gồm tỷ lệ tìm được đường, thời gian bế tắc và khả năng phục hồi khi bị chặn. Các chỉ số này cần cùng một định nghĩa thời điểm bắt đầu–kết thúc; nếu không, kết quả ở các lần chạy khó so sánh.

# CHƯƠNG 2. GIỚI THIỆU MÔ HÌNH TỐI ƯU TUYẾN ĐƯỜNG VÀ GIẢI QUYẾT XUNG ĐỘT

## 2.1. Khái niệm và bài toán mô hình hóa

Mô hình nghiên cứu là một kho hàng mô phỏng ba chiều, trong đó sáu AGV đại diện cho những phương tiện thực hiện nhiệm vụ lấy hàng và vận chuyển đến vị trí giao. Người vận hành chủ động chọn sản phẩm, robot nhận lệnh và đích giao; hệ thống có trách nhiệm xác lập tuyến đường hợp lệ, cập nhật chuyển động và tránh các điều kiện vận hành nguy hiểm theo những quy tắc được cài đặt. Hàng hóa được sắp xếp trực quan theo FEFO để làm rõ quan hệ giữa thông tin tồn kho và hoạt động thực hiện đơn.

Bài toán thứ nhất là lập kế hoạch cho mỗi nhiệm vụ: từ vị trí ban đầu hoặc trạm sạc tới ô lấy hàng (PICK), từ ô lấy hàng tới vị trí giao (DROP), sau đó nhận đơn tiếp theo hoặc quay về (RETURN). Cùng một vị trí đích có thể có nhiều tuyến khả thi vì kệ chặn đường thẳng. Do đó, robot cần đường đi trên lưới có chi phí hợp lý, chứ không đơn giản di chuyển theo vectơ nối hai điểm.

Bài toán thứ hai là phối hợp nhiều robot trong một vùng kho chung. Khi các tuyến khả thi về mặt tĩnh giao nhau, robot có thể cùng muốn đi vào một ngã giao hoặc hành lang hẹp. Việc tính toán tuyến đường không tính yếu tố thời gian có thể khiến robot dừng kéo dài. Mô hình V21 sử dụng nhiều lớp xử lý như phạt chi phí gần robot, CPA, giới hạn tốc độ, kiểm tra bước đi và tìm đường lại nhằm giảm tình huống này; tuy nhiên đây chưa phải cơ chế tối ưu đa robot theo thời gian có chứng minh an toàn tuyệt đối.

## 2.2. Cấu trúc logic của mô hình

Tài liệu V21 xác định chuỗi thành phần chính: nguồn CSV từ Kaggle → Python xử lý dữ liệu → JavaScript khởi tạo mô phỏng và xử lý nhiệm vụ → Three.js hiển thị môi trường 3D → Tablet WMS để người dùng thao tác và theo dõi. Trong kiến trúc này, Python vận hành trước khi dựng giao diện để chuẩn hóa hàng tồn; JavaScript là nơi cập nhật vị trí và trạng thái robot trong vòng lặp hoạt ảnh. Vì vậy tên gọi “back-end” được dùng theo nghĩa logic điều khiển mô phỏng, không phải một máy chủ REST API độc lập.

**Hình 1. Sơ đồ kiến trúc logic của mô hình kho thông minh V21 (nhóm tổng hợp)**

Cấu trúc trên có tính mô-đun về chức năng nhưng hiện chưa tách hoàn chỉnh thành các dịch vụ độc lập. Lợi thế là người dùng có thể chạy mô phỏng trong môi trường Colab và xem kết quả trực quan, nhưng dữ liệu lịch sử chưa được lưu trên cơ sở dữ liệu bền vững. Việc tải lại trang có thể làm mất lịch sử chưa xuất tệp.

## 2.3. Các thực thể và quan hệ dữ liệu

Bốn nhóm đối tượng quan trọng là hàng hóa, vị trí/kệ, robot và nhiệm vụ. Hàng hóa có Product ID, SKU hoặc tên, số lượng tồn và ngày hết hạn; vị trí có mã kệ và tọa độ; robot có ID, trạng thái, pin, vị trí, tốc độ và danh sách lệnh; nhiệm vụ liên kết robot với một đơn vị hàng, vị trí lấy, vị trí giao và các mốc thời gian. Hệ thống cũng có danh sách những vị trí đã được chọn vào hàng đợi hoặc đang được robot giữ để giảm nguy cơ hai robot cùng lấy một ô.

**Bảng 4. Các đối tượng dữ liệu chính trong mô hình**

### Bảng 4

| Đối tượng | Thuộc tính sử dụng | Ý nghĩa |
|---|---|---|
| Inventory item | Product_ID; Product_Name; Expiration_Date; Stock_Quantity | Nguồn thông tin FEFO |
| Slot / Rack | slotId; rowIdx; bay; level; x; z | Định vị kiện hàng và đường tránh kệ |
| Robot | id; position; speed; battery; phase | Theo dõi trạng thái tác nghiệp |
| Job | slotId; sku; robotId; destination | Yêu cầu lấy hàng và giao hàng |
| Task history | robot; sku; estimated; actual; meters; conflicts; collisions | Phân tích hiệu quả sau tác nghiệp |

Một rủi ro dữ liệu đáng chú ý là mã vị trí trong tài liệu V21 có thể được hình thành chỉ từ dãy và tầng, trong khi mỗi dãy có nhiều ngăn. Những ô trên cùng dãy và tầng vì thế có nguy cơ trùng mã hiển thị. Nhóm đề xuất định danh gồm dãy–ngăn–tầng, chẳng hạn H03-B05-T02, đồng thời lưu một slotId duy nhất trong hệ thống để ngăn phát nhầm lệnh.

## 2.4. Phạm vi chức năng của sản phẩm

**Bảng 5. Ma trận chức năng và phạm vi đánh giá**

### Bảng 5

| Nhóm chức năng | Mô tả | Trạng thái theo tài liệu V21 |
|---|---|---|
| Quản lý hàng | Tải CSV; lọc; phân nhóm FEFO; hiển thị kiện | Có mô tả triển khai |
| Tìm đường | Từ robot tới PICK, DROP, RETURN theo A* | Có mô tả triển khai |
| Tránh xung đột | CPA; giới hạn tốc độ; kiểm tra bước đi | Có mô tả triển khai |
| Phục hồi bế tắc | Tìm đường lại, detour, quét 360° mô phỏng | Có mô tả triển khai |
| Đa nhiệm | Hàng đợi nhiều SKU cho từng robot | Có mô tả triển khai |
| Giám sát | FPS, 3D quản lý, minimap, Tablet WMS | Có mô tả triển khai |
| Đánh giá | Ghi log lịch sử và xuất CSV | Có mô tả triển khai; chưa có số đo |
| Tự chọn robot tối ưu | Tự phân công theo pin, vị trí, tải | Chưa triển khai theo tài liệu |
| MAPF không–thời gian | Đặt chỗ ô theo từng thời điểm | Đề xuất phát triển |

## 2.5. Bố cục mặt bằng mô phỏng

Theo tài liệu kỹ thuật, kho có kích thước 28 × 28 m, bao gồm các dãy kệ nhiều tầng, khu Inbound, khu Despatch và trạm sạc bố trí dọc tường. Robot chạy trên mặt sàn, vì vậy bản đồ đi lại là lưới hai chiều x–z; trục đứng chỉ phục vụ mô tả tầng hàng và đối tượng 3D. Cách biểu diễn này giúp giảm độ phức tạp tính toán khi mục tiêu nghiên cứu là điều phối chuyển động trên mặt bằng.

Phiên bản V21 đã bỏ một kệ tập kết nhỏ gần lối Inbound để hành lang nhập hàng thông thoáng hơn, trong khi kệ tập kết ở Despatch vẫn được giữ lại. Đây là thay đổi bố cục tĩnh có thể làm thay đổi đường đi và nguy cơ cản trở. Tuy nhiên việc bỏ kệ chưa tự động chứng minh hiệu suất tốt hơn; để đánh giá cần so sánh hai phiên bản với bộ lệnh và vị trí hàng có thể đối chiếu.

## 2.6. Mục tiêu tối ưu và ràng buộc

Từ góc độ vận trù học, chi phí tổng hợp của một nhiệm vụ có thể phân thành chi phí đường đi, chi phí thời gian chờ và chi phí rủi ro xung đột. Một dạng hàm mục tiêu đề xuất cho giai đoạn phát triển tiếp theo là J = αL + βW + γC, trong đó L là độ dài hành trình, W là thời gian chờ và C là mức phạt xung đột; α, β, γ là trọng số cần hiệu chỉnh bằng dữ liệu thực nghiệm. Đây là cách diễn đạt mục tiêu nghiên cứu, không phải một hàm mục tiêu được chứng minh đã có sẵn trong V21.

Đề xuất: min J = αL + βW + γC, với α, β, γ ≥ 0

Các ràng buộc thiết yếu gồm: robot chỉ di chuyển qua ô hợp lệ; không chiếm vùng kệ hoặc tường; giữ khoảng cách phù hợp; không nhận cùng một ô hàng đang bị giữ chỗ; tốc độ không vượt giới hạn mô phỏng; chỉ giao hàng sau khi đã tới điểm PICK; và sau khi hoàn thành tất cả đơn thì robot quay về trạng thái sẵn sàng. Khi phát triển MAPF, bổ sung ràng buộc mỗi ô và cạnh chuyển tiếp không được có xung đột theo bước thời gian.

## 2.7. Chu trình logic xử lý một lệnh

**Hình 2. Chu trình nhiệm vụ từ phát lệnh đến trở về sạc theo mô tả V21**

Quy trình thể hiện tư duy điều khiển theo trạng thái (Finite State Machine). Ở mỗi bước, điều kiện chuyển tiếp được kiểm tra thay vì giả định robot luôn đến đích thành công. Điều này tạo cơ sở để mô hình có thể dừng, chờ, tìm đường lại hoặc chấp nhận đơn tiếp theo tùy vào tình hình giao thông kho.

# CHƯƠNG 3. XÂY DỰNG MÔ HÌNH TỐI ƯU TUYẾN ĐƯỜNG VÀ CHỐNG VA CHẠM

## 3.1. Mục tiêu và yêu cầu thiết kế

Thiết kế mô hình nhằm tái hiện rõ tương tác giữa người vận hành, dữ liệu tồn kho, robot và các khu chức năng, đồng thời duy trì nguyên tắc dùng chung thuật toán cho cả sáu robot. Những yêu cầu ưu tiên là tính đúng đắn của dữ liệu đầu vào, khả năng đi qua hành lang có vật cản tĩnh, khả năng xử lý nhiều lệnh liên tiếp và quan sát được trạng thái khi xung đột phát sinh. Hệ thống cần bảo đảm rằng mỗi chức năng có thể được kiểm tra độc lập trước khi đánh giá hiệu quả toàn đội.

## 3.2. Kiến trúc tổng thể

Kiến trúc V21 gồm hai pha logic. Ở pha chuẩn bị, Python tải tập dữ liệu, kiểm tra cột bắt buộc, chuyển ngày hết hạn, lọc sản phẩm và tạo cấu trúc JSON cho trình duyệt. Ở pha mô phỏng, JavaScript dựng hình kho, xác định các ô lưới di chuyển, khởi tạo đối tượng robot và chạy vòng lặp cập nhật theo khung hình. Three.js đảm nhận cảnh 3D; lớp HTML/CSS tạo giao diện và các bảng điều khiển. Sự phân pha này làm giảm khối lượng xử lý dữ liệu trực tiếp trong vòng lặp hoạt ảnh.

Trong quá trình vận hành, vòng lặp animate() cập nhật thời gian delta rồi thực hiện hàm cập nhật đội robot, ví dụ updateFiveFleet(delta) trong tài liệu V21. Tên hàm có chữ “Five” là dấu vết đặt tên của phiên bản trước; cách xác định số robot ở mức thực thi cần dựa vào phần tử của mảng fleet5, không căn cứ vào tên hàm. Theo mô tả, mảng hiện chứa sáu robot cùng logic trạng thái.

## 3.3. Các thư viện và công cụ cần thiết

**Bảng 6. Môi trường phần mềm được tài liệu V21 mô tả**

### Bảng 6

| Công cụ / thư viện | Vai trò | Ghi chú khi thiết lập |
|---|---|---|
| Google Colab / Python 3 | Thực thi khối chuẩn bị dữ liệu | Môi trường notebook; cần quyền chạy |
| kagglehub | Tải Grocery Inventory | Có thể cần cài pip |
| pandas | Đọc CSV và lọc bản ghi | Thường có sẵn trong Colab |
| numpy | Xử lý mảng ngày và đếm theo ngưỡng | Thường có sẵn trong Colab |
| os; glob | Tìm vị trí tệp | Thư viện chuẩn Python |
| json; base64 | Đưa dữ liệu/HTML vào trang | Thư viện chuẩn Python |
| IPython.display | Nhúng mô phỏng trong notebook | Thư viện môi trường Colab |
| Three.js | Tạo kho, kệ, robot, đường 3D | Tải bằng CDN theo tài liệu |
| Tailwind CSS | Bố cục giao diện | Tải bằng CDN |
| Font Awesome | Biểu tượng điều khiển | Tải bằng CDN |

Lệnh cài tối thiểu được nhóm đưa ra là %pip install -q kagglehub. Những thư viện os, glob, json và base64 thuộc thư viện chuẩn; không cần cài riêng. Khi chạy lại trên môi trường mới, cần kiểm tra phiên bản và tài nguyên CDN để hạn chế thay đổi bất ngờ do phụ thuộc ngoài. Việc sử dụng CDN còn đòi hỏi kết nối mạng ở phía trình duyệt để tải tập lệnh và CSS.

%pip install -q kagglehub

import os, glob, json, base64

import pandas as pd

import numpy as np

import kagglehub

Thư viện kagglehub cung cấp hàm dataset_download() để lấy một tập dữ liệu và trả về vị trí lưu trữ cục bộ; tài liệu chính thức được công bố trong kho mã của Kaggle. Three.js là thư viện phục vụ xây dựng cảnh 3D trên web, quản lý đối tượng, camera, ánh sáng và vật liệu (Kaggle, n.d.; Three.js, n.d.).

## 3.4. Thiết kế dữ liệu đầu vào và xử lý dữ liệu

### 3.4.1. Nguồn dữ liệu và trường bắt buộc

Nguồn dữ liệu của V21 được khai báo bằng tên bộ dữ liệu “willianoliveiragibin/grocery-inventory” và đọc từ tệp CSV. Những trường bắt buộc theo tài liệu gồm Product_ID, Product_Name, Expiration_Date và Stock_Quantity. Khi triển khai lại, cần đối chiếu tên trường thực tế, mã hóa văn bản, kiểu ngày tháng và đơn vị số lượng; không nên giả định mọi phiên bản dữ liệu đều có cấu trúc không đổi.

dataset_path = kagglehub.dataset_download(

"willianoliveiragibin/grocery-inventory"

)

csv_files = sorted(glob.glob(

os.path.join(dataset_path, "**", "*.csv"), recursive=True

))

### 3.4.2. Chuẩn hóa và làm sạch

Quy trình tiền xử lý hợp lý gồm: kiểm tra tệp CSV tồn tại; xác nhận cột; loại các bản ghi thiếu mã hoặc ngày hết hạn; chuyển ngày hết hạn về kiểu ngày; loại hàng có số lượng tồn không dương; kiểm tra ngày mô phỏng; tính số ngày còn hạn; loại hàng hết hạn; sắp xếp theo FEFO và chuyển thành danh sách JSON. Những bước này là tiền đề để robot không nhận nhiệm vụ đối với hàng đã không còn khả dụng trong hệ thống mô phỏng.

Tài liệu mô tả V21 không sử dụng ngày hiện tại của máy tính làm mặc định. Chương trình lựa chọn một ngày trong khoảng dữ liệu với mục tiêu tạo ra đủ ba nhóm hàng theo hạn dùng nhằm phục vụ trực quan hóa. Phép chọn ngày là phương pháp xây dựng kịch bản mô phỏng chứ không phải bằng chứng về hoạt động thực của kho tại một thời điểm lịch sử. Khi viết báo cáo nghiên cứu cần ghi rõ ngày được chọn và cách chọn để tái lập kết quả.

inventory_list.sort(key=lambda item: item["daysLeft"])

Giá trị xuất cho JavaScript có thể là danh sách đối tượng bao gồm ID, tên, số lượng, hạn dùng, số ngày còn hạn và thuộc tính hiển thị. Cần tránh tạo dữ liệu sản phẩm ngẫu nhiên khi tải Kaggle thất bại mà không thông báo, vì điều đó làm sai lệch bản chất nguồn dữ liệu được khai báo.

## 3.5. Xây dựng thuật toán tối ưu tuyến đường

### 3.5.1. Chuyển mặt bằng thành bản đồ lưới

Mỗi ô trên bản đồ lưới được gắn tọa độ (gx,gz), trạng thái đi được/không đi được và các ô láng giềng. Vị trí thế giới thực tế (x,z) được ánh xạ về chỉ số lưới bằng phép đổi thang theo bước 0,5 m và gốc hệ tọa độ. Phạm vi không gian được giới hạn trong 56 hàng và 56 cột; các ô trùng hình học kệ hoặc tường được đánh dấu không thể đi qua. Những quy tắc đổi tọa độ cần nhất quán giữa mô hình vật thể 3D và thuật toán tìm đường.

### 3.5.2. Cơ chế A* áp dụng trong V21

Theo phân tích mã nguồn kèm tài liệu, hàm tính tuyến chính mang tên f5PlanCost(). Thuật toán sử dụng mảng/hệ ánh xạ gScore để lưu chi phí tốt nhất, parent để truy vết tuyến và một binary heap làm hàng đợi ưu tiên. Từ ô nguồn, A* xét bốn ô láng giềng, bỏ qua các ô bị chặn, cập nhật chi phí nếu tìm thấy đường tốt hơn và ưu tiên mở rộng ô có f thấp nhất.

const h = n =>

Math.abs(n.x - goal.x) + Math.abs(n.z - goal.z);

const directions = [[1,0], [-1,0], [0,1], [0,-1]];

gScore[sourceKey] = 0;

push({ n: start, f: h(start) });

Một cải tiến trong mô tả V21 là đưa vùng lân cận robot khác vào hàm chi phí mềm. Thay vì cấm tuyệt đối toàn bộ ô quanh robot đang đứng, hệ thống tăng chi phí theo ba mức khoảng cách. Khi khoảng cách nhỏ hơn SAFE_GAP+0,12 m, chi phí cộng 28; ở ngưỡng dưới SAFE_GAP+0,65 m cộng 7; dưới SAFE_GAP+1,3 m cộng 1,7. Điều này tạo xu hướng chọn đường thông thoáng nhưng vẫn cho phép tìm được đường trong một số hành lang hẹp mà cơ chế cấm cứng có thể làm bế tắc.

if (d < SAFE_GAP + .12) cost += 28;

else if (d < SAFE_GAP + .65) cost += 7;

else if (d < SAFE_GAP + 1.3) cost += 1.7;

Cần phân biệt cơ chế trên với thuật toán Weighted A* theo cách gọi chuẩn của tài liệu thuật toán: V21 được mô tả là A* với chi phí cạnh có bổ sung mức phạt gần robot, không có bằng chứng từ tài liệu đính kèm về việc nhân trực tiếp heuristic h bằng hệ số w>1. Vì vậy tiểu luận dùng tên “A* có trọng số chi phí tránh robot” để mô tả chính xác hành vi hơn. Chi phí động làm kết quả phụ thuộc vào vị trí robot tại thời điểm lập kế hoạch; nếu môi trường thay đổi, tuyến trước đó có thể không còn thuận lợi.

### 3.5.3. Dijkstra làm phương pháp đối chiếu

Đề cương có yêu cầu phân tích Dijkstra và A*. Dijkstra được đưa vào như thuật toán nền để giải thích tiêu chí đường ngắn nhất và đề xuất làm đối chứng trong thử nghiệm sau này. Với cùng bản đồ tĩnh, cùng đơn vị chi phí cạnh, có thể chạy riêng Dijkstra và A* để so sánh số nút mở rộng, thời gian lập kế hoạch và tổng chi phí tuyến; nếu hàm heuristic hợp lệ thì hai thuật toán có thể thu được đường có cùng tổng chi phí tối ưu. Không có căn cứ từ tài liệu V21 để khẳng định mã hiện tại thực sự gọi Dijkstra khi robot di chuyển.

### 3.5.4. Tối ưu hành trình ba chặng và nhiều đơn

Một nhiệm vụ tiêu chuẩn có hai chặng đang phục vụ đơn: từ vị trí hiện tại tới PICK và từ PICK tới DROP. Nếu robot hết đơn, hệ thống bổ sung chặng RETURN về trạm. Trường hợp một robot có nhiều đơn, sau DROP của đơn trước, robot tiếp tục thực hiện PICK của đơn sau mà không nhất thiết quay về sạc giữa chừng. Cách tổ chức này hạn chế lượt chạy rỗng không cần thiết và làm tăng tính liên tục của chu trình tác nghiệp. Tuy nhiên hệ thống chưa tự động sắp lại thứ tự nhiều SKU nhằm tối thiểu tổng quãng đường của hàng đợi.

## 3.6. Xây dựng thuật toán chống va chạm, xung đột

### 3.6.1. Lớp dự đoán CPA

V21 tính vị trí tương đối giữa robot đang xét và robot khác, ước lượng vận tốc tương đối theo hướng di chuyển hiện tại và tìm thời điểm chúng gần nhau nhất trong khoảng 2,4 giây tới. Nếu khoảng cách gần nhất nhỏ hơn ngưỡng an toàn, hệ thống hạn chế tốc độ, tạo điều kiện cho một robot nhường đường trước khi đi vào điểm giao. Điểm mạnh so với kiểm tra khoảng cách tức thời là nhận biết nguy cơ giao cắt khi hai xe còn cách nhau một quãng.

const t = rv2 > 1e-8

? Math.max(0, Math.min(CONFLICT_HORIZON,

-(rx * rvx + rz * rvz) / rv2))

: 0;

const closest = Math.hypot(rx + rvx*t, rz + rvz*t);

Tuy vậy, CPA giả định vận tốc/hướng chuyển động được giữ gần như không đổi trong cửa sổ ngắn. Khi nhiều robot thay đổi vận tốc cùng lúc, dự báo có thể lệch thực tế. Đối với giao lộ có lưu lượng lớn, phương án tốt hơn là kết hợp CPA với điều phối quyền ưu tiên hoặc đặt chỗ khu vực giao theo thời gian.

### 3.6.2. Điều tốc theo khoảng cách an toàn và phanh

Thông số mô phỏng được trích từ tài liệu V21 gồm khoảng cách SAFE_GAP=0,98 m, tốc độ tối đa MAX_SPEED=2,3 m/s, gia tốc ACCEL=1,15 m/s² và độ giảm tốc BRAKE=2,7 m/s². Bộ điều khiển xác định khoảng trống hữu ích phía trước, tính giới hạn tốc độ theo công thức phanh, đồng thời xét ràng buộc khi vào cua và từ dự báo CPA; tốc độ thực cập nhật theo gia tốc/giảm tốc chứ không nhảy tức thời giữa hai mức.

const SAFE_GAP = 0.98;

const MAX_SPEED = 2.3;

const ACCEL = 1.15;

const BRAKE = 2.7;

const cap = Math.sqrt(2 * BRAKE * clearance);

limit = Math.min(limit, cap);

Như vậy, chức năng tránh xung đột có thể làm thay đổi cả thời gian và chiều dài hành trình. Để đánh giá thuật toán công bằng, không thể chỉ tính đường đi theo lý thuyết mà phải đo thời gian robot thực sự dùng cho tăng tốc, vào cua, dừng chờ, tìm đường lại và giao hàng.

### 3.6.3. Kiểm tra an toàn trước từng bước di chuyển

Lớp kiểm tra f5AllowedMove() xem đoạn nối vị trí cũ tới vị trí dự kiến mới có đi quá gần vị trí robot khác không. Hình chiếu của vị trí robot khác lên đoạn chuyển động được chặn trong khoảng [0,1] để tính điểm gần nhất, sau đó so sánh với SAFE_GAP. Nếu không đáp ứng ngưỡng, bước đi bị hủy. Cơ chế này có ích vì tránh trường hợp một bước cập nhật dài làm robot “nhảy xuyên” qua vị trí robot khác trong mô phỏng.

Dù vậy, phép kiểm tra dựa chủ yếu trên vị trí robot khác tại thời điểm kiểm tra, chưa phải va chạm liên tục giữa hai vật thể đồng thời chuyển động với quỹ đạo đầy đủ. Muốn kiểm chứng an toàn cần xây dựng bộ giám sát hình học độc lập, ghi nhận khoảng cách tối thiểu của từng cặp AGV ở mỗi khung thời gian.

### 3.6.4. Tìm đường lại, detour và quét 360°

Khi một tuyến đường bị chặn, bộ điều khiển ưu tiên giảm tốc và chờ ngắn, tiếp theo xem xét cập nhật tuyến hoặc tìm đường vòng (detour). Khi tình trạng bế tắc thực sự kéo dài, hệ thống mới mô phỏng hành vi quay 360° để đánh giá những hướng khả thi. Tham số REPLAN_INTERVAL=2,6 giây, BLOCKED_SCAN_AFTER=14,0 giây, SCAN_COOLDOWN=25,0 giây và SCAN_ANGULAR_RATE=3,2 rad/s giúp hạn chế việc robot xoay liên tục vì dao động giao thông ngắn hạn.

Theo tài liệu, hàm quét đánh giá 16 hướng với hai bán kính ứng viên 1,5 m và 2,5 m. Các hướng được tính bằng tọa độ và trạng thái lưới mô phỏng; không có tín hiệu LiDAR đo thực. Vì vậy thuật ngữ “quét 360°” trong báo cáo phải được hiểu là mô phỏng logic tìm hướng khả thi, không phải robot đã được trang bị cảm biến vật lý.

### 3.6.5. Hạn chế của cơ chế phối hợp hiện tại

Dù có nhiều lớp an toàn, A* theo vị trí tức thời vẫn không giải quyết đầy đủ bài toán tranh chấp ô theo tương lai. Chẳng hạn, hai robot từ hai đầu hành lang có thể cùng tìm được một tuyến hợp lệ tại thời điểm khác nhau, rồi cùng muốn đi vào một đoạn không có chỗ tránh. CPA và điều tốc có thể cho chúng dừng trước khi va chạm nhưng chưa nhất thiết cho chúng lối thoát, làm xuất hiện deadlock. Cần phát triển thêm luật phân quyền giao lộ hoặc MAPF có trục thời gian để quyết định quyền đi trước một cách hệ thống.

## 3.7. Điều phối sáu robot và hàng đợi nhiệm vụ

Hệ thống tách ba trạng thái của một ô hàng: đang chờ phát lệnh (pendingDispatches), đã được thêm vào hàng đợi của robot nhưng chưa thực hiện (queuedSlotIds) và đã được robot nhận giữ chỗ khi xử lý (reservedSlotIds). Sự phân biệt này làm giảm nguy cơ hai tác vụ cùng xuất một ô và là ví dụ về đồng bộ dữ liệu nghiệp vụ với hành vi AGV. Mỗi robot có jobQueue riêng, giúp một xe thực hiện nối tiếp nhiều đơn.

const reservedSlotIds = new Set();

const queuedSlotIds = new Set();

let pendingDispatches = [];

// Với lệnh hợp lệ:

r.jobQueue.push({...cmd});

queuedSlotIds.add(cmd.slotId);

Trong vòng lặp cập nhật, mô hình V21 còn thay đổi thứ tự xử lý robot theo chu kỳ khoảng bốn giây để hạn chế một ID luôn được ưu tiên cập nhật. Đây là giải pháp công bằng ở mức trình tự vòng lặp, không tương đương với bộ điều phối quyền ưu tiên toàn cục. Tài liệu cũng nêu rõ người vận hành quyết định robot nhận đơn; hệ thống chưa tự tối ưu phân công dựa trên vị trí, pin hay số lệnh đang chờ.

## 3.8. Máy trạng thái robot

Các trạng thái được ghi nhận trong tài liệu gồm IDLE (sẵn sàng), PICK (đi lấy), DROP (đi giao), WAIT_NEXT (chờ nhiệm vụ kế), RETURN (về sạc), DOCK_TURN (quay đầu trong ô sạc), CHARGE (sạc), SCAN_360 (quét hướng khi bế tắc) và DONE (vừa hoàn thành đơn). Trạng thái chính phản ánh bước của quy trình tác nghiệp, còn WAIT_NEXT và SCAN_360 là trạng thái xử lý phụ khi điều kiện giao thông không bình thường.

**Bảng 7. Tóm tắt máy trạng thái robot V21**

### Bảng 7

| Trạng thái | Điều kiện điển hình | Trạng thái kế tiếp |
|---|---|---|
| IDLE | Có lệnh hợp lệ | PICK |
| PICK | Tới ô lấy hàng | DROP |
| DROP | Tới điểm giao | DONE / WAIT_NEXT |
| WAIT_NEXT | Còn đơn trong jobQueue | PICK |
| RETURN | Đã đến vị trí sạc | DOCK_TURN |
| DOCK_TURN | Quay đúng hướng | CHARGE |
| CHARGE | Kết thúc thời gian sạc mô phỏng | IDLE |
| SCAN_360 | Quét và chọn được hướng | Quay về pha đang xử lý |

Việc tổ chức thành máy trạng thái giúp giảm tình trạng thay đổi vị trí mà bỏ qua điều kiện nghiệp vụ, ví dụ robot nhận nhiệm vụ mới trước khi đã hoàn thành chặng giao. Đồng thời, trạng thái minh bạch giúp Tablet WMS trình bày cho người vận hành lý do robot đang đứng yên hoặc chưa quay về sạc.

## 3.9. Thiết kế giao diện mô phỏng và tương tác (front-end)

Giao diện V21 được thiết kế theo hướng quan sát trực quan. Phần trung tâm là cảnh kho 3D gồm kệ, kiện hàng theo ba màu FEFO, sáu robot có màu phân biệt, đường di chuyển, trạm sạc và khu vực Inbound–Despatch. Ở chế độ FPS, người dùng dùng W, A, S, D để di chuyển góc nhìn và dùng chuột điều chỉnh hướng quan sát; ở góc nhìn quản lý có thể xoay và quan sát toàn bộ bố cục từ trên cao khi điều khiển OrbitControls được tải thành công.

Tablet WMS cung cấp chức năng tìm SKU hoặc tên sản phẩm, chọn robot từ 1 đến 6, chỉ định nơi giao, thêm lệnh vào danh sách chờ và bấm phát lệnh. Ngoài tab robot, hệ thống có chức năng tra cứu tồn kho, thống kê FEFO, minimap 2D và lịch sử lấy hàng. Tại lịch sử, mỗi bản ghi có robot, SKU, thời gian dự tính, thời gian thực tế, quãng đường, số xung đột và số va chạm theo bộ đếm của chương trình. Có thể xuất CSV để phân tích ngoài mô phỏng.

Các nguyên tắc thiết kế giao diện nên bao gồm: thống nhất mã màu và nhãn; báo lỗi rõ khi SKU không còn khả dụng; phân biệt lệnh đang chờ với lệnh đang chạy; cho phép lọc nhanh lịch sử theo robot; hiển thị cảnh báo khi robot chờ lâu; và ghi rõ đơn vị m, s, m/s. Khi ứng dụng mở rộng sang thiết bị thật, cần có cơ chế dừng khẩn cấp và phân quyền vận hành độc lập; những chức năng này không được khẳng định là đã có trong V21.

# CHƯƠNG 4. QUY TRÌNH VẬN HÀNH CỦA MÔ HÌNH

## 4.1. Khởi tạo và thiết lập môi trường

Quy trình vận hành được bắt đầu từ notebook Colab hoặc một môi trường Python tương đương có đủ thư viện. Người dùng thực thi phần cài đặt phụ thuộc, tải dữ liệu Grocery Inventory, chạy khối tiền xử lý và hiển thị HTML mô phỏng. Vì mã giao diện sử dụng thư viện JavaScript từ CDN, cần bảo đảm trình duyệt có thể truy cập các nguồn này. Nếu không hiển thị được cảnh 3D, bước kiểm tra đầu tiên là xem các gói đã được tải đúng, trình duyệt có hỗ trợ đồ họa cần thiết và HTML có nhận được cấu trúc dữ liệu hợp lệ.

Trong khâu dựng môi trường 3D, chương trình tạo sàn kho, bố trí kệ, cửa, vùng giao nhận và trạm sạc, sau đó ánh xạ các đối tượng tĩnh thành ô cản trên lưới. Sáu robot được khởi tạo với vị trí, trạng thái và mảng nhiệm vụ. Bộ đếm thời gian mô phỏng và lịch sử nhiệm vụ được đặt ở trạng thái bắt đầu; những thay đổi về giờ chạy hoặc ngưỡng FEFO cần được ghi lại để quá trình thí nghiệm có thể lặp lại.

## 4.2. Chuẩn hóa và lọc dữ liệu

V21 đọc dữ liệu hàng hóa từ CSV và kiểm tra sự tồn tại của bốn trường bắt buộc. Việc loại bỏ bản ghi không hợp lệ phải thực hiện trước khi tính ưu tiên FEFO, bởi dữ liệu thiếu ngày hết hạn có thể dẫn tới phân loại sai. Kế tiếp, hệ thống chuyển hạn dùng sang kiểu ngày, xác định ngày vận hành mô phỏng và tính số ngày còn hạn. Các bản ghi có ngày đã qua hoặc tồn kho không dương được loại khỏi danh sách mô phỏng. Những sản phẩm còn hợp lệ được sắp theo daysLeft và phân nhóm màu.

**Bảng 8. Quy trình xử lý dữ liệu hàng hóa**

### Bảng 8

| Công đoạn | Điều kiện kiểm tra | Đầu ra mong đợi |
|---|---|---|
| Tìm dữ liệu | Tệp CSV tồn tại; đường dẫn hợp lệ | Danh sách tệp để đọc |
| Xác nhận cấu trúc | Đủ cột bắt buộc | Bảng dữ liệu hợp lệ về cấu trúc |
| Kiểm tra ngày | Có thể chuyển Expiration_Date sang ngày | Ngày hết hạn chuẩn hóa |
| Kiểm tra số lượng | Stock_Quantity lớn hơn 0 | Danh sách hàng còn tồn |
| Chọn ngày mô phỏng | Ngày nằm trong phạm vi cần mô phỏng | Mốc tính daysLeft |
| Phân nhóm FEFO | daysLeft không âm | Danh sách đỏ – vàng – xanh |
| Xuất cho giao diện | JSON đúng định dạng | Dữ liệu cho cảnh kho 3D |

Chức năng phân nhóm màu phục vụ hai mục đích: trình bày trực quan mức độ ưu tiên và giúp người vận hành tìm nhanh SKU sắp hết hạn. Tuy nhiên, cần lưu ý dữ liệu được dựng lên các kệ chịu giới hạn sức chứa 3D và không nhất thiết có số ô bằng tổng bản ghi CSV hợp lệ; thống kê trực quan theo kệ phải có nhãn phạm vi để tránh bị hiểu là số liệu tồn kho tổng thể.

## 4.3. Quy trình tính toán khoảng cách và chọn lộ trình

Khi có nhiệm vụ, bộ lập kế hoạch xác định ô nguồn từ vị trí robot hiện tại và ô đích từ kệ hoặc điểm giao. Sau khi chuyển về tọa độ lưới, hệ thống tìm đường qua những ô có thể đi; những ô kệ và tường bị loại khỏi tập ứng viên. Với mỗi bước mở rộng, A* cộng chi phí cạnh, phạt vùng gần robot khác (nếu đang bật điều kiện tương ứng) và cộng h(n) để ưu tiên ô mở rộng. Khi gặp ô đích, hệ thống truy ngược parent để tạo danh sách điểm mà robot cần theo lần lượt.

Sau khi robot bắt đầu di chuyển, tuyến đường lập kế hoạch được sử dụng như hướng dẫn thay vì một mệnh lệnh bất biến. Nếu một robot khác xuất hiện khiến một đoạn đường trở nên khó đi, lớp kiểm soát tốc độ có thể buộc robot chậm lại, dừng hoặc phát yêu cầu tìm lại tuyến. Trong khi đó phần hiển thị cập nhật vệt đường dự kiến và vị trí hiện thời để người vận hành phân biệt đường kế hoạch với hành trình đã hoàn thành.

Vì chi phí gồm mức phạt động, cần xác định rõ chỉ số “độ dài” và “tổng chi phí” không phải luôn như nhau. Độ dài tính từ quãng đường robot thực di chuyển (m), còn tổng chi phí quy đổi có thể lớn hơn khi tuyến đi sát robot khác. Khi so sánh hai thuật toán, cần dùng chung đơn vị chi phí và thiết lập điều kiện giống nhau.

## 4.4. Quy trình chống va chạm trong thời gian mô phỏng

Cơ chế xung đột được tổ chức theo nhiều lớp liên tục. Trước hết, đường đi đã lập được tính lại khi có dấu hiệu tắc nghẽn. Tiếp theo, mỗi khung hình bộ điều khiển ước lượng khoảng cách tới robot gần và CPA để suy ra mức độ nguy hiểm sắp tới. Nếu cần, vận tốc mục tiêu bị giới hạn theo khoảng trống và độ giảm tốc. Ngay trước bước cập nhật vị trí, hàm kiểm tra đoạn chuyển động ngăn hành vi tiến quá gần một xe khác. Nếu robot bị cản kéo dài, bộ điều khiển tìm đường vòng hoặc chuyển sang trạng thái quét hướng. Mỗi lớp xử lý khác nhau nên cần được kiểm chứng theo tình huống riêng.

**Hình 3. Sơ đồ lớp kiểm soát xung đột và xử lý bế tắc của robot**

Cơ chế này giúp xử lý nhiều tình huống thực tế trong mô phỏng nhưng chưa đưa ra bảo đảm kiểm chứng hình thức rằng mọi cặp robot đều không va chạm trong mọi lịch trình. Đặc biệt ở hành lang hẹp, một xe không có ô tránh có thể khiến xe đối diện dừng vô thời hạn. Đây là điểm yếu cần được đưa vào kịch bản thử nghiệm và không nên diễn giải rằng chỉ cần gọi hàm quét 360° là sẽ giải quyết mọi bế tắc.

## 4.5. Quy trình tác nghiệp từ khi nhận lệnh đến khi sạc

Từ Tablet WMS, người vận hành tìm một SKU và xác nhận robot sẽ thực hiện. Hệ thống đối chiếu SKU với danh sách ô hàng đang sẵn có, kiểm tra ô đã được đặt trong hàng đợi hay giữ chỗ chưa, sau đó thêm lệnh hợp lệ vào danh sách đang chờ phát. Khi nhấn “Phát lệnh”, danh sách được gán vào hàng đợi robot tương ứng. Robot chuyển từ IDLE sang PICK, lập tuyến tới vị trí hàng rồi di chuyển có kiểm soát tốc độ.

Sau khi đạt điểm lấy hàng theo ngưỡng nhận diện của mô phỏng, robot chuyển sang DROP. Khi giao xong, chương trình ghi nhận thời gian thực tế và quãng đường của nhiệm vụ, kết thúc đơn hiện tại. Nếu jobQueue còn nhiệm vụ, robot xử lý tiếp từ vị trí hiện tại; nếu đã hết, nó chuyển RETURN để tìm đường về ô sạc, thực hiện DOCK_TURN rồi CHARGE trước khi về IDLE. Tài liệu mô tả pin giảm theo mức cố định sau mỗi đơn và thời gian sạc mô phỏng ngắn, vì vậy thời lượng sạc hiện không phản ánh tiêu thụ năng lượng vật lý.

Một ví dụ nguyên lý có thể xảy ra: Robot 1 được xếp ba SKU A–C–F, Robot 2 nhận SKU B và Robot 3 nhận D–E, còn các robot khác ở trạng thái chờ. Robot 1 đi A → C → F → trạm sạc, không quay về trạm giữa mỗi đơn. Đây là ví dụ minh họa về hoạt động hàng đợi, không phải bản ghi thí nghiệm đã đo từ phiên chạy V21.

## 4.6. Theo dõi trên front-end và truy xuất lịch sử

Trong suốt phiên chạy, giao diện quản lý 3D giúp quan sát kệ, robot, lối giao nhận và vệt đi; minimap phản ánh toàn cảnh từ trên xuống và giảm việc phải liên tục đổi camera. Chế độ FPS cho phép người dùng kiểm tra một tuyến đường từ vị trí gần mặt sàn, hữu ích khi phân tích các điểm giao hẹp hay những vị trí robot đứng chờ. Tablet WMS đảm nhận bảng điều khiển nhập lệnh và thống kê.

Mỗi bản ghi lịch sử nhiệm vụ trong mô tả V21 gồm robot, SKU, thời gian ước tính, thời gian thực tế, số mét đã đi, số xung đột và số va chạm theo bộ đếm. Thời gian ước tính được tính lý tưởng dựa trên chiều dài đường đi chia cho tốc độ tối đa 2,3 m/s; nó chưa trừ hao thời gian tăng tốc, giảm tốc, quay đầu hay chờ. Thời gian thực tế là đồng hồ mô phỏng từ khi bắt đầu đơn tới khi hoàn thành giao hàng, không bao gồm đoạn RETURN. Khi xây dựng KPI về tổng chu kỳ, cần ghi thêm phần về sạc để tránh sai lệch giữa các chỉ tiêu.

Việc xuất CSV là bước cần thiết để tính trung bình, độ lệch chuẩn và số lần xảy ra tình huống bất thường. Bộ đếm xung đột phản ánh logic mà chương trình đã định nghĩa, không thay thế được hệ đo khoảng cách độc lập. Trong thí nghiệm, nếu muốn kết luận “không va chạm”, nhóm cần đối soát cảnh 3D với nhật ký tọa độ và bộ phát hiện giao cắt hình học.

## 4.7. Xử lý các tình huống ngoại lệ

**Bảng 9. Các trường hợp cần kiểm thử ngoại lệ**

### Bảng 9

| Tình huống | Nguy cơ | Cách xử lý/kiểm thử khuyến nghị |
|---|---|---|
| CSV thiếu cột bắt buộc | Phân nhóm FEFO sai | Thông báo lỗi; không chạy với dữ liệu thiếu |
| Không có SKU được chọn | Phát lệnh rỗng | Từ chối lệnh và giải thích lý do |
| Một slot được chọn hai lần | Hai robot cùng lấy | Kiểm tra queuedSlotIds / reservedSlotIds |
| Lối đi trước robot bị chặn | Robot dừng kéo dài | Điều tốc, tìm đường lại, detour, quét |
| Hai robot đối đầu hành lang | Deadlock | Kiểm thử thời gian chờ và luật ưu tiên |
| Không tải được CDN | Mô phỏng không hiển thị | Kiểm tra mạng và phiên bản thư viện |
| Tải lại trang không xuất lịch sử | Mất dữ liệu phiên | Xuất CSV hoặc bổ sung lưu bền vững |

Những tình huống trên cho thấy tính đúng đắn và độ bền của một hệ AGV không chỉ phụ thuộc vào độ tối ưu của A*. Chất lượng dữ liệu, quản trị tác vụ và phản hồi giao diện quyết định việc người vận hành có nhận biết được lỗi hay không. Khi đánh giá báo cáo, cần tách rõ lỗi thuộc tầng dữ liệu, lỗi lập kế hoạch, lỗi an toàn chuyển động và lỗi trực quan hóa để đưa ra phương án khắc phục phù hợp.

# CHƯƠNG 5. THÍ NGHIỆM VÀ ĐÁNH GIÁ MÔ HÌNH

## 5.1. Mục đích và nguyên tắc tổ chức thí nghiệm

Thí nghiệm nhằm kiểm chứng, thay vì mặc định, mức độ hoàn thành nhiệm vụ, tính thông suốt của tuyến đường và khả năng giảm xung đột của mô hình. Các phép thử được chia thành tình huống đơn giản để kiểm tra cơ chế cốt lõi và tình huống mật độ cao để đánh giá sự phối hợp. Khi báo cáo số liệu cần gắn mỗi phép thử với bộ SKU cụ thể, vị trí xuất phát, trạng thái hàng tồn, lựa chọn điểm giao, số robot tham gia, phiên bản mô hình và thông số vận hành.

Để giảm biến động không kiểm soát, đề xuất lặp lại mỗi kịch bản tối thiểu mười lần và ghi nhận cùng cấu hình đầu vào. Nếu có yếu tố ngẫu nhiên, cần cố định seed hoặc ghi rõ seed cho từng lượt. Khi so sánh V20 và V21, phải kiểm soát thay đổi vị trí hàng do bỏ kệ Inbound; không thể quy toàn bộ khác biệt hiệu suất cho việc loại bỏ kệ khi cấu hình lưu trữ cũng thay đổi.

## 5.2. Thiết kế bảy kịch bản thí nghiệm

**Bảng 10. Ma trận thí nghiệm đề xuất cho V21**

### Bảng 10

| Mã thử | Thiết lập | Mục tiêu kiểm tra |
|---|---|---|
| TN1 – Một robot | Robot 1 thực hiện liên tục 10 đơn | Hàng đợi, giao hàng, RETURN và sạc |
| TN2 – Ba robot | 3 robot, mỗi robot 5 đơn (15 đơn) | Phối hợp ở mật độ trung bình |
| TN3 – Sáu robot | 6 robot, mỗi robot 5 đơn (30 đơn) | Thông lượng, ùn tắc và công bằng |
| TN4 – Giao nhận tập trung | 6 robot có nhiều đơn cùng điểm Despatch | Giao lộ, xung đột tại cửa xuất |
| TN5 – Lấy hàng phân tán | 6 robot lấy các SKU trên nhiều dãy | Khả năng tìm đường, cập nhật tuyến |
| TN6 – Trạm sạc | 6 robot cùng quay về gần nhau | Tranh chấp đường vào sạc, DOCK_TURN |
| TN7 – V20 so với V21 | Cùng danh sách đơn; cấu hình kệ được kiểm soát | Đánh giá tác động bỏ kệ gần Inbound |

Trong TN1, nhóm cần tập trung vào tính liên tục của máy trạng thái: robot không được quay về trạm sạc khi hàng đợi vẫn còn đơn hợp lệ. TN2 và TN3 kiểm tra mức độ tăng ùn tắc khi số AGV hoạt động tăng; cùng một số đơn tổng hợp sẽ cho thấy sự đánh đổi giữa song song hóa và xung đột. TN4, TN6 tác động trực tiếp đến khu vực dễ xuất hiện điểm nghẽn. TN5 phân tích tính ổn định của A* khi đích phân bố xa nhau. TN7 là phép kiểm tra bố trí mặt bằng, cần tách với thay đổi phần mềm điều phối.

## 5.3. Hệ thống chỉ số và công thức đánh giá

Để dữ liệu có thể đối chiếu, thời gian của từng nhiệm vụ được xác định từ khi robot thực sự bắt đầu nhận đơn đến khi kết thúc giao, phù hợp định nghĩa lịch sử V21. Nếu cần đánh giá từ thời điểm người vận hành phát lệnh, nên lập thêm chỉ số thời gian chờ trong hàng đợi. Quãng đường tính từ đồng hồ quãng đường robot tại thời điểm bắt đầu và kết thúc đơn. Các chỉ tiêu chủ yếu gồm:

Tỷ lệ hoàn thành:  R = (Nhoàn thành / Ngiao) × 100%

Thời gian bình quân:  T̄ = (Σ Tᵢ) / Nhoàn thành

Quãng đường bình quân:  D̄ = (Σ Dᵢ) / Nhoàn thành

Thông lượng:  Q = Nhoàn thành / Tmô phỏng   (đơn / giây hoặc đơn / giờ)

Sai lệch thời gian:  ΔTᵢ = Tthực tế,i − Tdự tính,i

Tỷ lệ vi phạm an toàn đề xuất:  V = Nsự kiện vi phạm / Thời gian mô phỏng

Ở đây N_giao là số đơn được nhận vào hệ thống, N_hoàn thành là số đơn đã kết thúc thành công, và T_mô phỏng là tổng khoảng thời gian quan sát. Nếu một phép thử còn đơn chưa xong, cần ghi nguyên nhân (bế tắc, hết thời gian, lỗi dữ liệu) chứ không lặng lẽ loại khỏi mẫu. Đối với xung đột, một robot dừng liên tục trong 10 giây không nhất thiết tương đương 600 sự kiện xung đột ở tần số 60 FPS; cần quy định tiêu chuẩn đếm sự kiện có thời gian bắt đầu và kết thúc để tránh đếm trùng theo mỗi khung hình.

## 5.4. Phương án thu thập và kiểm tra số liệu

Trước mỗi lần chạy, nhóm lưu bảng thông số phiên: thời điểm mô phỏng FEFO, phiên bản mã, số robot, ngưỡng SAFE_GAP, tốc độ tối đa, cấu hình kệ và danh sách lệnh. Sau khi chạy, xuất CSV lịch sử và một log robot theo thời gian gồm (robotId, thời điểm, x, z, speed, phase, goal, blocked). Đối với phép đo va chạm độc lập, tại mỗi khung hình tính khoảng cách giữa mọi cặp robot (6 robot tạo 15 cặp), so sánh với ngưỡng hình học có xét kích thước thân xe và ghép những khung liên tiếp thành một sự kiện duy nhất.

Bộ ghi hiện có trong tài liệu V21 đã lưu quãng đường và sự kiện xung đột/va chạm theo chương trình; log tọa độ khung hình và kiểm định độc lập là đề xuất bổ sung. Không có dữ liệu này, báo cáo chỉ có thể mô tả chức năng xử lý và nêu giới hạn, không được khẳng định tỷ lệ va chạm bằng 0 hay hiệu quả tối ưu theo phần trăm.

## 5.5. Biểu mẫu tổng hợp kết quả thực nghiệm

**Bảng 11. Bảng kết quả thực nghiệm – chưa có số đo thực tế**

### Bảng 11

| Chỉ tiêu | TN1: 10 đơn | TN2: 15 đơn | TN3: 30 đơn |
|---|---|---|---|
| Đơn hoàn thành | Chưa đo | Chưa đo | Chưa đo |
| Tỷ lệ hoàn thành (%) | Chưa đo | Chưa đo | Chưa đo |
| Thời gian bình quân (s/đơn) | Chưa đo | Chưa đo | Chưa đo |
| Quãng đường bình quân (m/đơn) | Chưa đo | Chưa đo | Chưa đo |
| Thông lượng (đơn/giờ) | Chưa đo | Chưa đo | Chưa đo |
| Số sự kiện xung đột | Chưa đo | Chưa đo | Chưa đo |
| Số sự kiện va chạm độc lập | Chưa đo | Chưa đo | Chưa đo |
| Thời gian dừng chờ (s) | Chưa đo | Chưa đo | Chưa đo |

Các ô “Chưa đo” là chỉ báo trung thực về tình trạng dữ liệu. Nhóm cần chạy notebook, lưu ảnh hoặc video của tình huống thử nghiệm, xuất bảng lịch sử, tính KPI và cập nhật bảng trước khi nộp bản có kết luận định lượng. Kết quả nên được trình bày thêm dưới dạng đồ thị thời gian trung bình theo số robot, số xung đột theo từng kịch bản và biểu đồ phân phối thời gian thực tế so với thời gian ước tính.

## 5.6. Đánh giá kết quả đạt được trên phương diện thiết kế

**Bảng 12. Đánh giá các năng lực đã được mô tả của V21**

### Bảng 12

| Yêu cầu | Giải pháp được mô tả trong V21 | Kết luận về triển khai |
|---|---|---|
| Ưu tiên hàng gần hết hạn | Tính daysLeft; phân nhóm FEFO và tô màu | Đã có chức năng phân loại |
| Tránh kệ và tường | A* bốn hướng trên lưới 0,5 m | Đã có chức năng tìm đường |
| Không mặc định coi AGV đỗ là tường | Cộng chi phí mềm quanh robot khác | Đã có cơ chế hỗ trợ |
| Nhận biết nguy cơ giao cắt | Dự đoán CPA trong 2,4 s | Đã có cơ chế dự báo |
| Giảm tốc có kiểm soát | Giới hạn theo phanh, CPA và góc cua | Đã có cơ chế điều tốc |
| Tránh xuyên qua vị trí robot khác | Kiểm tra f5AllowedMove() | Đã có bước kiểm soát |
| Nhiều đơn cho cùng robot | jobQueue riêng; queued/reserved slot | Đã có khả năng xếp hàng |
| Quay về sạc sau khi hết đơn | RETURN → DOCK_TURN → CHARGE | Đã có luồng trạng thái |
| Thông suốt tuyệt đối khi 6 robot hoạt động | Chưa có đặt chỗ không–thời gian hoàn chỉnh | Chưa có bằng chứng xác nhận |

Từ bảng trên, có thể ghi nhận rằng V21 đã kết hợp nhiều nhóm thuật toán thành một luồng vận hành tương đối hoàn chỉnh: dữ liệu hàng, lệnh, đường đi, tốc độ, trạng thái và giám sát. Đây là thành quả đáng chú ý ở cấp mô hình học thuật, nhưng tính hoàn chỉnh chức năng không đồng nghĩa bảo đảm tối ưu toàn cục. Vấn đề còn lại không chỉ là “robot có di chuyển được hay không”, mà là “di chuyển hiệu quả và không bế tắc trong bao nhiêu phần trăm trường hợp, với sai số đo lường ra sao”.

## 5.7. Các hạn chế kỹ thuật cần nhìn nhận

### 5.7.1. Chưa phối hợp tuyến theo chiều thời gian

A* có phạt vùng gần robot khác dựa vào vị trí tại một thời điểm; chưa có bảng đặt chỗ nút và cạnh theo thời gian cho tất cả AGV. Hai robot vẫn có thể dự tính đi vào cùng một nút ở cùng thời điểm hoặc trao đổi vị trí trên cùng cạnh. Dù bộ điều tốc hạn chế va chạm tức thời, trường hợp hai robot đối đầu trong hành lang không có vùng tránh vẫn có thể gây deadlock.

### 5.7.2. Chưa tối ưu phân công nhiệm vụ toàn đội

Người dùng đang chọn robot cho từng SKU. Hệ thống chưa có thuật toán xét đồng thời cự ly đến hàng, tải công việc, mức pin, thời gian chờ dự đoán và độ khẩn FEFO. Một robot gần kệ hơn nhưng đang kẹt hoặc có hàng đợi dài chưa chắc là lựa chọn tốt nhất. Vì vậy quy trình phát lệnh hiện hỗ trợ vận hành thủ công có cấu trúc hơn là tối ưu toàn bộ phân phối công việc.

### 5.7.3. Định danh vị trí kệ và tính nhất quán dữ liệu

Mã vị trí được tài liệu phân tích là ghép từ chỉ số dãy và tầng, dẫn đến khả năng nhiều ngăn cùng dãy – tầng trùng mã hiển thị. Điều này khiến tìm kiếm, chọn hàng và báo cáo dễ gây nhầm lẫn dù slotId nội bộ còn duy nhất. Giải pháp là thống nhất schema vị trí theo dãy–ngăn–tầng và bảo đảm ràng buộc duy nhất ở lớp dữ liệu.

### 5.7.4. Mô phỏng cơ cấu vật lý và cảm biến chưa đầy đủ

AGV di chuyển trên mặt phẳng, nhưng chưa mô phỏng cơ cấu gắp/nâng theo nhiều tầng kệ, hạn chế tải trọng, ma sát, độ chính xác định vị hoặc dữ liệu LiDAR thực. Bởi vậy tốc độ tối đa 2,3 m/s và khoảng cách 0,98 m chỉ là tham số của V21. Để triển khai phương tiện thật, cần đánh giá rủi ro và kiểm định theo tiêu chuẩn phù hợp, trong đó ISO 3691-4:2023 là một tài liệu kỹ thuật tham chiếu quan trọng.

### 5.7.5. Pin, đo lường và lưu trữ

Theo tài liệu, pin giảm khoảng 10% khi hoàn thành một đơn và thời gian sạc mô phỏng khoảng 10 giây, chưa phụ thuộc quãng đường hay khối lượng. Lịch sử nhiệm vụ tồn tại trong bộ nhớ JavaScript, xuất được CSV nhưng chưa có lưu lâu dài. Bộ đếm xung đột dựa trên logic phần mềm, chưa phải phép đo độc lập về khoảng cách hình học. Đây là ba nguồn hạn chế nếu muốn dùng kết quả để quyết định chi phí hoặc an toàn vận hành ngoài thực tế.

## 5.8. Đề xuất giải pháp và định hướng phát triển

**Bảng 13. Lộ trình hoàn thiện mô hình sau V21**

### Bảng 13

| Ưu tiên | Giải pháp đề xuất | Tác động kỳ vọng |
|---|---|---|
| Cao | Cooperative A* / CBS hoặc MAPF có đặt chỗ thời gian | Giảm tranh chấp nút và cạnh trong tương lai |
| Cao | Chuẩn hóa mã kệ dãy–ngăn–tầng | Tránh chọn sai ô hàng |
| Cao | Bộ kiểm tra va chạm độc lập và log sự kiện | Có cơ sở kiểm chứng độ an toàn |
| Trung bình | Tự động phân đơn theo vị trí, pin, hàng đợi | Giảm thời gian hoàn thành toàn đội |
| Trung bình | Luật ưu tiên ngã giao hoặc đường một chiều | Hạn chế deadlock tại hành lang hẹp |
| Trung bình | Mô hình tiêu thụ năng lượng theo tải/quãng đường | Lập kế hoạch sạc hợp lý hơn |
| Dài hạn | Lưu nhiệm vụ vào PostgreSQL; kết nối WMS/ERP | Theo dõi lâu dài và phân tích dữ liệu |
| Dài hạn | Mô phỏng tải trọng, LiDAR, cơ cấu nâng | Tiếp cận hành vi AGV thực |

Trong các phương án, ưu tiên nghiên cứu MAPF có đặt chỗ theo thời gian vì trực tiếp giải quyết điểm yếu đặc thù khi nhiều robot cùng hoạt động. Cooperative A* sử dụng không gian–thời gian để lập đường cho từng tác tử trong bối cảnh có tuyến của tác tử khác (Silver, 2005); CBS phân rã mâu thuẫn ở cấp phối hợp và lập kế hoạch từng robot (Sharon et al., 2015). Việc lựa chọn giữa hai hướng cần dựa trên khả năng mở rộng, độ phức tạp cài đặt và thời gian phản hồi mong muốn đối với đội robot chỉ có sáu phương tiện.

Về thứ tự triển khai, nên chuẩn hóa dữ liệu và định nghĩa KPI trước, tiếp theo bổ sung logger và bộ kiểm tra an toàn độc lập, sau đó thiết lập bộ thí nghiệm hồi quy; cuối cùng mới so sánh các thuật toán MAPF và tinh chỉnh chiến lược giao lộ. Cách triển khai này bảo đảm mỗi nâng cấp có chỉ tiêu chứng minh giá trị, thay vì thêm nhiều chức năng mà không biết thay đổi có cải thiện kết quả hay không.

## 5.9. Tiêu chí nghiệm thu cho phiên bản tiếp theo

Đề xuất hệ thống đạt yêu cầu khi (i) toàn bộ bảy kịch bản đều có bảng dữ liệu từ ít nhất mười lượt chạy; (ii) số lượng đơn và định danh SKU khớp giữa lệnh đầu vào và lịch sử; (iii) mọi lần vi phạm ngưỡng khoảng cách đều có log thời điểm và tọa độ; (iv) không có nhiệm vụ bị bỏ quên mà không ghi nguyên nhân; (v) thuật toán mới được so sánh trên cùng cấu hình với V21 và (vi) các tiêu chí hiệu suất trình bày kèm phân tán số liệu, không chỉ dùng một kết quả thuận lợi nhất. Chỉ khi đó nhóm mới có cơ sở đánh giá mức tăng/giảm cụ thể về thời gian, quãng đường hoặc xung đột.

# CHƯƠNG 6. KẾT LUẬN VÀ KIẾN NGHỊ

## 6.1. Kết luận

Đề tài “Tối ưu hóa tuyến đường và giải quyết xung đột trong vận hành robot tự hành (AGV) tại nhà kho thông minh” đã kết nối cơ sở lý luận về tổ chức kho với phương pháp biểu diễn không gian bằng đồ thị và điều phối tác nghiệp trong môi trường mô phỏng. Trên nền tảng sản phẩm V21 được mô tả trong tài liệu nhóm, nghiên cứu phân tích một cấu trúc kho FEFO ba chiều gồm sáu AGV, dữ liệu hàng hóa từ Kaggle, Python tiền xử lý, JavaScript điều khiển và Three.js trực quan hóa.

Ở bài toán tối ưu tuyến đường, thuật toán A* được sử dụng để tìm tuyến đi hợp lệ qua lưới kho, đồng thời cộng chi phí tránh vùng gần robot khác nhằm giảm lựa chọn đường có nguy cơ ùn tắc. Ở bài toán xung đột, mô hình kết hợp dự đoán CPA, kiểm soát vận tốc theo khoảng cách phanh, kiểm tra bước di chuyển và tìm đường lại khi gặp trở ngại. Hệ thống còn có hàng đợi nhiều lệnh cho từng robot, máy trạng thái từ PICK–DROP tới RETURN–CHARGE, giao diện quản lý 3D và khả năng ghi lịch sử nhiệm vụ. Những chức năng này tạo thành một nguyên mẫu có thể giải thích và kiểm thử từng thành phần.

Tuy nhiên, phân tích cũng chỉ ra ranh giới giữa kết quả thiết kế và bằng chứng thực nghiệm. Mô hình chưa có cơ chế đặt chỗ không–thời gian hoàn chỉnh, chưa tối ưu phân công nhiệm vụ tự động, chưa mô phỏng đủ yếu tố vật lý và chưa cung cấp bộ số liệu kiểm thử độc lập để khẳng định loại bỏ hoàn toàn va chạm hoặc bế tắc. Do đó, kết luận phù hợp là V21 đã triển khai cơ chế hỗ trợ tìm đường và chống xung đột trong mô phỏng, chưa đủ chứng cứ xác nhận hiệu quả định lượng hay an toàn tuyệt đối trong mọi trường hợp.

## 6.2. Kiến nghị đối với nhóm nghiên cứu

Trước khi hoàn thiện phiên bản nộp chính thức, nhóm nên chạy đầy đủ các kịch bản TN1–TN7 và xuất log, bảng KPI, hình minh họa có chú thích phiên bản. Trong các thử nghiệm, cần đặc biệt quan sát tình huống hai robot đối đầu cùng hành lang, nhiều robot tới Despatch và cùng lúc trở về trạm sạc. Nhóm cũng nên sửa định danh vị trí kệ thành mã duy nhất, thống nhất định nghĩa các bộ đếm xung đột/va chạm, và ghi rõ ngày vận hành FEFO được chọn trong dữ liệu.

Ở giai đoạn tiếp theo, hướng nghiên cứu ưu tiên là MAPF với đặt chỗ theo thời gian hoặc điều phối quyền ưu tiên tại giao lộ. Trên nền dữ liệu thống nhất, nhóm có thể bổ sung thuật toán tự phân công nhiệm vụ theo chi phí thực tế, kết nối lịch sử vào cơ sở dữ liệu và xây dựng bộ thử nghiệm tự động. Khi nâng cấp lên hệ thống AGV vật lý, cần có một chu trình đánh giá rủi ro và kiểm định riêng cho phần cơ khí, điện, cảm biến và an toàn; mô phỏng hiện tại chỉ là bước chuẩn bị công nghệ.

## 6.3. Đóng góp và giá trị ứng dụng

Giá trị cốt lõi của nghiên cứu là tạo ra một khung phân tích có thể tái sử dụng: đưa nhu cầu logistics thành dữ liệu có cấu trúc, chuyển mặt bằng thành đồ thị, định nghĩa chu trình xử lý bằng máy trạng thái, tổ chức các lớp an toàn và đo hiệu quả bằng chỉ số có thể kiểm chứng. Khung này có thể hỗ trợ công tác giảng dạy và thiết kế nguyên mẫu kho tự động, đồng thời là cơ sở cho những nghiên cứu tiếp theo về tối ưu giao thông nội bộ, tồn kho FEFO và tích hợp dữ liệu WMS.

TÀI LIỆU THAM KHẢO

Tài liệu được trình bày theo thứ tự chữ cái, hướng tới chuẩn APA 7. Các nguồn nội bộ của nhóm được phân biệt với tài liệu khoa học và trang tài liệu kỹ thuật công khai.

de Koster, R., Le-Duc, T., & Roodbergen, K. J. (2007). Design and control of warehouse order picking: A literature review. European Journal of Operational Research, 182(2), 481–501. https://doi.org/10.1016/j.ejor.2006.07.009

Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. Numerische Mathematik, 1, 269–271. https://doi.org/10.1007/BF01386390

Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. IEEE Transactions on Systems Science and Cybernetics, 4(2), 100–107. https://doi.org/10.1109/TSSC.1968.300136

Hertog, M. L. A. T. M., Uysal, I., McCarthy, U., Verlinden, B. M., & Nicolaï, B. M. (2014). Shelf life modelling for first-expired-first-out warehouse management. Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, 372(2017), 20130306. https://doi.org/10.1098/rsta.2013.0306

International Organization for Standardization. (2023). Industrial trucks—Safety requirements and verification—Part 4: Driverless industrial trucks and their systems (ISO 3691-4:2023). https://www.iso.org/standard/83545.html

Kaggle. (n.d.). kagglehub: Python library to access Kaggle resources [Computer software]. GitHub. https://github.com/Kaggle/kagglehub

Nhóm 1. (2026). Mô hình kho FEFO 3D với 6 robot AGV – notebook Google Colab [Nguyên mẫu phần mềm; chưa được xác minh trực tiếp tại thời điểm biên soạn]. https://colab.research.google.com/drive/1Jp62mZYAKMOq1mxhKuBAacoYc40y3zUu

Nhóm 1. (2026). TaskTable_SMART LOGISTICS [Tài liệu phân công và phân tích mã nguồn V21, lưu hành nội bộ].

Sharon, G., Stern, R., Felner, A., & Sturtevant, N. R. (2015). Conflict-based search for optimal multi-agent pathfinding. Artificial Intelligence, 219, 40–66. https://doi.org/10.1016/j.artint.2014.11.006

Silver, D. (2005). Cooperative pathfinding. Proceedings of the AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment, 1(1), 117–122. https://doi.org/10.1609/aiide.v1i1.18726

Three.js. (n.d.). Fundamentals. https://threejs.org/manual/pages/fundamentals.html

Wurman, P. R., D’Andrea, R., & Mountz, M. (2008). Coordinating hundreds of cooperative, autonomous vehicles in warehouses. AI Magazine, 29(1), 9–19. https://doi.org/10.1609/aimag.v29i1.2082

PHỤ LỤC A. CÁC ĐOẠN MÃ THAM KHẢO TỪ TÀI LIỆU V21

Các đoạn mã dưới đây được trích/tái định dạng từ phần phân tích kỹ thuật V21 trong tài liệu nhóm. Chúng có mục đích giải thích cơ chế, không phải bản sao đầy đủ có thể chạy độc lập.

## A.1. Chọn hàng theo ngày hết hạn

inventory_list.sort(key=lambda item: item["daysLeft"])

if (item.daysLeft <= 15) {

colorHex = 0xef4444;  // red

} else if (item.daysLeft <= 45) {

colorHex = 0xfacc15;  // yellow

} else {

colorHex = 0x22c55e;  // green

}

## A.2. Kiểm tra lệnh trùng

if (!slot || slot.isEmpty || !r ||

reservedSlotIds.has(cmd.slotId) ||

queuedSlotIds.has(cmd.slotId)) continue;

r.jobQueue.push({...cmd});

queuedSlotIds.add(cmd.slotId);

## A.3. Ghi lịch sử nhiệm vụ

taskHistory.push({

robot: `Robot ${r.id + 1}`,

sku: t.sku,

estimated: t.estimatedSeconds,

actual: fleet5Clock - t.start,

meters: r.distance - t.startDistance,

conflicts: t.conflictCount,

collisions: t.collisionCount

});

## A.4. Bản ghi cấu hình robot

const SAFE_GAP = 0.98;

const MAX_SPEED = 2.3;

const ACCEL = 1.15;

const BRAKE = 2.7;

const REPLAN_INTERVAL = 2.6;

const BLOCKED_SCAN_AFTER = 14.0;

const SCAN_COOLDOWN = 25.0;

const SCAN_ANGULAR_RATE = 3.2;

PHỤ LỤC B. MẪU NHẬT KÝ THÍ NGHIỆM

**Bảng 14. Biên bản chạy một lượt thí nghiệm**

### Bảng 14

| Trường | Giá trị phải điền |
|---|---|
| Mã kịch bản | TN1 / TN2 / TN3 / TN4 / TN5 / TN6 / TN7 |
| Phiên bản phần mềm | V21 hoặc phiên bản đối chứng |
| Ngày và giờ chạy | [Chưa cập nhật] |
| Ngày vận hành FEFO | [Chưa cập nhật] |
| Danh sách SKU | [Chưa cập nhật] |
| Số AGV chạy | [Chưa cập nhật] |
| Cấu hình kệ / Inbound | [Chưa cập nhật] |
| Ngưỡng vận tốc, gia tốc, an toàn | [Chưa cập nhật] |
| Thời điểm kết thúc | [Chưa cập nhật] |
| Đường dẫn CSV đầu ra | [Chưa cập nhật] |
| Sự cố hoặc nhận xét | [Chưa cập nhật] |

Sau khi đủ mười lượt của mỗi kịch bản, nhóm sử dụng một bảng dữ liệu tổng hợp có cột run_id, robot_count, order_count, completed, completion_rate, mean_actual_time, mean_distance, total_conflicts, independent_collisions, wait_seconds và throughput_per_hour. Nên lưu kèm version, cấu hình kệ và seed (nếu có) để có thể truy xuất nguồn số liệu.

PHỤ LỤC C. ĐỀ XUẤT QUY TRÌNH KIỂM THỬ ĐỘC LẬP

Bước 1. Xác nhận tải và chuẩn hóa dữ liệu thành công; lưu số lượng bản ghi còn hợp lệ sau mỗi bước.

Bước 2. Với bản đồ kho cố định, thử đường từ từng trạm sạc tới các khu vực PICK, DROP và RETURN; kiểm tra ô đi được.

Bước 3. Khởi tạo hai robot đi ngược chiều trên một hành lang; ghi toàn bộ các khoảng thời gian dừng, quay đầu và tìm lại tuyến.

Bước 4. Tăng lên sáu robot giao nhận tập trung; ghi thời gian thực tế, số sự kiện chặn đường và khoảng cách tối thiểu từng cặp.

Bước 5. So sánh kết quả đo theo đồng hồ mô phỏng với lịch sử xuất CSV; xác định phần không được tính trong một nhiệm vụ.

Bước 6. Tái thực hiện cùng điều kiện ít nhất mười lần; tính số trung bình, độ lệch chuẩn và tỷ lệ thất bại.

Bước 7. Với phép thử cải tiến MAPF hoặc thay đổi kệ, sử dụng cùng đầu vào và báo cáo cả trường hợp cải thiện lẫn trường hợp xấu đi.

PHỤ LỤC D. HƯỚNG DẪN HOÀN THIỆN BẢN NỘP

Để bài tiểu luận phản ánh đúng sản phẩm cuối cùng, nhóm cần điền thông tin bìa, xác thực notebook V21, cập nhật bảng kết quả chương 5 sau khi chạy đủ kịch bản, bổ sung ảnh chụp màn hình do nhóm trực tiếp tạo ra (toàn cảnh kho, chế độ FPS, Tablet WMS, minimap, lịch sử) và ghi chú nguồn “Ảnh chụp từ mô hình V21 của nhóm”. Nếu có thay đổi mã so với mô tả trong TaskTable, phải sửa các mục liên quan đến tham số, trạng thái và thuật toán để bảo đảm toàn bộ báo cáo nhất quán.

Cần phân biệt rõ ba lớp phát biểu trong báo cáo: (1) Nội dung được xác nhận từ tài liệu V21; (2) giải thích lý thuyết từ nguồn học thuật; (3) giải pháp hoặc thí nghiệm đề xuất chưa được thực hiện. Đây là điều kiện cần để các kết luận về hiệu quả mô phỏng có tính kiểm chứng và đáp ứng yêu cầu dẫn nguồn minh bạch của nhóm.

## Hình ảnh nhúng

Các hình ảnh nhúng trong DOCX được giữ trong thư mục `assets/01-tong-quan-mo-hinh`.

- `assets/01-tong-quan-mo-hinh/image1.png`

- `assets/01-tong-quan-mo-hinh/image2.png`

- `assets/01-tong-quan-mo-hinh/image3.png`
