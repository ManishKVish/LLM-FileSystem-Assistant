"""
File System Tools for LLM-Powered Assistant
Module: fs_tools.py
Implements core file I/O operations, structured text extraction for PDF/DOCX/TXT,
directory traversal, file creation, and contextual keyword search.
"""
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Supported document parsers
try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None


def read_file(filepath: str) -> Dict[str, Any]:
    """
    Reads resume/document files (PDF, TXT, DOCX), extracts text content,
    and returns a structured response with content and metadata.
    Handles errors gracefully with clear status codes.
    """
    path = Path(filepath)

    if not path.exists():
        return {
            "status": "error",
            "error_code": "FILE_NOT_FOUND",
            "message": f"File does not exist: {filepath}",
            "filepath": str(path.resolve()),
            "content": "",
            "metadata": {}
        }

    if not path.is_file():
        return {
            "status": "error",
            "error_code": "NOT_A_FILE",
            "message": f"Path is not a regular file: {filepath}",
            "filepath": str(path.resolve()),
            "content": "",
            "metadata": {}
        }

    try:
        stat = path.stat()
        file_size = stat.st_size
        modified_at = datetime.fromtimestamp(stat.st_mtime).isoformat()
        extension = path.suffix.lower()

        content = ""
        extra_metadata = {}

        if extension == ".txt":
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            extra_metadata["line_count"] = len(content.splitlines())

        elif extension == ".pdf":
            if pypdf is None:
                raise ImportError("pypdf is required to parse PDF documents.")
            reader = pypdf.PdfReader(str(path))
            extra_metadata["page_count"] = len(reader.pages)
            extracted_pages = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                extracted_pages.append(page_text)
            content = "\n".join(extracted_pages)

        elif extension in (".docx", ".doc"):
            if docx is None:
                raise ImportError("python-docx is required to parse DOCX documents.")
            doc = docx.Document(str(path))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            extra_metadata["paragraph_count"] = len(paragraphs)
            content = "\n".join(paragraphs)

        else:
            # Fallback text attempt
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

        return {
            "status": "success",
            "filepath": str(path.resolve()),
            "filename": path.name,
            "extension": extension,
            "content": content,
            "metadata": {
                "filename": path.name,
                "file_size_bytes": file_size,
                "modified_at": modified_at,
                "extension": extension,
                **extra_metadata
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error_code": "READ_ERROR",
            "message": f"Failed reading file {filepath}: {str(e)}",
            "filepath": str(path.resolve()),
            "content": "",
            "metadata": {}
        }


def list_files(directory: str, extension: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Lists all files in a directory with optional extension filtering.
    Returns structured metadata for each file (name, path, size, modified date).
    """
    dir_path = Path(directory)

    if not dir_path.exists() or not dir_path.is_dir():
        return []

    results = []
    target_ext = extension.lower() if extension else None
    if target_ext and not target_ext.startswith("."):
        target_ext = f".{target_ext}"

    for entry in sorted(dir_path.iterdir()):
        if entry.is_file():
            if target_ext and entry.suffix.lower() != target_ext:
                continue

            stat = entry.stat()
            results.append({
                "filename": entry.name,
                "filepath": str(entry.resolve()),
                "extension": entry.suffix.lower(),
                "size_bytes": stat.st_size,
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })

    return results


def write_file(filepath: str, content: str) -> Dict[str, Any]:
    """
    Writes content to a file. Automatically creates parent directories if needed.
    Returns success/failure status and metadata.
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        stat = path.stat()
        return {
            "status": "success",
            "message": "File written successfully.",
            "filepath": str(path.resolve()),
            "filename": path.name,
            "bytes_written": stat.st_size
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed writing to file {filepath}: {str(e)}"
        }


def search_in_file(filepath: str, keyword: str) -> Dict[str, Any]:
    """
    Performs case-insensitive keyword search in file content.
    Returns matches with surrounding context (lines/snippets).
    """
    file_result = read_file(filepath)
    if file_result["status"] != "success":
        return {
            "status": "error",
            "message": file_result.get("message", "Unable to read file"),
            "matches": [],
            "match_count": 0
        }

    content = file_result["content"]
    lines = content.splitlines()
    matches = []

    pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    for line_idx, line in enumerate(lines):
        if pattern.search(line):
            start_ctx = max(0, line_idx - 1)
            end_ctx = min(len(lines), line_idx + 2)
            context_block = "\n".join(lines[start_ctx:end_ctx])

            matches.append({
                "line_number": line_idx + 1,
                "matching_line": line.strip(),
                "context": context_block
            })

    return {
        "status": "success",
        "filepath": file_result["filepath"],
        "filename": file_result["filename"],
        "keyword": keyword,
        "match_count": len(matches),
        "matches": matches
    }
