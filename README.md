# 🐎 Horse Racing Portal (Flask App)

A unified Flask web application for:

- 🧠 Horse racing data analysis using LLMs (OpenRouter / OpenAI)
  - This allows you to cut and paste racing data from a betting site
  - Currently works with data tables available under twinspires
  - On a betting window for a race, use the pace and the summary tabs for the data
  - (Note: Summary tab access may require a TwinSpires account.)
- 📝 Manual horse input analysis
  - Allows you to copy and paste readily available horse past performance data from common US betting sites
  - Much of this data is accessible without needing an account on the betting site
- 🎱 Pool data arbitrage analysis
  - Asks the LLM to arbitrage the place and show pools to find under-bet horses in those pools
  - This can provide better odds for a winning ticket and possibly better payouts than usual for place/show bets, using the win pool as the efficient market benchmark
- 📄 Uploading and splitting race PDFs into individual races
  - This works for an entire track card pdf.
  - Currently works for brisnet ultimate PP with comments
  - It should work for other services pdfs
  - The races need to be split to make sure you can use AI models with lower context limits
- 🗑️ Management interface to clean up old uploads and split files

This Flask web server application is meant to run locally on a personal machine. You will need your own
accounts for openrouter and the betting application of your choice. It does not automatically place 
bets for you. It is only meant to test out how different AI models analyze races. The goal is to
find the best model for your particular betting style. In limited testing most models are able to 
pick the short morning line odds horses since they have the best numbers in their past performance. 
Grok seems to be able flag higher priced horses that have a chance to upset (but not as its first pick).
It may have to do with the prompt being used. There are no statistics on this. There will need to be some 
experimentation with the prompt, especially if you like to play exotics.


## Support

If you like the project and want to help support financially or you hit it big at the track using the 
software and want to show your appreciation. The project would appreciate it:

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/yourusername)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

# 🛠️ Development Environment Setup

This project uses `uv` for dependency management and virtual environments.

Setup instructions included for:

- macOS (Homebrew + Python 3.13)
- Windows PowerShell (Python 3.13 + uv MSI installer)
- Windows WSL2 (Ubuntu)
- Native Ubuntu Linux

---

# 🍎 macOS Setup (Homebrew + Python 3.13 + uv)

## Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew doctor
```

## Install Python 3.13
```bash
brew install python@3.13
```

## Install uv
```bash
brew tap astral-sh/uv
brew install uv
```

Verify:
```bash
uv --version
```

---

# 🪟 Windows Setup (PowerShell)

This setup does **not** use WSL — it installs everything natively on Windows.

## 1. Install Python 3.13
Download the official installer:

https://www.python.org/downloads/windows/

Make sure to check:
- "Add python.exe to PATH"
- "Install pip"

Verify:
```powershell
python --version
```

## 2. Install uv (Windows Native)
Download the official MSI installer:

https://astral.sh/uv/install/windows

Run it, then verify:

```powershell
uv --version
```

## 3. Create the Virtual Environment
```powershell
cd pythondev\AIHorseHandicapper
uv venv --python python --prompt AIHH
```

Activate:
```powershell
.\.venv\Scripts\activate
```

Verify:
```powershell
python --version
```

## 4. Install Dependencies
```powershell
uv sync
```

---

# 🪟 Windows WSL2 (Ubuntu)

## Install Python 3.13
```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev -y
```

## Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

Verify:
```bash
uv --version
```

---

# 🐧 Ubuntu Linux (Native)

## Install Python 3.13
```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev -y
```

## Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

---

# ☁️ Project Setup (All Systems)

## 1. Clone the Repository
```bash
mkdir pythondev
cd pythondev
git clone https://github.com/tmcguirefl/AIHorseHandicapper.git
cd AIHorseHandicapper
```

## 2. Create Virtual Environment

macOS:
```bash
uv venv --python /opt/homebrew/bin/python3.13 --prompt AIHH
```

WSL / Ubuntu:
```bash
uv venv --python python3.13 --prompt AIHH
```

Windows PowerShell:
```powershell
uv venv --python python --prompt AIHH
```

Activate:

macOS / Linux:
```bash
source .venv/bin/activate
```

Windows PowerShell:
```powershell
.\.venv\Scripts\activate
```

## 3. Install Dependencies
```bash
uv sync
```

---

# 🚀 Running the App

After activating your virtual environment:

```bash
flask run
```

Then visit:

```
http://localhost:5500
```

---

# 📂 Project Structure

```
horse-portal/
├── app/
│   ├── __init__.py
│   ├── horsesite.py
│   ├── horsepdf.py
│   ├── management.py
├── templates/
│   ├── layout.html
│   ├── horsesite.html
│   ├── horsepdf.html
│   ├── manage.html
│   ├── result.html
├── uploads/
├── split_races/
├── pyproject.toml
├── main.py
├── models.json
```

---

# 🔑 Environment Variables

Set your API key in `.env`:

```
OPENROUTER_API_KEY=<your-api-key-here>
```

---

# 👥 About

Built with ❤️ using Flask, OpenRouter, and PyPDF2 for racing enthusiasts who want AI‑powered racing insights.

Contributions welcome!

