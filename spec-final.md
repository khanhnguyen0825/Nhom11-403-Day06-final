# AI Product SPEC Draft: V-Triage (Vinmec AI Triage Assistant)

**Track:** B — Vinmec
**Topic:** Trợ lý AI Phân tuyến chuyên khoa khám bệnh dựa trên triệu chứng
**Nhóm:** Nhom 11
**Ngày:** 08/04/2026

---

## Phân công
1. Khánh: AI Product Canvas + Failure modes.
2. Minh: User Stories 4 paths.
3. Thành: Eval metrics + ROI.
4. Phước: Prototype research + Prompt engineering & testing.
5. Hoài: Xây dựng Test cases + Tổng hợp SPEC Final.


## Problem Statement

Bệnh nhân tại Vinmec thường lúng túng khi tự chọn chuyên khoa phù hợp để thăm khám, dẫn đến việc phải di chuyển qua nhiều khoa gây mất thời gian; bằng cách sử dụng AI Triage, hệ thống giúp phân loại chính xác chuyên khoa ngay tại nhà đồng thời đảm bảo an toàn bằng cách nhận diện sớm các dấu hiệu nguy kịch cần cấp cứu.


## 1. AI Product Canvas

| Mảng | Chi tiết |
|---|---|
| **Value (Giá trị)** | **User:** Bệnh nhân đến khám tại Vinmec.<br>**Pain:** Người bệnh thường hoang mang, không biết mình cần khám khoa nào khi có những triệu chứng mơ hồ, dẫn đến xếp hàng sai khoa, mất thời gian.<br>**AI Value:** Hệ thống phân tích ngôn ngữ tự nhiên từ người dùng (text/voice) và ánh xạ sang phác đồ chuyên khoa của Vinmec 24/7. |
| **Trust (Sự tin cậy)** | **Khi AI sai:** Bệnh nhân có thể phải chờ khám nhầm khoa. <br>**Cách nhận biết:** Bệnh nhân xác nhận lại triệu chứng trước khi chốt lịch, hoặc bác sĩ sàng lọc phát hiện.<br>**Cách sửa:** UI cung cấp nút "Kết quả chưa đúng" hoặc "Bổ sung triệu chứng" để AI phân tích lại. Cung cấp chỉ số niềm tin (Confidence Score). |
| **Feasibility (Khả thi)** | **Cost (Chi phí):** ~0.005$ - 0.01$/request khi dùng API LLM (Gemini/GPT).<br>**Latency (Độ trễ):** 1-3 giây cho mỗi lần phân tích.<br>**Risk chính:** AI bị "ảo giác" (hallucination) tự ý kê đơn thuốc hoặc phớt lờ các triệu chứng nguy hiểm. |

### Automation hay Augmentation?
☑ **Augmentation** — AI chỉ gợi ý chuyên khoa, người dùng (hoặc điều dưỡng) là người quyết định bấm nút "Đặt lịch".
**Justify:** Trong y tế, mọi sai sót đều đánh đổi bằng sức khỏe. AI đóng vai trò như người hỗ trợ sàng lọc ban đầu (triage) chứ không thay thế hoàn toàn bác sĩ trong việc chẩn đoán.

### Learning Signal
1. **User correction đi vào đâu:** Bấm nút "Sửa triệu chứng" / Đổi khoa khám sẽ được log lại vào database.
2. **Product thu signal gì:** Tỉ lệ chấp nhận kết quả đầu tiên (First-time Acceptance Rate) và dữ liệu những ca phải điều chỉnh chuyên khoa.
3. **Data thuộc loại nào:** Domain-specific (Dữ liệu y tế Vinmec) & User-specific (Hành vi đặt lịch).

### Marginal Value: 
Marginal value có khi dữ liệu tạo ra cải thiện mà model nền và đối thủ không dễ có. Dữ liệu triage chung ít lợi thế; dữ liệu vòng kín theo hành trình bệnh nhân thật tại Vinmec (input triệu chứng, quyết định phân tuyến, chỉnh sửa của điều dưỡng/bác sĩ, outcome sau khám) mới tạo lợi thế bền vững.

---

## 2. User Stories theo 4 Paths

**Path 1: Happy Path (AI phân tích đúng, tự tin > 0.8)**
* **Story:** Là một người đau răng, tôi nhập "Tôi đau răng khôn và sưng má". AI tự tin hiển thị: "Khoa Răng Hàm Mặt" và đề xuất nút đặt lịch. Tôi hài lòng và bấm đặt lịch.

**Path 2: Uncertain Path (AI không chắc chắn, tự tin 0.4 - 0.7)**
* **Story:** Là một người đau bụng, tôi nhập "Tôi đau bụng quá". AI chưa đủ thông tin để phân loại giữa Nội tiêu hóa, Ngoại khoa, hay Sản khoa. Trợ lý AI không đoán mò mà hiển thị: "Bạn đau ở vị trí nào quanh rốn? Có kèm buồn nôn không?" kèm các tùy chọn để tôi nhấn.

**Path 3: Error Path (AI phân loại sai / Người dùng sửa)**
* **Story:** Tôi nhập "Tôi bị mỏi tay", AI xếp vào Khoa Cơ Xương Khớp. Tôi nhận ra mình quên chi tiết, bấm nút "Sửa triệu chứng", nhập thêm "Mỏi tay sau khi bị côn trùng cắn". AI xin lỗi, cập nhật lại và chuyển gợi ý sang Khoa Da liễu/Dị ứng.

**Path 4: Safety / Exit Path (Cảnh báo nguy hiểm hoặc Mất lòng tin)**
* **Story:** Tôi nhập "Tôi cảm thấy nhói ở ngực trái và khó thở". AI nhận dạng từ khóa nguy hiểm, màn hình lập tức chuyển cảnh báo Đỏ, không gợi ý chuyên khoa thông thường mà bật thẳng nút gọi khẩn cấp [GỌI 115 / CẤP CỨU VINMEC].

---

## 3. Eval Metrics (Chỉ số đánh giá)

| Metric | Mô tả | 
|---|---|
| **1. Triage Precision** | Tỉ lệ AI gợi ý đúng chuyên khoa so với đánh giá thực tế của bác sĩ. |
| **2. First-time Acceptance** | Tỉ lệ người dùng chấp nhận ngay kết quả đầu tiên mà không cần dùng đến nút "Sửa lỗi". |
| **3. Escalation Rate** | Tỉ lệ các ca AI nhận định là "Không chắc chắn" và chuyển sang hỏi ý kiến điều dưỡng/con người thật. |

* **Threshold (Ngưỡng an toàn):** Triage Precision > 80% (để bắt đầu thử nghiệm thực tế). Nếu dưới ngưỡng này, hệ thống sẽ tự động ép AI chạy ở Path 2 (hỏi thêm câu hỏi) thay vì đoán.
* **Red Flag (Cảnh báo đỏ):** Hệ thống bỏ sót (False Negative) các ca bệnh nguy hiểm đe dọa tính mạng (tức là phân luồng nhầm ca cần cấp cứu sang khoa thường). Nếu số ca này > 0, lập tức vô hiệu hóa AI và điều chỉnh mô hình.

---

## 4. Top 3 Failure Modes (Kịch bản thất bại)

| Failure Mode | Trigger (Nguyên nhân kích hoạt) | Hậu quả | Mitigation (Cách khắc phục) |
|---|---|---|---|
| **1. Ảo giác tư vấn y tế** | User cố tình hỏi LLM về cách uống thuốc hoặc cách tự chữa bệnh tại nhà. | Thay vì bảo đi khám, AI lại dõng dạc kê toa hướng dẫn (Rất nguy hiểm). | **Prompt Engineering:** Ép chặt System Prompt "Tuyệt đối không chẩn đoán/kê đơn". **Rule-based filter:** Cảnh báo mọi output có chứa tên thuốc hoặc liều lượng. |
| **2. Nhận diện sai ca cấp cứu** | User nhập triệu chứng cấp cứu (VD: "ngực nhói") nhưng dùng từ ngữ lạ, lóng. | Phân loại từ "Cấp cứu 115" thành "Khám nội khoa thông thường", gây mất thời gian vàng. | **Redundancy:** Dùng một danh sách keyword khẩn cấp (rule-based) chạy song song với LLM. Bất cứ khi nào dính cụm từ nhạy cảm -> Ép chạy thẳng sang Safety Path. |
| **3. Out-of-scope (Lạc đề)** | Người dùng hỏi những chuyện không liên quan đến viện (VD: Giá xe hơi). | Lãng phí token API, giảm trải nghiệm người dùng, làm loãng dữ liệu. | **Classifier ban đầu:** Cho AI đánh giá "Câu hỏi này có phải y tế không?". Nếu Không -> "Xin lỗi, tôi chỉ hỗ trợ phân tuyến y tế." |

---

## 5. ROI theo 3 kịch bản

| Kịch bản | Giả định | ROI |
|---|---|---|
| **Thận trọng (Conservative)** | AI độ chính xác thấp (60%), bác sĩ vẫn phải can thiệp nhiều. Người dùng e dè. Khởi chạy ở quy mô nhỏ. | Tiết kiệm 10% thời gian sàng lọc của lễ tân. Do mất tiền vận hành Server/API, ROI năm đầu **±0 (Hòa vốn)**. Lợi ích chủ yếu là data thu về. |
| **Thực tế (Realistic)** | Độ chính xác trung bình cao (80%). Người dùng quen với việc dùng AI trước khi đến bệnh viện. | Tiết kiệm 30-40% khối lượng công việc của tổng đài và lễ tân. Giảm tải 20% ca khám nhầm khoa. ROI kỳ vọng: **X1.5 đến X2** chi phí. |
| **Lạc quan (Optimistic)** | Độ chính xác cao (>90%), Data Flywheel hoạt động mạnh mẽ. Thay thế hoàn toàn quy trình phân bệnh thủ công. | Phân luồng hoàn toàn tự động hàng ngàn ca mỗi ngày. Chi phí nhân sự trực Triage giảm 80%. Tăng độ hài lòng bệnh nhân lên mức tối đa. ROI kỳ vọng: **> X5 lần**. |

---

## 6. Mini AI Spec (Cấu hình kỹ thuật sơ bộ)
* **Model:** gpt-4o-mini (hoặc mô hình tương đương đảm bảo xử lý nhanh).
* **System Prompt Core:** 
  > *"Bạn là trợ lý phân loại bệnh nhân (Triage) của Vinmec. Nhiệm vụ của bạn là đọc triệu chứng và phân loại vào 1 trong 20 chuyên khoa đã được cung cấp. TUYỆT ĐỐI KHÔNG chẩn đoán bệnh, KHÔNG kê đơn thuốc. Nếu gặp triệu chứng đe dọa tính mạng (đau ngực, đột quỵ, khó thở nặng), hãy trả về mã EMERGENCY. Output bằng JSON: {'chuyen_khoa': '...', 'confidence_score': 0-1, 'cau_hoi_them': '...'}"*
* **Công cụ tích hợp:** Giao diện (Streamlit / Web App) bắt các luồng JSON để render ra thành khung UI (Thẻ khoa, Cảnh báo đỏ) thay vì chỉ hiện text.
