# Lottie Local Lower Thirds (LLLT)

**LLLT (Lottie Local Lower Thirds)** is a local engine converting Lottie animations into edit-ready **.mov (Alpha)** files. It replaces heavy templates with a simple GUI for fast asset generation. Built for extensibility: swap the default JSON with your own to create custom, brand-specific templates. Fast and stable.

---

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
*   `LowerThirds_Control.exe` — Main GUI application[cite: 1].
*   `data.txt` — Current text and color data[cite: 1, 7].
*   `index.js` — Lottie dynamic bridge[cite: 1, 2].
*   `lottie.js` — Lottie-web library[cite: 1, 3].
*   `lowerthird.html` — Web wrapper[cite: 1, 4].
*   `lowerthird.json` — Swappable Lottie template[cite: 1, 5].

---

## Customization 

LLLT is designed as a **universal engine**. To use your own graphics:
1. Replace `lowerthird.json` with your file[cite: 1].
2. Ensure your Lottie layers are named:
   * `.f0`, `.f1` — for Text[cite: 1, 2].
   * `.py0` to `.py3` — for Colors[cite: 1, 5].
3. Run `LowerThirds_Control.exe` and generate your asset.

---

## Author
**Oleg Gamulinskii**  
**@gam_ol**
**gamulinsky@gmail.com**

---

##  License
MIT License.
