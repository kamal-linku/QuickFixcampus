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
from views.login_view import LoginView

def main(page: ft.Page):
    # App Window Configuration
    page.title = "QuickFix — Smart Campus Issue Management"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F1F5F9"
    page.padding = 0

    # Initialize Services
    storage = StorageService()
    notifications = NotificationService()

    # Session / Local Storage Check
    saved_session = storage.get_session()
    is_logged_in = [saved_session is not None and saved_session.get("logged_in", False)]
    current_role = [saved_session.get("role", "Student") if is_logged_in[0] else "Student"]
    current_user = [saved_session if is_logged_in[0] else None]

    # App State
    selected_index = [3 if current_role[0] == "Admin" else 0] # 0: Home, 1: Report, 2: My Issues, 3: Admin, 4: Profile
    viewing_issue = [None]                                     # If not None, renders IssueDetailsView

    # Notification Listener
    def on_new_notification(notif):
        if is_logged_in[0]:
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

    # Login / Logout Handlers
    def handle_login_success(role: str, user_data: dict):
        is_logged_in[0] = True
        current_role[0] = role
        current_user[0] = user_data
        viewing_issue[0] = None

        if role == "Admin":
            selected_index[0] = 3
            nav_bar.selected_index = 3
        else:
            selected_index[0] = 0
            nav_bar.selected_index = 0

        render_content()

    def handle_logout():
        storage.clear_session()
        is_logged_in[0] = False
        current_user[0] = None
        viewing_issue[0] = None
        render_content()
        page.show_dialog(
            ft.SnackBar(content="You have signed out successfully.", bgcolor="#475569", open=True)
        )

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
        user_data = current_user[0] or {}
        user_data["role"] = new_role
        storage.save_session(user_data)
        if new_role == "Admin":
            selected_index[0] = 3
            nav_bar.selected_index = 3
        else:
            selected_index[0] = 0
            nav_bar.selected_index = 0
        render_content()

    # Content Area Container
    content_area = ft.Container(expand=True)

    # Top App Bar Widgets
    role_badge_text = ft.Text(current_role[0], size=11, color="#FFFFFF", weight=ft.FontWeight.BOLD)
    role_badge_container = ft.Container(
        content=role_badge_text,
        padding=ft.Padding(8, 2, 8, 2),
        border_radius=10,
        bgcolor="#7C3AED" if current_role[0] == "Admin" else "#3B82F6"
    )

    top_app_bar = ft.Container(
        visible=is_logged_in[0],
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
                    spacing=6,
                    controls=[
                        role_badge_container,
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT_ROUNDED,
                            icon_color="#93C5FD",
                            icon_size=18,
                            tooltip="Sign Out",
                            on_click=lambda _: handle_logout()
                        )
                    ]
                )
            ]
        )
    )

    # Bottom Navigation Bar
    nav_bar = ft.NavigationBar(
        visible=is_logged_in[0],
        selected_index=selected_index[0],
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
        if not is_logged_in[0]:
            top_app_bar.visible = False
            nav_bar.visible = False
            content_area.content = LoginView(
                storage=storage,
                page=page,
                on_login_success=handle_login_success
            ).build()
        else:
            top_app_bar.visible = True
            nav_bar.visible = True
            role_badge_text.value = current_role[0]
            role_badge_container.bgcolor = "#7C3AED" if current_role[0] == "Admin" else "#3B82F6"

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
                    on_role_change=on_role_switched,
                    on_logout=handle_logout
                ).build()

        page.update()

    # Mobile Shell Container
    phone_frame = ft.Container(
        expand=True,
        bgcolor="#F8FAFC",
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                top_app_bar,
                content_area,
                nav_bar
            ]
        )
    )

    # Responsive layout: full width on mobile devices, centered mockup on desktop
    is_mobile = False
    try:
        if hasattr(page, "platform") and page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]:
            is_mobile = True
        elif hasattr(page, "client_user_agent") and page.client_user_agent:
            ua = str(page.client_user_agent).lower()
            if "android" in ua or "iphone" in ua or "mobile" in ua:
                is_mobile = True
    except Exception:
        pass

    if is_mobile:
        app_wrapper = ft.SafeArea(
            expand=True,
            content=phone_frame
        )
    else:
        app_wrapper = ft.SafeArea(
            expand=True,
            content=ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                bgcolor="#E2E8F0",
                content=ft.Container(
                    width=440,
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
