# CEP: Compass for European Patents

Welcome to the repository for **CEP (Compass for European Patents)**, our proposal for CodeFest 2025. CEP is a full-stack application designed to analyze patent data and map it to the **United Nations Sustainable Development Goals (SDGs)**.

![Webview screenshot](./assets/webview.png)

---

## Table of Contents

- [CEP: Compass for European Patents](#cep-compass-for-european-patents)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Production Setup](#production-setup)
  - [Development Setup](#development-setup)
    - [Prerequisites](#prerequisites)
    - [Running Docker Containers](#running-docker-containers)
    - [Feed the Database](#feed-the-database)
    - [Install Tesseract](#install-tesseract)
    - [Frontend Setup](#frontend-setup)
    - [Backend Setup](#backend-setup)

---

## Overview

CEP leverages advanced data analysis techniques to provide insights into how patents contribute to achieving SDGs. The application is built with a modern tech stack, including **Docker**, **Python**, **Node.js**, and **Poetry**, ensuring scalability and ease of development.

---

## Production Setup

To deploy the application in a production environment, follow these steps:

1. Copy the example configuration file and update it with your credentials:
   ```bash
   cp backend/config-example.yaml backend/src/api/config/config.yaml
   ```
   - Provide your **Consumer Key** and **Consumer Secret** for the OPS API in the `config.yaml` file.

2. Start the application using Docker Compose:
   ```bash
   docker compose up -d
   ```
3. Download the `db.sql` file from this Dropbox [link]().

4. Feed the database with the SQL file.
   ```bash
   docker exec -i postgres psql -U user -d cep < {path-to-your-file}/db.sql
   ```
5. Visit the application in your browser at [`http://localhost:5173`](http://localhost:5173).

---

## Development Setup

### Prerequisites

Ensure the following tools are installed on your system:

- **Docker**
- **Docker Compose**
- **Python 3.13+**
- **Poetry** (Python dependency management)
- **Node.js** (for the frontend)
- **npm** (Node.js package manager)

### Running Docker Containers

Start the required services (e.g., `ollama` and `postgres`) using Docker Compose:

```bash
docker compose up ollama postgres -d
```

### Feed the Database

To initialize the database, follow these steps:
1. Download the `db.sql` file from this Dropbox [link](https://www.dropbox.com/scl/fi/hx14qzlyu6eijn286udzx/db.sql?rlkey=399xtryml3r40e5ez3x6z1alh&st=fnj4ti5q&dl=0).

2. Feed the database with the SQL file.
```bash
docker exec -i postgres psql -U user -d cep < {path-to-your-file}/db.sql
```

### Install Tesseract

To use Tesseract for OCR, install it on your system. For example, on Ubuntu, you can run:

```bash
sudo apt-get install tesseract-ocr
```

On Arch Linux, use:

```bash
sudo pacman -S python-pytesseract
```

If you want more information about the installation, refer to the [Tesseract Installation Guide](https://github.com/madmaze/pytesseract)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```
2. Install the required Node.js packages:
```bash
npm install
```
3. Copy `.env.example` to `.env` and fill in the required values:
```bash
cp .env.example .env
```
4. Start the frontend development server:
```bash
npm run dev
```
5. Open your browser and navigate to `http://localhost:5173` to view the application.

### Backend Setup

Make sure to install Poetry and Python 3.13+.

1. Install Poetry :
```bash
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc # or ~/.zshrc
source ~/.bashrc # or ~/.zshrc
```

If it works, you should be able to run:
```bash
poetry --version
```

2. Install dependencies:
```bash
cd backend
poetry install
```

You may have to install `poppler-utils` to use the `pdf2image` library. Normally, it is already installed on most systems, but if you encounter issues, you can install it using:
```bash
sudo apt-get install poppler-utils
```

3. Create `config.yaml` file copy from `config-example-dev.yaml` and fill in the values.
```bash
cd backend
cp config-example-dev.yaml src/api/config/config.yaml
```

Normally, you should replace \<postgres host\> and \<ollama host\> with `localhost` if you are running the containers locally.

4. Run the backend server:
```bash
poetry run dev
```