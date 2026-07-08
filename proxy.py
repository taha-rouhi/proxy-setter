import tkinter as tk
from tkinter import messagebox
import subprocess
import os

CONFIG_FILE = "last_proxy.txt"

def load_last_proxy():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def save_last_proxy(address):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(address)

def get_proxy_status():
    try:
        result = subprocess.run([
            "reg", "query",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            "/v", "ProxyEnable"
        ], capture_output=True, text=True, shell=True)
        if "0x1" in result.stdout:
            return "✅ Active"
        else:
            return "❌ DeActive"
    except:
        return "Undefine"

def update_status_label():
    status = get_proxy_status()
    status_label.config(text=f"Status: {status}")

def set_proxy():
    address = proxy_entry.get()
    if not address:
        messagebox.showerror("eror", "Insert Proxy Address.")
        return
    try:
        subprocess.run([
            "reg", "add",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            "/v", "ProxyServer",
            "/t", "REG_SZ",
            "/d", address,
            "/f"
        ], shell=True)
        subprocess.run([
            "reg", "add",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            "/v", "ProxyEnable",
            "/t", "REG_DWORD",
            "/d", "1",
            "/f"
        ], shell=True)
        save_last_proxy(address)
        update_status_label()
    except Exception as e:
        messagebox.showerror("eror", str(e))

def disable_proxy():
    try:
        subprocess.run([
            "reg", "add",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            "/v", "ProxyEnable",
            "/t", "REG_DWORD",
            "/d", "0",
            "/f"
        ], shell=True)
        update_status_label()
    except Exception as e:
        messagebox.showerror("eror", str(e))

# رابط گرافیکی
root = tk.Tk()
root.title("Proxy Set")
root.geometry("400x220")

tk.Label(root, text="  (ex 127.0.0.1:8080) Proxy Address:").pack(pady=5)
proxy_entry = tk.Entry(root, width=40)
proxy_entry.pack(pady=5)

last_proxy = load_last_proxy()
proxy_entry.insert(0, last_proxy)

tk.Button(root, text="Proxy On", command=set_proxy).pack(pady=5)
tk.Button(root, text="Proxy Off", command=disable_proxy).pack(pady=5)

status_label = tk.Label(root, text="Proxy Status: ...", fg="blue")
status_label.pack(pady=10)

tk.Button(root, text="🔄 Check Status", command=update_status_label).pack()

update_status_label()  # بارگذاری اولیه وضعیت

root.mainloop()