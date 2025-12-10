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
Absolutely! Here's a clean Markdown snippet including **steps 1–4** for installing **`uv` with Homebrew on macOS**, ready to paste into your `README.md` file:

---
## ✅ Prerequisites for macOS insall
- Homebrew
- Python 3.13 installed via Homebrew
- [`uv`](https://github.com/astral-sh/uv) installed via Homebrew

### 1. ✅ Make sure Homebrew is installed

If you don’t already have Homebrew installed, run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then verify the installation:

```bash
brew doctor
```

---

### Python 3.13 installed via Homebrew:

  ```sh
  brew install python@3.13
  ```

---

### 🚀 Installing `uv` on macOS using Homebrew

Follow these steps to install the ultra-fast Python package manager [`uv`](https://github.com/astral-sh/uv) on macOS.



### 1. ✅ Tap the Astral `uv` formula

Add Astral’s official Homebrew tap:

```bash
brew tap astral-sh/uv
```

---

### 2. ✅ Install `uv`

Install `uv` via Homebrew:

```bash
brew install uv
```

---

### 4. ✅ Verify the `uv` installation

Ensure that `uv` is installed successfully:

```bash
uv --version
```

You should see an output similar to:

```
uv 0.1.x
```

---

Now you're ready to use `uv` to quickly manage Python virtual environments and packages! 🐍⚡

--- 


## ☁️ How to Set Up the Project

### 1. Clone the Repo
Usually you want to clone in a subdirectory off your main tree. For example a
directory called pythondev.  
```sh
mkdir pythondev
cd pythondev
git clone https://github.com/tmcguirefl/AIHorseHandicapper.git
cd AIHorseHandicapper
```

### 2. Create a Virtual Environment (Python 3.13)
To be sure you are using the correct python version we will use command line
flags to tell "uv" which python version to use when you enter the virtual environment. We also add a prompt which should appear in your shell prompt when you 
activate the virtual envionment.

```sh
uv venv --python /opt/homebrew/bin/python3.13 --prompt AIHH
source .venv/bin/activate
```

- Verify the Python version:

  ```sh
  python3 --version  # Should show Python 3.13.x
  ```

---

### 3. uv sync the repository to bring in the required libraries

```sh
uv sync
```

---

## 🚀 Running the App

After installing dependencies:

```sh
Flask run
```

Then visit:

```
http://localhost:5500
```

### App Routes:

| Route              | Description                          |
|--------------------|--------------------------------------|
| `/`                | Landing page / Portal                |
| `/horsesite`       | Horse data processor via LLM         |
| `/horsepdf`        | Upload & split PDF files             |
| `/manage`          | Delete split folders and PDFs        |

---

## 📂 Project Structure

```
horse-portal/
├── app/
│   ├── __init__.py
│   ├── horsesite.py        # Twinspires cut and paste LLM UI logic
│   ├── horsepdf.py         # PDF splitting logic
│   ├── management.py       # Delete split/uploaded files
│
├── templates/
│   ├── layout.html
│   ├── horsesite.html
│   ├── horsepdf.html
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

You must set the following environment variable in the ".env" file to access OpenRouter. Just edit the ".env" with your favorite text editor and find the line below:

```
OPENROUTER_API_KEY=<your-api-key-here>
```
add you Openrouter API_KEY there. 


---


## 👥 About

Built with ❤️ using Flask, OpenRouter, and PyPDF2 for racing enthusiasts who want AI-powered racing insights.

Contributions welcome!
