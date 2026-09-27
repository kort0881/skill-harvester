---
name: youtube-transcript
description: Download YouTube video transcripts with automatic translation to Vietnamese and AI summarization. Perfect for learning English from YouTube, managing knowledge base, and extracting insights from video content.
allowed-tools: Bash,Read,Write,WebFetch,Grep
---

# YouTube Transcript Skill v2.0

**Tự động bóc tách → Dịch → Tóm tắt → Lưu cục bộ**

Giải quyết vấn đề học tiếng Anh qua YouTube:
- Video tiếng Anh nhiều, khó hiểu
- Copy transcript thủ công tốn thời gian
- Phụ thuộc vào AI bên ngoài (ChatGPT, NotebookLM)
- Khó tổ chức và quản lý dữ liệu học tập

## 🎯 Tính năng

| Tính năng | Mô tả | Command |
|-----------|-------|---------|
| **📥 Download** | Lấy transcript gốc (EN/VI) | `-l en` hoặc `-l vi` |
| **🌐 Dịch tự động** | Dịch sang tiếng Việt | `--translate` |
| **📝 Tóm tắt** | Tổng hợp kiến thức, phân tích cấu trúc | `--summarize` |
| **💾 Lưu cục bộ** | Theo cấu trúc folder chủ đề | `-o path` |

## 🎓 Use Cases

### 🎓 Học tiếng Anh qua YouTube
- Video tiếng Anh nhiều → khó hiểu → tải transcript để đọc
- Đọc bản dịch tiếng Việt để hiểu nhanh hơn
- So sánh EN-VI để học từ vựng, ngữ pháp

### 💼 Quản lý kiến thức cá nhân
- Lưu transcript vào thư mục có cấu trúc theo chủ đề
- Tổng hợp từ nhiều video → xây dựng knowledge base
- Không phụ thuộc vào AI cloud (ChatGPT, NotebookLM)

### 📝 Nghiên cứu & Học tập
- Phân tích cấu trúc nội dung video
- Tạo summary và ghi chú tự động
- Trích xuất insights từ video dài

---

## 🚀 Quick Start

### Basic (Chỉ download transcript)

```bash
# Windows - Download transcript tiếng Anh
py scripts/yt_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Windows - Download transcript tiếng Việt
py scripts/yt_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" -l vi

# Mac/Linux
python3 scripts/yt_transcript.py "URL" -l en
```

### With Translation (Download + Dịch tiếng Việt)

```bash
py scripts/yt_transcript.py "URL" --translate
py scripts/yt_transcript.py "URL" -l en --translate -o ./output
```

### Full Pipeline (Download + Dịch + Tóm tắt)

```bash
# Tất cả tính năng
py scripts/yt_transcript.py "URL" --translate --summarize

# Với output folder tùy chỉnh
py scripts/yt_transcript.py "URL" --translate --summarize -o "E:\work\diginno\docs\personal\learning\ai"
```

---

## 📖 Cấu trúc Output

### Default Output

```
E:\work\diginno\transcripts\
└── {video_title}.txt           # Transcript gốc
```

### Với --translate

```
output/
├── {video_title}.txt           # Transcript gốc
└── {video_title}_vi.txt        # Bản dịch tiếng Việt
```

### Với --summarize (Full Pipeline)

```
output/
├── 00_metadata.json            # Video info (title, channel, URL)
├── 01_original.txt             # Transcript gốc (EN)
├── 02_translation.txt          # Bản dịch tiếng Việt
└── 03_summary.md               # Tóm tắt + Phân tích
```

---

## ⚙️ Command Line Options

```
python yt_transcript.py <youtube_url> [options]

Options:
    -l, --lang         Language: en, vi, en-orig, vi-orig (default: en)
    -o, --output       Output directory (default: ./transcripts)
    -t, --translate    Dịch transcript sang tiếng Việt
    -s, --summarize    Tạo summary + phân tích cấu trúc
    -f, --format       Format: txt, vtt, both (default: txt)
    -k, --keep-vtt     Keep VTT file sau khi convert
    -h, --help         Show help message
```

### Ví dụ đầy đủ

```bash
# Download + Dịch + Tóm tắt → Lưu vào folder learning
py scripts/yt_transcript.py "https://youtube.com/watch?v=..." \
    --translate \
    --summarize \
    -o "E:\work\diginno\docs\personal\learning\ai"

# Chỉ download (nhanh)
py scripts/yt_transcript.py "URL" -l en

# Download tiếng Việt
py scripts/yt_transcript.py "URL" -l vi
```

---

## 📁 Thư mục lưu trữ khuyến nghị

```
diginno/
├── docs/
│   ├── personal/                    # Học tập cá nhân
│   │   └── learning/
│   │       ├── ai/                  # Trí tuệ nhân tạo
│   │       ├── programming/         # Lập trình
│   │       ├── productivity/        # Năng suất
│   │       └── business/            # Kinh doanh
│   └── work/                        # Học tập công việc
│       └── training/
│           ├── tools/               # Công cụ làm việc
│           └── skills/              # Kỹ năng mềm
└── transcripts/                     # Raw transcripts (temp)
```

### Ví dụ lưu

```bash
# AI/ML learning
py scripts/yt_transcript.py "URL" --translate --summarize \
    -o "E:\work\diginno\docs\personal\learning\ai"

# Programming tutorial
py scripts/yt_transcript.py "URL" -l en \
    -o "E:\work\diginno\docs\personal\learning\programming\fastapi"

# Work training
py scripts/yt_transcript.py "URL" --translate \
    -o "E:\work\diginno\docs\work\training\notion"
```

---

## 📊 So sánh với các công cụ khác

| Tiêu chí | **YouTube Transcript Skill** | ChatGPT | NotebookLM |
|----------|------------------------------|---------|------------|
| **Dữ liệu** | Lưu cục bộ tại máy | Trên cloud | Trên cloud |
| **Tổ chức** | Theo folder chủ đề | Khó tổ chức | Khó tổ chức |
| **Phụ thuộc** | Không phụ thuộc | Phụ thuộc OpenAI | Phụ thuộc Google |
| **Dịch VI** | Tự động | Có (có phí) | Không |
| **Tóm tắt** | Có (cấu trúc) | Có | Có |
| **Chi phí** | Miễn phí | Có phí theo token | Có phí |
| **Tùy chỉnh** | Cao | Trung bình | Thấp |

### Tại sao chọn YouTube Transcript Skill?

1. **Chủ động kiểm soát dữ liệu** - Không lo mất dữ liệu khi service đổi chính sách
2. **Không phụ thuộc** - Dùng offline được
3. **Tổ chức khoa học** - Folder theo chủ đề, dễ tìm
4. **Miễn phí** - Không tốn chi phí API

---

## 🔄 Workflow Examples

### Workflow 1: Học nhanh (không cần xem video)

```bash
# 1. Tải + Dịch + Tóm tắt
py scripts/yt_transcript.py "https://youtube.com/watch?v=..." \
    --translate --summarize \
    -o "E:\work\diginno\docs\personal\learning\[topic]"

# 2. Đọc file 03_summary.md để nắm nội dung chính

# 3. Nếu cần chi tiết → đọc 02_translation.txt
```

### Workflow 2: Xây dựng Knowledge Base

```bash
# Tạo folder cho series/video course
mkdir "E:\work\diginno\docs\personal\learning\[course-name]"

# Tải từng video trong series
py scripts/yt_transcript.py "URL1" --translate --summarize \
    -o "E:\work\diginno\docs\personal\learning\[course-name]"

py scripts/yt_transcript.py "URL2" --translate --summarize \
    -o "E:\work\diginno\docs\personal\learning\[course-name]"

# ... tiếp tục với các video còn lại
```

### Workflow 3: Học tập công việc

```bash
# Video hướng dẫn công cụ mới
py scripts/yt_transcript.py "URL" --translate --summarize \
    -o "E:\work\diginno\docs\work\training\[tool-name]"
```

---

## 🎯 When to Use This Skill

Kích hoạt skill này khi user:

| Tình huống | Ví dụ |
|------------|-------|
| Cung cấp YouTube URL | "Lấy transcript video này: https://..." |
| Yêu cầu download transcript | "Download transcript từ YouTube" |
| Yêu cầu dịch tiếng Việt | "Dịch sang tiếng Việt", "soạn tiếng việt" |
| Yêu cầu tóm tắt | "Tóm tắt video này", "summary video" |
| Muốn lưu để học sau | "Lưu video này để học sau" |
| Học tiếng Anh | "Giúp tôi học từ video tiếng Anh này" |

### Vietnamese triggers:
- "lấy transcript", "tải phụ đề", "download phụ đề"
- "dịch tiếng việt", "soạn tiếng việt", "việt hóa"
- "tóm tắt video", "tổng hợp nội dung"

### English triggers:
- "download transcript", "get captions from YouTube"
- "translate to Vietnamese", "summary this video"
- "learn from this English video"

---

## ⚙️ How It Works

### Pipeline xử lý:

```
YouTube URL → Extract → Download → Clean → [Translate] → [Summarize] → Save
                 ↓                                   ↓
            Video Info                          Vietnamese
            (metadata)                          Translation
                                                        ↓
                                              Summary + Insights
```

### Chi tiết từng bước:

1. **Extract** - Lấy video info (title, channel, duration)
2. **Download** - Tải transcript (chọn EN hoặc VI)
3. **Clean** - Loại bỏ timestamps, duplicate lines
4. **Translate** (optional) - Dịch sang tiếng Việt bằng deep-translator
5. **Summarize** (optional) - Phân tích cấu trúc, tạo summary
6. **Save** - Lưu theo cấu trúc folder

### Features:

- Auto-install yt-dlp if not present
- Hỗ trợ nhiều ngôn ngữ (en, vi)
- Tự động loại bỏ dòng trùng lặp
- Sanitize filename cho mọi OS
- Color-coded terminal output
- Cross-platform (Windows, Mac, Linux)

---

## 📂 File Structure

```
youtube-transcript/
├── SKILL.md                 # This file
└── scripts/
    ├── yt_transcript.py     # Main Python script
    ├── yt-transcript.bat    # Windows batch file
    └── yt-transcript.sh     # Mac/Linux shell script
```

---

## 📤 Output Files

### Basic (Chỉ download)

```
{output_dir}/
└── {video_title}.txt           # Transcript gốc với metadata header
```

### Với --translate

```
{output_dir}/
├── {video_title}.txt           # Transcript gốc
└── {video_title}_vi.txt        # Bản dịch tiếng Việt
```

### Với --translate --summarize (Full Pipeline)

```
{output_dir}/
├── 00_metadata.json            # Video info (title, channel, URL, duration)
├── 01_original.txt             # Transcript gốc tiếng Anh
├── 02_translation.txt          # Bản dịch tiếng Việt
└── 03_summary.md               # Tóm tắt + Phân tích cấu trúc
```

### Metadata JSON format:

```json
{
  "video_id": "abc123",
  "title": "Video Title",
  "channel": "Channel Name",
  "url": "https://youtube.com/watch?v=...",
  "duration": "15:30",
  "description": "Video description...",
  "download_date": "2026-01-25"
}
```

---

## 📦 Requirements

### Cơ bản (Chỉ download)
- Python 3.6+
- yt-dlp (auto-installed if missing)
- Internet connection

### Với --translate (Dịch tiếng Việt)
- `deep-translator`
- `googletrans` (fallback)

### Với --summarize (Tóm tắt)
- `langchain` (optional, cho AI summarization)
- Hoặc dùng Claude Read để tóm tắt

### Cài đặt đầy đủ:

```bash
pip install yt-dlp deep-translator langchain
```

---

## 🔧 Troubleshooting

### Không có subtitles available

Một số video không có phụ đề. Thử:
```bash
# Thử ngôn ngữ khác
py scripts/yt_transcript.py "URL" -l vi

# Thử bản gốc (chất lượng cao hơn)
py scripts/yt_transcript.py "URL" -l en-orig

# Kiểm tra video có captions không
# (vào YouTube → CC icon phải được bật)
```

### Lỗi yt-dlp

```bash
# Cập nhật yt-dlp
pip install --upgrade yt-dlp
```

### Lỗi translation

```bash
# Cài đặt deep-translator
pip install deep-translator

# Nếu lỗi quota, thử Google Translate alternative
pip install googletrans==4.0.0-rc1
```

### Permission denied (Mac/Linux)

```bash
chmod +x scripts/yt-transcript.sh
```

### Không tạo được folder

```bash
# Kiểm tra quyền ghi
ls -la {output_dir}

# Tạo folder thủ công trước
mkdir -p "E:\work\diginno\docs\personal\learning\ai"
```

---

## 🚀 Advanced Usage (Claude Code)

### Download + Dịch + Tóm tắt

```bash
# Windows - Full pipeline
py scripts/yt_transcript.py "URL" --translate --summarize \
    -o "E:\work\diginno\docs\personal\learning\[topic]"

# Mac/Linux
python3 scripts/yt_transcript.py "URL" --translate --summarize \
    -o "~/diginno/docs/personal/learning/[topic]"
```

### Claude Code workflow

```bash
# 1. Download + Translate + Summarize
py scripts/yt_transcript.py "https://youtube.com/watch?v=..." \
    --translate --summarize \
    -o "E:\work\diginno\docs\personal\learning\[topic]"

# 2. Claude đọc file output
# Read 03_summary.md → nắm nội dung chính
# Read 02_translation.txt → đọc chi tiết

# 3. Nếu cần → Claude tạo thêm ghi chú
```

### Script handles:

- Auto-install yt-dlp
- Language fallback (en → en-orig → vi)
- VTT → TXT conversion với deduplication
- Filename sanitization
- Error handling với helpful messages
- Translation (nếu có --translate)
- Summary generation (nếu có --summarize)

---

## 💡 Tips & Best Practices

### 📚 Học tiếng Anh

1. **Đọc song song**: Mở 01_original.txt (EN) + 02_translation.txt (VI) cạnh nhau
2. **Từ vựng**: Copy từ mới từ transcript vào Anki hoặc notebook
3. **Nghe đọc**: Dùng transcript để nghe audio, so sánh pronunciation

### 📁 Tổ chức Knowledge Base

1. **Đặt tên folder theo chủ đề**: `ai/`, `programming/`, `productivity/`
2. **Series video**: Tạo subfolder riêng cho từng course
3. **Backup**: Đồng bộ folder docs/ lên cloud (Google Drive, Dropbox)

### ⏱️ Hiệu quả

1. **Video dài (>1h)**: Tải về đọc offline, tiết kiệm thời gian xem
2. **Series**: Tải nhiều video cùng lúc bằng script loop
3. **Sau khi tóm tắt**: Xóa file gốc trong `transcripts/` nếu không cần

---

## 📚 Nguồn video tham khảo

Một số kênh YouTube chất lượng cao để test:

**AI & Machine Learning:**
- MIT OpenCourseWare
- Stanford Online
- Andrew Ng's DeepLearning.AI

**Programming:**
- Traversy Media
- Fireship
- FreeCodeCamp

**Productivity & Learning:**
- Thomas Frank
- Ali Abdaal
- Matt D'Avella

---

## ✅ Quick Reference

```bash
# CHỈ DOWNLOAD
py scripts/yt_transcript.py "URL" -l en

# DOWNLOAD + DỊCH
py scripts/yt_transcript.py "URL" --translate

# FULL PIPELINE
py scripts/yt_transcript.py "URL" --translate --summarize \
    -o "E:\work\diginno\docs\personal\learning\[topic]"
```

**Remember:** Dữ liệu của bạn = Dữ liệu của bạn. Không phụ thuộc vào AI cloud!

---

*YouTube Transcript Skill v2.0 - Built by Diginno*
