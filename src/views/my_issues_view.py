import flet as ft
from services.storage_service import StorageService
from models.issue import Issue, IssueStatus
from views.components import get_category_icon, build_priority_badge, build_status_badge, build_timeline_widget

class MyIssuesView:
    def __init__(self, storage: StorageService, page: ft.Page, on_open_issue):
        self.storage = storage
        self.page = page
        self.on_open_issue = on_open_issue
        self.active_filter = "ALL"
        self.search_query = ""

    def build(self) -> ft.Control:
        all_issues = self.storage.get_all()

        # Filter buttons
        filter_chips = []
        filter_options = [
            ("ALL", "All"),
            (IssueStatus.SUBMITTED, "Submitted"),
            (IssueStatus.VERIFIED, "Verified"),
            (IssueStatus.IN_PROGRESS, "In Progress"),
            (IssueStatus.RESOLVED, "Resolved")
        ]

        def set_filter(f_val):
            self.active_filter = f_val
            self.refresh_list()

        for code, label in filter_options:
            is_active = (self.active_filter == code)
            btn = ft.Container(
                content=ft.Text(
                    label,
                    size=12,
                    weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,
                    color="#FFFFFF" if is_active else "#475569"
                ),
                bgcolor="#1E3A8A" if is_active else "#F1F5F9",
                border=ft.Border.all(1, "#1E3A8A" if is_active else "#E2E8F0"),
                border_radius=20,
                padding=ft.Padding(12, 6, 12, 6),
                on_click=lambda _, val=code: set_filter(val)
            )
            filter_chips.append(btn)

        filter_row = ft.Container(
            padding=ft.Padding(16, 4, 16, 8),
            content=ft.Row(
                spacing=8,
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=filter_chips
            )
        )

        # Search Bar
        search_field = ft.TextField(
            hint_text="Search issue by ID, title, or location...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=12,
            border_color="#CBD5E1",
            content_padding=12,
            text_size=12,
            on_change=lambda e: self.update_search(e.control.value)
        )

        search_container = ft.Container(
            padding=ft.Padding(16, 4, 16, 8),
            content=search_field
        )

        self.list_container = ft.Column(spacing=8)
        self.refresh_list()

        return ft.ListView(
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    padding=ft.Padding(16, 14, 16, 4),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text("Track Issues", size=20, weight=ft.FontWeight.BOLD, color="#0F172A"),
                                    ft.Text("Live timeline & status updates", size=12, color="#64748B")
                                ]
                            ),
                            ft.Container(
                                content=ft.Text(f"{len(all_issues)} Reports", size=11, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                                padding=ft.Padding(8, 4, 8, 4),
                                bgcolor="#EFF6FF",
                                border_radius=8
                            )
                        ]
                    )
                ),
                search_container,
                filter_row,
                ft.Container(
                    padding=ft.Padding(16, 4, 16, 24),
                    content=self.list_container
                )
            ]
        )

    def update_search(self, val: str):
        self.search_query = val.lower().strip()
        self.refresh_list()

    def refresh_list(self):
        issues = self.storage.get_all()
        # Filter by status
        if self.active_filter != "ALL":
            issues = [i for i in issues if i.status == self.active_filter]

        # Filter by query
        if self.search_query:
            issues = [
                i for i in issues if
                self.search_query in i.id.lower() or
                self.search_query in i.title.lower() or
                self.search_query in i.location.lower() or
                self.search_query in i.category.lower()
            ]

        self.list_container.controls.clear()

        if not issues:
            self.list_container.controls.append(
                ft.Container(
                    padding=40,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.SEARCH_OFF_ROUNDED, size=40, color="#94A3B8"),
                            ft.Text("No reports found", size=14, weight=ft.FontWeight.BOLD, color="#64748B"),
                            ft.Text("Try adjusting your filters or submit a new problem.", size=12, color="#94A3B8")
                        ]
                    )
                )
            )
        else:
            for issue in issues:
                card = ft.Container(
                    padding=14,
                    border_radius=16,
                    bgcolor="#FFFFFF",
                    border=ft.Border.all(1, "#E2E8F0"),
                    on_click=lambda _, iss=issue: self.on_open_issue(iss),
                    content=ft.Column(
                        spacing=10,
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
                                                    ft.Text(f"Ticket #{issue.id} • {issue.category}", size=11, color="#64748B")
                                                ]
                                            )
                                        ]
                                    ),
                                    build_priority_badge(issue.priority)
                                ]
                            ),
                            ft.Row(
                                spacing=4,
                                controls=[
                                    ft.Icon(ft.Icons.LOCATION_ON, size=14, color="#EF4444"),
                                    ft.Text(issue.location, size=12, color="#475569", weight=ft.FontWeight.W_500)
                                ]
                            ),
                            ft.Text(issue.description, size=11, color="#64748B", max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Divider(height=1, color="#F1F5F9"),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        spacing=4,
                                        controls=[
                                            ft.Icon(ft.Icons.CALENDAR_TODAY, size=11, color="#94A3B8"),
                                            ft.Text(issue.created_at[:10], size=11, color="#94A3B8")
                                        ]
                                    ),
                                    build_status_badge(issue.status)
                                ]
                            )
                        ]
                    )
                )
                self.list_container.controls.append(card)

        if hasattr(self.page, "update"):
            self.page.update()
