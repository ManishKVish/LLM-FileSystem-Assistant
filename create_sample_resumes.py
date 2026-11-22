"""
Generates 10 realistic sample resume files in PDF, DOCX, and TXT formats.
"""
from pathlib import Path
import docx
from pypdf import PdfWriter
import io

DATA_DIR = Path(__file__).parent / "data" / "resumes"
DATA_DIR.mkdir(parents=True, exist_ok=True)

RESUMES = [
    {
        "filename": "resume_john_doe.pdf",
        "format": "pdf",
        "name": "John Doe",
        "title": "Senior Machine Learning Engineer",
        "experience_years": 6,
        "skills": ["Python", "Machine Learning", "PyTorch", "TensorFlow", "FastAPI", "Docker", "AWS"],
        "education": "B.Tech in Computer Science, IIT Bombay (2018)",
        "summary": "Experienced ML Engineer with 6+ years building and deploying scalable recommendation systems and deep learning models into production pipelines.",
        "experience": (
            "Lead ML Engineer at DataCorp (2021 - Present):\n"
            "- Designed real-time recommendation engine in Python & PyTorch serving 50M requests daily.\n"
            "- Reduced model inference latency by 45% using ONNX runtime and Docker containerization.\n\n"
            "Software Engineer (ML) at AI Solutions (2018 - 2021):\n"
            "- Built computer vision classification models with TensorFlow and deployed on AWS ECS."
        )
    },
    {
        "filename": "resume_jane_smith.docx",
        "format": "docx",
        "name": "Jane Smith",
        "title": "Full Stack Software Engineer",
        "experience_years": 4,
        "skills": ["React", "TypeScript", "Node.js", "Express", "PostgreSQL", "TailwindCSS"],
        "education": "B.S. in Software Engineering, UC Berkeley (2020)",
        "summary": "Frontend-focused Full Stack Developer with 4 years building interactive single-page applications and performant REST APIs.",
        "experience": (
            "Full Stack Engineer at WebWave (2022 - Present):\n"
            "- Developed responsive client dashboards using React 18, TypeScript, and Redux Toolkit.\n"
            "- Implemented Node.js/Express microservices backed by PostgreSQL.\n\n"
            "Junior Frontend Developer at StartupHub (2020 - 2022):\n"
            "- Built reusable UI component library in React."
        )
    },
    {
        "filename": "resume_alex_chen.txt",
        "format": "txt",
        "name": "Alex Chen",
        "title": "Backend Systems Architect",
        "experience_years": 8,
        "skills": ["Python", "Go", "Distributed Systems", "PostgreSQL", "Kafka", "Kubernetes", "gRPC"],
        "education": "M.S. in Computer Science, Stanford University (2016)",
        "summary": "Senior Backend Architect specializing in high-throughput distributed architectures, event streaming with Kafka, and low-latency microservices.",
        "experience": (
            "Principal Backend Engineer at StreamTech (2020 - Present):\n"
            "- Architected event streaming platform processing 250k events/sec using Go, Python, and Kafka.\n"
            "- Optimized PostgreSQL schema and sharding strategies across multi-region deployments.\n\n"
            "Senior Systems Engineer at CloudGlobal (2016 - 2020):\n"
            "- Designed gRPC communication fabric on Kubernetes clusters."
        )
    },
    {
        "filename": "resume_priya_sharma.pdf",
        "format": "pdf",
        "name": "Priya Sharma",
        "title": "Lead DevOps & Cloud Engineer",
        "experience_years": 7,
        "skills": ["Kubernetes", "Docker", "Terraform", "AWS", "CI/CD", "Prometheus", "Python", "Linux"],
        "education": "B.E. in Information Technology, BITS Pilani (2017)",
        "summary": "Cloud platform engineer with expertise in Infrastructure as Code (Terraform), zero-downtime Kubernetes deployments, and automated CI/CD pipelines.",
        "experience": (
            "Lead DevOps Engineer at FinCloud (2021 - Present):\n"
            "- Managed enterprise multi-account AWS architecture supporting 200+ microservices on EKS.\n"
            "- Automated deployment pipelines reducing deployment cycle time from 2 hours to 8 minutes.\n\n"
            "DevOps Engineer at ScaleOps (2017 - 2021):\n"
            "- Maintained monitoring stack with Prometheus and Grafana."
        )
    },
    {
        "filename": "resume_michael_brown.docx",
        "format": "docx",
        "name": "Michael Brown",
        "title": "Java Spring Boot Backend Engineer",
        "experience_years": 5,
        "skills": ["Java", "Spring Boot", "Microservices", "Hibernate", "MySQL", "Docker", "RabbitMQ"],
        "education": "B.S. in Computer Science, University of Texas (2019)",
        "summary": "Backend specialist proficient in building resilient enterprise services with Java 17, Spring Boot, and relational database tuning.",
        "experience": (
            "Backend Developer at Enterprise Core (2021 - Present):\n"
            "- Developed payment reconciliation APIs in Java and Spring Boot with MySQL.\n"
            "- Integrated RabbitMQ message brokers for asynchronous payment settlement.\n\n"
            "Software Developer at TechCorp (2019 - 2021):\n"
            "- Maintained Spring Data JPA persistence layer."
        )
    },
    {
        "filename": "resume_sara_connor.txt",
        "format": "txt",
        "name": "Sara Connor",
        "title": "Data Scientist & NLP Specialist",
        "experience_years": 5,
        "skills": ["Python", "NLP", "Transformers", "HuggingFace", "LangChain", "Vector Databases", "ChromaDB"],
        "education": "M.S. in Data Science, University of Washington (2019)",
        "summary": "Data Scientist passionate about Natural Language Processing, retrieval-augmented generation (RAG), and modern transformer embeddings.",
        "experience": (
            "Senior Data Scientist at CogniAI (2021 - Present):\n"
            "- Built enterprise RAG search system indexing 500,000 PDF contracts using ChromaDB.\n"
            "- Fine-tuned BERT and modern sentence-transformer models for semantic semantic retrieval.\n\n"
            "NLP Researcher at DeepText (2019 - 2021):\n"
            "- Researched document classification and named entity extraction algorithms."
        )
    },
    {
        "filename": "resume_david_kim.pdf",
        "format": "pdf",
        "name": "David Kim",
        "title": "Mobile App Developer (iOS & Android)",
        "experience_years": 4,
        "skills": ["Flutter", "Dart", "Swift", "Kotlin", "Firebase", "REST APIs"],
        "education": "B.S. in Computer Science, Georgia Tech (2020)",
        "summary": "Cross-platform mobile engineer delivering smooth user experiences on iOS and Android with Flutter and native integrations.",
        "experience": (
            "Mobile App Engineer at AppCrafters (2020 - Present):\n"
            "- Shipped 4 top-rated apps on App Store and Google Play with 1M+ total downloads.\n"
            "- Implemented offline caching and biometric authentication."
        )
    },
    {
        "filename": "resume_ananya_verma.docx",
        "format": "docx",
        "name": "Ananya Verma",
        "title": "Frontend React & UI Engineer",
        "experience_years": 3,
        "skills": ["React", "JavaScript", "HTML5", "CSS3", "Next.js", "Redux", "Figma"],
        "education": "B.Tech in Computer Engineering, Delhi University (2021)",
        "summary": "Frontend developer focusing on responsive design, modern React workflows, performance profiling, and design systems.",
        "experience": (
            "Frontend Developer at StudioPixel (2021 - Present):\n"
            "- Built Next.js web portals achieving 98+ Google Lighthouse performance scores.\n"
            "- Translated Figma wireframes into pixel-perfect accessible React components."
        )
    },
    {
        "filename": "resume_carlos_rodriguez.txt",
        "format": "txt",
        "name": "Carlos Rodriguez",
        "title": "Site Reliability Engineer (SRE)",
        "experience_years": 6,
        "skills": ["Python", "Bash", "Linux", "Kubernetes", "Ansible", "Datadog", "Terraform"],
        "education": "B.S. in Computer Systems, Florida State University (2018)",
        "summary": "Reliability engineer dedicated to high uptime, automated incident response, chaos testing, and infrastructure observability.",
        "experience": (
            "SRE at CloudCore Systems (2020 - Present):\n"
            "- Maintained 99.99% service availability across multi-cloud infrastructure.\n"
            "- Automated deployment failovers using Python scripts and Ansible playbooks."
        )
    },
    {
        "filename": "resume_emily_watson.pdf",
        "format": "pdf",
        "name": "Emily Watson",
        "title": "Senior Python & FastApi Developer",
        "experience_years": 5,
        "skills": ["Python", "FastAPI", "SQLAlchemy", "Redis", "Celery", "PostgreSQL", "Pytest"],
        "education": "B.S. in Computer Science, University of Illinois (2019)",
        "summary": "Experienced Python engineer building async microservices, background job queues with Celery/Redis, and comprehensive test suites.",
        "experience": (
            "Senior Python Developer at DataFleet (2021 - Present):\n"
            "- Built async REST APIs using FastAPI and SQLAlchemy with 95% unit test coverage.\n"
            "- Reduced API response times from 350ms to 45ms using Redis caching layers.\n\n"
            "Python Developer at CodeBase (2019 - 2021):\n"
            "- Developed ETL pipelines and automated web scrapers."
        )
    }
]

def create_simple_pdf(filepath: Path, text: str):
    """Generates a valid standard PDF document without external GUI dependencies"""
    writer = PdfWriter()
    # Create a blank page
    page = writer.add_blank_page(width=612, height=792)
    
    # Standard PDF text stream
    # Note: pypdf allows creating and saving clean PDF structures
    with open(filepath, "wb") as f:
        writer.write(f)
    
    # Write a PDF with text stream metadata
    pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    )
    
    # Format text for PDF stream
    escaped_lines = []
    y = 720
    for line in text.splitlines():
        clean = line.replace("(", "\(").replace(")", "\)").replace("-", "-")
        escaped_lines.append(f"1 0 0 1 50 {y} Tm ({clean}) Tj")
        y -= 15
        if y < 50:
            break
            
    stream_data = "BT\n/F1 10 Tf\n" + "\n".join(escaped_lines) + "\nET"
    stream_bytes = stream_data.encode("latin-1", "replace")
    
    pdf_content += (
        f"4 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n".encode("latin-1") +
        stream_bytes +
        b"\nendstream\nendobj\n"
        b"xref\n0 6\n0000000000 65535 f \n"
        b"trailer\n<< /Root 1 0 R /Size 6 >>\nstartxref\n500\n%%EOF"
    )
    
    with open(filepath, "wb") as f:
        f.write(pdf_content)

def generate_all():
    for item in RESUMES:
        out_path = DATA_DIR / item["filename"]
        full_text = (
            f"NAME: {item['name']}\n"
            f"TITLE: {item['title']}\n"
            f"EXPERIENCE: {item['experience_years']} years\n"
            f"EDUCATION: {item['education']}\n"
            f"SKILLS: {', '.join(item['skills'])}\n\n"
            f"PROFESSIONAL SUMMARY:\n{item['summary']}\n\n"
            f"WORK EXPERIENCE:\n{item['experience']}\n"
        )
        
        if item["format"] == "txt":
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(full_text)
                
        elif item["format"] == "docx":
            doc = docx.Document()
            doc.add_heading(item["name"], level=1)
            doc.add_paragraph(f"{item['title']} | {item['experience_years']} years experience")
            doc.add_paragraph(f"Education: {item['education']}")
            doc.add_paragraph(f"Skills: {', '.join(item['skills'])}")
            doc.add_heading("Summary", level=2)
            doc.add_paragraph(item["summary"])
            doc.add_heading("Experience", level=2)
            doc.add_paragraph(item["experience"])
            doc.save(str(out_path))
            
        elif item["format"] == "pdf":
            create_simple_pdf(out_path, full_text)
            
    print(f"Generated {len(RESUMES)} sample resumes in {DATA_DIR}")

if __name__ == "__main__":
    generate_all()
