# FastAPI Setup ⚙️

This section covers the installation and basic development environment setup required for working with FastAPI.

---

## 1. Prerequisites

Before starting with FastAPI, make sure the following are installed:

* Python 3.10+
* VS Code or another code editor
* Git
* Command Prompt / PowerShell / Terminal

Check Python:

```bash
python --version
```

Example:

```text
Python 3.12.10
```

---

## 2. Create a Virtual Environment

A virtual environment keeps project dependencies isolated from the system Python installation.

Create a virtual environment:

```bash
python -m venv venv
```

This creates:

```text
FastAPI-Learning/
└── venv/
```

The `venv` folder should not be committed to Git because it is already included in `.gitignore`.

---

## 3. Activate the Virtual Environment

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
venv\Scripts\activate
```

After activation, the terminal will usually show:

```text
(venv)
```

Example:

```text
(venv) PS C:\FastAPI-Learning>
```

---

## 4. Install FastAPI

Install FastAPI with its standard dependencies:

```bash
pip install "fastapi[standard]"
```

This provides FastAPI along with commonly required development tools.

---

## 5. Verify FastAPI Installation

Check the installed FastAPI package:

```bash
pip show fastapi
```

You can also verify the installation from Python:

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

---

## 6. Update requirements.txt

The project keeps its direct dependencies in `requirements.txt`.

Current dependency:

```text
fastapi[standard]
```

Install all project dependencies using:

```bash
pip install -r requirements.txt
```

This makes it easier for another developer to reproduce the development environment.

---

## 7. VS Code Python Interpreter

When using VS Code, select the Python interpreter belonging to the project's virtual environment.

Open the Command Palette:

```text
Ctrl + Shift + P
```

Then select:

```text
Python: Select Interpreter
```

Choose the interpreter from:

```text
venv\Scripts\python.exe
```

This ensures that VS Code uses the project's virtual environment.

---

## 8. Verify the Environment

Run:

```bash
python --version
```

Then:

```bash
pip --version
```

And:

```bash
pip show fastapi
```

If these commands work correctly, the FastAPI environment is ready.

---

## 9. Running a FastAPI Application

FastAPI applications can be run using the FastAPI CLI.

For example:

```bash
fastapi dev main.py
```

The development server will normally be available at:

```text
http://127.0.0.1:8000
```

The API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

ReDoc is available at:

```text
http://127.0.0.1:8000/redoc
```

The actual FastAPI application will be created in the next topic.

---

## 10. Development Server

The development server automatically reloads the application when code changes are detected.

This makes development easier because you normally do not need to manually restart the server after every code change.

---

## 11. Deactivate the Virtual Environment

When you finish working on the project:

```bash
deactivate
```

The `(venv)` prefix will disappear from the terminal.

---

## 12. Basic Setup Workflow

The typical workflow is:

```text
Create Project
     ↓
Create Virtual Environment
     ↓
Activate Virtual Environment
     ↓
Install Dependencies
     ↓
Select VS Code Interpreter
     ↓
Create FastAPI Application
     ↓
Run Development Server
```

---

## 13. Important Commands

| Command                           | Purpose                      |
| --------------------------------- | ---------------------------- |
| `python -m venv venv`             | Create virtual environment   |
| `.\venv\Scripts\Activate.ps1`     | Activate venv in PowerShell  |
| `venv\Scripts\activate`           | Activate venv in CMD         |
| `pip install "fastapi[standard]"` | Install FastAPI              |
| `pip install -r requirements.txt` | Install project dependencies |
| `pip show fastapi`                | Check FastAPI installation   |
| `fastapi dev main.py`             |                              |
