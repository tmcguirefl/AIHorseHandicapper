## 📘 README.md

# 🐎 Horse Racing Portal (Flask App)

A unified Flask web application for:

- 🧠 Horse racing data analysis using LLMs (e.g., OpenRouter / OpenAI)
- 📄 Uploading and splitting race PDFs into individual races
- 🗑️ Management interface to clean up old uploads and split files

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## 🛠️ Development Environment Setup (macOS + Python 3.13 + uv)

This project uses [`uv`](https://github.com/astral-sh/uv) for fast dependency management and a virtual environment with **Python 3.13** (installed via Homebrew).

### ✅ Prerequisites

- Homebrew
- [`uv`](https://github.com/astral-sh/uv) installed:
  
  ```sh
  pip install uv
  ```

- Python 3.13 installed via Homebrew:

  ```sh
  brew install python@3.13
  ```

---

## ☁️ How to Set Up the Project

### 1. Clone the Repo

```sh
git clone https://github.com/your-username/horse-portal.git
cd horse-portal
```

### 2. Create a Virtual Environment (Python 3.13)

```sh
uv venv --python /opt/homebrew/bin/python3.13 --prompt flaskWEB
source .venv/bin/activate
```

- Verify the Python version:

  ```sh
  python3 --version  # Should show Python 3.13.x
  ```

### 3. Add Required Packages

```sh
uv add flask requests PyPDF2 dotenv
```

You can confirm packages are installed with:

```sh
uv pip list
```

---

## 🚀 Running the App

After installing dependencies:

```sh
python3 main.py
```

Then visit:

```
http://localhost:5000
```

### App Routes:

| Route              | Description                          |
|--------------------|--------------------------------------|
| `/`                | Landing page / Portal                |
| `/horsesite`       | Horse data processor via LLM         |
| `/split`           | Upload & split PDF files             |
| `/manage`          | Delete split folders and PDFs        |

---

## 📂 Project Structure

```
horse-portal/
├── app/
│   ├── __init__.py
│   ├── horsesite.py        # LLM UI logic
│   ├── split_app.py        # PDF splitting logic
│   ├── management.py       # Delete split/uploaded files
│
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── manage.html
│   ├── result.html
│
├── uploads/                # Uploaded PDFs
├── split_races/            # Split race folders
├── pyproject.toml
├── main.py                 # Unified Flask app runner
└── models.json             # Optional LLM models config
```

---

## 🔑 Environment Variables

You must set the following environment variable to access OpenRouter or other LLM providers:

```sh
export OPENROUTER_API_KEY="your-api-key-here"
```

You may want to add this line to your `.zshrc` or `.bashrc`.

---

## ✅ Example `pyproject.toml`
The following example is contained in the repo with the name pyproject.toml.start
It's contents are as follows:

```toml
[project]
name = "horse-portal"
version = "0.1.0"

```

---

## 👥 About

Built with ❤️ using Flask, OpenRouter, and PyPDF2 for racing enthusiasts who want AI-powered racing insights.

Contributions welcome!
