import flet as ft
from models.issue import IssueStatus, PriorityLevel

def get_category_icon(category: str) -> ft.IconData:
    mapping = {
        "Electrical": ft.Icons.LIGHTBULB,
        "Water": ft.Icons.WATER_DROP,
        "Cleanliness": ft.Icons.CLEANING_SERVICES,
        "Infrastructure": ft.Icons.CONSTRUCTION,
        "Network": ft.Icons.WIFI,
        "Sanitation": ft.Icons.WASH,
        "Equipment": ft.Icons.DEVICES,
        "Other": ft.Icons.WARNING_AMBER_ROUNDED
    }
    return mapping.get(category, ft.Icons.ERROR_OUTLINE)

def get_priority_color(priority: str) -> str:
    mapping = {
        PriorityLevel.CRITICAL: "#DC2626", # Red
        PriorityLevel.HIGH: "#EA580C",     # Orange
        PriorityLevel.MEDIUM: "#D97706",   # Amber
        PriorityLevel.LOW: "#16A34A"       # Green
    }
    return mapping.get(priority, "#64748B")

def get_status_color(status: str) -> str:
    mapping = {
        IssueStatus.SUBMITTED: "#64748B",   # Slate / Blue Grey
        IssueStatus.VERIFIED: "#7C3AED",    # Purple
        IssueStatus.IN_PROGRESS: "#2563EB", # Blue
        IssueStatus.RESOLVED: "#10B981"     # Emerald Green
    }
    return mapping.get(status, "#64748B")

def build_priority_badge(priority: str) -> ft.Container:
    color = get_priority_color(priority)
    return ft.Container(
        content=ft.Row(
            spacing=4,
            controls=[
                ft.Container(width=8, height=8, border_radius=4, bgcolor=color),
                ft.Text(priority, size=11, weight=ft.FontWeight.W_700, color=color)
            ]
        ),
        padding=ft.Padding(8, 4, 8, 4),
        border_radius=12,
        bgcolor=f"{color}18", # 10% opacity
        border=ft.Border.all(1, f"{color}44")
    )

def build_status_badge(status: str) -> ft.Container:
    color = get_status_color(status)
    display_text = status.replace("_", " ")
    return ft.Container(
        content=ft.Text(display_text, size=11, weight=ft.FontWeight.BOLD, color=color),
        padding=ft.Padding(8, 4, 8, 4),
        border_radius=12,
        bgcolor=f"{color}18",
        border=ft.Border.all(1, f"{color}44")
    )

def build_timeline_widget(timeline: list) -> ft.Container:
    steps = [
        ("SUBMITTED", "Submitted", ft.Icons.SEND),
        ("VERIFIED", "Verified", ft.Icons.VERIFIED_OUTLINED),
        ("IN_PROGRESS", "In Progress", ft.Icons.BUILD_OUTLINED),
        ("RESOLVED", "Resolved", ft.Icons.CHECK_CIRCLE)
    ]

    time_map = {}
    note_map = {}
    completed_map = {}
    for item in timeline:
        st = item.get("status")
        time_map[st] = item.get("timestamp", "")
        note_map[st] = item.get("note", "")
        completed_map[st] = item.get("completed", False)

    controls = []
    for i, (st_code, label, icon) in enumerate(steps):
        is_done = completed_map.get(st_code, False)
        t_str = time_map.get(st_code, "")
        n_str = note_map.get(st_code, "")
        color = "#10B981" if is_done else "#CBD5E1"
        text_color = "#1E293B" if is_done else "#94A3B8"

        step_col = ft.Column(
            spacing=2,
            controls=[
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.Icon(icon, size=18, color=color),
                        ft.Text(label, weight=ft.FontWeight.BOLD if is_done else ft.FontWeight.NORMAL, color=text_color, size=13),
                        ft.Text(f"• {t_str}" if t_str else "", size=11, color="#64748B", italic=True)
                    ]
                ),
                ft.Container(
                    padding=ft.Padding(left=26, top=0, right=0, bottom=0),
                    content=ft.Text(n_str, size=11, color="#64748B")
                ) if n_str else ft.Container()
            ]
        )

        controls.append(step_col)
        if i < len(steps) - 1:
            controls.append(
                ft.Container(
                    margin=ft.Margin(left=8, top=2, right=0, bottom=2),
                    width=2,
                    height=18,
                    bgcolor="#10B981" if is_done else "#E2E8F0"
                )
            )

    return ft.Container(
        content=ft.Column(spacing=2, controls=controls),
        padding=12,
        bgcolor="#F8FAFC",
        border_radius=12,
        border=ft.Border.all(1, "#E2E8F0")
    )
