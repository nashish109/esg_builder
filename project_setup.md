# ESG Builder Project Setup

This document outlines the initial project structure and file contents for the ESG Builder application.

## 1. Directory Structure

The following directory structure should be created:

```
esg_builder/
├── .gitignore
├── README.md
├── requirements.txt
├── config/
│   ├── __init__.py
│   └── settings.py
├── data_collection/
│   ├── __init__.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── news_scraper.py
│   │   └── reports_scraper.py
│   └── utils.py
├── nlp_engine/
│   ├── __init__.py
│   ├── analysis.py
│   └── models/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── services/
│       ├── __init__.py
│       ├── portfolio_service.py
│       └── esg_service.py
├── database/
│   ├── __init__.py
│   ├── postgres_setup.sql
│   └── mongo_setup.py
├── dashboard/
│   ├── __init__.py
│   └── app.py
└── tests/
    ├── __init__.py
    ├── test_data_collection.py
    ├── test_nlp_engine.py
    └── test_backend.py
```

## 2. File Contents

### .gitignore

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.idea/
.vscode/
*.sublime-project
*.sublime-workspace
```

### README.md

```md
# ESG Builder

A platform that scrapes ESG-related data, analyzes ESG performance using NLP, and recommends portfolios based on user-defined filters.
```

### requirements.txt

This file will be populated as we add dependencies. For now, it can be empty or contain the initial set of libraries.

```txt
# Data Collection
scrapy
beautifulsoup4
requests
feedparser

# NLP
transformers
spacy
torch

# Backend
fastapi
uvicorn

# Database
psycopg2-binary
pymongo

# Dashboard
streamlit
plotly