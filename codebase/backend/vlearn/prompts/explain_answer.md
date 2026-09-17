# Quy tắc cấu trúc giải thích đáp án (dùng chung cho MCQ và tự luận)

File này KHÔNG phải một system prompt gọi LLM riêng — nó là bản mô tả cấu
trúc giải thích thống nhất mà cả hai nơi dưới đây phải tuân theo:

- `grader.py` khi dựng giải thích deterministic cho câu MCQ (không gọi LLM).
- `prompts/grade_text.md` khi LLM chấm câu tự luận (có gọi LLM).

## Cấu trúc bắt buộc: Nhận định → Vì sao → Trích dẫn

1. **Nhận định** — một câu ngắn nói thẳng: đúng, sai, đúng một phần, hay
   không đủ thông tin để chấm.
2. **Vì sao** — 1-2 câu giải thích lý do, bám sát ý trong transcript (không
   thêm kiến thức ngoài nguồn).
3. **Trích dẫn** — nhắc lại (hoặc dẫn) đúng đoạn transcript làm căn cứ, kèm
   mã `[Txx-NNN]` thật.

## Ví dụ (MCQ, đúng)

> **Đúng.** Bạn đã chọn đúng: token là đơn vị máy dùng để "đọc" văn bản, có
> thể là một phần của từ chứ không phải nguyên một từ. Theo transcript
> `[T04-049]`: "...nó không phải là từ, không phải là chữ cái, mà nó là
> token... Nó sẽ chẻ nhỏ những cái từ đấy ra thành token...".

## Ví dụ (tự luận, sai)

> **Sai.** Câu trả lời cho rằng hallucination là do lỗi phần mềm/server, nhưng
> theo transcript, đây là hệ quả của cách model dự đoán từ tiếp theo, không
> phải lỗi kỹ thuật. Trích `[T04-048]`: "...nó đang cố nối những cái từ với
> nhau cho có nghĩa thôi...".

Giữ giải thích ngắn (2-4 câu), không lan man, không thêm ý ngoài transcript.
