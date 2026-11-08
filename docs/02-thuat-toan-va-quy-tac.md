# Chương 3_3.5-3.6-3.7

> Chuyển tự động từ `Chương 3_3.5-3.6-3.7.docx`. Nội dung được giữ theo thứ tự đoạn và bảng; công thức/hình ảnh được lưu riêng khi DOCX có nhúng.
DANH MỤC KÝ HIỆU VÀ TỪ VIẾT TẮT

### Bảng 1

| Ký hiệu | Giải thích |
|---|---|
| AGV | Automated Guided Vehicle – robot tự hành theo hướng dẫn |
| FEFO | First Expired, First Out – ưu tiên hàng gần hết hạn trước |
| A* | Thuật toán tìm đường kết hợp chi phí đã đi và ước lượng còn lại |
| CPA | Closest Point of Approach – khoảng cách tiếp cận gần nhất |
| FPS | First-Person View – góc nhìn thứ nhất |
| WMS | Warehouse Management System – hệ thống quản lý kho |
| MAPF | Multi-Agent Path Finding – tìm đường đa tác tử |
| SKU | Stock Keeping Unit – mã phân biệt sản phẩm |
| Δt | Khoảng thời gian giữa hai lần cập nhật |
| f, g, h | Các đại lượng chi phí của thuật toán A* |

# CHƯƠNG 3: XÂY DỰNG MÔ HÌNH TỐI ƯU TUYẾN ĐƯỜNG
VÀ GIẢI QUYẾT XUNG ĐỘT, VA CHẠM
TRONG KHO THÔNG MINH

### 3.5. XÂY DỰNG MÔ HÌNH TỐI ƯU TUYẾN ĐƯỜNG (THUẬT TOÁN TÍNH QUÃNG ĐƯỜNG)

#### 3.5.1. Mục tiêu và bài toán tối ưu

Trong nhà kho thông minh, hoạt động vận chuyển hàng hóa giữa kệ lưu trữ, khu vực giao nhận và trạm sạc quyết định đáng kể đến thời gian hoàn thành đơn hàng. Khi nhiều robot AGV cùng vận hành trong không gian có hạn, một tuyến ngắn về hình học có thể trở nên không hiệu quả nếu phải chờ tại giao lộ hoặc đi qua hành lang đang bị robot khác chiếm dụng. Vì vậy, bài toán điều hướng cần tối ưu chi phí đường đi trong điều kiện có các vật cản tĩnh và vật cản động.

Mô hình Warehouse AGV V21 được mô tả thực hiện chu trình PICK → DROP, tiếp tục lấy đơn tiếp theo từ hàng đợi nếu có, sau đó RETURN → DOCK_TURN → CHARGE → IDLE. Trên phương diện thiết kế, các mục tiêu cụ thể gồm: xác định đường đi có chi phí thấp; không đi xuyên kệ hàng; tránh ưu tiên tuyến gần robot khác; tính lại đường khi bị chặn; và hạn chế những hành trình quay về trạm không cần thiết .

Lưu ý rằng “chi phí thấp nhất” không luôn đồng nghĩa với “quãng đường hình học ngắn nhất”: khi bổ sung trọng số tránh robot, tuyến được chọn có thể dài hơn nhưng ít nguy cơ xung đột hơn.

#### 3.5.2. Mô hình hóa không gian kho và cách tính khoảng cách

Hình 3.5-1. Sơ đồ khái niệm mặt bằng 28 × 28 m, lưới 56 × 56 và các khu vực vận hành. Kệ và tuyến nét đứt chỉ mang tính minh họa.

Kho V21 có mặt bằng 28 × 28 m. Chương trình mô tả việc chia lưới với cạnh mỗi ô là 0,5 m. Do đó số ô trên mỗi chiều bằng 28/0,5 = 56 và toàn lưới có 56 × 56 = 3.136 ô. Những ô thuộc kệ hoặc vật cản tĩnh được đánh dấu không đi qua; mỗi ô hợp lệ là một nút trong đồ thị tìm đường. Các nút lân cận được mở rộng theo bốn hướng trái – phải – trước – sau .

N =  = 56 ô / chiều

Ntotal = 56 × 56 = 3.136 ô

Khoảng cách Euclid đo đường thẳng giữa hai điểm trên mặt phẳng; khoảng cách Manhattan đo tổng độ lệch theo hai trục tọa độ. Khi dùng chỉ số ô lưới, Manhattan là số bước tối thiểu của một lộ trình bốn hướng trong điều kixện không có vật cản.

d_E(A,B)

d_M(A,B) =

Ví dụ tính toán 3.5-A – So sánh hai khoảng cách

Robot xuất phát từ ô A(4; 6), cần đến ô B(11; 9). Chênh lệch tọa độ là Δx = 7 ô và Δz = 3 ô; mỗi bước tương ứng 0,5 m.

Khoảng cách Manhattan bằng 7 + 3 = 10 bước, tương đương 5,0000 m. Khoảng cách Euclid là 0,5 × ≈ 3,8079 m. Vì các bước mở rộng nút bị giới hạn theo bốn hướng, Manhattan thích hợp làm heuristic trong lưới của V21.

d_M = (7 + 3) × 0,5 = 5,0000 m

d_E = 0,5 × √58 = 3,8079 m

Trích từ code V21 — Heuristic Manhattan và bốn hướng mở rộng

### Bảng 2

| const h = n => Math.abs(n.x - goal.x) + Math.abs(n.z - goal.z); const directions = [ [1, 0], [-1, 0], [0, 1], [0, -1] ]; |
|---|

Mã minh họa bổ sung

### Bảng 3

| const CELL_SIZE = 0.5; function manhattan(a, b) { return Math.abs(a.x - b.x) + Math.abs(a.z - b.z); } function euclidean(a, b) { return Math.hypot(a.x - b.x, a.z - b.z); } const A = { x: 4, z: 6 }; const B = { x: 11, z: 9 }; console.log(manhattan(A, B) * CELL_SIZE); // 5 console.log(euclidean(A, B) * CELL_SIZE); // 3.8079... |
|---|

Hệ số CELL_SIZE = 0,5 m/ô dùng để quy đổi từ chỉ số ô sang mét. Trong đoạn code V21, hàm h() dùng số ô làm đại lượng heuristic; các đơn vị chi phí của g(n) cần được thiết kế nhất quán với h(n).

#### 3.5.3. Thuật toán Dijkstra – Cơ sở đối chiếu

Hình 3.5-2. Đường Manhattan theo bốn hướng so với khoảng cách Euclid trong ví dụ A(4;6) → B(11;9).

Dijkstra tìm đường đi có tổng trọng số nhỏ nhất trên đồ thị mà các cạnh đều có trọng số không âm. Thuật toán bắt đầu với chi phí tại nút nguồn bằng 0 và các nút khác bằng vô cùng; mỗi lượt chọn nút chưa xử lý có chi phí tạm thời nhỏ nhất để cập nhật các nút kề .

d(v) ← min{ d(v), d(u) + w(u,v) }

### Bảng 4

| Ký hiệu | Ý nghĩa |
|---|---|
| d(u), d(v) | Chi phí tốt nhất đang biết từ nguồn đến u, v |
| w(u,v) | Trọng số không âm trên cạnh nối u và v |
| min | Chọn chi phí nhỏ hơn giữa tuyến đã biết và tuyến vừa xét |

Ví dụ tính toán 3.5-B – Dijkstra trên đồ thị bốn điểm

Giả sử các cạnh có chi phí: S–A = 2, S–B = 5, A–B = 1, A–G = 6 và B–G = 2 (đơn vị chi phí giả định). Ban đầu d(S)=0, các nút còn lại là vô cùng.

Từ S, cập nhật d(A)=2 và d(B)=5. Chọn A, ta được d(B)=min(5,2+1)=3 và d(G)=min(∞,2+6)=8. Chọn B, cập nhật d(G)=min(8,3+2)=5. Đường ngắn nhất là S→A→B→G, tổng chi phí 5.

d(B) = min(5, 2 + 1) = 3

d(G) = min(8, 3 + 2) = 5

Mã minh họa bổ sung

### Bảng 5

| function dijkstra(graph, start, goal) { const dist = {}, prev = {}, visited = new Set(); for (const n in graph) dist[n] = Infinity; dist[start] = 0; while (true) { let u = null; for (const n in graph) { if (!visited.has(n) && (u === null \|\| dist[n] < dist[u])) u = n; } if (u === null \|\| dist[u] === Infinity \|\| u === goal) break; visited.add(u); for (const [v, weight] of graph[u]) { const candidate = dist[u] + weight; if (candidate < dist[v]) { dist[v] = candidate; prev[v] = u; } } } const path = []; if (dist[goal] !== Infinity) { for (let n = goal; n !== undefined; n = prev[n]) path.unshift(n); } return { cost: dist[goal], path }; } const graph = { S: [['A',2],['B',5]], A: [['S',2],['B',1],['G',6]], B: [['S',5],['A',1],['G',2]], G: [['A',6],['B',2]] }; console.log(dijkstra(graph, 'S', 'G')); |
|---|

#### 3.5.4. Thuật toán A* – Bộ lập kế hoạch đường đi chính

A* kết hợp chi phí đã đi g(n) với chi phí ước lượng h(n) đến đích; nút có tổng f(n) nhỏ nhất được ưu tiên mở rộng. Cơ sở toán học của A* được Hart, Nilsson và Raphael công bố . Trong V21, h(n) là Manhattan và hàm lập đường chính được tài liệu gọi là f5PlanCost(), có các cấu trúc gScore, parent và hàng đợi ưu tiên kiểu binary heap .

f(n) = g(n) + h(n)

h(n) = |x_n − x_goal| + |z_n − z_goal|

### Bảng 6

| Thành phần | Vai trò |
|---|---|
| g(n) | Chi phí tích lũy từ nút bắt đầu đến nút n |
| h(n) | Ước lượng chi phí còn lại từ nút n đến đích |
| f(n) | Giá trị xếp thứ tự ưu tiên khi mở rộng nút |
| parent | Lưu nút trước đó để truy vết lộ trình |
| gScore | Lưu chi phí tốt nhất đã biết đến từng nút |

Ví dụ tính toán 3.5-C – A* trên lưới bốn hướng

Giả sử robot ở S(1;1) và đích tại G(5;4), mỗi bước di chuyển tạm coi có chi phí 1. Tại nguồn: g(S)=0, h(S)=|5−1|+|4−1|=7 nên f(S)=7.

Nếu mở rộng sang A(2;1), ta có g(A)=1, h(A)=6, f(A)=7. Sang B(1;2) cũng cho g(B)=1, h(B)=6, f(B)=7. Việc chọn nút đồng hạng phụ thuộc quy tắc cài đặt; nếu gặp kệ hàng, các nút bị chặn không được đưa vào tuyến.

f(S) = 0 + 7 = 7

f(A) = 1 + 6 = 7

D_min = (4 + 3) × 0,5 = 3,5000 m

Trích từ đoạn code V21 — Khởi tạo tìm đường A*

### Bảng 7

| const h = n => Math.abs(n.x - goal.x) + Math.abs(n.z - goal.z); const directions = [[1,0],[-1,0],[0,1],[0,-1]]; gScore[sourceKey] = 0; push({ n: start, f: h(start) }); |
|---|

Mã minh họa bổ sung

### Bảng 8

| // Mã giả bổ sung mô tả quy trình A* while (!openSet.isEmpty()) { const current = openSet.popMinF(); if (isGoal(current, goal)) return reconstructPath(parent, current); for (const next of getValidNeighbors(current)) { const tentativeG = gScore[current.key] + movementCost(current, next); if (tentativeG < (gScore[next.key] ?? Infinity)) { parent[next.key] = current.key; gScore[next.key] = tentativeG; openSet.pushOrUpdate(next, tentativeG + h(next)); } } } |
|---|

Các hàm openSet.popMinF(), getValidNeighbors() và reconstructPath() trong mã giả không phải là tên hàm xác nhận của V21. Chúng được dùng để làm rõ trình tự chọn nút, cập nhật chi phí và dựng lại lộ trình. Heuristic Manhattan duy trì tính phù hợp khi mỗi bước bốn hướng có chi phí nền không thấp hơn 1 và các phụ phí không âm; điều kiện tối ưu của A* còn phụ thuộc cách cài đặt danh sách mở, cập nhật nút và trọng số cạnh.

#### 3.5.5. Bổ sung chi phí tránh robot khác vào A*

Khi nhiều robot hoạt động, một robot khác không nhất thiết phải được xem như vật cản cố định tuyệt đối. Thay vì khóa mọi ô gần robot, V21 bổ sung chi phí lớn ở vùng rất gần và chi phí nhỏ hơn ở vùng xa hơn; đường đi có nhiều nút gần robot thường có tổng chi phí cao hơn .

C_total(n) = C_movement(n) + C_avoid(n)

Trích từ đoạn code V21 — Chi phí mềm tránh robot

### Bảng 9

| if (avoidOccupied) { for (const other of otherRobots) { const d = f5Dist(world, other.mesh.position); if (d < SAFE_GAP + .12) cost += 28; else if (d < SAFE_GAP + .65) cost += 7; else if (d < SAFE_GAP + 1.3) cost += 1.7; } } |
|---|

Với SAFE_GAP = 0,98 m, các khoảng phạt được tính bằng phép cộng trực tiếp: 0,98+0,12 = 1,10 m; 0,98+0,65 = 1,63 m; 0,98+1,30 = 2,28 m. Các mức 28, 7 và 1,7 là trọng số chi phí mô phỏng, không phải số mét hoặc số giây. Nếu một nút gần nhiều robot, vòng lặp có thể cộng nhiều khoản phạt.

### Bảng 10

| Khoảng cách so với robot khác | Phát sinh mô phỏng |
|---|---|
| d < 1,10 m | +28 |
| 1,10 m ≤ d < 1,63 m | +7 |
| 1,63 m ≤ d < 2,28 m | +1,7 |
| d ≥ 2,28 m | 0 |

Ví dụ tính toán 3.5-D – Đổi đường do phát sinh

Giả sử tuyến 1 dài 12 bước và qua một ô có phát sinh là 28; tuyến 2 dài 16 bước và không gặp bất kỳ phát sinh nào. Đặt chi phí nền mỗi bước bằng 1, ta được tuyến 1 có chi phí 40, tuyến 2 có chi phí 16.

Vì 16 < 40, thuật toán ưu tiên tuyến 2 dù dài hơn 4 bước, tức dài hơn 2 m trên lưới 0,5 m. Cơ chế này làm rõ sự khác biệt giữa tối thiểu chi phí tổng hợp và tối thiểu chiều dài hình học.

C_1 = 12 + 28 = 40

C_2 = 16 + 0 = 16

D_1 = 6 m;  D_2 = 8 m

Hạn chế cốt lõi là việc tăng chi phí dựa trên vị trí hiện tại không tạo ra lịch chiếm chỗ các ô theo thời gian. Hai robot vẫn có thể chọn đường hợp lệ nhưng tiến vào cùng giao lộ trong tương lai. Vì vậy, A* cần kết hợp CPA và kiểm tra bước chuyển động ở mục 3.6. Hướng nghiên cứu xa hơn là MAPF có ràng buộc xung đột, chẳng hạn Conflict-Based Search .

#### 3.5.6. Tính quãng đường PICK – DROP – RETURN

Đường thực hiện của một nhiệm vụ gồm chặng đến vị trí hàng, chặng giao hàng và chặng về sạc (nếu không có nhiệm vụ kế tiếp). Chiều dài toàn hành trình bằng tổng chiều dài các chặng, trong khi thời gian lý tưởng bằng chiều dài chia cho vận tốc giả định không đổi. V21 cho phép robot làm nhiều đơn trong jobQueue trước khi về trạm, vì vậy không phải đơn nào cũng có chặng RETURN riêng ngay sau khi DROP .

D_total = D_pick + D_drop + D_return

T_ideal = D_total / v_max

Ví dụ tính toán 3.5-E – Tổng chiều dài và thời gian

Giả sử chiều dài ba chặng lần lượt là 7 m, 11 m và 9 m. Tổng hành trình bằng 27 m. Nếu dùng v_max=2,3 m/s của V21 thì thời gian lý tưởng 27/2,3 = 11,7391 s, chưa kể tăng giảm tốc, quay góc và chờ nhường đường.

D_total = 7 + 11 + 9 = 27 m

T_ideal = 27 / 2,3 = 11,7391 s

Mã minh họa bổ sung

### Bảng 11

| const MAX_SPEED = 2.3; const dPick = 7, dDrop = 11, dReturn = 9; const totalDistance = dPick + dDrop + dReturn; const idealTime = totalDistance / MAX_SPEED; console.log({ totalDistance, idealTime }); |
|---|

#### 3.5.7. Tính lại tuyến đường khi bị chặn

V21 có cơ chế lập kế hoạch lại khi tuyến đang đi không còn thuận lợi. Tham số REPLAN_INTERVAL = 2,6 được mô tả là nhịp điều tiết thử xử lý lại lộ trình; robot có thể ưu tiên giảm tốc/chờ hoặc tìm lối vòng trước khi thực hiện quét khi bế tắc kéo dài .

Trích từ đoạn code V21 — Tham số phục hồi đường đi

### Bảng 12

| const REPLAN_INTERVAL = 2.6; |
|---|

Ví dụ tính toán 3.5-F – Thời điểm có thể thử lập đường lại

Nếu điều kiện bị chặn được phát hiện từ t=10 s, một khoảng chờ 2,6 s gợi ý thời điểm thử tiếp theo t=12,6 s. Đây là ví dụ về ngưỡng thời gian, không khẳng định mọi robot luôn chạy lại A* đúng mỗi 2,6 s trong bất kỳ trạng thái nào.

t_next = 10 + 2,6 = 12,6000 s

Kết luận mục 3.5: A* có chi phí tránh robot là cơ chế tìm đường chính đã được tài liệu V21 mô tả. Dijkstra được trình bày để đối chiếu lý thuyết. Việc giảm thời gian vận hành cần được kiểm chứng bằng cùng bộ nhiệm vụ, bố cục và tiêu chí đo.

#### 3.5.8. Quy tắc điều hướng chủ động trong A* và đường về

Bên cạnh mô tả toán học của A*, mã V21 triển khai sáu quy tắc điều hướng cụ thể. Các quy tắc QT01–QT06 tác động ngay từ bước lập tuyến, trước khi robot thực sự chuyển động. Trọng số tránh robot trong A* là mức phạt tương đối trên đồ thị, không phải khoảng cách hoặc thời gian đo trực tiếp .

Bảng 3.5-1. Sáu quy tắc lựa chọn tuyến đường và bố trí điểm giao

### Bảng 13

| STT | Quy tắc | Điều kiện kích hoạt / Cách xử lý | Code minh họa trích V21 |
|---|---|---|---|
| 01 | Không đi xuyên qua kệ hàng | Ô có thuộc tính walkable=false bị loại khỏi A*; khi lập lưới kệ, thêm biên 0,25 m. | if(!gridMap[nx][nz].walkable) continue; // markGridUnwalkable: gridMap[x][z].walkable = false; |
| 02 | Tránh robot khác bằng A* | Robot khác là chi phí mềm: dưới 1,10 m cộng 28; dưới 1,63 m cộng 7; dưới 2,28 m cộng 1,7. | if(d<SAFE_GAP+.12) cost+=28; else if(d<SAFE_GAP+.65) cost+=7; else if(d<SAFE_GAP+1.3) cost+=1.7; |
| 03 | Tránh vị trí robot khác sắp tới | Nếu robot khác chạy >0,1 m/s, cách ô <2,5 m và vị trí dự đoán sau 0,65 s quá gần, tăng chi phí 8. | if(other.speed>.1 && d<2.5){ // future uses other.speed*.65 if(f5Dist(world,future)<SAFE_GAP+.25) cost+=8; } |
| 04 | Không đi tắt phía sau trạm sạc | Chặn các nút A* trong dải sau trạm sạc; lối vào/ra ô sạc dùng đường tiếp cận riêng. | if(world.x<2.22 && world.z>17.55 && world.z<26.85) continue; |
| 05 | Hạn chế cắt qua cửa Inbound/Despatch lúc RETURN | Đối với đường về sạc, cộng phí vùng cửa: +85 vùng gần, +6 vùng rộng; không phải cấm tuyệt đối. | if(returnTrip) cost+= returnDoorPenalty(world.x,world.z); |
| 06 | Chia điểm giao theo robot | Giao mặc định tại mỗi cửa chia sáu điểm lệch nhau 1,4 m theo trục x, tránh cùng một điểm đích. | const drop=dropSlot \|\| { x:dock.x+(r.id-2.5)*1.40, z:26.65,y:.15 }; |

Phân tích hệ số: SAFE_GAP = 0,98 m nên ba ngưỡng tránh robot lần lượt là 1,10 m; 1,63 m; 2,28 m. Chi phí cộng 28, 7, 1,7 tạo sự ưu tiên định tính cho đường ít ùn tắc. Ngoài ra, vị trí dự báo của robot khác sau 0,65 s có thể làm tăng chi phí thêm 8. Khi RETURN, returnDoorPenalty() thêm 85 hoặc 6 để ưu tiên tránh cửa giao nhận; không khóa hoàn toàn các lối thoát .

Ví dụ kiểm chứng: Tuyến thứ nhất dài 12 bước (chi phí nền 12) và đi qua một ô bị phạt 28, tổng chi phí bằng 40. Tuyến thứ hai dài 16 bước nhưng không bị phạt, tổng chi phí bằng 16. V21 có thể chọn tuyến thứ hai dù dài hơn 2 m trên lưới 0,5 m. Nếu vùng gần một robot bị chặn tuyệt đối thay vì cộng chi phí mềm, hành lang duy nhất có thể bị loại khiến thuật toán kết luận không có đường.

Điểm cần phân biệt: QT04 là vùng cấm trong đồ thị thông thường, nhưng robot vẫn có đường tiếp cận riêng để ra/vào ô sạc; QT05 chỉ là chi phí phạt ở cửa. QT06 giúp giảm tranh chấp đích tại cửa nhưng không bảo đảm loại bỏ xung đột trên đường đến đó. Vì thế các điều kiện an toàn theo thời gian ở mục 3.6 vẫn bắt buộc.

### 3.6. XÂY DỰNG MÔ HÌNH CHỐNG VA CHẠM VÀ XUNG ĐỘT

#### 3.6.1. Bài toán và kiến trúc phòng tránh nhiều lớp

Hình 3.6-1. Các lớp kiểm soát chuyển động và phục hồi bế tắc trong V21 (sơ đồ diễn giải).

Đường đi hợp lệ tại thời điểm lập kế hoạch không bảo đảm sẽ an toàn trong toàn bộ quá trình vận hành: các robot có thể đối đầu trong hành lang hẹp, cắt nhau tại ngã tư, tiến sát nhau khi theo đuôi hoặc cùng chờ nhau dẫn tới bế tắc. V21 dùng nhiều lớp xử lý: đo khoảng cách; dự đoán CPA; giới hạn vận tốc theo khả năng phanh; kiểm tra bước chuyển động f5AllowedMove(); tính đường vòng/quét khi bị chặn; và luân phiên thứ tự cập nhật sáu robot .

Cần phân biệt: tất cả các phép kiểm tra được tài liệu mô tả ở đây là logic phần mềm. V21 chưa xét đến các yếu tố thực tế, chưa đủ khả năng thu nhận dữ liệu trực tiếp từ cảm biến LiDAR, camera hoặc radar trên thiết bị AGV vật lý; gọi là “cảm biến ảo” mang nghĩa mô phỏng đo khoảng cách từ tọa độ các đối tượng.

#### 3.6.2. Phát hiện vật thể ở gần bằng khoảng cách Euclid

Trong mặt phẳng x–z, tọa độ của robot A và B được dùng để tính khoảng cách. Khoảng cách nhỏ hơn một ngưỡng được thiết lập cho phép đánh dấu tình huống tiến sát; tuy nhiên chỉ biết khoảng cách hiện tại không đủ để xác định hai robot có đang tiến đến va chạm hay không.

d_AB = √[(x_B − x_A)² + (z_B − z_A)²]

Ví dụ tính toán 3.6-A – Phát hiện tiếp cận

Giả sử robot A ở (5;8) m và robot B ở (6;8,6) m, nghĩa là x_B=6 và z_B=8,6. Khi đó Δx=1 m, Δz=0,6 m; khoảng cách là √(1+0,36)=1,1662 m. Khoảng cách lớn hơn SAFE_GAP=0,98 m nên chưa vi phạm ngưỡng tại thời điểm xét, nhưng hướng và tốc độ vẫn phải được kiểm tra bằng CPA.

d_AB = √(1² + 0,6²) = 1,1662 m

1,1662 > 0,98 (m)

Mã minh họa bổ sung

### Bảng 14

| const SAFE_GAP = 0.98; function distance(A, B) { return Math.hypot(B.x - A.x, B.z - A.z); } const A = {x: 5, z: 8}; const B = {x: 6, z: 8.6}; const d = distance(A, B); console.log({d, tooClose: d < SAFE_GAP}); |
|---|

SAFE_GAP = 0,98 m là tham số mô phỏng của V21 , không phải khoảng cách được chứng nhận an toàn cho mọi robot, tải trọng và tốc độ trong môi trường thực tế.

#### 3.6.3. Thuật toán CPA – Closest Point of Approach

Hình 3.6-2. Ví dụ tính CPA với hai robot có đường đi vuông góc; dự đoán giao cắt tại t = 2 giây.

CPA dự đoán thời điểm và khoảng cách gần nhất giữa hai robot trong một khoảng thời gian ngắn nếu hướng và vận tốc được giữ theo giả định dự đoán. Đây là cách nhận biết nguy cơ ở giao lộ ngay cả khi khoảng cách hiện tại còn lớn. Gọi r là vị trí tương đối và vr là vận tốc tương đối:

r = p_B − p_A;      v_r = v_B − v_A

r(t) = r + v_r × t

d(t) = ‖r + v_r × t‖

Bình phương khoảng cách là hàm bậc hai theo thời gian. Lấy đạo hàm và cho bằng 0 để tìm thời điểm cực tiểu trước khi giới hạn kết quả vào cửa sổ dự đoán.

d²(t) = ‖r‖² + 2t(r · v_r) + t²‖v_r‖²

t* = −(r · v_r) / ‖v_r‖²

t_CPA = clamp(t*, 0, T)

d_CPA = ‖r + v_r × t_CPA‖

### Bảng 15

| Biến/hệ số | Ý nghĩa, đơn vị |
|---|---|
| r = (rx, rz) | Vectơ vị trí tương đối, m |
| v_r = (rvx, rvz) | Vectơ vận tốc tương đối, m/s |
| T = 2,4 s | Khoảng dự đoán ngắn hạn trong tài liệu V21 |
| 1e−8 | Ngưỡng số học phòng chia cho vận tốc tương đối gần 0 |
| clamp(x,0,T) | Chặn thời điểm kết quả vào miền [0,T] |

Ví dụ tính toán 3.6-B – Hai robot cắt nhau sau 2 giây

Robot A ở (0;2), vận tốc (1;0) m/s. Robot B ở (2;0), vận tốc (0;1) m/s. Ta có r=(2;−2), v_r=(−1;1), tích vô hướng r·v_r=−4 và ‖v_r‖²=2. Do đó t*=−(−4)/2=2 s, nằm trong cửa sổ 2,4 s.

Tại t=2 s, vectơ khoảng cách tương đối là (2;−2)+2(−1;1)=(0;0), nên d_CPA=0 m. Trong khi đó khoảng cách hiện tại là √8=2,8284 m. Điều này minh họa vì sao chỉ đo khoảng cách hiện tại không đủ phát hiện nguy cơ giao cắt.

t_CPA = 2,0000 s

d_CPA = 0,0000 m

d_now = √8 = 2,8284 m

Trích từ đoạn code V21 — Bước tính CPA

### Bảng 16

| const rvx = ov.x * other.speed - ux * closingSpeed; const rvz = ov.z * other.speed - uz * closingSpeed; const rv2 = rvx * rvx + rvz * rvz; const t = rv2 > 1e-8 ? Math.max(0, Math.min( CONFLICT_HORIZON, -(rx * rvx + rz * rvz) / rv2 )) : 0; const closest = Math.hypot(rx + rvx * t, rz + rvz * t); |
|---|

Mã minh họa bổ sung

### Bảng 17

| function calculateCPA(A, B, T = 2.4) { const rx = B.x - A.x, rz = B.z - A.z; const rvx = B.vx - A.vx, rvz = B.vz - A.vz; const rv2 = rvx * rvx + rvz * rvz; const raw = rv2 > 1e-8 ? -(rx * rvx + rz * rvz) / rv2 : 0; const tCPA = Math.max(0, Math.min(T, raw)); const dCPA = Math.hypot(rx + rvx * tCPA, rz + rvz * tCPA); return {tCPA, dCPA}; } console.log(calculateCPA( {x:0,z:2,vx:1,vz:0}, {x:2,z:0,vx:0,vz:1} )); |
|---|

CPA V21 là một dự báo cục bộ, không phải dự báo mọi quỹ đạo tương lai. Khi robot đổi hướng hoặc giảm tốc sau thời điểm dự đoán, hệ thống phải cập nhật đánh giá ở các khung tiếp theo.

#### 3.6.4. Tính thời gian tiến đến ngưỡng an toàn

Một phép tính bổ trợ để phân tích tình huống đối đầu thẳng hàng là thời gian tiến đến khoảng cách an toàn. Với hai robot đang tiến gần nhau theo cùng đường thẳng, nếu tốc độ đóng khoảng cách tương đối v_closing>0 và d_0>d_safe thì:

t_safe = (d_0 − d_safe) / v_closing

Ví dụ tính toán 3.6-C – Thời gian còn lại trước ngưỡng 0,98 m

Hai robot cách nhau 3 m, mỗi robot đi đối đầu với tốc độ 1 m/s. Khi đó v_closing=2 m/s, ngưỡng an toàn là 0,98 m. Thời gian còn lại là (3−0,98)/2 = 1,0100 s. Công thức chỉ đúng trong điều kiện tốc độ tiến gần không đổi.

v_closing = 1 + 1 = 2 m/s

t_safe = (3 − 0,98) / 2 = 1,0100 s

Mã minh họa bổ sung

### Bảng 18

| function timeToSafetyGap(d, closingSpeed, safeGap = 0.98) { if (d <= safeGap) return 0; if (closingSpeed <= 0) return Infinity; return (d - safeGap) / closingSpeed; } console.log(timeToSafetyGap(3, 2)); // 1.01 |
|---|

Lưu ý học thuật: Đây là phép tính giải thích bổ sung, không phải hàm có tên được xác nhận trong V21; nó không thay thế thuật toán CPA.

#### 3.6.5. Điều tốc dựa trên quãng đường phanh

Biểu đồ 3.6-1. Giới hạn vận tốc lý tưởng theo khoảng trống với BRAKE = 2,7 m/s², MAX_SPEED = 2,3 m/s (đường tính toán, không phải dữ liệu đo).

Khi dự đoán nguy cơ, robot cần giới hạn tốc độ theo quãng đường còn có thể đi. Với gia tốc phanh có độ lớn a_brake không đổi, phương trình động học v_f²=v_0²+2as cho phép suy ra quãng đường phanh và vận tốc giới hạn theo khoảng trống .

d_brake = v² / (2a_brake)

v_safe = √(2a_brake × d_free)

Trích từ đoạn code V21 — Các tham số động học

### Bảng 19

| const SAFE_GAP = 0.98; const MAX_SPEED = 2.3; const ACCEL = 1.15; const BRAKE = 2.7; |
|---|

### Bảng 20

| Thông số | Giá trị | Vai trò |
|---|---|---|
| SAFE_GAP | 0,98 m | Ngưỡng khoảng cách trong mô phỏng |
| MAX_SPEED | 2,3 m/s | Vận tốc tối đa |
| ACCEL | 1,15 m/s² | Độ lớn gia tốc khi tăng tốc |
| BRAKE | 2,7 m/s² | Độ lớn gia tốc khi giảm tốc |

Ví dụ tính toán 3.6-D – Quãng đường phanh từ vận tốc tối đa

Giả sử robot đang chạy 2,3 m/s và mô hình dùng độ lớn phanh 2,7 m/s². Quãng đường phanh động học lý tưởng là 2,3²/(2×2,7)=0,9796 m. Đây chưa tính thời gian trễ, tải trọng và sai số thực tế.

d_brake = 5,29 / 5,4 = 0,9796 m

Ví dụ tính toán 3.6-E – Vận tốc giới hạn còn lại

Nếu khoảng trống cho phép chỉ còn d_free=0,5 m, giới hạn vận tốc lý tưởng là √(2×2,7×0,5)=1,6432 m/s, thấp hơn tốc độ tối đa 2,3 m/s.

v_safe = √2,7 = 1,6432 m/s

Trích từ đoạn code V21 — Tính giới hạn tốc độ

### Bảng 21

| const clearance = Math.max( 0, forward - longitudinal - .04 ); const cap = Math.sqrt(2 * BRAKE * clearance); limit = Math.min(limit, cap); |
|---|

Trong biểu thức, clearance là khoảng còn trống sau khi trừ các thành phần hình học theo hướng chuyển động. Hệ số 0,04 là khoảng đệm trừ thêm trong mã; nếu các biến tính bằng mét thì tương ứng 0,04 m. Do chưa đối chiếu toàn bộ hàm, nghĩa hình học chính xác của forward và longitudinal cần kiểm tra lại trong notebook gốc.

Ví dụ tính toán 3.6-F – Cập nhật vận tốc theo bước thời gian

Robot đang ở 2 m/s, muốn giảm về 1,6432 m/s, bước mô phỏng 0,1 s và độ lớn phanh tối đa 2,7 m/s². Mức giảm tốc trong một bước không vượt 0,27 m/s; vì vậy vận tốc sau bước là max(1,6432; 2−0,27)=1,7300 m/s.

Δv = 2,7 × 0,1 = 0,2700 m/s

v_new = max(1,6432; 1,7300) = 1,7300 m/s

Mã minh họa bổ sung

### Bảng 22

| function updateSpeed(current, target, dt) { const ACCEL = 1.15, BRAKE = 2.7, MAX_SPEED = 2.3; target = Math.max(0, Math.min(MAX_SPEED, target)); if (target > current) return Math.min(target, current + ACCEL * dt); return Math.max(target, current - BRAKE * dt); } console.log(updateSpeed(2, 1.6432, 0.1)); // 1.73 |
|---|

#### 3.6.6. Kiểm tra an toàn của toàn đoạn chuyển động

Hình 3.6-3. Kiểm tra hình chiếu của robot khác lên toàn đoạn di chuyển dự kiến bằng f5AllowedMove().

CPA là lớp dự đoán; hàm f5AllowedMove() được mô tả là lớp kiểm tra ngay trước cập nhật vị trí. Thay vì chỉ xét điểm đầu/cuối, chương trình tìm khoảng cách ngắn nhất từ vị trí robot khác P tới đoạn từ A (vị trí hiện tại) tới B (vị trí dự kiến). Bước không hợp lệ nếu khoảng cách này nhỏ hơn gap .

u = clamp( (P−A)·(B−A) / ‖B−A‖², 0, 1 )

Q = A + u(B−A)

Nếu ‖P−Q‖ < SAFE_GAP ⇒ từ chối bước di chuyển

Ví dụ tính toán 3.6-G – Khoảng cách từ robot đến đoạn đi

Xét A=(0;0), B=(2;0), robot khác ở P=(1;0,4) m. Khi đó B−A=(2;0), bình phương độ dài bằng 4; u=[(1;0,4)·(2;0)]/4=0,5. Điểm gần nhất Q=(1;0), khoảng cách ‖P−Q‖=0,4 m. Vì 0,4<0,98, bước di chuyển bị từ chối.

u = 2 / 4 = 0,5

Q = (1; 0)

d(P,Q) = 0,4000 m < 0,9800 m

Trích từ đoạn code V21 — Kiểm tra đoạn di chuyển

### Bảng 23

| function f5AllowedMove(from, to, exceptId, gap = SAFE_GAP) { for (const other of f5OtherPositions(exceptId)) { const vx = to.x - from.x; const vz = to.z - from.z; const len2 = vx * vx + vz * vz; const u = len2 > 0 ? Math.max(0, Math.min(1, ((other.x-from.x)*vx + (other.z-from.z)*vz) / len2 )) : 0; const closest = { x: from.x + vx*u, z: from.z + vz*u }; if (f5Dist(closest, other) < gap) return false; } return true; } |
|---|

Các biến from/to xác định đoạn đi; exceptId loại robot đang được xét khỏi tập vật cản; len2 là bình phương độ dài đoạn; u là tham số hình chiếu bị giới hạn [0,1]. Hàm này kiểm tra các vị trí robot khác ở thời điểm xử lý, chưa phải kiểm tra quỹ đạo liên tục đồng thời của hai robot trong toàn bộ bước thời gian.

#### 3.6.7. Tìm đường lại, vòng tránh và quét 360° khi bế tắc

Hình 3.6-4. Bộ ứng viên quét 360° gồm 16 hướng và hai bán kính; vùng đỏ minh họa một ứng viên cần loại.

Khi robot bị chặn, V21 ưu tiên giảm tốc/nhường và thử tìm đường lại; khi cần có thể sử dụng hàm hỗ trợ vòng tránh f5TryCooperativeDetour(); nếu bế tắc kéo dài thì xem xét cơ chế f5ScanAndReplan() quét các hướng ứng viên. Đây là hoạt động mô phỏng bằng phần mềm và phép quay đối tượng 3D, không phải quét LiDAR thực .

Trích từ đoạn code V21 — Ngưỡng phục hồi bế tắc

### Bảng 24

| const REPLAN_INTERVAL = 2.6; const BLOCKED_SCAN_AFTER = 14.0; const SCAN_COOLDOWN = 25.0; const SCAN_ANGULAR_RATE = 3.2; |
|---|

### Bảng 25

| Tham số | Giá trị | Giải thích |
|---|---|---|
| REPLAN_INTERVAL | 2,6 s | Nhịp thử lập lại đường |
| BLOCKED_SCAN_AFTER | 14 s | Thời gian bị chặn trước khi xét quét |
| SCAN_COOLDOWN | 25 s | Khoảng nghỉ giữa các lần quét |
| SCAN_ANGULAR_RATE | 3,2 | Tốc độ quay mô phỏng; cần kiểm tra đơn vị trong mã gốc |

Theo tài liệu, hàm quét khảo sát 16 hướng với hai bán kính ứng viên là 1,5 m và 2,5 m. Góc chia đều là Δθ = 360°/16 = 22,5°. Với vị trí ban đầu (x_0,z_0), điểm ứng viên ở hướng θ và bán kính r được tính bằng x=x_0+r cosθ, z=z_0+r sinθ.

Δθ = 360° / 16 = 22,5°

x_k = x_0 + r cos(kΔθ)

z_k = z_0 + r sin(kΔθ)

Ví dụ tính toán 3.6-H – Hướng ứng viên khi quét

Giả sử robot ở (10;10) m. Tại θ=90°, bán kính r=1,5 m cho điểm (10;11,5); bán kính r=2,5 m cho điểm (10;12,5). Nếu xét đủ 16 hướng với hai bán kính có tối đa 32 điểm ứng viên, nhưng các điểm phải được kiểm tra vật cản và tính khả thi đường đi.

N_candidates = 16 × 2 = 32

P(90°, 1,5) = (10; 11,5)

P(90°, 2,5) = (10; 12,5)

Mã minh họa bổ sung

### Bảng 26

| function generateScanCandidates(robot) { const candidates = []; const radii = [1.5, 2.5]; const directions = 16; for (const r of radii) { for (let k = 0; k < directions; k++) { const a = 2 * Math.PI * k / directions; candidates.push({ x: robot.x + r * Math.cos(a), z: robot.z + r * Math.sin(a), radius: r, angle: a }); } } return candidates; } console.log(generateScanCandidates({x:10,z:10}).length); // 32 |
|---|

Nếu SCAN_ANGULAR_RATE=3,2 được dùng theo đơn vị rad/s, thời gian quay 2π rad lý tưởng là 2π/3,2 ≈ 1,9635 s (với π lấy theo giá trị chuẩn của thư viện). Đây chỉ là phép tính theo giả định đơn vị, không phải thời gian quét đo thực tế V21.

T_rotation = 2π / 3,2 ≈ 1,9635 s  (nếu đơn vị là rad/s)

#### 3.6.8. Luân phiên thứ tự xử lý sáu robot

Biểu đồ 3.6-2. Thứ tự cập nhật robot đầu tiên luân phiên sau mỗi 4 giây mô phỏng.

Để hạn chế một robot luôn được cập nhật trước, V21 thay đổi chỉ số bắt đầu vòng xử lý theo chu kỳ bốn giây. Kỹ thuật này tăng sự luân phiên ở mức vòng cập nhật, không tương đương một thuật toán phân quyền giao lộ hay đặt chỗ hành lang theo thời gian .

Trích từ đoạn code V21 — Thứ tự cập nhật luân phiên

### Bảng 27

| function updateFiveFleet(delta) { fleet5Clock += delta; const priority = Math.floor(fleet5Clock / 4) % Math.max(1, fleet5.length); for (let k = 0; k < fleet5.length; k++) { f5Advance(fleet5[(k + priority) % fleet5.length], delta); } } |
|---|

Ví dụ tính toán 3.6-I – Thay đổi thứ tự theo thời gian

Với sáu robot, chỉ số bắt đầu priority = floor(t/4) mod 6. Khi t=0 s, priority=0; t=4 s, priority=1; t=8 s, priority=2; t=24 s, priority quay lại 0. Chu kỳ lặp chỉ số là 6×4=24 s.

priority(t) = floor(t/4) mod 6

T_cycle = 6 × 4 = 24 s

#### 3.6.9. Bộ quy tắc nhường đường, phòng tránh và phục hồi xung đột

Mười sáu quy tắc QT07–QT22 cụ thể hóa ba lớp điều khiển: (i) phát hiện và điều tốc; (ii) kiểm tra an toàn trước mỗi bước; (iii) phục hồi khi bị chặn. Các bảng sau trích những điều kiện và phép tính quan trọng từ bản mã nguồn V21, không phải thuật toán tự sáng tác .

Bảng 3.6-1. Quy tắc cảm biến ảo, dự đoán và giới hạn vận tốc (QT07–QT13)

### Bảng 28

| STT | Quy tắc | Điều kiện kích hoạt / Cách xử lý | Code minh họa trích V21 |
|---|---|---|---|
| 07 | Giảm tốc khi robot nằm trực diện phía trước | Xét vị trí trước robot theo hướng chuyển động và độ lệch ngang <0,8036 m; giới hạn vận tốc theo clearance. | const isDirectlyAhead= forward>.12 && lateral<SAFE_GAP*.82; if(isDirectlyAhead){ const cap=Math.sqrt(2*BRAKE*clearance); limit=Math.min(limit,cap); } |
| 08 | Robot bên cạnh/sau: giảm tốc, không mặc định dừng | Trong khoảng SIDE_RANGE=1,8 m, tốc độ bị hạn chế thận trọng; kiểm tra đoạn di chuyển vẫn có quyền dừng. | if(dist<SIDE_RANGE){ const cap=Math.max(.45,Math.min( MAX_SPEED,.45+(dist-SAFE_GAP)*1.20)); limit=Math.min(limit,cap); } |
| 09 | CPA dự đoán xung đột giao cắt | Trong cửa sổ 2,4 s, khi khoảng cách gần nhất dự báo <1,14 m thì giới hạn vận tốc. | const t=rv2>1e-8 ? Math.max(0, Math.min(CONFLICT_HORIZON, -(rx*rvx+rz*rvz)/rv2)) : 0; if(closest<SAFE_GAP+.16){ reason='CPA_CONFLICT';risk++; } |
| 10 | Tốc độ an toàn theo khoảng cách phanh | Với robot trực diện trong phạm vi cảm biến, giới hạn vận tốc bằng sqrt(2 × BRAKE × free). | const free=Math.max(0, ahead-SAFE_GAP-0.08); const vSafe=Math.sqrt(2*BRAKE*free); allowed=Math.min(allowed,vSafe); |
| 11 | Giảm tốc khi gần kệ hoặc góc kệ | Lấy mẫu các điểm phía trước; nếu gặp hộp vật cản, tính tốc độ theo forwardGap; khi kệ sát bên giới hạn 0,9 m/s. | if(Number.isFinite(forwardGap)){ const vSafe=Math.sqrt(2*BRAKE* Math.max(0,forwardGap-.25)); allowed=Math.min(allowed, Math.max(.25,vSafe)); }else if(close<.9){allowed=Math.min(allowed,.9);} |
| 12 | Giảm tốc trước và sau góc cua | Trước khi vào cua tính giới hạn theo khoảng cách còn lại; sau cua tiếp tục khống chế tại 0,85 m/s. | const safeTurnSpeed=Math.sqrt( TURN_SPEED*TURN_SPEED+2*BRAKE* Math.max(0,dist-.35)); targetSpeed=Math.min(targetSpeed,safeTurnSpeed); |
| 13 | Xoay tại chỗ khi hướng lệch lớn | Góc sai lệch >1,2 rad: tốc độ mục tiêu =0; >0,4 rad: giới hạn còn 0,51 m/s. | const steeringInPlace=headingError>1.2; if(steeringInPlace) targetSpeed=0; else if(headingError>.4) targetSpeed=Math.min(targetSpeed,TURN_SPEED*.6); |

Tính ngưỡng: SAFE_GAP × 0,82 = 0,8036 m (hành lang phía trước trực diện); SAFE_GAP + 0,16 = 1,14 m (ngưỡng CPA); SIDE_RANGE = 1,80 m (cảm biến bên/sau). CPA sử dụng CONFLICT_HORIZON = 2,4 s và vận tốc tương đối; phép tính giới hạn vận tốc tuân theo v_safe = √(2 × BRAKE × d_free), với BRAKE = 2,7 m/s². Các hệ số .45, 1.20, .25 và .35 là tham số điều chỉnh mô phỏng, không phải định luật vật lý độc lập.

Ví dụ: Nếu khoảng trống trước robot còn 0,50 m, giới hạn động học lý tưởng là √(2 × 2,7 × 0,50) = 1,6432 m/s. Trường hợp robot phía bên cạnh chỉ cách 1,20 m, nhánh SIDE_NEIGHBOR cho giới hạn .45 + (1,20−0,98) × 1,20 = 0,7140 m/s, nhưng không tự kết luận phải dừng hẳn. Nếu nhiều nhánh cùng có hiệu lực, bộ điều khiển lấy giới hạn vận tốc nhỏ hơn. Bước cuối vẫn chịu kiểm tra QT14 .

Bảng 3.6-2. Quy tắc kiểm tra bước đi, ghi nhận nhường đường (QT14–QT15)

### Bảng 29

| STT | Quy tắc | Điều kiện kích hoạt / Cách xử lý | Code minh họa trích V21 |
|---|---|---|---|
| 14 | Từ chối bước chuyển động nguy hiểm | Kiểm tra khoảng cách nhỏ nhất từ robot khác tới đoạn đường dự kiến; nếu dưới SAFE_GAP thì hủy bước. | const preventedByRobot=step>0 && !f5AllowedMove(a,next,r.id); if(preventedByRobot){speed=0;step=0;} |
| 15 | Ghi nhận khi thực sự nhường đường | Nếu bắt đầu bị cản bởi robot khác thì tăng conflictCount một lần cho sự kiện; trạng thái hiển thị nhường đường. | if(r.activeTask && blockedByRobot && !r.blockedNow) r.activeTask.conflictCount++; r.blockedNow=blockedByRobot; |

QT14 đánh giá khoảng cách từ robot khác đến toàn đoạn di chuyển dự kiến. Nếu khoảng cách nhỏ hơn 0,98 m, chương trình đặt step = 0. Do đó, một đường A* hợp lệ vẫn có thể bị chặn ở thời điểm thực hiện. QT15 ghi nhận một sự kiện chuyển từ “không bị chặn” sang “bị chặn”, nên conflictCount không phải số khung hình đứng yên. Riêng trường hợp xoay tại chỗ có chủ đích được loại khỏi logic bế tắc .

Bảng 3.6-3. Quy tắc tìm lại đường, tránh ùn tắc và quét 360° (QT16–QT21)

### Bảng 30

| STT | Quy tắc | Điều kiện kích hoạt / Cách xử lý | Code minh họa trích V21 |
|---|---|---|---|
| 16 | Lập lại tuyến có giới hạn chu kỳ | Chỉ thử khi đã qua >=2,6 s, ưu tiên tránh robot, bỏ kết quả mà bước đi mới gần như giống đường cũ. | if(fleet5Clock-r.lastRouteTryAt< REPLAN_INTERVAL) return false; let candidate=planCurrentFleetRoute(r,true); |
| 17 | Tìm lối vòng tránh qua điểm trung gian | Dò bán kính 1,5/2,5/3,5 m và tám hướng; loại điểm gần robot khác; chấm điểm độ dài +0,2 × bán kính. | for(const radius of [1.5,2.5,3.5]) for(let k=0;k<8;k++){ /* ... */ } const score=pathDistance(a,route)+radius*.2; |
| 18 | Nhường robot khác đang đi qua, chưa quét | Không bắt đầu quét nếu robot khác đang di chuyển >0,10 m/s trong phạm vi 2,5 m. | if(nearbyMoving){ r.state='NHƯỜNG ROBOT ĐANG ĐI QUA'; return false; } |
| 19 | Chỉ quét 360° khi thực sự không có tuyến lâu | Nhánh không có đường: thử lại tuyến, tìm vòng sau 4 s; quét được cân nhắc khi không đường >=14 s và hết cooldown. | if(waited>=BLOCKED_SCAN_AFTER && fleet5Clock>=r.nextScanAllowedAt){ if(!r.path.length) f5StartScan(r); } |
| 20 | Quét và chọn hướng tránh vị trí tương lai | Đánh giá 16 hướng × 2 bán kính; loại điểm ứng viên gần vị trí robot khác dự báo ở 0; 0,8; 1,5 s. | return [0,.8,1.5].some(t=> f5Dist(candidate,{ x:pos.x+heading.x*other.speed*t, z:pos.z+heading.z*other.speed*t })<SAFE_GAP+.30); |
| 21 | Tránh quét lặp liên tục | Sau khi bắt đầu lượt quét, khóa chức năng quét thêm tối thiểu 25 giây. | r.nextScanAllowedAt= fleet5Clock+SCAN_COOLDOWN; |

Chu trình phục hồi có điều kiện: (1) QT16 giới hạn thử lập đường lại bằng REPLAN_INTERVAL = 2,6 s; (2) khi đã có đường nhưng không tiến được, nhánh f5Advance() thử lối vòng nếu blockedFor ≥ 4,5 s và thời gian từ lastReplanAt ≥ 6 s; (3) nhánh KHÔNG CÓ ĐƯỜNG thử lối vòng khi waited ≥ 4 s và đã qua 6 s kể từ lần thử trước; (4) chỉ nhánh không có đường mới cân nhắc f5StartScan() sau BLOCKED_SCAN_AFTER = 14 s và khi hết SCAN_COOLDOWN = 25 s. Nếu robot khác đang đi qua gần đó, QT18 hoãn quét. Vì vậy, không thể phát biểu rằng robot luôn quay 360° ngay sau đúng 14 giây đứng yên .

QT17 dò tối đa ba bán kính × tám hướng ứng viên, chấm điểm theo tổng chiều dài tuyến cộng 0,2 lần bán kính. QT20 kiểm tra 16 hướng × hai bán kính, dự báo vị trí robot khác ở các mốc 0; 0,8; 1,5 giây và loại ứng viên cách robot dự báo dưới SAFE_GAP + 0,30 = 1,28 m. Cả hai cơ chế vẫn phụ thuộc khả năng tìm được tuyến hợp lệ đến mục tiêu, chưa triển khai bảng đặt chỗ không gian–thời gian cho toàn bộ đội robot.

Bảng 3.6-4. Quy tắc công bằng trong thứ tự cập nhật (QT22)

### Bảng 31

| STT | Quy tắc | Điều kiện kích hoạt / Cách xử lý | Code minh họa trích V21 |
|---|---|---|---|
| 22 | Luân phiên thứ tự xử lý sáu robot | Dịch vị trí bắt đầu vòng cập nhật sau mỗi 4 s, hạn chế luôn cho một robot chạy tính trước. | const priority= Math.floor(fleet5Clock/4)% Math.max(1,fleet5.length); |

Với sáu robot, chỉ số priority = floor(fleet5Clock/4) mod 6. Tại t = 0, 4, 8, 12, 16, 20 s, robot được xử lý đầu tiên lần lượt là Robot 1, 2, 3, 4, 5, 6; chu kỳ lặp lại sau 24 s. Đây là luân phiên thứ tự xử lý, không phải ưu tiên qua giao lộ hay thuật toán phát lệnh robot phải nhường robot khác một cách toàn cục .

Giới hạn cần công khai: Không có hệ thống reservation-table theo thời gian; biến priorityBoost được khởi tạo và gán lại 0 nhưng không được thấy sử dụng để tăng quyền ưu tiên trong nhánh điều phối chính; collisionCount có mặt trong lịch sử nhưng chưa thấy cơ chế tăng đếm khi kiểm tra va chạm độc lập. Vì vậy số va chạm bằng 0 không tự nó chứng minh an toàn tuyệt đối. Nhóm phát triển cần xem xét và bổ sung kiểm thử hình học độc lập, tình huống đối đầu và kẹt giao lộ trước khi đưa ra kết luận định lượng.

#### 3.6.10. Đánh giá và giới hạn của cơ chế chống va chạm

### Bảng 32

| Lớp xử lý | Cơ chế V21 | Phạm vi hỗ trợ |
|---|---|---|
| Tìm đường | A* với chi phí tránh robot | Giảm ưu tiên tuyến đông robot |
| Phát hiện | Khoảng cách Euclid | Nhận biết vị trí robot ở gần |
| Dự đoán | CPA ngắn hạn | Ước tính khoảng cách gần nhất |
| Điều tốc | Khoảng cách phanh | Giới hạn tốc độ phù hợp |
| Bảo vệ bước | f5AllowedMove() | Không nhận bước đi quá gần robot khác |
| Phục hồi | Replan, detour, scan 360° | Xử lý khi bị chặn |
| Luân phiên | Thay đổi thứ tự update | Giảm ưu tiên cố định |

V21 đã mô tả các cơ chế xử lý ở nhiều lớp, song vẫn thiếu lịch dự trữ ô lưới theo thời gian và bộ đánh giá va chạm độc lập. Như nghiên cứu về Conflict-Based Search chỉ ra, phối hợp đường đi cho nhiều tác tử là bài toán có ràng buộc xung đột liên thời gian . Do đó, không nên kết luận V21 tránh được 100% va chạm hoặc deadlock nếu chưa có số liệu kiểm thử định lượng đáng tin cậy.

### 3.7. THIẾT KẾ GIAO DIỆN MÔ PHỎNG (FPS)

#### 3.7.1. Mục tiêu và công nghệ triển khai

Hình 3.7-1. Phối cảnh bố cục giao diện user FPS

Hình 3.7-2. Phối cảnh bố cục giao diện user - Tablet

Giao diện mô phỏng liên kết tác vụ phát lệnh với bộ điều khiển và quá trình cập nhật trạng thái. Từ đoạn mã của V21, Python chuẩn bị dữ liệu đầu vào; JavaScript xử lý mô phỏng thời gian thực trên trình duyệt; Three.js dựng kho 3D, robot, kệ và đường di chuyển; HTML/CSS/Tailwind CSS/Font Awesome tạo giao diện; IPython.display hỗ trợ hiển thị trang trong Google Colab .

Hai chế độ quan sát chính gồm FPS – người dùng di chuyển trong kho bằng bàn phím và chuột – cùng góc nhìn quản lý 3D, có thể sử dụng OrbitControls nếu thư viện hoạt động. Mini-map 2D cung cấp bố cục từ trên xuống và Tablet WMS hỗ trợ tra cứu, chọn robot, phát lệnh và xem lịch sử.

### Bảng 33

| Thành phần | Vai trò |
|---|---|
| Three.js | Cảnh, đối tượng, camera, ánh sáng, renderer |
| HTML/CSS/Tailwind | Bố cục và hiển thị điều khiển |
| JavaScript | Tương tác người dùng, điều phối và cập nhật |
| Mini-map 2D | Theo dõi vị trí, tuyến và khu vực kệ |
| Tablet WMS | Tra cứu SKU, chọn robot và điểm giao, xuất dữ liệu |

#### 3.7.2. Xây dựng không gian kho 3D

Trong Three.js, Scene chứa các vật thể; Camera xác định góc quan sát; Renderer dựng hình từ Scene và Camera. Mặt sàn kho của mô hình rộng 28 × 28 m, tương ứng diện tích hình học 784 m² nếu một đơn vị không gian bằng một mét. Đây không phải diện tích lưu trữ thực dùng được sau khi trừ kệ và hành lang.

S_floor = 28 × 28 = 784 m²

Mã minh họa bổ sung

### Bảng 34

| const scene = new THREE.Scene(); scene.background = new THREE.Color(0xeaf5f0); const floor = new THREE.Mesh( new THREE.PlaneGeometry(28, 28), new THREE.MeshStandardMaterial({color: 0xd8e2dc}) ); floor.rotation.x = -Math.PI / 2; scene.add(floor); scene.add(new THREE.HemisphereLight(0xffffff, 0x999999, 2)); |
|---|

Hệ số 28 được dùng để xác định hai chiều mặt sàn. Phép xoay −π/2 rad giúp mặt phẳng nằm ngang. Màu sắc và cường độ sáng trong mã minh họa là lựa chọn trình bày, không phải tham số được xác nhận từ V21.

Tài liệu V21 ghi nhận kệ nhỏ gần Inbound đã bị loại bỏ nhằm giữ lối vào thông thoáng, trong khi kệ tập kết Despatch còn lại với cấu hình bên dưới .

Trích từ đoạn code V21 — Cấu hình kệ Despatch

### Bảng 35

| rackConfigs.push({ rowIdx: 2, startX: 24.0, startZ: 18.8, bays: 5, bayWidth: 1.0, depth: 0.8, levels: 3, title: 'Despatch Staging Rack', orientation: 'vertical' }); |
|---|

Ví dụ tính toán 3.7-A – Cấu hình ngăn và tầng kệ

Kệ có 5 bay, mỗi bay rộng 1,0 m, và có 3 tầng. Chiều dài phần ngăn theo hướng xếp giả định là 5×1,0=5 m; tổng vị trí lưu trữ theo cấu hình là 5×3=15 ô. Số kiện hàng thực tế có thể thấp hơn nếu có ô trống.

L_bays = 5 × 1,0 = 5 m

N_slots = 5 × 3 = 15 ô

#### 3.7.3. Camera FPS và công thức góc nhìn phối cảnh

Camera phối cảnh mô phỏng cảm nhận chiều sâu: vật ở xa thường xuất hiện nhỏ hơn vật ở gần. Trong Three.js, PerspectiveCamera có bốn tham số chính (fov, aspect, near, far), trong đó fov là góc nhìn dọc, aspect là tỷ số kích thước vùng render, near/far là mặt phẳng cắt .

θ_horizontal = 2 arctan[ aspect × tan(θ_vertical / 2) ]

### Bảng 36

| Thông số | Ý nghĩa |
|---|---|
| fov | Góc nhìn dọc, độ |
| aspect | Chiều rộng / chiều cao khung hình |
| near | Khoảng cách đến mặt phẳng cắt gần |
| far | Khoảng cách đến mặt phẳng cắt xa |
| camera.position | Tọa độ vị trí quan sát |

Ví dụ tính toán 3.7-B – Góc nhìn ngang từ camera 75°

Giả sử cấu hình minh họa có fov dọc 75°, vùng hiển thị 1280×720 px. Khi đó aspect=16/9≈1,7778; θ_horizontal=2 arctan[(16/9)tan(37,5°)]≈107,5124°. Đây là giá trị ví dụ, không phải thông số đã xác minh của camera V21.

aspect = 1280 / 720 = 1,7778

θ_horizontal ≈ 107,5124°

Mã minh họa bổ sung

### Bảng 37

| const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 100 ); camera.position.set(0, 1.65, 0); camera.rotation.order = 'YXZ'; const renderer = new THREE.WebGLRenderer({antialias: true}); renderer.setSize(window.innerWidth, window.innerHeight); document.body.appendChild(renderer.domElement); |
|---|

Trong đoạn minh họa, độ cao camera 1,65 m giả lập mắt người đứng, fov=75° là lựa chọn tham khảo, near=0,1 và far=100 là khoảng cắt. Tất cả phải đối chiếu với notebook nếu dùng để mô tả cấu hình thật.

#### 3.7.4. Di chuyển FPS bằng các phím W/A/S/D

Theo V21, chế độ FPS cho phép người dùng di chuyển bằng W/A/S/D và xoay góc nhìn bằng chuột. Để tốc độ camera không phụ thuộc tốc độ dựng hình của thiết bị, phép cập nhật vị trí nên nhân tốc độ với thời gian giữa hai khung hình: Δs=vΔt.

Δs = v × Δt

Ví dụ tính toán 3.7-C – Di chuyển theo 60 FPS

Giả sử camera có tốc độ 2 m/s và chương trình hiển thị 60 khung hình/giây. Thời gian một khung hình khoảng 1/60 s, quãng dịch chuyển mỗi khung xấp xỉ 2/60=0,0333 m. Sau một giây giữ cùng hướng với tốc độ không đổi, camera di chuyển khoảng 2 m.

Δt = 1 / 60 s

Δs = 2 / 60 = 0,0333 m/khung

Mã minh họa bổ sung

### Bảng 38

| const keys = new Set(); document.addEventListener('keydown', e => keys.add(e.key.toLowerCase())); document.addEventListener('keyup', e => keys.delete(e.key.toLowerCase())); function updateFPS(dt) { const MOVE_SPEED = 2.0; const forward = new THREE.Vector3(); camera.getWorldDirection(forward); forward.y = 0; forward.normalize(); const right = new THREE.Vector3() .crossVectors(forward, new THREE.Vector3(0,1,0)) .normalize(); const move = new THREE.Vector3(); if (keys.has('w')) move.add(forward); if (keys.has('s')) move.sub(forward); if (keys.has('d')) move.add(right); if (keys.has('a')) move.sub(right); if (move.lengthSq() > 0) { move.normalize(); camera.position.addScaledVector(move, MOVE_SPEED * dt); } } |
|---|

Việc chuẩn hóa vectơ move tránh cho tốc độ di chuyển chéo lớn hơn tốc độ đi thẳng khi hai phím cùng được nhấn. Đây là mã minh họa, chưa bao gồm kiểm tra xuyên tường hoặc kệ; việc bổ sung kiểm tra va chạm camera là cần thiết nếu dùng làm trải nghiệm FPS hoàn chỉnh.

#### 3.7.5. Điều khiển góc nhìn bằng chuột

Chuột tạo độ dịch chuyển Δx, Δy theo pixel; hệ số nhạy k_m (rad/pixel) chuyển đổi chúng sang góc yaw và pitch. Có thể giới hạn pitch để người dùng không nhìn lật camera quá mức.

Δθ_yaw = k_m × Δx

Δθ_pitch = k_m × Δy

Ví dụ tính toán 3.7-D – Góc xoay camera theo chuột

Đặt hệ số nhạy minh họa k_m=0,002 rad/pixel, con trỏ dịch chuyển 100 pixel theo phương ngang. Góc xoay là 0,2 rad, tương đương khoảng 11,4592°. Hệ số này là giá trị tham khảo, không được xác nhận là tham số V21.

Δθ = 100 × 0,002 = 0,2000 rad

Δθ ≈ 11,4592°

Mã minh họa bổ sung

### Bảng 39

| const MOUSE_SENSITIVITY = 0.002; const MAX_PITCH = Math.PI * 85 / 180; function handleMouseLook(deltaX, deltaY) { camera.rotation.y -= deltaX * MOUSE_SENSITIVITY; camera.rotation.x -= deltaY * MOUSE_SENSITIVITY; camera.rotation.x = THREE.MathUtils.clamp( camera.rotation.x, -MAX_PITCH, MAX_PITCH ); } |
|---|

#### 3.7.6. Chọn kiện hàng trong môi trường 3D bằng Raycasting

Để người dùng nhấp chọn một kiện hàng, kỹ thuật raycasting tạo một tia từ camera đi qua vị trí con trỏ đã chuẩn hóa và kiểm tra giao điểm với các mesh. Three.js cung cấp Raycaster, phương thức setFromCamera() và intersectObjects() phục vụ thao tác chọn đối tượng .

x_NDC = 2x_mouse / W − 1

y_NDC = 1 − 2y_mouse / H

Ví dụ tính toán 3.7-E – Quy đổi chuột sang NDC

Vùng render kích thước W=1280, H=720 px. Người dùng nhấp tại (960;360) px, tương ứng x_NDC = 2×960/1280−1=0,5 và y_NDC = 1−2×360/720=0. Tọa độ chuẩn hóa là (0,5;0).

P_NDC = (0,5000; 0,0000)

Mã minh họa bổ sung

### Bảng 40

| const raycaster = new THREE.Raycaster(); const mouse = new THREE.Vector2(); renderer.domElement.addEventListener('click', event => { const rect = renderer.domElement.getBoundingClientRect(); mouse.x = 2 * (event.clientX-rect.left) / rect.width - 1; mouse.y = 1 - 2 * (event.clientY-rect.top) / rect.height; raycaster.setFromCamera(mouse, camera); const hits = raycaster.intersectObjects(productMeshes, true); if (hits.length) { console.log('Selected product', hits[0].object.userData); } }); |
|---|

#### 3.7.7. Chuyển tọa độ kho thành Mini-map 2D

Mini-map hiển thị vị trí robot và các tuyến từ trên xuống. Một phép ánh xạ tuyến tính có thể chuyển tọa độ thế giới sang pixel. Nếu giả định kho trải từ −14 đến +14 m trên cả hai trục và Mini-map rộng W_map, cao H_map, phép biến đổi là:

x_map = [(x_world + 14) / 28] × W_map

y_map = [(z_world + 14) / 28] × H_map

Ví dụ tính toán 3.7-F – Tọa độ robot trên Mini-map

Với Mini-map 280×280 px và robot tại (−7;4) m, ta có x_map=[(−7+14)/28]×280=70 px; y_map=[(4+14)/28]×280=180 px. Kết quả phụ thuộc giả định gốc tọa độ của kho; nếu V21 dùng tọa độ từ 0 đến 28 hoặc đảo chiều z, công thức phải được hiệu chỉnh.

P_map = (70; 180) pixel

Mã minh họa bổ sung

### Bảng 41

| function worldToMinimap(x, z, mapWidth=280, mapHeight=280) { const SIZE = 28, HALF = 14; return { mapX: (x + HALF) / SIZE * mapWidth, mapY: (z + HALF) / SIZE * mapHeight }; } console.log(worldToMinimap(-7, 4)); |
|---|

#### 3.7.8. Tablet WMS và hàng đợi nhiệm vụ

Giao diện Tablet WMS hỗ trợ tra cứu sản phẩm theo SKU, Product ID, tên hoặc vị trí; lựa chọn Robot 1–6; chọn điểm giao Inbound/Despatch hoặc vị trí kệ; thêm lệnh chờ và phát lệnh nhiều nhiệm vụ một lần. Theo mô tả V21, hàng đợi của mỗi robot được xử lý tuần tự, robot chỉ về sạc sau khi hết nhiệm vụ .

Trích từ đoạn code V21 — Tập ô hàng và lệnh chờ

### Bảng 42

| const reservedSlotIds = new Set(); const queuedSlotIds = new Set(); let pendingDispatches = []; |
|---|

Trích từ đoạn code V21 — Phát lệnh vào hàng đợi

### Bảng 43

| for (const cmd of pendingDispatches) { const slot = slotsData.find(s => s.id === cmd.slotId); const r = fleet5[cmd.robotId]; if (!slot \|\| slot.isEmpty \|\| !r \|\| reservedSlotIds.has(cmd.slotId) \|\| queuedSlotIds.has(cmd.slotId)) continue; r.jobQueue.push({...cmd}); queuedSlotIds.add(cmd.slotId); } |
|---|

pendingDispatches lưu các lệnh chưa phát, queuedSlotIds chứa ô đã được xếp hàng, reservedSlotIds chứa ô được robot đang xử lý giữ chỗ. Set hỗ trợ kiểm tra có/không một ID nhanh, giảm khả năng hai lệnh dùng cùng vị trí.

Ví dụ tính toán 3.7-G – Khối lượng nhiệm vụ bình quân

Giả sử người vận hành giao 12 đơn cho sáu robot theo số lượng (3,2,2,1,3,1). Trung bình là 12/6=2 nhiệm vụ/robot. Thống kê này không phản ánh cân bằng thời gian làm việc, vì các nhiệm vụ có thể có quãng đường và độ khó khác nhau.

N_avg = 12 / 6 = 2 nhiệm vụ/robot

#### 3.7.9. Quy tắc điều phối hàng đợi và ra/vào trạm sạc (QT23–QT24)

Ngoài lớp tránh va chạm theo thời gian, V21 có hai quy tắc tổ chức nhiệm vụ và không gian phục vụ giao diện điều phối: chuẩn hóa đường ra/vào ô sạc và chống giao trùng ô hàng. Chúng không trực tiếp quyết định quyền đi trước tại giao lộ nhưng làm giảm số tình huống tranh chấp trên tuyến .

Bảng 3.7-1. Hai quy tắc điều phối trạm sạc và hàng đợi (QT23–QT24)

### Bảng 44

| STT | Quy tắc | Điều kiện kích hoạt / Cách xử lý | Code minh họa trích V21 |
|---|---|---|---|
| 23 | Đi vào/ra ô sạc theo đường tiếp cận riêng | Rời ô sạc ra x=2,75 trước khi lập tuyến; RETURN vào thẳng ô; quay 180° sau khi đã vào ô sạc. | path.push({x:DOCK_APPROACH_X,z:r.bay.z}); path.push({x:r.bay.x,z:r.bay.z}); // In bay: beginDockTurn(r) |
| 24 | Giữ chỗ ô hàng, xử lý hàng đợi rồi về sạc | Không giao trùng ô đã chờ/đang làm; nếu có đơn tiếp theo thì nhận, nếu hết đơn mới gọi fleetReturn(r). | r.jobQueue.push({...cmd}); queuedSlotIds.add(cmd.slotId); // After DROP, when queue is empty: fleetReturn(r); |

Đối với QT23, robot rời ô sạc bằng chuyển động ra điểm tiếp cận tại x = 2,75, rồi mới đi vào tuyến A*. Khi trở về, tuyến được đưa đến vị trí tiếp cận có cùng tọa độ z với ô sạc của robot, tiếp đó tiến thẳng vào ô; DOCK_TURN chỉ thực hiện quay 180° sau khi tới vị trí đỗ. QT24 phân biệt pendingDispatches (chưa phát), queuedSlotIds (đã vào hàng đợi) và reservedSlotIds (đang giữ chỗ thực hiện). Sau DROP, robot nhận đơn tiếp theo nếu còn trong jobQueue; nếu hết mới gọi fleetReturn(r) .

Ví dụ vận hành: Robot 1 nhận các SKU A, C và F, robot 2 nhận SKU B. Robot 1 thực hiện tuần tự A → C → F rồi trở về sạc; robot 2 thực hiện B rồi trở về sạc. Việc này giảm các lượt về sạc trung gian, nhưng thời gian và quãng đường tiết kiệm phải đo từ lịch sử và quỹ đạo thực tế, không suy ra chỉ từ số đơn hàng.

#### 3.7.10. Vòng lặp cập nhật trạng thái và khung hình

Theo mô tả V21, animate() là vòng lặp dựng hình, mỗi khung tính delta và cập nhật đội robot bằng updateFiveFleet(delta). Tốc độ di chuyển trong một khung phụ thuộc Δs=vΔt. Trong Three.js, phương thức Clock.getDelta() trả về khoảng thời gian theo giây giữa hai lần gọi .

Ví dụ tính toán 3.7-H – Khoảng đi trên một frame

Với robot chạy 1,4 m/s và tốc độ hiển thị 60 FPS, Δt≈1/60 s. Khoảng đi lý tưởng trong một frame là 1,4/60≈0,0233 m. Trong V21, con số thực có thể thấp hơn vì điều tốc hoặc hủy bước khi không an toàn.

Δs = 1,4 × (1/60) = 0,0233 m

Mã minh họa bổ sung

### Bảng 45

| const clock = new THREE.Clock(); function animate() { requestAnimationFrame(animate); const delta = clock.getDelta(); updateFPS(delta); // Hàm minh họa FPS updateFiveFleet(delta); // Hàm robot được tài liệu V21 nhắc tới renderer.render(scene, camera); } animate(); |
|---|

#### 3.7.11. Lịch sử nhiệm vụ và cách đánh giá thời gian

Biểu đồ 3.7-1. Ví dụ giả định so sánh thời gian ước tính và thực tế; minh họa cách tính chênh lệch, không phải kết quả chạy mô phỏng.

Sau khi hoàn thành nhiệm vụ, V21 ghi lại robot, SKU, thời gian dự tính, thời gian thực tế, quãng đường đã di chuyển, số xung đột và số va chạm. Các dữ liệu được lưu trong bộ nhớ JavaScript và có thể xuất CSV. Khi làm thí nghiệm, cần tách rõ thời gian giao hàng với thời gian quay về trạm .

Trích từ đoạn code V21 — Ghi nhận lịch sử

### Bảng 46

| taskHistory.push({ robot: `Robot ${r.id + 1}`, sku: t.sku, estimated: t.estimatedSeconds, actual: fleet5Clock - t.start, meters: r.distance - t.startDistance, conflicts: t.conflictCount, collisions: t.collisionCount }); |
|---|

T_estimated = D_plan / v_max

T_actual = t_finish − t_start

ΔT = T_actual − T_estimated

Ví dụ tính toán 3.7-I – Sai lệch thời gian thực tế và dự tính

Nếu quãng đường dự tính của chặng lấy hàng đến giao hàng là 23 m, ở v_max=2,3 m/s thì T_estimated=10 s. Giả sử đồng hồ mô phỏng ghi T_actual=14,5 s, ta được ΔT=4,5 s; tỷ lệ vượt là 4,5/10×100%=45%. Đây là số liệu giả định, không phải đo từ V21.

T_estimated = 23 / 2,3 = 10,0000 s

ΔT = 14,5 − 10 = 4,5000 s

P_delay = 4,5 / 10 × 100% = 45,0000%

Mã minh họa bổ sung

### Bảng 47

| function evaluateTask(distance, actualTime) { const estimated = distance / 2.3; const delay = actualTime - estimated; const delayPercent = delay / estimated * 100; return {estimated, actualTime, delay, delayPercent}; } console.log(evaluateTask(23, 14.5)); |
|---|

Để so sánh có ý nghĩa, D_plan và T_actual phải đo trên cùng phạm vi nhiệm vụ. Trong V21, mô tả thời gian thực tế kết thúc khi giao hàng xong, không bao gồm đường RETURN. Khi dùng số liệu lịch sử để đánh giá tối ưu đường đi, cần đặc biệt tránh cộng thời gian trở về trạm vào một vế nhưng không cộng vào vế còn lại.

#### 3.7.12. Đánh giá giao diện mô phỏng

Giao diện 3D, FPS, Mini-map và Tablet WMS giúp quan sát vật thể và tuyến vận chuyển, hỗ trợ phát lệnh nhiều đơn, theo dõi trạng thái và ghi lịch sử. Việc trực quan hóa tạo điều kiện kiểm tra các tình huống giao nhau giữa robot và diễn giải vì sao hệ thống giảm tốc hoặc lập lại tuyến

Các giới hạn hiện có gồm khả năng hiển thị phụ thuộc hiệu suất trình duyệt; mô phỏng tương tác với hàng không đại diện đầy đủ cơ cấu nâng/hạ và tải trọng vật lý; mã vị trí kệ có thể trùng nếu không bổ sung ngăn; và lịch sử chưa lưu bền vững. Về mặt học thuật, ảnh màn hình và video chứng minh chức năng đã chạy nhưng không thay thế dữ liệu định lượng khi đánh giá hiệu suất thuật toán.

TÀI LIỆU THAM KHẢO

- E. W. Dijkstra, “A note on two problems in connexion with graphs,” Numerische Mathematik, vol. 1, pp. 269–271, 1959, doi: 10.1007/BF01386390.

- P. E. Hart, N. J. Nilsson, and B. Raphael, “A formal basis for the heuristic determination of minimum cost paths,” IEEE Trans. Syst. Sci. Cybern., vol. 4, no. 2, pp. 100–107, Jul. 1968, doi: 10.1109/TSSC.1968.300136.

- G. Sharon, R. Stern, A. Felner, and N. R. Sturtevant, “Conflict-based search for optimal multi-agent pathfinding,” Artificial Intelligence, vol. 219, pp. 40–66, 2015, doi: 10.1016/j.artint.2014.11.006.

- Three.js, “PerspectiveCamera,” Three.js Documentation. [Online]. Available: https://threejs.org/docs/pages/PerspectiveCamera.html. [Accessed: Nov. 8, 2026].

- Three.js, “Raycaster,” Three.js Documentation. [Online]. Available: https://threejs.org/docs/pages/Raycaster.html. [Accessed: Nov. 8, 2026].

- Three.js, “Clock,” Three.js Documentation. [Online]. Available: https://threejs.org/docs/pages/Clock.html. [Accessed: Nov. 8, 2026].

## Hình ảnh nhúng

Các hình ảnh nhúng trong DOCX được giữ trong thư mục `assets/02-thuat-toan-va-quy-tac`.

- `assets/02-thuat-toan-va-quy-tac/image1.png`

- `assets/02-thuat-toan-va-quy-tac/image2.png`

- `assets/02-thuat-toan-va-quy-tac/image3.png`

- `assets/02-thuat-toan-va-quy-tac/image4.png`

- `assets/02-thuat-toan-va-quy-tac/image5.png`

- `assets/02-thuat-toan-va-quy-tac/image6.png`

- `assets/02-thuat-toan-va-quy-tac/image7.png`

- `assets/02-thuat-toan-va-quy-tac/image8.png`

- `assets/02-thuat-toan-va-quy-tac/image9.png`

- `assets/02-thuat-toan-va-quy-tac/image10.png`

- `assets/02-thuat-toan-va-quy-tac/image11.png`

- `assets/02-thuat-toan-va-quy-tac/image12.png`
