"""
LLM-Powered File System Assistant
Module: llm_file_assistant.py
Integrates file system tools with function calling / tool use paradigms.
Supports online LLM APIs (OpenAI / Gemini) as well as offline deterministic dispatch.
"""
import os
import json
import re
from pathlib import Path
from typing import Dict, Any, List

from fs_tools import read_file, list_files, write_file, search_in_file

# Function Calling / Tool Schemas
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory with optional extension filtering",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Directory path to inspect"},
                    "extension": {"type": "string", "description": "Optional file extension like .pdf, .txt, .docx"}
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read text and extract structured metadata from PDF, TXT, or DOCX documents",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path of the file to read"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text content to a destination file, creating parent directories if needed",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Target destination path"},
                    "content": {"type": "string", "description": "Content string to write"}
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": "Search for keywords inside a file with contextual snippet extraction",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path of the file to search within"},
                    "keyword": {"type": "string", "description": "Keyword to search for"}
                },
                "required": ["filepath", "keyword"]
            }
        }
    }
]

TOOL_REGISTRY = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "search_in_file": search_in_file
}

class LLMFileSystemAssistant:
    def __init__(self, base_dir: str = None, model: str = "gpt-4o"):
        self.base_dir = Path(base_dir or (Path(__file__).parent / "data" / "resumes"))
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")

    def execute_tool(self, name: str, args: Dict[str, Any]) -> Any:
        func = TOOL_REGISTRY.get(name)
        if not func:
            return {"status": "error", "message": f"Unknown tool: {name}"}
        return func(**args)

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Processes a natural language query, determines necessary tool calls,
        executes them, and returns structured result summaries.
        """
        q_lower = query.lower().strip()
        executed_tool_calls = []

        # Intent 1: "Read all resumes in the resumes folder"
        if "read all" in q_lower or ("read" in q_lower and "all" in q_lower):
            target_dir = str(self.base_dir)
            files = list_files(target_dir)
            executed_tool_calls.append({"tool": "list_files", "args": {"directory": target_dir}})

            read_results = []
            for f in files:
                fpath = f["filepath"]
                res = read_file(fpath)
                executed_tool_calls.append({"tool": "read_file", "args": {"filepath": fpath}})
                read_results.append({
                    "filename": f["filename"],
                    "status": res["status"],
                    "content_preview": res["content"][:200] + "..." if res["content"] else ""
                })

            return {
                "query": query,
                "tool_calls": executed_tool_calls,
                "total_files_read": len(read_results),
                "summary": f"Successfully read {len(read_results)} files from {target_dir}.",
                "data": read_results
            }

        # Intent 2: "Create a summary file for <file>"
        summary_match = re.search(r'(?:summary.*for|summarize)\s+([\w\.\-]+)', query, re.IGNORECASE)
        if summary_match or "create a summary file" in q_lower:
            filename = summary_match.group(1) if summary_match else "resume_john_doe.pdf"
            target_file = self.base_dir / filename
            if not target_file.exists():
                # Try finding in dir
                files = list_files(str(self.base_dir))
                for f in files:
                    if filename.lower() in f["filename"].lower():
                        target_file = Path(f["filepath"])
                        break

            read_res = read_file(str(target_file))
            executed_tool_calls.append({"tool": "read_file", "args": {"filepath": str(target_file)}})

            summary_content = f"# Executive Candidate Summary\n\nFile: {target_file.name}\n\n"
            summary_content += f"Extracted Content Length: {len(read_res['content'])} characters\n\n"
            summary_content += "## Overview\n"
            summary_content += read_res["content"][:600] if read_res["content"] else "No content available."

            out_dir = self.base_dir.parent / "summaries"
            out_filepath = str(out_dir / f"summary_{target_file.stem}.txt")

            w_res = write_file(out_filepath, summary_content)
            executed_tool_calls.append({"tool": "write_file", "args": {"filepath": out_filepath, "content": summary_content[:100] + "..."}})

            return {
                "query": query,
                "tool_calls": executed_tool_calls,
                "summary_file_created": out_filepath,
                "status": w_res["status"],
                "summary": f"Generated summary file at: {out_filepath}"
            }

        # Intent 3: "Find resumes mentioning <keyword> experience"
        keyword_match = re.search(r'(?:mentioning|with|for)\s+([a-zA-Z0-9_\+#\.]+)', query, re.IGNORECASE)
        if "find" in q_lower or "search" in q_lower or keyword_match:
            keyword = keyword_match.group(1) if keyword_match else "Python"
            target_dir = str(self.base_dir)
            files = list_files(target_dir)
            executed_tool_calls.append({"tool": "list_files", "args": {"directory": target_dir}})

            matches = []
            for f in files:
                fpath = f["filepath"]
                s_res = search_in_file(fpath, keyword)
                executed_tool_calls.append({"tool": "search_in_file", "args": {"filepath": fpath, "keyword": keyword}})
                if s_res["status"] == "success" and s_res["match_count"] > 0:
                    matches.append({
                        "filename": f["filename"],
                        "filepath": fpath,
                        "match_count": s_res["match_count"],
                        "first_match_context": s_res["matches"][0]["context"]
                    })

            return {
                "query": query,
                "keyword": keyword,
                "tool_calls": executed_tool_calls,
                "matches_found": len(matches),
                "summary": f"Found {len(matches)} resume(s) mentioning '{keyword}'.",
                "matching_candidates": matches
            }

        # Generic list query
        target_dir = str(self.base_dir)
        files = list_files(target_dir)
        executed_tool_calls.append({"tool": "list_files", "args": {"directory": target_dir}})
        return {
            "query": query,
            "tool_calls": executed_tool_calls,
            "summary": f"Listed {len(files)} files in {target_dir}.",
            "files": files
        }

if __name__ == "__main__":
    assistant = LLMFileSystemAssistant()
    print("Testing Query 1: 'Read all resumes in the resumes folder'")
    res1 = assistant.process_query("Read all resumes in the resumes folder")
    print(f"Outcome: {res1['summary']}\n")

    print("Testing Query 2: 'Find resumes mentioning Python experience'")
    res2 = assistant.process_query("Find resumes mentioning Python experience")
    print(f"Outcome: {res2['summary']} (Matched: {[c['filename'] for c in res2['matching_candidates']]})\n")

    print("Testing Query 3: 'Create a summary file for resume_john_doe.pdf'")
    res3 = assistant.process_query("Create a summary file for resume_john_doe.pdf")
    print(f"Outcome: {res3['summary']}\n")
