import flet as ft
from services.storage_service import StorageService
from services.notification_service import NotificationService

class ProfileView:
    def __init__(self, storage: StorageService, notifications: NotificationService, page: ft.Page, current_role: str, on_role_change):
        self.storage = storage
        self.notifications = notifications
        self.page = page
        self.current_role = current_role
        self.on_role_change = on_role_change

    def build(self) -> ft.Control:
        user_email = "student@quickfix.demo" if self.current_role == "Student" else "admin@quickfix.demo"
        user_name = "Alex Mercer (Student)" if self.current_role == "Student" else "Campus Facility Admin"

        # User Info Header Card
        user_card = ft.Container(
            margin=ft.Margin(16, 14, 16, 12),
            padding=16,
            border_radius=16,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E2E8F0"),
            content=ft.Row(
                spacing=14,
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.PERSON if self.current_role == "Student" else ft.Icons.ADMIN_PANEL_SETTINGS,
                            color="#FFFFFF",
                            size=28
                        ),
                        bgcolor="#1E3A8A" if self.current_role == "Student" else "#7C3AED",
                        border_radius=25,
                        width=50,
                        height=50,
                        alignment=ft.Alignment.CENTER
                    ),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(user_name, size=15, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            ft.Text(user_email, size=12, color="#64748B"),
                            ft.Container(
                                content=ft.Text(f"Current Role: {self.current_role.upper()}", size=10, weight=ft.FontWeight.BOLD, color="#1D4ED8"),
                                bgcolor="#EFF6FF",
                                padding=ft.Padding(6, 2, 6, 2),
                                border_radius=6
                            )
                        ]
                    )
                ]
            )
        )

        # Role Switcher Card (Pages 23 & 24)
        def handle_role_toggle(new_role):
            self.current_role = new_role
            self.on_role_change(new_role)
            self.page.show_dialog(
                ft.SnackBar(content=f"Switched role to {new_role}!", bgcolor="#1E3A8A", open=True)
            )

        role_switcher_card = ft.Container(
            margin=ft.Margin(16, 0, 16, 12),
            padding=16,
            border_radius=16,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E2E8F0"),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text("Demo Accounts & Role Switch", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text("Instantly toggle between Student reporting view and Staff Admin view for presentation:", size=11, color="#64748B"),
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.FilledButton(
                                content=ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.Icon(ft.Icons.SCHOOL, color="#FFFFFF", size=16),
                                        ft.Text("Student Mode", size=11, color="#FFFFFF")
                                    ]
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor="#1E3A8A" if self.current_role == "Student" else "#94A3B8",
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                ),
                                on_click=lambda _: handle_role_toggle("Student")
                            ),
                            ft.FilledButton(
                                content=ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.Icon(ft.Icons.SECURITY, color="#FFFFFF", size=16),
                                        ft.Text("Admin Mode", size=11, color="#FFFFFF")
                                    ]
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor="#7C3AED" if self.current_role == "Admin" else "#94A3B8",
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                ),
                                on_click=lambda _: handle_role_toggle("Admin")
                            )
                        ]
                    )
                ]
            )
        )

        # In-App Notifications History (Page 18)
        notifs = self.notifications.get_all()
        notif_items = []
        for n in notifs[:5]:
            notif_items.append(
                ft.Container(
                    padding=10,
                    border_radius=10,
                    bgcolor="#F8FAFC",
                    border=ft.Border.all(1, "#F1F5F9"),
                    content=ft.Row(
                        spacing=10,
                        controls=[
                            ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color="#2563EB", size=18),
                            ft.Column(
                                expand=True,
                                spacing=2,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(n.title, size=12, weight=ft.FontWeight.BOLD, color="#1E293B"),
                                            ft.Text(n.timestamp, size=10, color="#94A3B8")
                                        ]
                                    ),
                                    ft.Text(n.message, size=11, color="#64748B")
                                ]
                            )
                        ]
                    )
                )
            )

        notifications_card = ft.Container(
            margin=ft.Margin(16, 0, 16, 12),
            padding=16,
            border_radius=16,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E2E8F0"),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("In-App Notification Feed", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, color="#2563EB", size=18)
                        ]
                    ),
                    *notif_items
                ]
            )
        )

        # Prototype Data Controls
        def reset_data(e):
            self.storage.reset_demo_data()
            self.page.show_dialog(
                ft.SnackBar(content="Database reset with initial demo issues (#QF1024 - #QF1028)!", bgcolor="#10B981", open=True)
            )
            self.page.update()

        data_management_card = ft.Container(
            margin=ft.Margin(16, 0, 16, 12),
            padding=16,
            border_radius=16,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E2E8F0"),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text("Demonstration Data", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text("Reset or seed initial competition demo problems:", size=11, color="#64748B"),
                    ft.OutlinedButton(
                        content=ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(ft.Icons.RESTORE_ROUNDED, color="#2563EB", size=16),
                                ft.Text("Reset to Initial Demo Issues", size=11, color="#2563EB")
                            ]
                        ),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=reset_data
                    )
                ]
            )
        )

        # About Card & Pitch (Page 35)
        about_card = ft.Container(
            margin=ft.Margin(16, 0, 16, 24),
            padding=16,
            border_radius=16,
            bgcolor="#EFF6FF",
            border=ft.Border.all(1, "#BFDBFE"),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Text("QuickFix — Smart Campus Issue Management", size=13, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                    ft.Text("“See it. Report it. Track it. Fix it.”", size=12, italic=True, weight=ft.FontWeight.W_600, color="#1D4ED8"),
                    ft.Text("A digital pipeline enabling students and campus staff to report, intelligently categorize, prioritize, and track resolutions with complete transparency.", size=11, color="#475569")
                ]
            )
        )

        return ft.ListView(
            expand=True,
            spacing=0,
            controls=[
                user_card,
                role_switcher_card,
                notifications_card,
                data_management_card,
                about_card,
                ft.Container(height=30)
            ]
        )
