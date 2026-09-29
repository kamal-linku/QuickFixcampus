import flet as ft
import os
import base64
from services.storage_service import StorageService
from services.smart_engine import SmartEngine
from services.notification_service import NotificationService
from models.issue import Issue, IssueStatus
from views.components import build_priority_badge, get_priority_color

CAMPUS_LOCATIONS = [
    "Library Block",
    "Main Gate",
    "CSE Block",
    "ECE Block",
    "Hostel A",
    "Hostel B",
    "Cafeteria",
    "Parking",
    "Auditorium"
]

SAMPLE_PHOTOS = {
    "Electrical": "https://picsum.photos/seed/elec_report/400/250",
    "Water": "https://picsum.photos/seed/water_report/400/250",
    "Cleanliness": "https://picsum.photos/seed/clean_report/400/250",
    "Infrastructure": "https://picsum.photos/seed/infra_report/400/250",
    "Network": "https://picsum.photos/seed/net_report/400/250",
    "Default": "https://picsum.photos/seed/default_report/400/250"
}

class ReportView:
    def __init__(self, storage: StorageService, notifications: NotificationService, page: ft.Page, on_success, on_open_issue):
        self.storage = storage
        self.notifications = notifications
        self.page = page
        self.on_success = on_success
        self.on_open_issue = on_open_issue

        # State
        self.selected_category = "Electrical"
        self.selected_location = "Library Block"
        self.photo_url = SAMPLE_PHOTOS["Electrical"]
        self.photo_name = "evidence_photo.jpg"
        self.gps_coords = "20.2961° N, 85.8245° E"
        self.is_duplicate_suppressed = False

    def build(self) -> ft.Control:
        # Title & Category Dropdown
        title_field = ft.TextField(
            label="Issue Title",
            hint_text="e.g. Street Light Near Library Not Working",
            border_radius=12,
            border_color="#CBD5E1",
            content_padding=14,
            text_size=13
        )

        category_dropdown = ft.Dropdown(
            label="Category",
            value=self.selected_category,
            border_radius=12,
            border_color="#CBD5E1",
            text_size=13,
            options=[
                ft.DropdownOption("Electrical"),
                ft.DropdownOption("Water"),
                ft.DropdownOption("Cleanliness"),
                ft.DropdownOption("Infrastructure"),
                ft.DropdownOption("Network"),
                ft.DropdownOption("Sanitation"),
                ft.DropdownOption("Equipment"),
                ft.DropdownOption("Other")
            ]
        )

        location_dropdown = ft.Dropdown(
            label="Campus Location",
            value=self.selected_location,
            border_radius=12,
            border_color="#CBD5E1",
            text_size=13,
            options=[ft.DropdownOption(loc) for loc in CAMPUS_LOCATIONS]
        )

        # Smart Assist feedback banner
        smart_assist_text = ft.Text(
            "QuickFix SmartAssist: Type description to auto-categorize & assess priority.",
            size=11,
            color="#2563EB",
            weight=ft.FontWeight.W_500
        )
        smart_assist_container = ft.Container(
            padding=ft.Padding(10, 8, 10, 8),
            border_radius=10,
            bgcolor="#EFF6FF",
            border=ft.Border.all(1, "#DBEAFE"),
            content=ft.Row(
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.AUTO_AWESOME, color="#2563EB", size=16),
                    ft.Container(expand=True, content=smart_assist_text)
                ]
            )
        )

        # Smart Priority Live Preview Box (Pages 11, 12)
        priority_score_text = ft.Text("Priority Score: 18 (HIGH)", size=12, weight=ft.FontWeight.BOLD, color="#EA580C")
        priority_reason_text = ft.Text("High campus traffic area; safety hazard", size=11, color="#64748B")
        priority_chips_row = ft.Row(
            spacing=8,
            controls=[
                ft.Container(content=ft.Text("Severity: HIGH", size=10, weight=ft.FontWeight.BOLD, color="#EA580C"), bgcolor="#FFF7ED", border_radius=6, padding=4),
                ft.Container(content=ft.Text("Impact: HIGH", size=10, weight=ft.FontWeight.BOLD, color="#2563EB"), bgcolor="#EFF6FF", border_radius=6, padding=4),
                ft.Container(content=ft.Text("Category: 1.4x", size=10, weight=ft.FontWeight.BOLD, color="#16A34A"), bgcolor="#F0FDF4", border_radius=6, padding=4)
            ]
        )

        priority_preview_box = ft.Container(
            padding=12,
            border_radius=14,
            bgcolor="#FFFBEB",
            border=ft.Border.all(1, "#FDE68A"),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Icon(ft.Icons.ANALYTICS, color="#D97706", size=16),
                                    ft.Text("Smart Priority Analysis", size=12, weight=ft.FontWeight.BOLD, color="#92400E")
                                ]
                            ),
                            priority_score_text
                        ]
                    ),
                    priority_reason_text,
                    priority_chips_row
                ]
            )
        )

        # Duplicate Warning Banner (Page 14)
        duplicate_text = ft.Text("", size=11, color="#991B1B")
        existing_dup_issue = {"issue": None}

        def view_existing_dup(e):
            if existing_dup_issue["issue"]:
                self.on_open_issue(existing_dup_issue["issue"])

        duplicate_banner = ft.Container(
            visible=False,
            padding=12,
            border_radius=14,
            bgcolor="#FEF2F2",
            border=ft.Border.all(1, "#FECACA"),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        spacing=6,
                        controls=[
                            ft.Icon(ft.Icons.WARNING_ROUNDED, color="#DC2626", size=18),
                            ft.Text("Similar Issue Detected!", size=12, weight=ft.FontWeight.BOLD, color="#991B1B")
                        ]
                    ),
                    duplicate_text,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=8,
                        controls=[
                            ft.OutlinedButton(
                                content=ft.Text("View Existing Issue", size=11, color="#DC2626"),
                                on_click=view_existing_dup
                            ),
                            ft.TextButton(
                                content=ft.Text("Report Anyway", size=11, color="#475569"),
                                on_click=lambda _: set_suppress_dup()
                            )
                        ]
                    )
                ]
            )
        )

        def set_suppress_dup():
            self.is_duplicate_suppressed = True
            duplicate_banner.visible = False
            self.page.update()

        # Update Calculations when user types
        def recalculate(e=None):
            desc_val = desc_field.value or ""
            cat_val = category_dropdown.value or "Other"
            loc_val = location_dropdown.value or "Campus"

            # 1. Smart Category NLP detection
            if desc_val:
                detected_cat, conf = SmartEngine.detect_category(desc_val)
                if detected_cat != "Other" and conf >= 0.35 and detected_cat != category_dropdown.value:
                    category_dropdown.value = detected_cat
                    cat_val = detected_cat
                    smart_assist_text.value = f"SmartAssist: Auto-detected category '{detected_cat}' from keywords ({int(conf*100)}% match)."
                    smart_assist_container.bgcolor = "#F0FDF4"
                    smart_assist_container.border = ft.Border.all(1, "#BBF7D0")
                    smart_assist_text.color = "#15803D"

            # 2. Smart Priority calculation
            res = SmartEngine.calculate_priority(cat_val, loc_val, desc_val)
            color = get_priority_color(res["level"])
            priority_score_text.value = f"Score: {res['score']} ({res['level']})"
            priority_score_text.color = color
            priority_reason_text.value = res["reason"]

            priority_chips_row.controls = [
                ft.Container(content=ft.Text(f"Severity: {res['severity_label']}", size=10, weight=ft.FontWeight.BOLD, color=color), bgcolor=f"{color}18", border_radius=6, padding=4),
                ft.Container(content=ft.Text(f"Impact: {res['impact_label']}", size=10, weight=ft.FontWeight.BOLD, color="#2563EB"), bgcolor="#EFF6FF", border_radius=6, padding=4),
                ft.Container(content=ft.Text(f"Category: {res['category_weight']}x", size=10, weight=ft.FontWeight.BOLD, color="#16A34A"), bgcolor="#F0FDF4", border_radius=6, padding=4)
            ]

            # 3. Duplicate detection
            if not self.is_duplicate_suppressed and len(desc_val.strip()) >= 5:
                dup_result = SmartEngine.detect_duplicate(cat_val, loc_val, desc_val, self.storage.get_all())
                if dup_result:
                    existing_dup_issue["issue"] = dup_result["existing_issue"]
                    duplicate_text.value = f"A similar problem was already reported at {loc_val}: Issue #{dup_result['existing_issue'].id} ('{dup_result['existing_issue'].title}') is {dup_result['existing_issue'].status}."
                    duplicate_banner.visible = True
                else:
                    duplicate_banner.visible = False
            else:
                duplicate_banner.visible = False

            self.page.update()

        category_dropdown.on_select = recalculate
        location_dropdown.on_select = recalculate

        # Description Field
        desc_field = ft.TextField(
            label="Description",
            hint_text="e.g. Street light near library entrance is not working since yesterday night.",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=12,
            border_color="#CBD5E1",
            content_padding=14,
            text_size=13,
            on_change=recalculate
        )

        # Voice input simulation
        def trigger_voice_input(e):
            desc_field.value = "Street light near library is flickering and sparking. Need immediate repair."
            title_field.value = "Library Street Light Sparking"
            category_dropdown.value = "Electrical"
            location_dropdown.value = "Library Block"
            recalculate()
            self.page.show_dialog(
                ft.SnackBar(content="🎙️ Voice note transcribed: 'Library street light sparking...'", bgcolor="#1E3A8A", open=True)
            )

        voice_button = ft.OutlinedButton(
            content=ft.Row(
                spacing=4,
                controls=[
                    ft.Icon(ft.Icons.MIC_ROUNDED, color="#2563EB", size=16),
                    ft.Text("Speak instead (Voice Input)", size=11, color="#2563EB")
                ]
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(10, 8, 10, 8)
            ),
            on_click=trigger_voice_input
        )

        # Photo Preview & Selector (Pages 9 & 10)
        photo_image = ft.Image(
            src=self.photo_url,
            width=360,
            height=160,
            fit="cover",
            border_radius=12
        )
        photo_label = ft.Text("📷 Attached Evidence: Street light photo attached", size=11, color="#475569", italic=True)

        def apply_picked_file(picked):
            new_src = None
            if picked.bytes:
                b64 = base64.b64encode(picked.bytes).decode("utf-8")
                new_src = f"data:image/jpeg;base64,{b64}"
            elif picked.path and os.path.exists(picked.path):
                try:
                    with open(picked.path, "rb") as img_f:
                        b64 = base64.b64encode(img_f.read()).decode("utf-8")
                        new_src = f"data:image/jpeg;base64,{b64}"
                except Exception:
                    new_src = picked.path
            else:
                new_src = picked.path or ""

            if new_src:
                self.photo_url = new_src
                photo_image.src = self.photo_url
                photo_label.value = f"📷 Gallery Photo Attached: {picked.name}"
                self.page.show_dialog(
                    ft.SnackBar(content=f"🖼️ Attached evidence photo: {picked.name}", bgcolor="#10B981", open=True)
                )
                self.page.update()

        def on_file_picked(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                apply_picked_file(e.files[0])

        file_picker = ft.FilePicker(on_result=on_file_picked)
        if hasattr(self.page, "services") and self.page.services is not None:
            if file_picker not in self.page.services:
                self.page.services.append(file_picker)

        async def handle_gallery(e):
            try:
                files = await file_picker.pick_files(
                    dialog_title="Select Campus Evidence Photo",
                    file_type=ft.FilePickerFileType.IMAGE,
                    with_data=True
                )
                if files and len(files) > 0:
                    apply_picked_file(files[0])
            except Exception as ex:
                print(f"Gallery picker: {ex}")

        async def handle_camera(e):
            captured = False
            try:
                import cv2
                cap = cv2.VideoCapture(0)
                if cap.isOpened():
                    ret, frame = cap.read()
                    cap.release()
                    if ret and frame is not None:
                        _, buffer = cv2.imencode(".jpg", frame)
                        b64 = base64.b64encode(buffer).decode("utf-8")
                        self.photo_url = f"data:image/jpeg;base64,{b64}"
                        photo_image.src = self.photo_url
                        photo_label.value = "📸 Live Camera Snapshot Attached"
                        self.page.show_dialog(
                            ft.SnackBar(content="📸 Photo captured live from camera!", bgcolor="#10B981", open=True)
                        )
                        self.page.update()
                        captured = True
            except Exception:
                captured = False

            if not captured:
                try:
                    files = await file_picker.pick_files(
                        dialog_title="Capture or Select Photo",
                        file_type=ft.FilePickerFileType.IMAGE,
                        with_data=True
                    )
                    if files and len(files) > 0:
                        apply_picked_file(files[0])
                except Exception as ex:
                    print(f"Camera picker: {ex}")

        def set_preset_photo(cat, label_name):
            self.photo_url = SAMPLE_PHOTOS.get(cat, SAMPLE_PHOTOS["Default"])
            photo_image.src = self.photo_url
            photo_label.value = f"📷 Evidence Preset: {label_name}"
            self.page.show_dialog(
                ft.SnackBar(content=f"Attached sample: {label_name}", bgcolor="#2563EB", open=True)
            )
            self.page.update()

        photo_controls_row = ft.Row(
            spacing=8,
            controls=[
                ft.FilledButton(
                    content=ft.Row(
                        spacing=4,
                        controls=[
                            ft.Icon(ft.Icons.CAMERA_ALT_ROUNDED, color="#FFFFFF", size=16),
                            ft.Text("Take Photo", size=11, color="#FFFFFF")
                        ]
                    ),
                    style=ft.ButtonStyle(bgcolor="#1E3A8A", shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=handle_camera
                ),
                ft.OutlinedButton(
                    content=ft.Row(
                        spacing=4,
                        controls=[
                            ft.Icon(ft.Icons.PHOTO_LIBRARY_ROUNDED, color="#475569", size=16),
                            ft.Text("Choose from Gallery", size=11, color="#475569")
                        ]
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=handle_gallery
                )
            ]
        )

        preset_chips = ft.Row(
            spacing=6,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Chip(label=ft.Text("💡 Street Light", size=10), on_click=lambda _: set_preset_photo("Electrical", "Street Light")),
                ft.Chip(label=ft.Text("💧 Pipe Leak", size=10), on_click=lambda _: set_preset_photo("Water", "Pipe Leak")),
                ft.Chip(label=ft.Text("⚡ Hazard Wire", size=10), on_click=lambda _: set_preset_photo("Electrical", "Hazard Wire")),
                ft.Chip(label=ft.Text("🪑 Broken Bench", size=10), on_click=lambda _: set_preset_photo("Infrastructure", "Broken Bench")),
            ]
        )

        # Location Options (Pages 10, 28, 29)
        gps_display = ft.Text(f"📍 GPS: {self.gps_coords}", size=11, color="#64748B")

        def simulate_gps(e):
            self.gps_coords = "20.2961° N, 85.8245° E (Accuracy: ±2m)"
            gps_display.value = f"📍 GPS: {self.gps_coords}"
            self.page.show_dialog(
                ft.SnackBar(content="📍 High-accuracy GPS location acquired!", bgcolor="#2563EB", open=True)
            )
            self.page.update()

        # QR Location Feature (Pages 28 & 29)
        def simulate_qr_scan(e):
            location_dropdown.value = "Library Block"
            title_field.value = title_field.value or "Library Ground Floor Issue"
            gps_display.value = "📍 QR Tag: [LIB-BLK-01] Library Block - Ground Floor"
            recalculate()
            self.page.show_dialog(
                ft.SnackBar(content="📱 QR Code Scanned: 'Library Block - Ground Floor' auto-filled!", bgcolor="#7C3AED", open=True)
            )

        location_quick_buttons = ft.Row(
            spacing=8,
            controls=[
                ft.OutlinedButton(
                    content=ft.Row(
                        spacing=4,
                        controls=[
                            ft.Icon(ft.Icons.MY_LOCATION, color="#1D4ED8", size=14),
                            ft.Text("Use Current GPS", size=11, color="#1D4ED8")
                        ]
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=simulate_gps
                ),
                ft.OutlinedButton(
                    content=ft.Row(
                        spacing=4,
                        controls=[
                            ft.Icon(ft.Icons.QR_CODE_SCANNER, color="#7C3AED", size=14),
                            ft.Text("Scan Campus QR", size=11, color="#7C3AED")
                        ]
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=simulate_qr_scan
                )
            ]
        )

        # Submit Action Handler
        def handle_submit(e):
            desc = desc_field.value.strip() if desc_field.value else ""
            if not desc:
                self.page.show_dialog(
                    ft.SnackBar(content="⚠️ Please provide an issue description.", bgcolor="#DC2626", open=True)
                )
                return

            cat = category_dropdown.value or "Other"
            loc = location_dropdown.value or "Campus"
            title = title_field.value.strip() if title_field.value and title_field.value.strip() else f"{cat} Problem at {loc}"

            # Smart calculation
            p_calc = SmartEngine.calculate_priority(cat, loc, desc)
            new_id = self.storage.generate_next_id()

            new_issue = Issue(
                id=new_id,
                title=title,
                description=desc,
                category=cat,
                location=loc,
                severity=p_calc["severity_label"],
                impact=p_calc["impact_label"],
                priority=p_calc["level"],
                priority_score=p_calc["score"],
                priority_reason=p_calc["reason"],
                status=IssueStatus.SUBMITTED,
                image=self.photo_url,
                reporter="student@quickfix.demo"
            )

            self.storage.add_issue(new_issue)
            self.notifications.notify(
                title="Issue Submitted",
                message=f"Issue #{new_id} successfully submitted. Priority: {new_issue.priority}.",
                issue_id=new_id,
                status=IssueStatus.SUBMITTED
            )

            # Show Success Dialog
            def close_dialog(dlg_e):
                self.page.pop_dialog()
                self.on_success(new_issue)

            success_dlg = ft.AlertDialog(
                title=ft.Row(
                    spacing=8,
                    controls=[
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color="#10B981", size=24),
                        ft.Text("Issue Reported!", size=18, weight=ft.FontWeight.BOLD)
                    ]
                ),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Text(f"Ticket #{new_id} generated successfully.", weight=ft.FontWeight.BOLD, size=13),
                        ft.Text(f"Title: {title}", size=12),
                        ft.Text(f"Location: {loc} ({cat})", size=12),
                        ft.Row(
                            spacing=6,
                            controls=[
                                ft.Text("Priority:", size=12),
                                build_priority_badge(new_issue.priority)
                            ]
                        ),
                        ft.Text("Track progress on the My Issues timeline.", size=11, color="#64748B")
                    ]
                ),
                actions=[
                    ft.FilledButton(
                        content=ft.Text("Track Issue Timeline", color="#FFFFFF"),
                        style=ft.ButtonStyle(bgcolor="#1E3A8A"),
                        on_click=close_dialog
                    )
                ]
            )
            self.page.show_dialog(success_dlg)

        submit_button = ft.FilledButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.SEND_ROUNDED, color="#FFFFFF", size=18),
                    ft.Text("SUBMIT REPORT", weight=ft.FontWeight.W_900, size=14, color="#FFFFFF")
                ]
            ),
            style=ft.ButtonStyle(
                bgcolor="#1E3A8A",
                shape=ft.RoundedRectangleBorder(radius=14),
                padding=ft.Padding(16, 16, 16, 16)
            ),
            on_click=handle_submit
        )

        return ft.ListView(
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    padding=ft.Padding(16, 14, 16, 6),
                    content=ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("Report Campus Issue", size=20, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            ft.Text("Fill in problem details or let SmartAssist detect it", size=12, color="#64748B")
                        ]
                    )
                ),
                ft.Container(
                    margin=ft.Margin(16, 6, 16, 12),
                    padding=16,
                    border_radius=16,
                    bgcolor="#FFFFFF",
                    border=ft.Border.all(1, "#E2E8F0"),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            title_field,
                            category_dropdown,
                            smart_assist_container,
                            desc_field,
                            voice_button,
                            ft.Divider(height=1, color="#F1F5F9"),
                            ft.Text("Location Details", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            location_dropdown,
                            location_quick_buttons,
                            gps_display,
                            ft.Divider(height=1, color="#F1F5F9"),
                            ft.Text("Photo Evidence", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            photo_image,
                            photo_label,
                            photo_controls_row,
                            preset_chips,
                            ft.Divider(height=1, color="#F1F5F9"),
                            priority_preview_box,
                            duplicate_banner,
                            submit_button
                        ]
                    )
                ),
                ft.Container(height=30)
            ]
        )
