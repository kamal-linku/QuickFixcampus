import flet as ft
from models.issue import Issue, IssueStatus
from services.storage_service import StorageService
from services.notification_service import NotificationService
from views.components import get_category_icon, build_priority_badge, build_status_badge, build_timeline_widget

class IssueDetailsView:
    def __init__(self, issue: Issue, storage: StorageService, notifications: NotificationService, page: ft.Page, on_back, on_updated=None):
        self.issue = issue
        self.storage = storage
        self.notifications = notifications
        self.page = page
        self.on_back = on_back
        self.on_updated = on_updated

    def build(self) -> ft.Control:
        # Header with back button
        header = ft.Container(
            padding=ft.Padding(16, 12, 16, 12),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                        icon_size=18,
                        on_click=lambda _: self.on_back()
                    ),
                    ft.Text(f"Issue #{self.issue.id}", size=16, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    build_status_badge(self.issue.status)
                ]
            )
        )

        # Overview Card
        overview_card = ft.Container(
            margin=ft.Margin(16, 0, 16, 12),
            padding=16,
            border_radius=16,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E2E8F0"),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Column(
                                expand=True,
                                spacing=4,
                                controls=[
                                    ft.Text(self.issue.title, size=18, weight=ft.FontWeight.BOLD, color="#0F172A"),
                                    ft.Row(
                                        spacing=4,
                                        controls=[
                                            ft.Icon(ft.Icons.LOCATION_ON, size=14, color="#EF4444"),
                                            ft.Text(self.issue.location, size=13, color="#475569", weight=ft.FontWeight.W_500)
                                        ]
                                    )
                                ]
                            ),
                            build_priority_badge(self.issue.priority)
                        ]
                    ),
                    ft.Divider(height=1, color="#F1F5F9"),
                    ft.Row(
                        spacing=12,
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.Icon(get_category_icon(self.issue.category), size=14, color="#1E3A8A"),
                                        ft.Text(self.issue.category, size=11, weight=ft.FontWeight.BOLD, color="#1E3A8A")
                                    ]
                                ),
                                bgcolor="#EFF6FF",
                                padding=ft.Padding(8, 4, 8, 4),
                                border_radius=8
                            ),
                            ft.Container(
                                content=ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.Icon(ft.Icons.ANALYTICS_OUTLINED, size=14, color="#92400E"),
                                        ft.Text(f"Priority Score: {self.issue.priority_score}", size=11, weight=ft.FontWeight.BOLD, color="#92400E")
                                    ]
                                ),
                                bgcolor="#FEF3C7",
                                padding=ft.Padding(8, 4, 8, 4),
                                border_radius=8
                            )
                        ]
                    ),
                    ft.Text(self.issue.description, size=13, color="#334155"),
                    ft.Container(
                        padding=10,
                        border_radius=8,
                        bgcolor="#F8FAFC",
                        content=ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(ft.Icons.INFO_OUTLINE, size=14, color="#64748B"),
                                ft.Text(f"Smart Analysis: {self.issue.priority_reason}", size=11, color="#64748B", italic=True)
                            ]
                        )
                    )
                ]
            )
        )

        # Photo Evidence Card
        photo_card = ft.Container()
        if self.issue.image:
            photo_card = ft.Container(
                margin=ft.Margin(16, 0, 16, 12),
                padding=12,
                border_radius=16,
                bgcolor="#FFFFFF",
                border=ft.Border.all(1, "#E2E8F0"),
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("Photo Evidence", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                        ft.Image(
                            src=self.issue.image,
                            width=360,
                            height=180,
                            fit="cover",
                            border_radius=10
                        )
                    ]
                )
            )

        # Timeline Card (Pages 15 & 16)
        timeline_card = ft.Container(
            margin=ft.Margin(16, 0, 16, 12),
            padding=16,
            border_radius=16,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E2E8F0"),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Live Resolution Timeline", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            ft.Icon(ft.Icons.TIMELINE, color="#2563EB", size=18)
                        ]
                    ),
                    build_timeline_widget(self.issue.timeline)
                ]
            )
        )

        # Quick Status Update Action for Demonstration / Admin
        next_status_map = {
            IssueStatus.SUBMITTED: (IssueStatus.VERIFIED, "Mark as Verified", "#7C3AED"),
            IssueStatus.VERIFIED: (IssueStatus.IN_PROGRESS, "Mark as In Progress", "#2563EB"),
            IssueStatus.IN_PROGRESS: (IssueStatus.RESOLVED, "Mark as Resolved", "#10B981"),
            IssueStatus.RESOLVED: (None, "Issue Resolved", "#64748B")
        }

        next_st, next_label, next_color = next_status_map.get(self.issue.status, (None, "", ""))

        def handle_advance_status(e):
            if next_st:
                updated = self.storage.update_status(self.issue.id, next_st, f"Status updated to {next_st}")
                if updated:
                    self.issue = updated
                    self.notifications.notify_status_change(self.issue.id, next_st)
                    if self.on_updated:
                        self.on_updated(self.issue)
                    self.page.show_dialog(
                        ft.SnackBar(content=f"🔔 Issue #{self.issue.id} marked as {next_st}!", bgcolor=next_color, open=True)
                    )
                    self.on_back()

        action_container = ft.Container()
        if next_st:
            action_container = ft.Container(
                margin=ft.Margin(16, 0, 16, 24),
                content=ft.FilledButton(
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.UPDATE_ROUNDED, color="#FFFFFF", size=18),
                            ft.Text(f"Admin Action: {next_label}", weight=ft.FontWeight.BOLD, size=13, color="#FFFFFF")
                        ]
                    ),
                    style=ft.ButtonStyle(
                        bgcolor=next_color,
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.Padding(16, 14, 16, 14)
                    ),
                    on_click=handle_advance_status
                )
            )

        return ft.ListView(
            expand=True,
            spacing=0,
            controls=[
                header,
                overview_card,
                photo_card,
                timeline_card,
                action_container,
                ft.Container(height=30)
            ]
        )
