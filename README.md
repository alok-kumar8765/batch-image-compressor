# Batch Image Compressor GUI

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Repo](https://img.shields.io/badge/GitHub-alok--kumar8765-orange.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-blueviolet.svg)

An intuitive, high-performance desktop application designed to batch-compress image files without losing perceptual quality. Built with **Python**, **Tkinter**, and **Pillow (PIL)**, this tool offers multi-threading execution, automatic transparency preservation, and folder hierarchy maintenance.

---

## 📋 Table of Contents

- [Purpose & Use Cases](#-purpose--use-cases)
- [Key Features](#-key-features)
- [System Requirements](#-system-requirements)
- [Installation & Setup](#-installation--setup)
- [Project Architecture & Diagrams](#-project-architecture--diagrams)
  - [DFD Diagram](#dfd-data-flow-diagram)
  - [ER / Logic Diagram](#er--data-structure-diagram)
- [File Structure](#-file-structure)
- [Pros and Cons](#-pros-and-cons)
- [Limitations](#-limitations)
- [Known Bugs & Vulnerabilities](#-known-bugs--vulnerabilities)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [Acknowledgements & Star](#-acknowledgements--star)

---

## 🎯 Purpose & Use Cases

### **Purpose**
High-resolution images often consume excessive bandwidth, slow down web applications, and take up significant storage space. The **Batch Image Compressor** provides an effortless, offline desktop solution to optimize images for web deployment, cloud backup, or archive storage without requiring manual image editing software.

### **Use Cases**
* **Web Developers:** Reduce webpage loading times by compressing web assets (`.png`, `.jpg`) before uploading.
* **Photographers & Content Creators:** Quickly archive large batches of raw exports into lightweight formats.
* **App Developers:** Shrink static mobile application graphics to minimize install package sizes.

---

## ✨ Key Features

* **🎨 Graphical User Interface (GUI):** Built with native Tkinter for a clean, user-friendly experience.
* **⚡ Non-Blocking Multi-Threading:** Keeps the interface responsive even when processing thousands of files.
* **🛡️ Smart RGBA & Transparency Handling:** Automatically replaces alpha channels in PNG files with white canvas backgrounds during conversion, eliminating black border glitches.
* **📁 Recursive Folder Structure:** Traverses through nested subfolders and reconstructs the exact directory hierarchy in the output destination.
* **🎚️ Custom Compression Slider:** Easily set compression quality from 10% to 100%.
* **📊 Comprehensive Summary:** View total disk space saved (in MB and percentage) upon completion.

---

## 💻 System Requirements

* **Operating System:** Windows 10/11, macOS, or Linux.
* **Python Environment:** Python 3.8 or higher.
* **Dependencies:** `Pillow` library (`tkinter` comes pre-packaged with Python).

---

## ⚙️ Installation & Setup

### **1. Clone the Repository**
```bash
git clone https://github.com/alok--kumar8765/batch-image-compressor.git
cd batch-image-compressor
```

### **2. Create a Virtual Environment (Optional but Recommended)**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Required Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Launch the Application**
```bash
python main.py
```

---

## 📐 Project Architecture & Diagrams

### **DFD (Data Flow Diagram)**

```
 +------------------+
 |    User Input    |  (Input Folder, Output Folder, Quality Slider)
 +--------+---------+
          |
          v
 +------------------+      Scans Files       +-------------------+
 |  GUI Interface   | --------------------> | Folder Traversal  |
 +--------+---------+                        +---------+---------+
          |                                            |
          | Spawns Thread                              | Builds Task List
          v                                            v
 +------------------+                        +-------------------+
 | Processing Worker| <--------------------- | File Queue List   |
 +--------+---------+                        +-------------------+
          |
          +---> Reads Image Data -> Image Conversion & Transparency Fix -> Saves to Output Path
          |
          v
 +------------------+
 | Log & Metrics UI |  (Displays completion statistics and MB saved)
 +------------------+
```

### **ER / Data Structure Diagram**

Because this tool is an offline application, it relies on in-memory object relational models rather than a database engine.

```
+-------------------------------------------------------------------+
|                        COMPRESSION_JOB                            |
+-------------------------------------------------------------------+
| - input_folder    : String                                        |
| - output_folder   : String                                        |
| - compression_lvl : Integer (10 - 100)                             |
| - total_files     : Integer                                       |
| - total_saved_mb  : Float                                         |
+---------------------------------+---------------------------------+
                                  |
                                  | 1 : N (Job contains many tasks)
                                  v
+-------------------------------------------------------------------+
|                           IMAGE_TASK                              |
+-------------------------------------------------------------------+
| - source_path     : String                                        |
| - target_path     : String                                        |
| - original_size   : BigInt (Bytes)                                |
| - compressed_size : BigInt (Bytes)                                |
| - file_type       : String (.png, .jpg, .jpeg)                    |
| - status          : Enum [PENDING, SUCCESS, FAILED]               |
+-------------------------------------------------------------------+
```

---

## 📁 File Structure

```
batch-image-compressor/
│
├── main.py                # Main application entry point and Tkinter GUI implementation
├── requirements.txt       # Project dependency list
├── README.md              # Project documentation
├── .gitignore             # Git ignore configuration
└── assets/                # Screenshots and UI assets (optional)
```

---

## ⚖️ Pros and Cons

### **Pros**
* **100% Offline & Private:** Your images never leave your local system.
* **Lightweight:** Negligible memory footprint during execution.
* **Easy to Use:** No command-line interface knowledge needed.
* **Folder Structure Integrity:** Keeps all original directory trees intact.

### **Cons**
* **Format Conversion:** Converts all target image formats into `.jpg` files by default.
* **Single Quality Setting:** Applies the selected compression quality globally to all files in the batch.

---

## ⚠️ Limitations

* Supports only `.jpg`, `.jpeg`, and `.png` file formats.
* Does not support animated GIFs or vector formats like `.svg`.
* Destruction of transparency (PNG transparency is filled with a solid background color upon conversion to JPEG).

---

## 🛡️ Known Bugs & Vulnerabilities

* **Memory Usage with Ultra-High Resolution Images:** Extensively large image files (e.g., 100MB+ TIFFs converted to PNG) may cause high RAM spikes during active processing.
* **Path Length Limit:** Windows systems without long path support enabled may encounter errors if directory trees are nested excessively deep.

---

## 🚀 Future Roadmap

- [ ] Add support for modern web formats (`.webp`, `.avif`).
- [ ] Add drag-and-drop support for input folders.
- [ ] Allow choosing output image format without forcing standard JPEG conversion.
- [ ] Add real-time visual side-by-side preview before running full batch jobs.
- [ ] Add EXIF metadata preservation options.

---

## 🤝 Contributing

Contributions, issues, and feature requests are always welcome!

1. **Fork the Project** (`https://github.com/alok--kumar8765/batch-image-compressor/fork`)
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

---

## ⭐ Acknowledgements & Support

If you find this project useful, please consider giving it a **Star** on GitHub!

* Created by [alok--kumar8765](https://github.com/alok--kumar8765)
* Powered by [Pillow (PIL)](https://python-pillow.org/) and Python Tkinter.