# 💀 HackerDoomsday-Safe

**HackerDoomsday-Safe** is a harmless prank program written in Python that simulates a fake virus infection on your friend's PC. Everything is designed to look terrifying — but nothing is permanently changed, no files are deleted, no registry is touched, and the PC reboots cleanly after the finale.

> ⚠️ **For personal fun only. Only use this on your own PC or with full consent of the target. Do not distribute maliciously.**

---

## 🖥️ What happens after launch?

### Phase 1 — The Fake Antivirus Installer
A fullscreen fake installer window appears with a siren playing in the background. A message warns the user that their internet traffic has been intercepted by unknown individuals and that an urgent antivirus update is required.

![First page of the application](https://github.com/user-attachments/assets/f70b3456-6d21-46d1-ad92-de26f7794313)
*First page of the application*

> 💡 Language can be changed between **English** and **Russian** using the buttons in the top-left corner — but only on the first page.

The user clicks through fake dropdowns to "configure" the antivirus. If they try to close the window or press **Alt+F4**, it does not work.

---

### Phase 2 — The Fake Installation
A progress bar runs from 0% to 100%. Before 50% it appears normal. At **50%**, everything turns red:
- A fake critical error message appears
- The "hacker group" reveals themselves in text on screen
- The wallpaper changes
- The music switches to something much scarier
- The progress bar turns red

---

### Phase 3 — First Hacker Video 🎬
Once the progress bar completes, a **Hacker starts talking to you** (`Hacker.mp4`) plays fullscreen with audio.

![Installation screen](https://github.com/user-attachments/assets/8a1cf927-dca7-45bb-9510-e426042dfbc4)

---

### Phase 4 — GDI Screen Chaos Effects
After the video ends, scary music kicks in and escalating screen corruption effects start layering on every 30 seconds:

| Threshold | Effect |
|-----------|--------|
| Start | Error icons following the cursor |
| +30s | Random error icons across screen |
| +60s | Screen melting (smelt) |
| +90s | Random images flashing |
| +120s | Tunnel zoom |
| +150s | Void darkening |
| +180s | Full screen inversion |
| +210s | Horizontal raster distortion |
| +240s | Melt drip |
| +270s | Sine wave warping |
| +330s | Screen panning |
| +390s | Rotation tunnel |
| +450s | Swipe screen |
| +510s | Hell mode |

After **60 seconds** of GDI chaos, the effects stop on their own.

---

### Phase 5 — Process Monitor (runs forever after GDI stops)
If the user opens any of the following apps, the GDI effects immediately stop and a second **Hacker video** (`Hacker2.mp4`) plays fullscreen, followed by a **real but clean BSOD**:

- Task Manager (`mmc.exe`, `resmon.exe`, `perfmon.exe`, `Taskmgr.exe`)
- System restore tools (`msconfig.exe`, `rstrui.exe`, `RecoveryDrive.exe`, `SystemPropertiesProtection.exe`)
- Process analysis tools (`ProcessHacker.exe`, `SystemInformer.exe`, `ProcessExplorer.exe`)

---

## 💣 Other features

- **Ctrl+Alt+Del → instant BSOD** — once Phase 4 starts, pressing Ctrl+Alt+Del triggers an immediate blue screen
- **Clean BSOD** — the BSOD is triggered by killing `csrss.exe`, a critical Windows process. Windows detects this, shows `CRITICAL_PROCESS_DIED`, and **automatically reboots cleanly** — no data loss, no permanent changes, boots back to normal

---

## ✅ What is NOT affected

| Thing | Safe? |
|-------|-------|
| Windows Registry | ✅ Untouched |
| System files | ✅ Untouched |
| User files | ✅ Untouched |
| Antivirus | ✅ Not killed or blocked |
| Startup / persistence | ✅ Does not persist after reboot |
| PC after BSOD | ✅ Reboots cleanly, works normally |

---

## 📁 Project Structure

```
HackerDoomsday-Safe-main/
├── main.py           # Entry point and phase controller
├── gui.py            # Fake installer GUI (tkinter)
├── multimedia.py     # Video playback, music, BSOD, process monitor
├── gdi.py            # All GDI screen corruption effects
├── start_gdi.py      # GDI effect launchers and shared stop_event
├── compile.bat       # PyInstaller compile script
└── resources/
    ├── Hacker.mp4        # First Hacker video
    ├── Hacker2.mp4       # Second Hacker video
    ├── runapp_main.MP3   # Intro siren music
    ├── after50.mp3       # Scary music after 50%
    ├── scaryfor3.MP3     # Music during GDI phase
    ├── background1.jpg   # GUI background page 1
    ├── background2.jpg   # GUI background page 2
    ├── background3.jpg   # GUI background page 3
    ├── background4.jpg   # GUI background page 4 (post 50%)
    ├── bg.jpg            # Wallpaper set at 50%
    └── 1.jpg - 5.jpg     # Images used in RandomImage GDI effect
```

---

## 🔧 Requirements

```
pip install pygame moviepy Pillow psutil pywin32
```

---

## 🛠️ Compiling to EXE

Run `compile.bat` — it uses PyInstaller to bundle everything into a single `HackerDoomsday.exe` in the `dist/` folder. The console window is hidden so nothing looks suspicious when your friend runs it.

---

## ▶️ Running from source

```
py main.py
```

---

## ⚡ Credits

Original concept and code by the project author. Safe version strips all permanently destructive behavior while keeping all the fun.
