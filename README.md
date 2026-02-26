Local Package Dependency Visualizer (DPV)

A fast, interactive tool to scan, analyze, and visualize dependencies inside any Python project.

⸻

🚀 Overview

Local Package Dependency Visualizer (DPV) is a tool that analyzes Python projects by scanning all modules, extracting imports via AST, building a dependency graph, detecting cycles, identifying dead modules, and generating a complete project dependency report.

It comes with:
	•	A CLI scanner (backend) that generates analysis reports
	•	A fully interactive frontend UI that visualizes graphs beautifully
	•	A guided splash experience and polished UX
	•	A workflow designed for both developers and students

DPV helps developers understand the structure of large codebases and spot problems early — like circular imports, unnecessary modules, and tightly coupled components.

⸻

✨ Features

Backend (Python)
	•	AST-based import extraction
	•	Module dependency graph construction
	•	Cycle detection
	•	Dead module detection
	•	Oversized modules analysis
	•	Graphviz export support
	•	JSON report output
	•	Pre-commit friendly performance
	•	Clean CLI interface

Frontend (HTML/JS/CSS)
	•	Beautiful animated splash onboarding
	•	Upload any report.json file
	•	Auto-load sample report
	•	Interactive dependency graph using vis-network
	•	Sidebar with summary stats
	•	Cycles + dead modules list
	•	Search modules in real time
	•	Node details panel (imports / imported-by)
	•	Fully responsive & polished UI

⸻

🎯 Why This Project Matters
	•	Helps understand real-world modularity
	•	Teaches AST parsing
	•	Visualizes program structure clearly
	•	Useful for refactoring legacy code
	•	Demonstrates full-stack integration

This project is a great demonstration of Python analysis, frontend visualization, and clean architecture.

⸻

🏗️ Project Architecture

dpv/
 ├─ cli/               -> CLI entrypoint (scan command)
 ├─ parser/            -> AST walker (extract imports)
 ├─ resolver/          -> Resolve module paths
 ├─ graph/             -> Build dependency graph
 ├─ reports/           -> Cycle + dead module finder
 └─ models/            -> ImportRecord dataclass

frontend/
 ├─ index.html         -> Main UI
 ├─ style.css          -> Full UI styling & animations
 ├─ script.js          -> DPV logic + graph rendering
 └─ sample_reports/    -> Example JSON report


⸻

💻 How to Use the Backend (CLI Scanner)

📌 Step 1: Install project (editable mode)

pip install -e .

📌 Step 2: Scan any Python project

python -m dpv.cli scan <project_path> --json report.json

Examples:

python -m dpv.cli scan my_project --json report.json
python -m dpv.cli scan . --json report.json

This generates:

report.json

Which contains:
	•	Graph adjacency lists
	•	Cycles found
	•	Dead modules
	•	Metadata

⸻

🌐 How to Run the Frontend

📌 Step 1: Start a simple local server

Open terminal inside the frontend/ folder:

python3 -m http.server 8000 --bind 127.0.0.1

📌 Step 2: Open the app

http://127.0.0.1:8000

📌 Step 3: Upload your generated report.json

Once uploaded, the UI automatically:
	•	Renders the dependency graph
	•	Shows stats
	•	Highlights cycles
	•	Highlights dead modules
	•	Allows searching
	•	Provides module-level insights

⸻

🧪 Sample Report

The frontend contains:

frontend/sample_reports/sample_report.json

The app auto-loads this for testing.

⸻

🖼️ Screenshots (add yours later)

Splash Screen

Dependency Graph

Sidebar Stats

Add actual images before submission.

⸻

⚙️ Tech Stack

Backend
	•	Python 3.10+
	•	AST (Abstract Syntax Trees)
	•	importlib
	•	pathlib
	•	graphviz export
	•	argparse

Frontend
	•	HTML + TailwindCSS
	•	Vanilla JavaScript
	•	vis-network for graph rendering
	•	CSS animations

⸻

📦 Folder Structure

.
├── dpv/                 # Backend code
├── frontend/            # Complete visualizer UI
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── sample_reports/
│       └── sample_report.json
└── README.md


⸻

📊 Evaluation Criteria (OJT)
	•	✔ AST walker extracts imports correctly
	•	✔ Dependency graph is accurate
	•	✔ Cycle detection works
	•	✔ Dead module detection works
	•	✔ CLI is functional
	•	✔ Frontend visualizer works
	•	✔ JSON is correctly consumed
	•	✔ Overall integration is clean and demonstrable

Everything is covered.

⸻

🚀 Future Improvements
	•	Web API for automatic scanning
	•	Drag-and-drop project folders
	•	Graph clustering by package
	•	Large graph performance optimization
	•	Light/dark theme toggle
	•	Report comparison mode (diff two scans)

⸻

🎤 Demo Flow (for viva/presentation)
	1.	Open terminal
	2.	Run scan:

python -m dpv.cli scan . --json report.json

	3.	Start frontend:

python3 -m http.server 8000

	4.	Upload report.json
	5.	Walk through graph, cycles, dead modules
	6.	Show clicking nodes
	7.	Search “utils” (example)
	8.	Explain insights & use cases

Total time: ~2 minutes.

⸻

✅ Conclusion

DPV is a complete system that:
	•	Scans Python projects
	•	Analyzes dependencies
	•	Detects code smells
	•	Visualizes architecture
	•	Enhances understanding of modularity

It is polished, functional, and ready for submission.

⸻