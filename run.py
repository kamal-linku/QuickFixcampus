import sys
import os
import argparse
import flet as ft

# Add src to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from main import main

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run QuickFix Smart Campus Issue Management App")
    parser.add_argument("--web", action="store_true", help="Run in web browser mode")
    parser.add_argument("--port", type=int, default=8550, help="Web server port (default: 8550)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address (default: 0.0.0.0)")
    args = parser.parse_args()

    print("=" * 60, flush=True)
    print("[*] Starting QuickFix - Smart Campus Issue Management", flush=True)
    print("[*] 'See it. Report it. Track it. Fix it.'", flush=True)
    print("=" * 60, flush=True)

    if args.web:
        print(f"[+] Running in Web mode: http://localhost:{args.port}", flush=True)
        print("[+] You can also access this from your mobile phone on the same Wi-Fi!", flush=True)
        ft.run(main, host=args.host, port=args.port, view=ft.AppView.WEB_BROWSER)
    else:
        print("[+] Running in Native Desktop Window mode...", flush=True)
        print("[+] Tip: Add '--web' flag to run in browser: python run.py --web", flush=True)
        ft.run(main, view=ft.AppView.FLET_APP)
