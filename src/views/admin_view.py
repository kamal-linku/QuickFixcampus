import flet as ft
from services.storage_service import StorageService
from services.notification_service import NotificationService
from models.issue import Issue, IssueStatus, PriorityLevel
from views.components import get_category_icon, build_priority_badge, build_status_badge

class AdminView:
    def __init__(self, storage: StorageService, notifications: NotificationService, page: ft.Page, on_open_issue):
        self.storage = storage
        self.notifications = notifications
        self.page = page
        self.on_open_issue = on_open_issue

    def build(self) -> ft.Control:
        stats = self.storage.get_stats()
        issues = self.storage.get_all()

        # Admin Header
        header = ft.Container(
            padding=ft.Padding(16, 14, 16, 8),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Text("QUICKFIX ADMIN", size=18, weight=ft.FontWeight.W_900, color="#1E3A8A"),
                                    ft.Container(
                                        content=ft.Text("STAFF MODE", size=10, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                                        padding=ft.Padding(6, 2, 6, 2),
                                        bgcolor="#DBEAFE",
                                        border_radius=6
                                    )
                                ]
                            ),
                            ft.Text("Campus Maintenance & Dispatch Center", size=12, color="#64748B")
                        ]
                    ),
                    ft.IconButton(
                        icon=ft.Icons.REFRESH_ROUNDED,
                        icon_color="#1E3A8A",
                        on_click=lambda _: self.page.update()
                    )
                ]
            )
        )

        # Campus Overview Stats 2x2 Grid (Pages 16 & 17)
        overview_card = ft.Container(
            margin=ft.Margin(16, 4, 16, 12),
            padding=16,
            border_radius=16,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E2E8F0"),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text("Campus Overview", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Row(
                        spacing=10,
                        controls=[
                            self._build_stat_box(str(stats["total"]), "Total Reports", "#1E3A8A", "#EFF6FF"),
                            self._build_stat_box(str(stats["pending"] + stats["verified"]), "Pending Action", "#EA580C", "#FFF7ED")
                        ]
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                            self._build_stat_box(str(stats["in_progress"]), "In Progress", "#2563EB", "#EFF6FF"),
                            self._build_stat_box(str(stats["resolved"]), "Resolved", "#16A34A", "#F0FDF4")
                        ]
                    )
                ]
            )
        )

        # Quick Status Update Action Center (Page 24)
        def advance_status(issue_id: str, new_status: str):
            self.storage.update_status(issue_id, new_status, f"Admin marked as {new_status}")
            self.notifications.notify_status_change(issue_id, new_status)
            self.page.show_dialog(
                ft.SnackBar(content=f"🔔 Issue #{issue_id} status updated to {new_status}!", bgcolor="#1E3A8A", open=True)
            )
            self.page.update()

        action_items = []
        for issue in issues[:5]:
            # Determine next action button
            btn_content = None
            if issue.status == IssueStatus.SUBMITTED:
                btn_content = ft.FilledButton(
                    content=ft.Text("Verify", size=11, color="#FFFFFF"),
                    style=ft.ButtonStyle(bgcolor="#7C3AED", shape=ft.RoundedRectangleBorder(radius=8), padding=ft.Padding(10, 6, 10, 6)),
                    on_click=lambda _, iid=issue.id: advance_status(iid, IssueStatus.VERIFIED)
                )
            elif issue.status == IssueStatus.VERIFIED:
                btn_content = ft.FilledButton(
                    content=ft.Text("Start Work", size=11, color="#FFFFFF"),
                    style=ft.ButtonStyle(bgcolor="#2563EB", shape=ft.RoundedRectangleBorder(radius=8), padding=ft.Padding(10, 6, 10, 6)),
                    on_click=lambda _, iid=issue.id: advance_status(iid, IssueStatus.IN_PROGRESS)
                )
            elif issue.status == IssueStatus.IN_PROGRESS:
                btn_content = ft.FilledButton(
                    content=ft.Text("Resolve", size=11, color="#FFFFFF"),
                    style=ft.ButtonStyle(bgcolor="#16A34A", shape=ft.RoundedRectangleBorder(radius=8), padding=ft.Padding(10, 6, 10, 6)),
                    on_click=lambda _, iid=issue.id: advance_status(iid, IssueStatus.RESOLVED)
                )

            item_row = ft.Container(
                padding=10,
                border_radius=12,
                bgcolor="#F8FAFC",
                border=ft.Border.all(1, "#F1F5F9"),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Row(
                                    spacing=6,
                                    controls=[
                                        ft.Text(f"#{issue.id}", size=12, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                                        build_priority_badge(issue.priority)
                                    ]
                                ),
                                ft.Text(issue.title, size=12, weight=ft.FontWeight.W_600, color="#1E293B", max_lines=1),
                                ft.Text(f"{issue.location} • {issue.category}", size=11, color="#64748B")
                            ]
                        ),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            spacing=4,
                            controls=[
                                build_status_badge(issue.status),
                                btn_content if btn_content else ft.Container()
                            ]
                        )
                    ]
                )
            )
            action_items.append(item_row)

        action_center_card = ft.Container(
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
                            ft.Text("Admin Action Center", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            ft.Text("Tap button to advance status", size=11, color="#64748B")
                        ]
                    ),
                    *action_items
                ]
            )
        )

        # Analytics: Category Distribution Bars (Page 17)
        cat_counts = stats["categories"]
        cat_bars = []
        max_cat = max(cat_counts.values()) if cat_counts else 1

        for cat_name, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
            pct = count / max(max_cat, 1)
            cat_bars.append(
                ft.Column(
                    spacing=3,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=6,
                                    controls=[
                                        ft.Icon(get_category_icon(cat_name), size=14, color="#1E3A8A"),
                                        ft.Text(cat_name, size=12, weight=ft.FontWeight.W_500, color="#1E293B")
                                    ]
                                ),
                                ft.Text(f"{count} issues", size=11, weight=ft.FontWeight.BOLD, color="#64748B")
                            ]
                        ),
                        ft.ProgressBar(value=pct, color="#2563EB", bgcolor="#E2E8F0", height=8, border_radius=4)
                    ]
                )
            )

        analytics_card = ft.Container(
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
                            ft.Text("Issues by Category", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            ft.Icon(ft.Icons.BAR_CHART_ROUNDED, color="#2563EB", size=20)
                        ]
                    ),
                    *cat_bars
                ]
            )
        )

        # Campus Problem Heatmap (Page 28)
        heatmap_locations = [
            ("Library Block", "🔴 High Priority (3 issues)", "#DC2626"),
            ("CSE Block", "🔴 Critical Hazard (2 issues)", "#DC2626"),
            ("Hostel B", "🟠 Flooding Risk (2 issues)", "#EA580C"),
            ("Cafeteria", "🟡 Moderate Network (1 issue)", "#D97706"),
            ("Main Gate", "🟢 Maintenance Clear (Resolved)", "#16A34A")
        ]

        heatmap_items = []
        for loc_name, tag, col in heatmap_locations:
            heatmap_items.append(
                ft.Container(
                    padding=10,
                    border_radius=10,
                    bgcolor="#F8FAFC",
                    border=ft.Border.all(1, "#E2E8F0"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Container(width=10, height=10, border_radius=5, bgcolor=col),
                                    ft.Text(loc_name, size=12, weight=ft.FontWeight.BOLD, color="#1E293B")
                                ]
                            ),
                            ft.Text(tag, size=11, color=col, weight=ft.FontWeight.W_600)
                        ]
                    )
                )
            )

        heatmap_card = ft.Container(
            margin=ft.Margin(16, 0, 16, 24),
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
                            ft.Text("Campus Problem Heatmap", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            ft.Icon(ft.Icons.MAP_ROUNDED, color="#DC2626", size=18)
                        ]
                    ),
                    ft.Text("Live trouble hotspot indicators across campus facilities:", size=11, color="#64748B"),
                    *heatmap_items
                ]
            )
        )

        return ft.ListView(
            expand=True,
            spacing=0,
            controls=[
                header,
                overview_card,
                action_center_card,
                analytics_card,
                heatmap_card,
                ft.Container(height=30)
            ]
        )

    def _build_stat_box(self, number: str, label: str, color: str, bgcolor: str) -> ft.Container:
        return ft.Container(
            expand=1,
            padding=12,
            border_radius=12,
            bgcolor=bgcolor,
            border=ft.Border.all(1, f"{color}33"),
            content=ft.Column(
                spacing=2,
                controls=[
                    ft.Text(number, size=22, weight=ft.FontWeight.W_900, color=color),
                    ft.Text(label, size=11, color="#64748B", weight=ft.FontWeight.W_500)
                ]
            )
        )
