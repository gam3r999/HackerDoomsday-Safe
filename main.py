"""
Fake virus prank - safe version.
Flow: GUI -> Hacker.mp4 -> GDI effects (60s) -> GDI stops
      If banned app opened during GDI -> GDI stops -> Hacker2.mp4
"""

import threading
import sys
import time
import os
from collections import defaultdict
import psutil

from gui import run_app
from multimedia import playMusic_runappmain, play_video_fullscreen, playmusic_for3, monitor_process, monitor_mei_folders, BSOD

from start_gdi import (
    stop_event,
    startdrawimages,
    starterrors,
    starthell,
    starticonscursor,
    startinvert,
    startmelt,
    startpanscreen,
    startrastagHori,
    startrottun,
    startsines,
    startsmelt,
    startswipescreen,
    starttunnel,
    startvoid,
)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, "resources")
    else:
        base_path = os.path.join(os.path.abspath("."), "resources")
    return os.path.join(base_path, relative_path)


def checkexe():
    """Escalating GDI effects based on how many new executables the user has opened."""
    print("[START] checkexe started")
    EXECUTABLE_EXTENSIONS = {".exe", ".bat", ".cmd", ".vbs", ".ps1"}
    tracked_apps = set()
    tracked_pids = set()
    existing_pids = {proc.pid for proc in psutil.process_iter(['pid'])}
    triggered_events = {
        2: False, 4: False, 8: False, 12: False, 16: False,
        18: False, 20: False, 24: False, 28: False,
        30: False, 35: False, 40: False,
        45: False, 50: False
    }
    actions = {
        2:  lambda: (print("[GDI] 2"),  starticonscursor()),
        4:  lambda: (print("[GDI] 4"),  starterrors()),
        8:  lambda: (print("[GDI] 8"),  startsmelt()),
        12: lambda: (print("[GDI] 12"), startdrawimages()),
        16: lambda: (print("[GDI] 16"), starttunnel()),
        18: lambda: (print("[GDI] 18"), startvoid()),
        20: lambda: (print("[GDI] 20"), startinvert()),
        24: lambda: (print("[GDI] 24"), startrastagHori()),
        28: lambda: (print("[GDI] 28"), startmelt()),
        30: lambda: (print("[GDI] 30"), startsines()),
        35: lambda: (print("[GDI] 35"), startpanscreen()),
        40: lambda: (print("[GDI] 40"), startrottun()),
        45: lambda: (print("[GDI] 45"), startswipescreen()),
        50: lambda: (print("[GDI] 50"), starthell()),
    }

    def schedule_events():
        sequence = [2, 4, 8, 12, 16, 18, 20, 24, 28, 30, 35, 40, 45, 50]
        time_map = {}
        delay = 0
        for num in sequence:
            if num <= 30:
                delay += 30
            elif num <= 50:
                delay += 60
            else:
                delay += 180
            time_map[num] = delay

        def timer_run(n, delay_sec):
            time.sleep(delay_sec)
            if not stop_event.is_set() and not triggered_events[n]:
                triggered_events[n] = True
                actions[n]()

        for n, delay in time_map.items():
            threading.Thread(target=timer_run, args=(n, delay), daemon=True).start()

    schedule_events()

    while True:
        if stop_event.is_set():
            break
        current_pids = set()
        app_instances = defaultdict(set)
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                pid = proc.info['pid']
                name = proc.info['name'].lower()
                user = proc.info.get('username', '')
                if any(name.endswith(ext) for ext in EXECUTABLE_EXTENSIONS):
                    current_pids.add(pid)
                    app_instances[name].add(pid)
                    if pid not in existing_pids and pid not in tracked_pids and user:
                        tracked_pids.add(pid)
                        tracked_apps.add(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        total_processes = len(tracked_apps)
        for threshold in triggered_events:
            if total_processes >= threshold and not triggered_events[threshold]:
                triggered_events[threshold] = True
                actions[threshold]()
        time.sleep(2)


def watch_ctrl_alt_del():
    """Polls for Ctrl+Alt+Del using GetAsyncKeyState and triggers BSOD.
    Hooking does not work since Windows intercepts Ctrl+Alt+Del at kernel level.
    Polling is the only reliable method.
    """
    import ctypes
    user32 = ctypes.windll.user32

    VK_CONTROL = 0x11
    VK_MENU    = 0x12
    VK_DELETE  = 0x2E

    print("[WATCH] Ctrl+Alt+Del BSOD watcher started")
    triggered = False
    while not triggered:
        ctrl = user32.GetAsyncKeyState(VK_CONTROL) & 0x8000
        alt  = user32.GetAsyncKeyState(VK_MENU)    & 0x8000
        delete = user32.GetAsyncKeyState(VK_DELETE) & 0x8000
        if ctrl and alt and delete:
            print("[WATCH] Ctrl+Alt+Del detected — triggering BSOD")
            triggered = True
            BSOD()
        time.sleep(0.05)


def _state_3():
    """Phase 3: scary music + escalating GDI effects for 60s + process monitor.
    GDI stops after 60s. Hacker2.mp4 only plays if a banned app is opened.
    Ctrl+Alt+Del triggers BSOD.
    """
    print("[STATE 3] Starting GDI effects and process monitor")

    # Clear stop_event so GDI effects can run, small delay for safety
    stop_event.clear()
    time.sleep(0.5)

    # Start Ctrl+Alt+Del BSOD hook
    threading.Thread(target=watch_ctrl_alt_del, daemon=True).start()

    playmusic_for3()
    threading.Thread(target=monitor_process, daemon=True).start()
    threading.Thread(target=monitor_mei_folders, daemon=True).start()
    threading.Thread(target=checkexe, daemon=True).start()

    def stop_gdi_after_timeout():
        time.sleep(60)
        if not stop_event.is_set():
            print("[INFO] 60 seconds up — stopping GDI effects.")
            stop_event.set()

    threading.Thread(target=stop_gdi_after_timeout, daemon=True).start()

    # Keep main thread alive so all daemon threads keep running
    while True:
        time.sleep(1)


def _state_1():
    """First run: play intro music, show GUI, then Hacker.mp4, then phase 3."""
    try:
        import gui
        gui.on_install_complete = _state_3  # fired after Hacker.mp4 finishes
        playMusic_runappmain()
        run_app()  # blocking — returns when GUI window is destroyed
        # _state_3 runs in its own non-daemon thread, keep main thread alive
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"[ERROR] state_1: {e}")


if __name__ == "__main__":
    _state_1()