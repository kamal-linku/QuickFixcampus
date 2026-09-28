import flet as ft
from services.storage_service import StorageService
from views.components import get_category_icon, build_priority_badge, build_status_badge

class HomeView:
    def __init__(self, storage: StorageService, on_navigate, on_open_issue):
        self.storage = storage
        self.on_navigate = on_navigate
        self.on_open_issue = on_open_issue

    def build(self) -> ft.Control:
        stats = self.storage.get_stats()
        recent_issues = self.storage.get_all()[:4]

        # Greeting Header
        header = ft.Container(
            padding=ft.Padding(16, 16, 16, 8),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Text("Hello, Student", size=20, weight=ft.FontWeight.BOLD, color="#0F172A"),
                                    ft.Text("👋", size=20)
                                ]
                            ),
                            ft.Text("Make your campus safer and better", size=13, color="#64748B")
                        ]
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE_OUTLINED, color="#1D4ED8", size=22),
                        padding=8,
                        border_radius=20,
                        bgcolor="#EFF6FF",
                        border=ft.Border.all(1, "#DBEAFE"),
                        on_click=lambda _: self.on_navigate(4) # Navigate to Profile/Notifs
                    )
                ]
            )
        )

        # Hero Action Card (Pages 7 & 8)
        hero_card = ft.Container(
            margin=ft.Margin(16, 4, 16, 12),
            padding=20,
            border_radius=18,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=["#1E3A8A", "#2563EB", "#3B82F6"]
            ),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.Icon(ft.Icons.BOLT, color="#FDE047", size=16),
                                        ft.Text("FAST CAMPUS RESPONSE", size=11, weight=ft.FontWeight.BOLD, color="#FDE047")
                                    ]
                                ),
                                padding=ft.Padding(8, 4, 8, 4),
                                border_radius=12,
                                bgcolor="#FFFFFF20"
                            ),
                            ft.Text("QuickFix v1.0", size=11, color="#E0E7FF")
                        ]
                    ),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("REPORT A PROBLEM", size=19, weight=ft.FontWeight.W_900, color="#FFFFFF"),
                            ft.Text("Report in less than 30 seconds with automatic priority calculation and smart categorization.", size=12, color="#DBEAFE")
                        ]
                    ),
                    ft.FilledButton(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.ADD_LOCATION_ALT_ROUNDED, color="#1E3A8A", size=18),
                                ft.Text("+ REPORT CAMPUS ISSUE", weight=ft.FontWeight.BOLD, color="#1E3A8A", size=13)
                            ]
                        ),
                        style=ft.ButtonStyle(
                            bgcolor="#FFFFFF",
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=ft.Padding(16, 14, 16, 14)
                        ),
                        on_click=lambda _: self.on_navigate(1) # Navigate to Report screen
                    )
                ]
            )
        )

        # My Issues Quick Stats Cards (Page 8)
        stats_row = ft.Container(
            padding=ft.Padding(16, 0, 16, 12),
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Container(
                        expand=1,
                        padding=14,
                        border_radius=16,
                        bgcolor="#FFFFFF",
                        border=ft.Border.all(1, "#E2E8F0"),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(str(stats["total"]), size=24, weight=ft.FontWeight.W_900, color="#1E3A8A"),
                                        ft.Text("Total Reports", size=12, color="#64748B", weight=ft.FontWeight.W_500)
                                    ]
                                ),
                                ft.Container(
                                    content=ft.Icon(ft.Icons.REPORT_GMAILERRORRED_ROUNDED, color="#2563EB", size=24),
                                    padding=10,
                                    border_radius=12,
                                    bgcolor="#EFF6FF"
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        expand=1,
                        padding=14,
                        border_radius=16,
                        bgcolor="#FFFFFF",
                        border=ft.Border.all(1, "#E2E8F0"),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(f"{stats['resolved']:02d}", size=24, weight=ft.FontWeight.W_900, color="#16A34A"),
                                        ft.Text("Resolved", size=12, color="#64748B", weight=ft.FontWeight.W_500)
                                    ]
                                ),
                                ft.Container(
                                    content=ft.Icon(ft.Icons.TASK_ALT_ROUNDED, color="#16A34A", size=24),
                                    padding=10,
                                    border_radius=12,
                                    bgcolor="#F0FDF4"
                                )
                            ]
                        )
                    )
                ]
            )
        )

        # Smart Engine Highlight Banner
        smart_banner = ft.Container(
            margin=ft.Margin(16, 0, 16, 14),
            padding=12,
            border_radius=14,
            bgcolor="#F0FDF4",
            border=ft.Border.all(1, "#BBF7D0"),
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Icon(ft.Icons.AUTO_AWESOME, color="#16A34A", size=22),
                    ft.Column(
                        expand=True,
                        spacing=1,
                        controls=[
                            ft.Text("QuickFix SmartAssist Active", size=12, weight=ft.FontWeight.BOLD, color="#15803D"),
                            ft.Text("AI auto-categorization & duplicate warning enabled", size=11, color="#166534")
                        ]
                    )
                ]
            )
        )

        # Recent Reports Section Header
        recent_header = ft.Container(
            padding=ft.Padding(16, 4, 16, 6),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("Recent Reports", size=16, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.TextButton(
                        content=ft.Text("View All", size=12, weight=ft.FontWeight.BOLD, color="#2563EB"),
                        on_click=lambda _: self.on_navigate(2) # My Issues
                    )
                ]
            )
        )

        # Recent Reports Cards List
        recent_items = []
        for issue in recent_issues:
            card = ft.Container(
                margin=ft.Margin(16, 4, 16, 6),
                padding=14,
                border_radius=16,
                bgcolor="#FFFFFF",
                border=ft.Border.all(1, "#E2E8F0"),
                on_click=lambda _, iss=issue: self.on_open_issue(iss),
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Container(
                                            content=ft.Icon(get_category_icon(issue.category), color="#1E3A8A", size=18),
                                            padding=6,
                                            border_radius=8,
                                            bgcolor="#EFF6FF"
                                        ),
                                        ft.Column(
                                            spacing=1,
                                            controls=[
                                                ft.Text(issue.title, size=13, weight=ft.FontWeight.BOLD, color="#0F172A", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                                ft.Row(
                                                    spacing=4,
                                                    controls=[
                                                        ft.Icon(ft.Icons.LOCATION_ON, size=12, color="#EF4444"),
                                                        ft.Text(issue.location, size=11, color="#64748B")
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                build_priority_badge(issue.priority)
                            ]
                        ),
                        ft.Divider(height=1, color="#F1F5F9"),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Ticket #{issue.id}", size=11, color="#94A3B8", weight=ft.FontWeight.W_500),
                                build_status_badge(issue.status)
                            ]
                        )
                    ]
                )
            )
            recent_items.append(card)

        return ft.ListView(
            expand=True,
            spacing=0,
            controls=[
                header,
                hero_card,
                stats_row,
                smart_banner,
                recent_header,
                *recent_items,
                ft.Container(height=24)
            ]
        )
