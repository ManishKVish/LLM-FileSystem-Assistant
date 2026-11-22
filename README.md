# LLM-Powered File System Assistant

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tool Calling](https://img.shields.io/badge/Function%20Calling-JSON%20Schema-green.svg)]()
[![Airtribe Assignment](https://img.shields.io/badge/Airtribe-Backend%20AI%20Track-orange.svg)]()

This repository contains the complete implementation for **Milestone 1 (LLM-Powered File System Assistant)** of the Airtribe Backend AI track.

---

## 🎯 Learning Objectives & Architecture

- Implement structured tool interfaces with JSON schema specifications.
- Parse multi-format documents (PDF, DOCX, TXT) with robust metadata extraction.
- Handle file I/O operations programmatically with error handling.
- Build an agent capable of interpreting natural language queries and executing tool sequences:
  - *"Read all resumes in the resumes folder"*
  - *"Find resumes mentioning Python experience"*
  - *"Create a summary file for resume_john_doe.pdf"*

---

## 📁 Repository Structure

```
├── fs_tools.py               # Part A: Core file system tools (read, list, write, search)
├── llm_file_assistant.py     # Part B: LLM function calling integration & query executor
├── create_sample_resumes.py  # Script generating sample PDF, DOCX, and TXT resumes
├── data/
│   └── resumes/              # 10 realistic sample resumes across engineering domains
├── tests/
│   └── test_fs_tools.py      # Automated test suite
├── requirements.txt
└── README.md
```

---

## 🛠️ Tool Specifications (`fs_tools.py`)

1. `read_file(filepath: str) -> dict`:
   - Supports `.pdf`, `.docx`, `.txt`.
   - Returns extracted content and metadata (`filename`, `file_size_bytes`, `modified_at`, `page_count` / `line_count`).
2. `list_files(directory: str, extension: str = None) -> list`:
   - Enumerates files in a directory with optional extension filtering.
3. `write_file(filepath: str, content: str) -> dict`:
   - Creates parent directories automatically and writes content.
4. `search_in_file(filepath: str, keyword: str) -> dict`:
   - Case-insensitive search returning matches with surrounding multi-line context.

---

## 🏃 Setup and Execution

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run automated tests:
   ```bash
   python -m unittest discover tests
   ```
3. Run the interactive assistant:
   ```bash
   python llm_file_assistant.py
   ```
