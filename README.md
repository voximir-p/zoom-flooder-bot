# Zoom Flooder Bot

> **⚠️ Important Notice**
> This project is provided **for educational and testing purposes only**.
> **Do not use this software to harass, disrupt, or interfere with meetings you do not own or have explicit permission to test.**

---

## Overview

This project demonstrates browser automation using **Python** and **Selenium WebDriver** to automate joining Zoom meetings via a web browser.
It also showcases **basic multithreading** and process coordination in Python.

**Primary goals of this project:**

* Learn browser automation with Selenium
* Experiment with multithreading behavior
* Understand resource management (CPU, RAM, browser instances)

---

## ⚠️ Legal & Ethical Warning

Using automation tools against online services **may violate**:

* Zoom’s **Terms of Service**
* Local or international **computer misuse laws**
* Workplace, school, or organizational policies

### You are solely responsible for how you use this software.

* **Only use this on meetings you own or have explicit permission to test**
* **Do not use this to harass, spam, or disrupt others**
* The author(s) **accept no liability** for misuse, bans, account actions, or legal consequences

If you are unsure whether your use is allowed, **do not run this software**.

---

## Features

* Automated Zoom meeting join via browser
* Configurable number of bot instances
* Multithreaded execution
* Optional randomized bot names
* Controlled shutdown mechanism

---

## Requirements

* **Python 3.9+** (recommended)
* Google Chrome (latest stable)
* ChromeDriver (matching your Chrome version)

### Python Dependencies

* `selenium`
* `keyboard`

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/voximir-p/zoom-flooder-bot.git
   cd zoom-flooder-bot
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   *(or run `installer.bat` on Windows)*

3. Download **ChromeDriver** from:
   [https://googlechromelabs.github.io/chrome-for-testing/#stable](https://googlechromelabs.github.io/chrome-for-testing/#stable)

4. Place the ChromeDriver executable in the project root directory.

---

## Usage

Run the program:

```bash
python main.py
```

The program will prompt you for:

* Number of threads
* Zoom meeting ID and passcode
* Number of bot instances
* Bot naming preferences

> ⚠️ **Resource Warning**
> Each bot launches a browser instance.
> High thread or bot counts can cause **high CPU usage, excessive RAM consumption, system instability, or crashes**.

### Exiting Safely

To ensure all browser instances close correctly:

* Use the built-in exit shortcut: **`Ctrl + Alt + Shift + E`**
* Avoid force-closing unless instructed by the program

---

## Limitations

* Relies on Zoom’s web UI, which may change at any time
* Not guaranteed to work with future Zoom updates
* Browser automation is inherently fragile

---

## Contributing

Contributions are welcome for:

* Code cleanup and refactoring
* Improved error handling
* Documentation improvements

Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with a clear description

---

## Change Log

### v0.1 Beta

* Initial proof-of-concept

### v1.0

* Added multithreading
* Updated Selenium usage
* Improved input validation
* Improved shutdown handling
* Bug fixes and stability improvements

---

## License

This project is released under the **MIT License**.
See [LICENSE](LICENSE) file for details.
