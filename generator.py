import os
import json
import time
import shutil
import subprocess
import threading
import http.server
import socketserver
from playwright.sync_api import sync_playwright

# --- 1. GLOBAL CONFIGURATION ---
FPS = 25 
PORT = 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Agnostic Discovery
HTML_FILE = next((f for f in os.listdir('.') if f.endswith('.html')), None)
JSON_FILE = next((f for f in os.listdir('.') if f.endswith('.json')), None)
DATA_FILE = "data.txt" 
FRAMES_DIR = "temp_frames"
OUTPUT_MOV = "master_render_alpha.mov"

# --- 2. DATA PAYLOAD GENERATOR ---
def get_render_payload():
    raw_data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    k, v = line.split(':', 1)
                    raw_data[k.strip()] = v.strip()
    
    mapping_config = {
        ".f0": "name", ".f1": "title",
        ".py0": "color_txt_name", ".py1": "color_txt_title",
        ".py2": "color_bg_name", ".py3": "color_bg_title"
    }

    payload = {lyr: raw_data[key].replace('#', '') for lyr, key in mapping_config.items() if key in raw_data}
    return payload

# --- 3. LOCAL WEB SERVER ---
class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

def run_server():
    server = ThreadedHTTPServer(("", PORT), http.server.SimpleHTTPRequestHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

# --- 4. RENDER ENGINE ---
def start_render():
    if not HTML_FILE or not JSON_FILE:
        print("❌ ERROR: Template missing."); return

    run_server()
    payload = get_render_payload()

    if os.path.exists(FRAMES_DIR): shutil.rmtree(FRAMES_DIR)
    os.makedirs(FRAMES_DIR)

    with sync_playwright() as p:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            lottie_json = json.load(f)

        width = lottie_json.get('w', 1920)
        height = lottie_json.get('h', 1080)
        total_frames = int(lottie_json.get('op', 125))
        
        print(f">>> Processing: {JSON_FILE} | Size: {width}x{height}")

        browser = p.chromium.launch(headless=True) 
        page = browser.new_page(viewport={'width': width, 'height': height})
        
        page.goto(f"http://localhost:{PORT}/{HTML_FILE}", wait_until="networkidle")
        
        page.evaluate(f"window.initLottie({json.dumps(lottie_json)})")
        page.wait_for_function("window.animLoaded === true")

        if payload:
            print(f">>> Injecting {len(payload)} parameters...")
            for layer, val in payload.items():
                page.evaluate(f"window.updateLayerText('{layer}', '{val}')")

        # Playhead warm-up (Force expression redraw)
        page.evaluate("window.anim.goToAndStop(5, true)")
        time.sleep(1)

        print(f"🎬 Capturing frames...")
        for frame in range(total_frames):
            page.evaluate(f"window.anim.goToAndStop({frame}, true)")
            page.screenshot(path=f"{FRAMES_DIR}/frame_{frame:04d}.png", omit_background=True)
            if frame % 25 == 0: print(f"    Progress: {frame}/{total_frames}")
        
        browser.close()

    # --- 5. FFMPEG COMPILATION ---
    print(">>> Finalizing Master MOV (ProRes 4444)...")
    subprocess.run([
        'ffmpeg', '-y', '-framerate', str(FPS),
        '-i', f'{FRAMES_DIR}/frame_%04d.png',
        '-c:v', 'prores_ks', '-profile:v', '4', '-pix_fmt', 'yuva444p10le',
        OUTPUT_MOV
    ])
    
    if os.path.exists(FRAMES_DIR): shutil.rmtree(FRAMES_DIR)
    print(f"\n✅ SUCCESS: Final Master at {OUTPUT_MOV}")

if __name__ == "__main__":
    start_render()