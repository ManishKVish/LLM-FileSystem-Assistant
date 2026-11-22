import unittest
from pathlib import Path
from fs_tools import read_file, list_files, write_file, search_in_file
from llm_file_assistant import LLMFileSystemAssistant

class TestFileSystemTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = Path(__file__).parent.parent / "data" / "resumes"

    def test_list_files(self):
        files = list_files(str(self.data_dir))
        self.assertGreaterEqual(len(files), 10)
        pdf_files = list_files(str(self.data_dir), extension=".pdf")
        self.assertGreaterEqual(len(pdf_files), 1)

    def test_read_txt_file(self):
        txt_path = self.data_dir / "resume_alex_chen.txt"
        res = read_file(str(txt_path))
        self.assertEqual(res["status"], "success")
        self.assertIn("Alex Chen", res["content"])
        self.assertIn("line_count", res["metadata"])

    def test_read_docx_file(self):
        docx_path = self.data_dir / "resume_jane_smith.docx"
        res = read_file(str(docx_path))
        self.assertEqual(res["status"], "success")
        self.assertIn("Jane Smith", res["content"])

    def test_read_pdf_file(self):
        pdf_path = self.data_dir / "resume_john_doe.pdf"
        res = read_file(str(pdf_path))
        self.assertEqual(res["status"], "success")
        self.assertIn("John Doe", res["content"])

    def test_search_in_file(self):
        txt_path = self.data_dir / "resume_alex_chen.txt"
        res = search_in_file(str(txt_path), "Kafka")
        self.assertEqual(res["status"], "success")
        self.assertGreaterEqual(res["match_count"], 1)

    def test_write_file(self):
        out_path = Path(__file__).parent.parent / "data" / "test_write.txt"
        res = write_file(str(out_path), "Automated test write content")
        self.assertEqual(res["status"], "success")
        self.assertTrue(out_path.exists())
        out_path.unlink()

    def test_llm_assistant_queries(self):
        assistant = LLMFileSystemAssistant(str(self.data_dir))

        # Query 1
        q1 = assistant.process_query("Read all resumes in the resumes folder")
        self.assertGreaterEqual(q1["total_files_read"], 10)

        # Query 2
        q2 = assistant.process_query("Find resumes mentioning Python experience")
        self.assertGreaterEqual(q2["matches_found"], 1)

        # Query 3
        q3 = assistant.process_query("Create a summary file for resume_john_doe.pdf")
        self.assertEqual(q3["status"], "success")
        self.assertTrue(Path(q3["summary_file_created"]).exists())

if __name__ == "__main__":
    unittest.main()
