# QuickFix — Smart Campus Issue Management

> **"See it. Report it. Track it. Fix it."**  
> *A smart campus issue-intelligence application built in Python that enables students and staff to report campus problems with evidence, dynamically prioritize issues, detect potential duplicates, and transparently track resolutions.*

---

## 📱 App Highlights & Architecture

QuickFix addresses the complete campus maintenance workflow with **3 core pillars**:
1. **Student Reporting Pipeline**: Rapid <30s reporting with photo evidence, campus location dropdown, GPS coordinates, and QR-code block scanning.
2. **QuickFix Smart Engine**:
   - **SmartAssist NLP Categorization**: Automatically detects categories (Electrical, Water, Cleanliness, Infrastructure, Network, Sanitation, Equipment) from descriptions.
   - **Dynamic Priority Engine**: Automatically calculates priority using `Severity × Impact × Category Weight` (CRITICAL, HIGH, MEDIUM, LOW) with transparent hazard reasons.
   - **Duplicate Issue Detection**: Identifies overlapping reports at the same campus facility before submission to prevent duplicate tickets.
3. **Campus Administration & Analytics**:
   - Live resolution timeline: `SUBMITTED` ➔ `VERIFIED` ➔ `IN PROGRESS` ➔ `RESOLVED`.
   - Real-time in-app notification alerts to the reporting student.
   - Campus overview metrics, category distribution bars, and campus trouble heatmap.

---

## 🚀 How to Run in VS Code (Windows)

### Step 1: Open the Project in VS Code
Open your VS Code terminal and navigate to the project directory:
```powershell
cd d:\Games\CarGame\quickfix
```

### Step 2: Install Dependencies
Flet is already installed in your Python environment. If needed:
```powershell
pip install -r requirements.txt
```

### Step 3: Run the App

#### Mode A: Run as Native Desktop Window (Default)
```powershell
python run.py
```
*This opens a desktop window styled with a realistic mobile smartphone frame!*

#### Mode B: Run in Web Browser / Mobile Emulator
```powershell
python run.py --web
```
*Opens `http://localhost:8550`. You can press `F12` in Chrome/Edge, toggle Device Emulation (Ctrl+Shift+M), and select iPhone 14 or Pixel 7 to test exact mobile gestures!*

#### Mode C: Instant Test on your Physical Android Phone over Wi-Fi
Make sure your phone and PC are connected to the same Wi-Fi router:
```powershell
python run.py --web --host 0.0.0.0 --port 8550
```
Open your mobile browser (Chrome on Android) and enter your PC's local IP address (e.g., `http://192.168.1.X:8550`). The app will open directly on your mobile device!

---

## 📦 How to Build the Mobile APK (Android)

You have two simple ways to generate the `.apk` file:

### Method 1: 1-Click Cloud Build with GitHub Actions (Recommended — Zero Local Setup)
Building an Android APK locally requires Android Studio, Java JDK 17, and Flutter SDK (over 15 GB of downloads). We have already configured a GitHub Actions workflow in `.github/workflows/build-apk.yml` that builds the APK in the cloud for free:

1. Create a repository on [GitHub](https://github.com/new).
2. Push your `quickfix` project to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial QuickFix Mobile App"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```
3. Go to the **Actions** tab on your GitHub repository.
4. The **Build Android APK** workflow will run automatically.
5. Once finished (approx. 5 minutes), click on the run and download the `quickfix-android-apk.zip` containing the ready-to-install `.apk`!
6. Transfer the `.apk` to your phone and install.

---

### Method 2: Local Build using Flet CLI (If Flutter & Android SDK are installed)
If you have Flutter and Android SDK installed on your machine:
```powershell
flet build apk --project-name quickfix --build-version 1.0.0
```
The compiled APK will be output in: `build/apk/app-release.apk`.

---

## 🧭 Live Demo & Judge Presentation Guide (15 Minutes)

Use this exact storyline during your demonstration:

| Time | Segment | What to Show & Say |
|---|---|---|
| **0:00–1:30** | **The Problem** | "Campus maintenance issues are scattered across verbal complaints and group chats. Students don't know if issues are noticed or being fixed." |
| **1:30–3:00** | **The QuickFix Solution** | Show Splash Screen & Home Dashboard. Explain: "QuickFix creates a transparent digital pipeline from reporting to resolution." |
| **3:00–6:00** | **Student Reporting Demo** | Click `+ Report Campus Issue`. Type: *"Street light near library is sparking"*. Show: (1) SmartAssist auto-detects **Electrical**, (2) Live Priority evaluates to **CRITICAL**, (3) Attached evidence photo, (4) Tap **Scan Campus QR** to auto-fill location, (5) Hit **Submit Report**. |
| **6:00–8:00** | **Duplicate Detection Innovation** | Try submitting a similar problem at Library Block. Show the **"⚠️ Similar Issue Detected"** warning dialog. |
| **8:00–11:00** | **Resolution Tracking Timeline** | Open **Issues** tab. Click on `#QF1024`. Walk through the 4-stage timeline: `Submitted` ➔ `Verified` ➔ `In Progress` ➔ `Resolved`. |
| **11:00–13:00** | **Admin Dispatch & Analytics** | Switch to **Admin Mode**. Show Campus Overview (Total, Pending, Resolved). Click `[Start Work]` or `[Resolve]` and demonstrate the instant in-app student notification! |
| **13:00–15:00** | **Heatmap & Future Vision** | Show the **Campus Problem Heatmap** showing hotspot clusters (Library, CSE Block, Hostel B), predictive maintenance, and IoT sensors. |

---

## 📁 Project Structure

```
quickfix/
├── pyproject.toml              # Flet app configuration & build metadata
├── requirements.txt            # Python dependencies
├── run.py                      # Universal runner (Desktop & Web)
├── README.md                   # Full documentation & demo guide
├── .github/
│   └── workflows/
│       └── build-apk.yml       # Cloud APK automated build pipeline
└── src/
    ├── main.py                 # App root, mobile frame, router & state
    ├── quickfix_data.json      # Local offline database with demo data
    ├── models/
    │   └── issue.py            # Issue, Status, Priority data model
    ├── services/
    │   ├── smart_engine.py     # NLP categorization, priority formula, duplicate detector
    │   ├── storage_service.py  # Local JSON persistent store & seed issues
    │   └── notification_service.py # In-app notification dispatcher
    └── views/
        ├── components.py       # Badges, icons, timeline widgets
        ├── home_view.py        # Student Home screen & quick report
        ├── report_view.py      # Issue submission with SmartAssist & QR scan
        ├── my_issues_view.py   # Search, status filters & issue list
        ├── issue_details_view.py # Detailed timeline tracker & status updater
        ├── admin_view.py       # Admin dashboard, analytics bars & heatmap
        └── profile_view.py     # Role switcher (Student/Admin) & notifications
```
