# ---------------------------------------------------------
# Author: Oleg Gamulinskii | @gam_ol | gamulinsky@gmail.com
# Project: Lottie Control Panel (GUI for EXE)
# ---------------------------------------------------------

import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from tkinter import ttk
import os
import subprocess
import threading

DATA_FILE = "data.txt"
REPORT_FILE = "render_report.txt"

class LottieManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Lottie Control Panel")
        self.root.geometry("350x600")
        self.root.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="TEXT CONTENT", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(self.root, text="Name:").pack()
        self.ent_name = tk.Entry(self.root, width=35); self.ent_name.insert(0, "Oleg"); self.ent_name.pack()
        tk.Label(self.root, text="Title:").pack()
        self.ent_title = tk.Entry(self.root, width=35); self.ent_title.insert(0, "@gam_ol"); self.ent_title.pack()

        tk.Label(self.root, text="COLORS", font=("Arial", 10, "bold")).pack(pady=10)
        cf1 = tk.Frame(self.root); cf1.pack()
        self.btn_txt_name = self.create_color_btn(cf1, "Name Txt", "#EEEEEE")
        self.btn_txt_title = self.create_color_btn(cf1, "Title Txt", "#141414")
        cf2 = tk.Frame(self.root); cf2.pack(pady=5)
        self.btn_bg_name = self.create_color_btn(cf2, "BG 1", "#892C2C")
        self.btn_bg_title = self.create_color_btn(cf2, "BG 2", "#EEEEEE")

        tk.Label(self.root, text="OUTPUT DIRECTORY", font=("Arial", 10, "bold")).pack(pady=10)
        pf = tk.Frame(self.root); pf.pack()
        self.ent_path = tk.Entry(pf, width=25); self.ent_path.insert(0, os.getcwd()); self.ent_path.pack(side="left")
        tk.Button(pf, text="Browse", command=self.browse_path).pack(side="left", padx=2)

        tk.Label(self.root, text="STATUS", font=("Arial", 10, "bold")).pack(pady=10)
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="indeterminate")
        self.progress.pack(pady=5)
        self.lbl_status = tk.Label(self.root, text="Idle", fg="grey"); self.lbl_status.pack()

        tk.Button(self.root, text="SAVE CONFIG", command=self.save_data, bg="#e1e1e1", width=25).pack(pady=5)
        self.btn_render = tk.Button(self.root, text="RUN RENDER", command=self.start_render_thread, bg="#2E7D32", fg="white", font=("Arial", 10, "bold"), width=25)
        self.btn_render.pack(pady=10)

    def create_color_btn(self, parent, label, default_hex):
        f = tk.Frame(parent); f.pack(side="left", padx=10)
        tk.Label(f, text=label, font=("Arial", 8)).pack()
        b = tk.Button(f, width=6, height=2, bg=default_hex, relief="groove")
        b.hex_value = default_hex.replace('#', '')
        b.config(command=lambda: self.pick_color(b)); b.pack()
        return b

    def pick_color(self, btn):
        color = colorchooser.askcolor(title="Select Color")[1]
        if color: btn.config(bg=color); btn.hex_value = color.replace('#', '')

    def browse_path(self):
        path = filedialog.askdirectory()
        if path: self.ent_path.delete(0, tk.END); self.ent_path.insert(0, path)

    def save_data(self):
        lines = [
            f"name: {self.ent_name.get()}",
            f"title: {self.ent_title.get()}",
            f"color_txt_name: {self.btn_txt_name.hex_value}",
            f"color_txt_title: {self.btn_txt_title.hex_value}",
            f"color_bg_name: {self.btn_bg_name.hex_value}",
            f"color_bg_title: {self.btn_bg_title.hex_value}",
            f"path: {self.ent_path.get()}"
        ]
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                f.write("\n\n".join(lines))
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e)); return False

    def start_render_thread(self):
        if self.save_data():
            self.btn_render.config(state="disabled")
            self.lbl_status.config(text="Rendering...", fg="blue")
            self.progress.start(10)
            threading.Thread(target=self.run_generator, daemon=True).start()

    def run_generator(self):
        try:
            # Важно: запускаем именно в текущей папке (cwd)
            base_dir = os.getcwd()
            result = subprocess.run(
                ["generator.exe"], 
                shell=True, 
                capture_output=True, 
                text=True,
                cwd=base_dir
            )
            with open(REPORT_FILE, "w", encoding="utf-8") as f:
                f.write("RENDER REPORT\n")
                f.write(f"Return Code: {result.returncode}\n\n")
                f.write("LOGS:\n" + result.stdout + "\n")
                f.write("ERRORS:\n" + result.stderr + "\n")
            self.root.after(0, lambda: self.finish_render(result.returncode == 0))
        except Exception as e:
            self.root.after(0, lambda: self.finish_render(False))

    def finish_render(self, success):
        self.progress.stop()
        self.btn_render.config(state="normal")
        self.lbl_status.config(text="Finished" if success else "Error", fg="green" if success else "red")
        messagebox.showinfo("Result", "Process complete" if success else "Process failed. Check render_report.txt")

if __name__ == "__main__":
    root = tk.Tk(); LottieManager(root); root.mainloop()