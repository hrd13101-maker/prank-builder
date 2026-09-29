# prank.py — ALPHA XK
# Python 3.8+
# pip install Pillow
# ملاحظة: *winsound يشتغل على Windows فقط — على Linux/Mac استخدم بديل*

import tkinter as tk
import os
import sys
import threading
import time
import random

# ============ الإعدادات ============
IMAGE_FILE = "prank_image.png"   # الصورة اللي تطلع في النوافذ
SOUND_FILE = "error.wav"         # الصوت
NUM_POPUPS = 20                  # عدد النوافذ
DELAY = 0.05                     # تأخير بين كل نافذة (ثانية)
WINDOW_SIZE = "300x300"

def resource_path(filename):
    """يحدد مسار الملف (يشتغل مع PyInstaller)"""
    if getattr(sys, '_MEIPASS', None):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def play_error_sound():
    """يشغّل صوت الخطأ"""
    try:
        import winsound
        path = resource_path(SOUND_FILE)
        if os.path.exists(path):
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            winsound.MessageBeep(winsound.MB_ICONHAND)
    except ImportError:
        # لو مو Windows، نستخدم print بدل الصوت
        print("\a", end="", flush=True)

def create_popup():
    """يفتح نافذة خطأ عشوائية"""
    window = tk.Toplevel()
    window.title("Ошибка / خطأ")
    window.configure(bg="black")

    # موقع عشوائي
    x = random.randint(0, 800)
    y = random.randint(0, 500)
    window.geometry(f"{WINDOW_SIZE}+{x}+{y}")

    # نجرب نحمل الصورة
    img_path = resource_path(IMAGE_FILE)
    try:
        from PIL import Image, ImageTk
        img = Image.open(img_path)
        img = img.resize((280, 280), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(window, image=photo, bg="black")
        label.image = photo  # نبقي مرجع
        label.pack(expand=True)
    except Exception:
        # لو ما فيه صورة، نعرض نص
        tk.Label(
            window,
            text="⚠ ОШИБКА ⚠\n\nخطأ في النظام",
            font=("Arial", 24, "bold"),
            fg="red",
            bg="black"
        ).pack(expand=True)

    # زر إغلاق
    tk.Button(
        window,
        text="إغلاق",
        command=window.destroy,
        bg="red",
        fg="white",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

def run_prank():
    """يشغّل السكربت كامل"""
    root = tk.Tk()
    root.withdraw()

    # نشغّل الصوت في thread منفصل
    sound_thread = threading.Thread(target=play_error_sound, daemon=True)
    sound_thread.start()

    # نفتح 20 نافذة
    for i in range(NUM_POPUPS):
        create_popup()
        root.update()
        time.sleep(DELAY)

    # نبقي النافذة الرئيسية شغالة
    root.mainloop()

if __name__ == "__main__":
    run_prank()
