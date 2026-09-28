import flet as ft
import time
import os
import sys

# Ensure local imports work regardless of execution directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.storage_service import StorageService
from services.notification_service import NotificationService
from views.home_view import HomeView
from views.report_view import ReportView
from views.my_issues_view import MyIssuesView
from views.admin_view import AdminView
from views.profile_view import ProfileView
from views.issue_details_view import IssueDetailsView

def main(page: ft.Page):
    # App Window Configuration
    page.title = "QuickFix — Smart Campus Issue Management"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F1F5F9"
    page.padding = 0

    # Initialize Services
    storage = StorageService()
    notifications = NotificationService()

    # App State
    current_role = ["Student"] # Student or Admin
    selected_index = [0]       # 0: Home, 1: Report, 2: My Issues, 3: Admin, 4: Profile
    viewing_issue = [None]     # If not None, renders IssueDetailsView

    # Notification Listener
    def on_new_notification(notif):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Row(
                    spacing=8,
                    controls=[
                        ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color="#FFFFFF", size=18),
                        ft.Text(f"{notif.title}: {notif.message}", color="#FFFFFF", size=12)
                    ]
                ),
                bgcolor="#1E3A8A",
                open=True
            )
        )
        page.update()

    notifications.subscribe(on_new_notification)

    # Navigation Handlers
    def navigate_to(idx: int):
        viewing_issue[0] = None
        selected_index[0] = idx
        nav_bar.selected_index = idx
        render_content()

    def open_issue_details(issue):
        viewing_issue[0] = issue
        render_content()

    def back_to_list():
        viewing_issue[0] = None
        render_content()

    def on_role_switched(new_role: str):
        current_role[0] = new_role
        if new_role == "Admin":
            selected_index[0] = 3
            nav_bar.selected_index = 3
        else:
            selected_index[0] = 0
            nav_bar.selected_index = 0
        render_content()

    # Content Area Container
    content_area = ft.Container(expand=True)

    # Bottom Navigation Bar
    nav_bar = ft.NavigationBar(
        selected_index=0,
        bgcolor="#FFFFFF",
        elevation=8,
        indicator_color="#DBEAFE",
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.ADD_CIRCLE_OUTLINE, selected_icon=ft.Icons.ADD_CIRCLE, label="Report"),
            ft.NavigationBarDestination(icon=ft.Icons.FORMAT_LIST_BULLETED_OUTLINED, selected_icon=ft.Icons.FORMAT_LIST_BULLETED, label="Issues"),
            ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Admin"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Profile")
        ],
        on_change=lambda e: navigate_to(e.control.selected_index)
    )

    def render_content():
        if viewing_issue[0] is not None:
            details_view = IssueDetailsView(
                issue=viewing_issue[0],
                storage=storage,
                notifications=notifications,
                page=page,
                on_back=back_to_list,
                on_updated=lambda updated: open_issue_details(updated)
            )
            content_area.content = details_view.build()
        elif selected_index[0] == 0:
            content_area.content = HomeView(
                storage=storage,
                on_navigate=navigate_to,
                on_open_issue=open_issue_details
            ).build()
        elif selected_index[0] == 1:
            content_area.content = ReportView(
                storage=storage,
                notifications=notifications,
                page=page,
                on_success=lambda iss: open_issue_details(iss),
                on_open_issue=open_issue_details
            ).build()
        elif selected_index[0] == 2:
            content_area.content = MyIssuesView(
                storage=storage,
                page=page,
                on_open_issue=open_issue_details
            ).build()
        elif selected_index[0] == 3:
            content_area.content = AdminView(
                storage=storage,
                notifications=notifications,
                page=page,
                on_open_issue=open_issue_details
            ).build()
        elif selected_index[0] == 4:
            content_area.content = ProfileView(
                storage=storage,
                notifications=notifications,
                page=page,
                current_role=current_role[0],
                on_role_change=on_role_switched
            ).build()

        page.update()

    # Mobile Shell Container: Responsive layout that looks like a smartphone on desktop and expands cleanly on mobile
    phone_frame = ft.Container(
        expand=True,
        bgcolor="#F8FAFC",
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # Top App Bar / Status Indicator
                ft.Container(
                    bgcolor="#1E3A8A",
                    padding=ft.Padding(16, 12, 16, 12),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.BOLT, color="#FDE047", size=20),
                                    ft.Text("QuickFix", size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF")
                                ]
                            ),
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Container(
                                        content=ft.Text(f"{current_role[0]}", size=11, color="#FFFFFF", weight=ft.FontWeight.BOLD),
                                        padding=ft.Padding(8, 2, 8, 2),
                                        border_radius=10,
                                        bgcolor="#3B82F6"
                                    ),
                                    ft.Icon(ft.Icons.WIFI, color="#93C5FD", size=16),
                                    ft.Icon(ft.Icons.BATTERY_FULL, color="#93C5FD", size=16)
                                ]
                            )
                        ]
                    )
                ),
                content_area,
                nav_bar
            ]
        )
    )

    # Center on desktop for mobile preview, or full screen
    app_wrapper = ft.SafeArea(
        expand=True,
        content=ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            bgcolor="#E2E8F0",
            content=ft.Container(
                width=450,
                expand=True,
                bgcolor="#FFFFFF",
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color="#64748B30"),
                content=phone_frame
            )
        )
    )

    page.add(app_wrapper)

    # Initial Render
    render_content()

if __name__ == "__main__":
    ft.run(main)
