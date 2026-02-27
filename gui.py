import ctypes
import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import random
from multimedia import playMusic_after50, set_wallpaper, change_txt_2, play_video_fullscreen

# Set by main.py before calling run_app() to avoid circular imports
on_install_complete = None


def resource_path(relative_path):
    base_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), "resources")
    return os.path.join(base_path, relative_path)


ctypes.windll.user32.SetProcessDPIAware()


def on_specific_selection():
    print("Specific selection triggered!")


def run_app():
    LABEL_OFFSET = 65
    GLITCH_DURATION = 5000
    GLITCH_CHARS = ["█", "▒", "░", "▓", "X", "#", "@", "%", "&", "■", "□", "◙"]
    PROGRESS_BAR_WIDTH = 1400
    PROGRESS_BAR_HEIGHT = 150

    root = tk.Tk()
    root.tk.call('tk', 'scaling', 1.5)
    root.attributes('-fullscreen', True, '-topmost', True)
    root.title("Installing")
    root.resizable(False, False)
    root.overrideredirect(True)

    texts = {
        "ru": {
            "install": "Установить",
            "error": "Критическая ошибка с кодом -234901",
            "virusbase": "Когда обновлять вирусные базы:",
            "welcome": (
                "ВНИМАНИЕ, только что была совершена\n"
                "попытка перехвата вашего интернет-трафика неизвестными личностями.\n"
                "Вы сейчас, вероятно, обеспокоены,\n"
                "но паника в данный момент только повредит.\n"
                "Чтобы сохранить компьютер в целостности, пройдите\n"
                "короткую установку по обновлению антивирусного ПО\n"
                "Нажмите на кнопку ниже, чтобы приступить."
            ),
            "select": "Выберите параметры",
            "path": "Путь для установки:",
            "product": "Выбери версию продукта:",
            "progress": "Установка, не выключайте компьютер...",
            "hack": (
                "Без паники. Только что вы\n"
                "попытались противодействовать хакерской группировке\n"
                "«Штурм диванных войск». К счастью, нам\n"
                "удалось перехватить ваш интернет-запрос.\n"
                "Не беспокойтесь, ваш компьютер останется в сохранности, если\n"
                "вы будете выполнять наши требования.\n"
                "Дождитесь окончания установки."
            ),
            "alt_f4_1": "Осталось 2 попытки до активации усиленной защиты!",
            "alt_f4_2": "Осталась 1 попытка до активации усиленной защиты!",
            "alt_f4_3": "Усиленная защита активирована!",
            "return": "Вернуться"
        },
        "en": {
            "install": "Install",
            "error": "Critical error code -234901",
            "virusbase": "When to update virus databases:",
            "welcome": (
                "WARNING, there has just been an attempt\n"
                "to intercept your internet traffic by unknown individuals.\n"
                "You are probably worried now, but\n"
                "panicking at this point will only hurt.\n"
                "To keep your computer intact, please go through a short\n"
                "installation to update your antivirus software.\n"
                "Click the button below to get started."
            ),
            "select": "Select options",
            "path": "Select the installation path:",
            "product": "Select the type of product:",
            "progress": "Installing, do not turn off your computer...",
            "hack": (
                "Don't panic. You've just tried to counteract the hacker\n"
                "group «Assault on the Armchair Troops». Fortunately,\n"
                "we managed to intercept your Internet request.\n"
                "Don't worry, your computer will remain\n"
                "safe if you follow our instructions.\n"
                "Wait for the installation to complete."
            ),
            "alt_f4_1": "2 attempts left until enhanced protection is activated!",
            "alt_f4_2": "1 attempt left until enhanced protection is activated!",
            "alt_f4_3": "Enhanced protection activated!",
            "return": "Return"
        }
    }

    current_lang = "en"
    alt_f4_count = 0
    is_protection_active = False
    is_alt_f4_page_open = False
    is_install_page = False
    is_fake_msgbox_open = False

    welcome_label = None
    install_button = None
    next_button = None
    bg_label = None

    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    def clear_container():
        nonlocal bg_label
        for widget in container.winfo_children():
            widget.destroy()
        bg_label = tk.Label(container)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def show_fake_msgbox():
        nonlocal is_fake_msgbox_open
        if is_fake_msgbox_open:
            return
        is_fake_msgbox_open = True
        messages = [
            "Critical system fault!",
            "Memory access violation at 0x000AFB",
            "Exception 0xC0000005 occurred",
            "Application error: Unknown behavior",
            "Runtime error: 0xDEAD0001",
            "Security module failure!",
            "Stack overflow detected!",
            "Antivirus service crashed!",
            "Access to system memory denied!",
            "Error 0x000000FE: Driver fault"
        ]
        box = tk.Toplevel(root)
        box.title("Error")
        box.geometry("400x180+600+300")
        box.configure(bg="black")
        box.attributes("-topmost", True)
        box.resizable(False, False)
        box.overrideredirect(True)
        msg = random.choice(messages)
        tk.Label(box, text=msg, font=("Consolas", 14), fg="red", bg="black", wraplength=380).pack(pady=30)

        def on_close():
            nonlocal is_fake_msgbox_open
            is_fake_msgbox_open = False
            box.destroy()

        tk.Button(box, text="OK", font=("Arial", 14), bg="darkred", fg="white", command=on_close).pack(pady=10)

        def shake(count=10):
            if count <= 0:
                return
            x = box.winfo_x()
            y = box.winfo_y()
            dx = random.randint(-10, 10)
            dy = random.randint(-10, 10)
            box.geometry(f"+{x + dx}+{y + dy}")
            box.after(50, lambda: shake(count - 1))

        box.after(100, shake)

    def set_background(image_path=None, redness=0):
        nonlocal bg_label
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        try:
            if image_path:
                if not os.path.exists(image_path):
                    print(f"Background file not found: {image_path}")
                    img = Image.new("RGB", (w, h), (0, 0, 0))
                else:
                    img = Image.open(image_path).resize((w, h), Image.LANCZOS)
            else:
                img = Image.new("RGB", (w, h), (redness, 0, 0))
            bg_label.image = ImageTk.PhotoImage(img)
            bg_label.config(image=bg_label.image)
        except Exception as e:
            print(f"Background error: {e}")
            img = Image.new("RGB", (w, h), (0, 0, 0))
            bg_label.image = ImageTk.PhotoImage(img)
            bg_label.config(image=bg_label.image)

    def add_fake_close_button():
        fake_close = tk.Button(container, text="✖", font=("Arial", 16, "bold"),
                               bg="black", fg="white", bd=0, command=show_fake_msgbox,
                               activebackground="black", activeforeground="red", cursor="hand2")
        fake_close.place(relx=0.98, rely=0.01, anchor="ne")

    def change_lang(new_lang):
        nonlocal current_lang
        current_lang = new_lang
        if welcome_label and install_button:
            welcome_label.config(text=texts[current_lang]["welcome"])
            install_button.config(text=texts[current_lang]["install"])
            show_main_page()

    def glitch_effect(label, base_redness, intensity, duration=GLITCH_DURATION, glitch_level=1):
        start_time = time.time()

        def update():
            if time.time() - start_time > duration / 1000:
                label.place_configure(relx=0.5, rely=0.4, anchor="center")
                label.config(text=label.original_text, fg="white", font=("Arial", 28, "bold"))
                set_background(redness=0)
                container.config(bg="black")
                return
            if random.random() < 0.4 * glitch_level:
                dx = random.uniform(-0.1 * glitch_level, 0.1 * glitch_level)
                dy = random.uniform(-0.1 * glitch_level, 0.1 * glitch_level)
                label.place_configure(relx=0.5 + dx, rely=0.4 + dy)
            if random.random() < 0.6 * glitch_level:
                glitched_text = "".join(
                    random.choice(GLITCH_CHARS) if random.random() < 0.3 * glitch_level else char
                    for char in label.original_text)
                label.config(text=glitched_text)
            else:
                label.config(text=label.original_text)
            r = max(0, min(255, base_redness + random.randint(-intensity, intensity)))
            color = f"#{random.randint(100, 255):02x}0000" if random.random() < 0.2 * glitch_level else f"#{r:02x}0000"
            label.config(fg=color)
            if random.random() < 0.1 * glitch_level:
                label.config(font=("Arial", random.randint(20, 32), "bold"))
            if random.random() < 0.3:
                set_background(redness=r)
            container.config(
                bg=f"#{random.randint(100, 255):02x}0000" if random.random() < 0.4 * glitch_level else "black")
            if random.random() < 0.05 * glitch_level and glitch_level >= 2:
                artifact = tk.Label(container, text="".join(random.choice(GLITCH_CHARS) for _ in range(5)),
                                    font=("Arial", random.randint(15, 25)), fg=f"#{random.randint(100, 255):02x}0000",
                                    bg="black")
                artifact.place(relx=random.uniform(0, 1), rely=random.uniform(0, 1))
                root.after(150, artifact.destroy)
            root.after(70, update)

        label.original_text = label.cget("text")
        update()

    def show_alt_f4_page(message, redness, intensity, glitch_level):
        nonlocal is_alt_f4_page_open
        is_alt_f4_page_open = True
        clear_container()
        set_background(redness=redness)
        label = tk.Label(container, text=message, font=("Arial", 28, "bold"), bg="black", fg="white",
                         wraplength=root.winfo_screenwidth() * 0.8)
        label.place(relx=0.5, rely=0.4, anchor="center")
        glitch_effect(label, redness, intensity, glitch_level=glitch_level)

        def on_return():
            nonlocal is_alt_f4_page_open
            is_alt_f4_page_open = False
            show_main_page()

        btn = tk.Button(container, text=texts[current_lang]["return"], font=("Arial", 22), bg="#400000", fg="white",
                        command=on_return, state=tk.DISABLED)
        btn.place(relx=0.5, rely=0.6, anchor="center")
        root.after(GLITCH_DURATION, lambda: btn.config(state=tk.NORMAL))

    def handle_alt_f4(event):
        nonlocal alt_f4_count, is_protection_active
        if is_protection_active or is_install_page:
            return "break"
        alt_f4_count += 1
        if alt_f4_count == 1:
            show_alt_f4_page(texts[current_lang]["alt_f4_1"], redness=100, intensity=50, glitch_level=1)
        elif alt_f4_count == 2:
            show_alt_f4_page(texts[current_lang]["alt_f4_2"], redness=150, intensity=100, glitch_level=2)
        else:
            is_protection_active = True
            on_specific_selection()
            show_alt_f4_page(texts[current_lang]["alt_f4_3"], redness=255, intensity=150, glitch_level=3)
        return "break"

    root.bind("<Alt-F4>", handle_alt_f4)

    def show_main_page():
        nonlocal welcome_label, install_button, is_install_page
        is_install_page = False
        clear_container()
        set_background(resource_path("background1.jpg"))
        welcome_label = tk.Label(container, text=texts[current_lang]["welcome"], font=("Consolas", 24), bg="black",
                                 fg="white", wraplength=root.winfo_screenwidth() * 0.8)
        welcome_label.pack(pady=150)
        install_button = tk.Button(container, text=texts[current_lang]["install"], font=("Arial", 20),
                                   command=show_page_2)
        install_button.pack(pady=20)
        tk.Button(container, text="RU", font=("Arial", 25), command=lambda: change_lang("ru")).place(x=10, y=10)
        tk.Button(container, text="EN", font=("Arial", 25), command=lambda: change_lang("en")).place(x=135, y=10)
        add_fake_close_button()

    def show_page_2():
        nonlocal next_button, is_install_page
        is_install_page = False
        clear_container()
        set_background(resource_path("background2.jpg"))
        tk.Label(container, text=texts[current_lang]["select"], font=("Arial", 24), bg="black", fg="white").pack(pady=50)
        choices = [
            ["ERROR:Failed to connect to server", "360 TOTAL SECURITY", "NORTON FREE", "SHADOW DEFENDER",
             "VIRUS GUARD 3000", "CRYPTO LOCKER PRO"],
            ["C:\\Program Files\\NewAntivirus", "C:\\Windows\\NewAntivirus", "C:\\System\\Critical",
             "C:\\Hidden\\Malware"],
            ["Every day.", "Every week.", "Never"]
        ]
        positions = [{"x": 70, "y": 300}, {"x": 1300, "y": 300}, {"x": 600, "y": 500}]
        label_texts = [texts[current_lang]["product"], texts[current_lang]["path"], texts[current_lang]["virusbase"]]
        dropdowns = []
        dropdown_vars = []

        def handle_selection(*_):
            if all(var.get() for var in dropdown_vars):
                next_button.config(state=tk.NORMAL)

        for options, pos, label_text in zip(choices, positions, label_texts):
            label_y = pos["y"] - LABEL_OFFSET
            tk.Label(container, text=label_text, font=("Arial", 24), bg="black", fg="white").place(x=pos["x"], y=label_y)
            var = tk.StringVar()
            dropdown = ttk.Combobox(container, values=options, textvariable=var, state="readonly", font=("Arial", 25))
            dropdown.option_add("*TCombobox*Listbox*Font", ("Arial", 20))
            dropdown.place(**pos)
            var.trace_add("write", handle_selection)
            dropdowns.append(dropdown)
            dropdown_vars.append(var)

        def on_install_pressed():
            if (dropdown_vars[0].get() == "CRYPTO LOCKER PRO" and
                    dropdown_vars[1].get() == "C:\\Hidden\\Malware" and
                    dropdown_vars[2].get() == "Never"):
                on_specific_selection()
            show_page_3()

        next_button = tk.Button(container, text=texts[current_lang]["install"], font=("Arial", 20),
                                bg="black", fg="white", command=on_install_pressed, state=tk.DISABLED)
        next_button.pack(pady=50)

        invisible_focus_target = tk.Button(container, text="", width=1, height=1)
        invisible_focus_target.place(x=-100, y=-100)

        def clear_focus(event):
            widget = event.widget
            if not any(widget is d or widget in d.winfo_children() for d in dropdowns):
                invisible_focus_target.focus_set()

        bg_label.bind("<Button-1>", clear_focus)
        add_fake_close_button()

    def show_page_3():
        nonlocal is_install_page
        is_install_page = True
        clear_container()
        set_background(resource_path("background3.jpg"))

        installing_label = tk.Label(container, text=texts[current_lang]["progress"], font=("Arial", 24),
                                    bg="black", fg="white")
        installing_label.place(relx=0.5, rely=0.55, anchor="center")

        canvas = tk.Canvas(container, width=PROGRESS_BAR_WIDTH, height=PROGRESS_BAR_HEIGHT, bg="black",
                           highlightthickness=1)
        canvas.place(relx=0.5, rely=0.2, anchor="center")
        progress_rect = canvas.create_rectangle(0, 0, 0, PROGRESS_BAR_HEIGHT, fill="#00ff00", width=0)

        percent_label = tk.Label(container, text="0%", font=("Arial", 24), fg="green", bg="black")
        percent_label.place(relx=0.5, rely=0.35, anchor="center")

        install_text = tk.Label(container, text=texts[current_lang]["error"], font=("Arial", 24), bg="black", fg="red")
        install_text.place_forget()

        hack_text = tk.Label(container, text=texts[current_lang]["hack"], font=("Arial", 24), bg="black", fg="red",
                             wraplength=root.winfo_screenwidth() * 0.8)
        hack_text.place_forget()

        def interpolate_color(progress):
            if progress < 30:
                return "#00ff00"
            if progress > 50:
                return "#ff0000"
            factor = (progress - 30) / 20.0
            r, g = int(255 * factor), int(255 * (1 - factor))
            return f"#{r:02x}{g:02x}00"

        def instability_effect(stop_event):
            try:
                while not stop_event.is_set():
                    if random.random() < 0.5:
                        installing_label.config(fg="red" if random.random() < 0.5 else "white")
                    if random.random() < 0.4:
                        dx, dy = random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)
                        installing_label.place_configure(relx=0.5 + dx, rely=0.55 + dy)
                    if random.random() < 0.3:
                        glitched = "".join(random.choice(GLITCH_CHARS) if random.random() < 0.4 else ch
                                           for ch in texts[current_lang]["progress"])
                        installing_label.config(text=glitched)
                    else:
                        installing_label.config(text=texts[current_lang]["progress"])
                    if random.random() < 0.2:
                        dx, dy = random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)
                        canvas.place_configure(relx=0.5 + dx, rely=0.2 + dy)
                        percent_label.place_configure(relx=0.5 + dx, rely=0.35 + dy)
                    if random.random() < 0.15:
                        try:
                            canvas.place_forget()
                            percent_label.place_forget()
                            root.after(300, lambda: (
                                canvas.place(relx=0.5, rely=0.2, anchor="center"),
                                percent_label.place(relx=0.5, rely=0.35, anchor="center")
                            ))
                        except:
                            pass
                    if random.random() < 0.1:
                        artifact = tk.Label(container, text="".join(random.choice(GLITCH_CHARS) for _ in range(5)),
                                            font=("Arial", random.randint(15, 25)), fg="red", bg="black")
                        artifact.place(relx=random.uniform(0, 1), rely=random.uniform(0, 1))
                        root.after(200, artifact.destroy)
                    time.sleep(0.1)
            except Exception as e:
                print(f"[instability_effect] Error: {e}")

        def heavy_50_percent_effects(canvas, installing_label, install_text, hack_text, percent_label, progress_rect):
            def update_ui():
                try:
                    set_background(resource_path("background4.jpg"))
                    install_text.place(relx=0.5, rely=0.45, anchor="center")
                    hack_text.place(relx=0.5, rely=0.65, anchor="center")
                    percent_label.config(fg="red")
                    installing_label.config(fg="red", text=texts[current_lang]["progress"])
                    installing_label.place_configure(relx=0.5, rely=0.1, anchor="center")
                    canvas.itemconfig(progress_rect, fill="#ff0000")
                    canvas.place_configure(relx=0.5, rely=0.2, anchor="center")
                    percent_label.place_configure(relx=0.5, rely=0.35, anchor="center")
                except Exception as e:
                    print(f"[heavy_50_percent_effects - UI] Error: {e}")

            def run_heavy_background_tasks():
                try:
                    playMusic_after50()
                    set_wallpaper(image_path=resource_path("bg.jpg"))
                    threading.Thread(target=change_txt_2, daemon=True).start()
                except Exception as e:
                    print(f"[heavy_50_percent_effects - background] Error: {e}")

            root.after(0, update_ui)
            threading.Thread(target=run_heavy_background_tasks, daemon=True).start()

        def update_progress():
            stop_event = threading.Event()
            effect_thread = threading.Thread(target=instability_effect, args=(stop_event,), daemon=True)
            effect_thread.start()

            def step(i=0):
                if i > 100:
                    print("[INFO] Fake install complete! Playing Loony Tunes...")
                    video_thread = threading.Thread(
                        target=lambda: play_video_fullscreen(
                            resource_path("Hacker.mp4"),
                            on_complete=on_install_complete
                        ),
                        daemon=False
                    )
                    video_thread.start()
                    root.destroy()
                    return

                percent_label.config(text=f"{i}%")
                canvas.coords(progress_rect, 0, 0, i / 100 * PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT)
                canvas.itemconfig(progress_rect, fill=interpolate_color(i))

                if i == 50:
                    stop_event.set()
                    threading.Thread(target=lambda: heavy_50_percent_effects(
                        canvas, installing_label, install_text, hack_text, percent_label, progress_rect
                    ), daemon=True).start()

                delay = random.uniform(0.7, 1.2) if i < 50 and random.random() < 0.3 else 0.5
                root.after(int(delay * 1000), lambda: step(i + 1))

            step()

        threading.Thread(target=update_progress, daemon=True).start()

    show_main_page()
    root.mainloop()