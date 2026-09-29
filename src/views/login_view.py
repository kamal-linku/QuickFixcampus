import flet as ft
from services.storage_service import StorageService

class LoginView:
    def __init__(self, storage: StorageService, page: ft.Page, on_login_success):
        self.storage = storage
        self.page = page
        self.on_login_success = on_login_success
        self.selected_role = "Student" # Student or Admin

    def build(self) -> ft.Control:
        # App Branding Header
        branding = ft.Container(
            padding=ft.Padding(24, 40, 24, 16),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Container(
                        width=64,
                        height=64,
                        border_radius=32,
                        bgcolor="#1E3A8A",
                        alignment=ft.Alignment.CENTER,
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=12, color="#1E3A8A44"),
                        content=ft.Icon(ft.Icons.BOLT, color="#FDE047", size=36)
                    ),
                    ft.Text("QuickFix", size=26, weight=ft.FontWeight.W_900, color="#1E3A8A"),
                    ft.Text("Smart Campus Issue Management", size=13, weight=ft.FontWeight.BOLD, color="#475569"),
                    ft.Container(
                        content=ft.Text("“See it. Report it. Track it. Fix it.”", size=11, italic=True, color="#2563EB", weight=ft.FontWeight.W_600),
                        padding=ft.Padding(8, 4, 8, 4),
                        bgcolor="#EFF6FF",
                        border_radius=12
                    )
                ]
            )
        )

        # Role Selector Buttons (Student vs Admin)
        role_indicator = ft.Text("Student Portal", size=13, weight=ft.FontWeight.BOLD, color="#1E3A8A")

        # Input fields
        email_field = ft.TextField(
            label="Email or Student ID",
            value="student@quickfix.demo",
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            border_radius=12,
            border_color="#CBD5E1",
            content_padding=14,
            text_size=13
        )

        password_field = ft.TextField(
            label="Password",
            value="demo123",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            border_radius=12,
            border_color="#CBD5E1",
            content_padding=14,
            text_size=13
        )

        remember_me = ft.Checkbox(
            label="Remember me on this device",
            value=True
        )

        student_btn_tab = ft.Container(
            expand=1,
            alignment=ft.Alignment.CENTER,
            padding=10,
            border_radius=10,
            bgcolor="#1E3A8A",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
                controls=[
                    ft.Icon(ft.Icons.SCHOOL, color="#FFFFFF", size=16),
                    ft.Text("Student", size=12, weight=ft.FontWeight.BOLD, color="#FFFFFF")
                ]
            )
        )

        admin_btn_tab = ft.Container(
            expand=1,
            alignment=ft.Alignment.CENTER,
            padding=10,
            border_radius=10,
            bgcolor="#F1F5F9",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
                controls=[
                    ft.Icon(ft.Icons.SECURITY, color="#64748B", size=16),
                    ft.Text("Admin / Staff", size=12, weight=ft.FontWeight.BOLD, color="#64748B")
                ]
            )
        )

        def switch_to_student(e):
            self.selected_role = "Student"
            role_indicator.value = "Student Portal"
            role_indicator.color = "#1E3A8A"
            email_field.label = "Email or Student ID"
            email_field.value = "student@quickfix.demo"
            student_btn_tab.bgcolor = "#1E3A8A"
            student_btn_tab.content.controls[0].color = "#FFFFFF"
            student_btn_tab.content.controls[1].color = "#FFFFFF"
            admin_btn_tab.bgcolor = "#F1F5F9"
            admin_btn_tab.content.controls[0].color = "#64748B"
            admin_btn_tab.content.controls[1].color = "#64748B"
            submit_btn.content.controls[1].value = "LOGIN AS STUDENT"
            submit_btn.style.bgcolor = "#1E3A8A"
            self.page.update()

        def switch_to_admin(e):
            self.selected_role = "Admin"
            role_indicator.value = "Campus Staff / Admin Portal"
            role_indicator.color = "#7C3AED"
            email_field.label = "Admin / Staff Email"
            email_field.value = "admin@quickfix.demo"
            admin_btn_tab.bgcolor = "#7C3AED"
            admin_btn_tab.content.controls[0].color = "#FFFFFF"
            admin_btn_tab.content.controls[1].color = "#FFFFFF"
            student_btn_tab.bgcolor = "#F1F5F9"
            student_btn_tab.content.controls[0].color = "#64748B"
            student_btn_tab.content.controls[1].color = "#64748B"
            submit_btn.content.controls[1].value = "LOGIN AS ADMIN"
            submit_btn.style.bgcolor = "#7C3AED"
            self.page.update()

        student_btn_tab.on_click = switch_to_student
        admin_btn_tab.on_click = switch_to_admin

        role_tab_row = ft.Container(
            padding=4,
            border_radius=12,
            bgcolor="#F1F5F9",
            content=ft.Row(
                spacing=4,
                controls=[student_btn_tab, admin_btn_tab]
            )
        )

        def do_login(e):
            email = email_field.value.strip() if email_field.value else ""
            if not email:
                self.page.show_dialog(
                    ft.SnackBar(content="⚠️ Please enter your email or ID.", bgcolor="#DC2626", open=True)
                )
                return

            user_data = {
                "role": self.selected_role,
                "email": email,
                "name": "Alex Mercer (Student)" if self.selected_role == "Student" else "Campus Facility Admin"
            }

            # Save session to local storage
            self.storage.save_session(user_data)

            self.page.show_dialog(
                ft.SnackBar(content=f"Welcome {user_data['name']}! Logging in...", bgcolor="#10B981", open=True)
            )

            # Transition to main app
            self.on_login_success(self.selected_role, user_data)

        def login_guest(e):
            user_data = {
                "role": "Student",
                "email": "guest@quickfix.demo",
                "name": "Campus Guest"
            }
            self.storage.save_session(user_data)
            self.on_login_success("Student", user_data)

        submit_btn = ft.FilledButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.LOGIN_ROUNDED, color="#FFFFFF", size=18),
                    ft.Text("LOGIN AS STUDENT", size=13, weight=ft.FontWeight.W_900, color="#FFFFFF")
                ]
            ),
            style=ft.ButtonStyle(
                bgcolor="#1E3A8A",
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding(16, 14, 16, 14)
            ),
            on_click=do_login
        )

        guest_btn = ft.TextButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
                controls=[
                    ft.Icon(ft.Icons.PERSON_OUTLINE, size=16, color="#64748B"),
                    ft.Text("Continue as Guest", size=12, color="#64748B", weight=ft.FontWeight.W_600)
                ]
            ),
            on_click=login_guest
        )

        # Login Form Card
        form_card = ft.Container(
            margin=ft.Margin(16, 0, 16, 16),
            padding=20,
            border_radius=18,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E2E8F0"),
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="#64748B15"),
            content=ft.Column(
                spacing=14,
                controls=[
                    role_tab_row,
                    role_indicator,
                    email_field,
                    password_field,
                    remember_me,
                    submit_btn,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(expand=True, height=1, bgcolor="#E2E8F0"),
                            ft.Text("  OR  ", size=11, color="#94A3B8"),
                            ft.Container(expand=True, height=1, bgcolor="#E2E8F0")
                        ]
                    ),
                    guest_btn
                ]
            )
        )

        # Quick Demo Account Chips
        demo_chips = ft.Container(
            padding=ft.Padding(16, 0, 16, 24),
            content=ft.Column(
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Competition Demo Accounts:", size=11, color="#64748B", weight=ft.FontWeight.W_600),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            ft.Chip(
                                label=ft.Text("Student Demo", size=11),
                                on_click=lambda _: switch_to_student(None)
                            ),
                            ft.Chip(
                                label=ft.Text("Admin Demo", size=11),
                                on_click=lambda _: switch_to_admin(None)
                            )
                        ]
                    )
                ]
            )
        )

        return ft.ListView(
            expand=True,
            spacing=0,
            controls=[
                branding,
                form_card,
                demo_chips
            ]
        )
