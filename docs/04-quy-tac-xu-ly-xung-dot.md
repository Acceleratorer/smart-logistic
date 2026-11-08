# CÁC QUY TẮC XỬ LÝ XUNG ĐỘT TRONG VẬN HÀNH ROBOT

> Chuyển tự động từ `CÁC QUY TẮC XỬ LÝ XUNG ĐỘT TRONG VẬN HÀNH ROBOT.docx`. Nội dung được giữ theo thứ tự đoạn và bảng; công thức/hình ảnh được lưu riêng khi DOCX có nhúng.
CÁC QUY TẮC XỬ LÝ XUNG ĐỘT TRONG VẬN HÀNH ROBOT

### Bảng 1

| STT | Quy tắc | Cách robot xử lý | Code minh họa (V21) |
|---|---|---|---|
| 1 | Tránh kệ hàng và vật cản cố định | Không tìm đường qua ô không thể đi. Bản đồ còn tạo khoảng đệm 0,25 m quanh vật cản khi đánh dấu lưới. | gridMap[x][z].walkable = false; |
| 2 | Tránh khu vực có robot khác | A* cộng chi phí vào vị trí gần robot khác để ưu tiên đường ít ùn tắc. | if(d<SAFE_GAP+.12)cost+=28; else if(d<SAFE_GAP+.65)cost+=7; else if(d<SAFE_GAP+1.3)cost+=1.7; |
| 3 | Tránh vị trí robot khác sắp tiến tới | Dự đoán vị trí sau 0,65 giây; nếu điểm dự đoán quá gần ô đang xét, cộng thêm chi phí 8. | if(other.speed>.1 && d<2.5) if(f5Dist(world,future)<SAFE_GAP+.25)cost+=8; |
| 4 | Không đi tắt phía sau trạm sạc | Loại vùng phía sau các ô sạc khỏi tuyến A* thông thường. | if(world.x<2.22 && world.z>17.55 && world.z<26.85)continue; |
| 5 | Tránh cửa Inbound và Despatch khi quay về sạc | Cộng chi phí vào tuyến RETURN để hạn chế đi qua khu vực giao nhận. | if(returnTrip)cost+=returnDoorPenalty(world.x,world.z); |
| 6 | Phân tách điểm giao hàng cho sáu robot | Tạo các vị trí giao hàng mặc định lệch nhau 1,4 m theo trục X thay vì dùng cùng một tọa độ. | x:dock.x+(r.id-2.5)*1.40, z:26.65 |
| 7 | Gặp robot ngay phía trước | Xác định vật cản trực diện và giới hạn vận tốc theo khoảng trống còn lại. | const isDirectlyAhead=forward>.12 && lateral<SAFE_GAP*.82; |
| 8 | Gặp robot ở bên cạnh hoặc phía sau | Giảm vận tốc thận trọng khi khoảng cách dưới 1,8 m, không mặc định dừng do cảm biến bên. | if(dist<SIDE_RANGE){...} limit=Math.min(limit,cap); |
| 9 | Dự đoán nguy cơ giao cắt bằng CPA | Tính khoảng cách tiếp cận gần nhất trong 2,4 giây. Nếu khoảng cách dưới 1,14 m, giảm giới hạn vận tốc. | if(closest<SAFE_GAP+.16){ reason='CPA_CONFLICT';risk++; } |
| 10 | Giảm tốc theo khoảng cách phanh | Tính vận tốc an toàn từ khoảng trống phía trước và hệ số phanh. | const vSafe=Math.sqrt(2*BRAKE*free); allowed=Math.min(allowed,vSafe); |
| 11 | Giảm tốc khi gần kệ hàng | Lấy mẫu vật cản theo hướng tiến. Nếu có vật cản phía trước, tính lại tốc độ giới hạn. | const vSafe=Math.sqrt(2*BRAKE*Math.max(0,forwardGap-.25)); |
| 12 | Giảm tốc trước và sau góc cua | Giảm tốc trước góc cua và tiếp tục hạn chế vận tốc ngay sau khi rẽ. | const safeTurnSpeed=Math.sqrt(TURN_SPEED*TURN_SPEED+2*BRAKE*Math.max(0,dist-.35)); |
| 13 | Xoay hướng khi lệch nhiều khỏi đường đi | Nếu sai lệch hướng lớn hơn 1,2 rad, đặt tốc độ mục tiêu bằng 0 để xoay. Nếu lớn hơn 0,4 rad, chạy chậm. | if(steeringInPlace)targetSpeed=0; else if(headingError>.4)targetSpeed=Math.min(targetSpeed,TURN_SPEED*.6); |
| 14 | Không thực hiện bước di chuyển không an toàn | Nếu f5AllowedMove() phát hiện nguy cơ tiến quá gần robot khác, hủy bước di chuyển. | const preventedByRobot=step>0&&!f5AllowedMove(a,next,r.id); if(preventedByRobot){speed=0;step=0;} |
| 15 | Ghi nhận trạng thái nhường đường | Khi bị robot khác cản trở, ghi nhận xung đột và chuyển sang trạng thái chờ nếu không tiến được. | if(r.activeTask && blockedByRobot&&!r.blockedNow)r.activeTask.conflictCount++; |
| 16 | Tính toán lại đường khi bị chặn | Thử tìm tuyến A* mới, nhưng không thử quá thường xuyên và không nhận tuyến gần như giống đường cũ. | if(fleet5Clock-r.lastRouteTryAt<REPLAN_INTERVAL)return false; let candidate=planCurrentFleetRoute(r,true); |
| 17 | Tìm lối vòng tránh khi bế tắc | Xét các vị trí trung gian quanh robot theo tám hướng và ba bán kính, rồi chọn tuyến có chi phí phù hợp. | for(const radius of [1.5,2.5,3.5]) for(let k=0;k<8;k++){...} const score=pathDistance(a,route)+radius*.2; |
| 18 | Nhường robot khác đang đi qua gần đó | Nếu robot khác chạy trên 0,1 m/s và cách dưới 2,5 m, không bắt đầu quét 360°. | if(nearbyMoving){r.state='NHƯỜNG ROBOT ĐANG ĐI QUA';return false;} |
| 19 | Quét 360° khi không tìm được đường kéo dài | Sau ít nhất 14 giây không có tuyến và đủ điều kiện, cân nhắc quét 360° để đánh giá hướng khác. | if(waited>=BLOCKED_SCAN_AFTER && fleet5Clock>=r.nextScanAllowedAt){ if(!r.path.length)f5StartScan(r); } |
| 20 | Loại các hướng quét có nguy cơ xung đột | Khi quét, kiểm tra vị trí dự đoán của robot khác tại 0; 0,8; 1,5 giây. Loại ứng viên có khoảng cách dưới 1,28 m. | return [0,.8,1.5].some(t=>f5Dist(candidate,{ x:pos.x+heading.x*other.speed*t, z:pos.z+heading.z*other.speed*t})<SAFE_GAP+.30); |
| 21 | Không quét 360° liên tục | Đặt thời gian nghỉ 25 giây giữa các lần quét. | r.nextScanAllowedAt=fleet5Clock+SCAN_COOLDOWN; |
| 22 | Luân phiên thứ tự cập nhật sáu robot | Thay đổi robot được cập nhật đầu tiên mỗi 4 giây để giảm hiện tượng một robot luôn được xử lý trước. | const priority=Math.floor(fleet5Clock/4)%Math.max(1,fleet5.length); |
| 23 | Ra vào trạm sạc theo lộ trình riêng | Ra khỏi ô sạc theo hướng tiếp cận; khi về, tiến thẳng vào ô rồi mới quay 180°. | path.push({x:DOCK_APPROACH_X,z:r.bay.z}); path.push({x:r.bay.x,z:r.bay.z}); |
| 24 | Tránh trùng nhiệm vụ và về sạc không cần thiết | Giữ chỗ ô hàng, xếp nhiệm vụ theo hàng đợi riêng; khi còn đơn thì tiếp tục làm, chỉ về sạc sau đơn cuối. | r.jobQueue.push({...cmd}); queuedSlotIds.add(cmd.slotId); fleetReturn(r); // Return only after the last delivery. |
