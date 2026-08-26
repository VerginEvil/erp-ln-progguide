# Skill: Infor ERP LN Programmer's Guide (Baan 4GL)

`erp-ln-progguide/` เป็น skill สำหรับ AI Agent / CLI ที่แปลงจากไฟล์ CHM
(`progguide_10.8.12pre_en.chm` + `progguide_10.8.12pre_en_sql.chm`) และ PDF
(`Infor LN Extensions Development Guide 108 (01062026).pdf`) ให้เป็น Markdown
ล้วน เพื่อให้ agent ค้นหาและอ่านได้โดยตรง

- **2,906 + 155 + 162 หน้า** | **2,366 function references** | **17 บท extensions** | ค้นหาด้วย `scripts/search.py`
- Agent อ่านเฉพาะหน้าที่ต้องใช้ -> ประหยัด token

## การติดตั้งให้ agent เรียกใช้

คัดลือกโฟลเดอร์ `erp-ln-progguide/` ไปยังตำแหน่ง skills ของเครื่องมือที่ใช้:

| Tool | ตำแหน่ง |
|---|---|
| opencode | `~/.config/opencode/skill/erp-ln-progguide/` (global) หรือ `.opencode/skill/` ในโปรเจกต์ |
| Claude Code / generic agents | `~/.agents/skills/erp-ln-progguide/` หรือ `.agents/skills/` ในโปรเจกต์ |

Agent จะ trigger skill นี้อัตโนมัติเมื่อเจองานเกี่ยวกับ Baan/LN 4GL, DAL, AFS,
LN SQL, SQLSTATE ฯลฯ ตาม `description` ใน `SKILL.md`

## วิธีใช้ (ที่ agent จะทำ)

```bash
# 1) หา function จากชื่อ
grep -i "seq.open" erp-ln-progguide/references/FUNCTION_INDEX.md

# 2) ค้นหาเชิงความหมาย
python erp-ln-progguide/scripts/search.py utc.add --dir guide
python erp-ln-progguide/scripts/search.py --list-groups
python erp-ln-progguide/scripts/search.py --regex "SQLSTATE" --dir sql

# 3) อ่านเฉพาะไฟล์ .md ที่ชี้มา
```

## โครงสร้าง

```
erp-ln-progguide/
├── SKILL.md                     # entry point + สรุปภาษา Baan 4GL
├── scripts/search.py            # full-text search (Python stdlib เท่านั้น)
├── index/INDEX.tsv              # title -> path ของทุกหน้า
└── references/
    ├── FUNCTION_INDEX.md        # index ฟังก์ชันทั้งหมด (grep ก่อนเสมอ)
    ├── EXTENSIONS_INDEX.md      # index เนื้อหา LN Extensions
    ├── extensions/...           # Infor LN Extensions Development Guide (17 chapters)
    ├── guide/progguide/...      # เนื้อหาหลัก mirror ตาม TOC เดิม
    └── sql/progguide/...        # LN SQL + SQLSTATE messages
```

## Build

สคริปต์แปลงอยู่ที่ temp build dir; CHM ต้นฉบับอยู่ในโฟลเดอร์นี้ หากต้องการ rebuild:
decompile ด้วย `hh.exe -decompile <out> <chm>` แล้วรัน converter (ดู git history)
