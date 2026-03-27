# Lottie Local Lower Thirds (LLLT)

**LLLT (Lottie Local Lower Thirds)** is a local engine converting Lottie animations into edit-ready **.mov (Alpha)** files. It replaces heavy templates with a simple GUI for fast asset generation. Built for extensibility: swap the default JSON with your own to create custom, brand-specific templates. Fast and stable.

---
## 🤝 Credits & Acknowledgements
This project is inspired by and based on the original CasparCG Lottie template logic created by **Heine Froholdt** (heine.froholdt@gmail.com).
## Versions 

### 1. LLLT_v01 (Source Code)
Clean Python scripts for developers and power users. Requires Python 3.10+ and Playwright.
*   **Core:** `manager.py`, `generator.py`.
*   **Assets:** `index.js`, `lottie.js`, `lowerthird.html`, `lowerthird.json`.

### 2. LLLTexe_v01 (Portable Build)
Ready-to-use standalone version for production. No installation required.

**File Structure:**
*   `pw-browser/` — Isolated Chromium environment.
*   `ffmpeg.exe` — Video encoding engine.
*   `generator.exe` — CLI rendering core.
*   `LowerThirds_Control.exe` — Main GUI application.
*   `data.txt` — Current text and color data.
*   `index.js` — Lottie dynamic bridge.
*   `lottie.js` — Lottie-web library.
*   `lowerthird.html` — Web wrapper.
*   `lowerthird.json` — Swappable Lottie template.

---

## Customization 

LLLT is designed as a **universal engine**. To use your own graphics:
1. Replace `lowerthird.json` with your file.
2. Ensure your Lottie layers are named:
   * `.f0`, `.f1` — for Text.
   * `.py0` to `.py3` — for Colors.
3. Run `LowerThirds_Control.exe` and generate your asset.

---

## Author
**Oleg Gamulinskii**  
**@gam_ol**
**gamulinsky@gmail.com**

---

##  License
MIT License.
