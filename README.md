![Uploading ChatGPT Image 27. März 2026, 10_43_15.png…]()


# SnapSpammer
<img width="885" height="189" alt="image" src="https://github.com/user-attachments/assets/8e0b5b6b-01c5-41d1-a9b6-4fc78bee1824" />




# 👻 **SnapSpammer TURBO**

> **Automate Snapchat snap & message sending on `web.snapchat.com`** — **fast, simple, and fully anonymous**.  
> Built with **Python + GUI automation** (`pyautogui`) for educational and productivity testing.  
> Created by **mrgbbn** — **TURBO EDITION**

---

## 🌟 **What It Does**

`SnapSpammer TURBO` lets you **send hundreds of snaps and messages in seconds** using **Snapchat Web** — no app, no phone, no limits.

It simulates real clicks and movements on your screen to:
- Open camera
- Select your shortcut
- Hit **"Send To"** → **Select All** → **Send**
- Spam messages to single or multiple users

Perfect for **testing**, **boosting streaks**, or **productivity experiments**.

---

## ⚡ **Features**

| Feature | Description |
|--------|-------------|
| **Snap Boost** | Send snaps to shortcuts automatically |
| **Message Spam** | Spam messages to a single user |
| **Multi Snap Spam** | Send snaps to **multiple users** at once |
| **Multi Chat Spam** | Spam messages to **multiple chats** at once |
| **Mouse Position Mapping** | Point & press `Y` to save button locations |
| **Custom Delays** | Fine-tune speed to avoid detection |
| **Shortcut Support** | Send to **1–100+ friends at once** |
| **Time Estimator** | Know exactly how long your session will take |
| **Colorful Terminal UI** | Smooth animations + ASCII boot sequence |
| **Auto-Help** | Opens README + Snapchat Web on first run |
| **Cross-Platform** | Works on **Windows**, **macOS**, **Linux** |

---

## 🚀 **Installation (Super Simple)**

> **No coding required** — just **download, run, and go!**

### **Windows (Easiest)**

1. **Download the ZIP**  
   → Click the green **"Code"** button → **"Download ZIP"**

2. **Extract the folder**

3. **Double-click `install.bat`**  
   → It installs **Python dependencies** automatically

4. **Run `start.bat`** to launch SnapSpammer TURBO

> **Done!** The banner appears → you're ready.

---

### **macOS**

```bash
# 1. Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python
brew install python

# 3. Download & extract the ZIP from GitHub

# 4. Open Terminal in the folder and run:
pip install pyautogui keyboard colorama

# 5. Launch
python3 main.py
```

### **Linux**

```bash
# 1. Update system
sudo apt update

# 2. Install Python & pip
sudo apt install python3 python3-pip

# 3. Install GUI dependencies (for pyautogui)
sudo apt install python3-tk python3-dev scrot

# 4. Download & extract the ZIP

# 5. Install Python packages
pip3 install pyautogui keyboard colorama

# 6. Run
python3 main.py
```

---

## 🎮 **Menu Options**

| # | Option | Description |
|---|--------|-------------|
| **1** | Start Snap Boost | Send snaps via shortcuts |
| **2** | Start Message Spam | Spam messages to one user |
| **3** | Multi Snap Spam | Send snaps to multiple targets |
| **4** | Multi Chat Spam | Spam messages to multiple chats |
| **5** | Settings | Configure delays, message, counts |
| **6** | Snap Positions | Set positions for Snap Boost |
| **7** | Chat Spam Positions | Set positions for Message Spam |
| **8** | Multi Snap Positions | Set positions for Multi Snap |
| **9** | Multi Chat Positions | Set positions for Multi Chat |
| **10** | Import Positions | Import from another settings.json |
| **11** | Estimate Time | Calculate session duration |
| **12** | Help | Open README & Snapchat Web |
| **0** | Exit | Save & quit |

---

## 📝 **How to Use**

### **Basic Snap Boost**
1. Open `web.snapchat.com` and log in
2. Run SnapSpammer TURBO
3. Press **[6]** to configure Snap Positions
   - Move mouse to **Camera** → press `Y`
   - Move to **Send To** → press `Y`
   - Move to **Shortcut** → press `Y`
   - Move to **Select All** → press `Y`
4. Press **[1]** to start Snap Boost
5. Press **F6** to stop

### **Message Spam**
1. Press **[5]** to set your spam message in Settings
2. Press **[7]** to configure Chat Spam Positions
3. Press **[2]** to start Message Spam
4. Press **F6** to stop

### **Multi Snap Spam**
1. Press **[8]** to configure Multi Snap Positions
   - Add multiple user shortcuts with `Y`
   - Press `N` when done
   - Set common positions (Camera, Send To, Select All)
2. Press **[3]** to start Multi Snap Spam
3. Press **F6** to stop

### **Multi Chat Spam**
1. Press **[5]** to set your spam message
2. Press **[9]** to configure Multi Chat Positions
   - Add multiple user chats with `Y`
   - Press `N` when done
   - Set common positions (Input, Send)
3. Press **[4]** to start Multi Chat Spam
4. Press **F6** to stop

---

## ⚙️ **Settings**

| Setting | Description | Default |
|---------|-------------|---------|
| Loop Delay | Time between snap batches | 0.15s |
| Click Delay | Time between clicks | 0.25s |
| Shortcut Count | Users per shortcut | 1 |
| Spam Message | Message to spam | (empty) |
| Spam Count | Messages per session | 50 |
| Spam Delay | Time between messages | 0.2s |
| Multi Snap Rounds | Rounds per target | 10 |
| Multi Chat Messages | Messages per target | 10 |

---

## ⌨️ **Controls**

| Key | Action |
|-----|--------|
| `Y` | Confirm position capture |
| `N` | Finish adding targets |
| `F6` | Stop current spam session |

---

## ⚠️ **Disclaimer**

This tool is for **educational purposes only**. Use responsibly and at your own risk. The developer is not responsible for any misuse or account restrictions.




