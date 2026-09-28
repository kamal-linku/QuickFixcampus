import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from models.issue import Issue, IssueStatus, PriorityLevel

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "quickfix_data.json")

DEMO_ISSUES = [
    {
        "id": "QF1024",
        "title": "Broken Street Light",
        "description": "Street light near library is not working since yesterday.",
        "category": "Electrical",
        "location": "Library Block",
        "latitude": 20.2961,
        "longitude": 85.8245,
        "severity": "HIGH",
        "impact": "HIGH",
        "priority": PriorityLevel.HIGH,
        "priority_score": 18,
        "priority_reason": "High campus traffic area at night; safety hazard",
        "status": IssueStatus.IN_PROGRESS,
        "image": "https://picsum.photos/seed/light1024/400/250",
        "reporter": "student@quickfix.demo",
        "created_at": "2026-09-27 10:42:00",
        "updated_at": "2026-09-27 14:30:00",
        "timeline": [
            {"status": IssueStatus.SUBMITTED, "timestamp": "27 Sep, 10:42 AM", "note": "Reported via QuickFix App by Student", "completed": True},
            {"status": IssueStatus.VERIFIED, "timestamp": "27 Sep, 11:10 AM", "note": "Verified by Campus Maintenance Officer", "completed": True},
            {"status": IssueStatus.IN_PROGRESS, "timestamp": "27 Sep, 02:30 PM", "note": "Electrician team dispatched with replacement fixture", "completed": True},
            {"status": IssueStatus.RESOLVED, "timestamp": "", "note": "Awaiting final testing and closure", "completed": False}
        ]
    },
    {
        "id": "QF1025",
        "title": "Exposed Electrical Wire",
        "description": "Exposed electrical wire hanging near CSE lab entrance. Sparks visible!",
        "category": "Electrical",
        "location": "CSE Block",
        "latitude": 20.2975,
        "longitude": 85.8258,
        "severity": "CRITICAL",
        "impact": "HIGH",
        "priority": PriorityLevel.CRITICAL,
        "priority_score": 25,
        "priority_reason": "Immediate risk of electric shock to students entering lab",
        "status": IssueStatus.SUBMITTED,
        "image": "https://picsum.photos/seed/wire1025/400/250",
        "reporter": "student@quickfix.demo",
        "created_at": "2026-09-28 08:30:00",
        "updated_at": "2026-09-28 08:30:00",
        "timeline": [
            {"status": IssueStatus.SUBMITTED, "timestamp": "28 Sep, 08:30 AM", "note": "Emergency alert received - flagged as CRITICAL", "completed": True},
            {"status": IssueStatus.VERIFIED, "timestamp": "", "note": "Pending verification", "completed": False},
            {"status": IssueStatus.IN_PROGRESS, "timestamp": "", "note": "Pending technician assignment", "completed": False},
            {"status": IssueStatus.RESOLVED, "timestamp": "", "note": "Pending fix", "completed": False}
        ]
    },
    {
        "id": "QF1026",
        "title": "Major Water Pipe Leakage",
        "description": "Water leaking rapidly from pipe near ground floor corridor, flooding floor.",
        "category": "Water",
        "location": "Hostel B",
        "latitude": 20.2940,
        "longitude": 85.8230,
        "severity": "HIGH",
        "impact": "MEDIUM",
        "priority": PriorityLevel.HIGH,
        "priority_score": 16,
        "priority_reason": "Water flooding risk and water wastage in residential hostel",
        "status": IssueStatus.IN_PROGRESS,
        "image": "https://picsum.photos/seed/water1026/400/250",
        "reporter": "student@quickfix.demo",
        "created_at": "2026-09-27 16:15:00",
        "updated_at": "2026-09-28 07:45:00",
        "timeline": [
            {"status": IssueStatus.SUBMITTED, "timestamp": "27 Sep, 04:15 PM", "note": "Reported by hostel resident", "completed": True},
            {"status": IssueStatus.VERIFIED, "timestamp": "27 Sep, 05:00 PM", "note": "Hostel warden confirmed leak", "completed": True},
            {"status": IssueStatus.IN_PROGRESS, "timestamp": "28 Sep, 07:45 AM", "note": "Plumber arrived, main valve temporarily shut", "completed": True},
            {"status": IssueStatus.RESOLVED, "timestamp": "", "note": "Repair underway", "completed": False}
        ]
    },
    {
        "id": "QF1027",
        "title": "Cafeteria Wi-Fi Access Point Offline",
        "description": "WiFi signal not transmitting in seating area, cannot connect.",
        "category": "Network",
        "location": "Cafeteria",
        "latitude": 20.2952,
        "longitude": 85.8265,
        "severity": "MEDIUM",
        "impact": "HIGH",
        "priority": PriorityLevel.MEDIUM,
        "priority_score": 8,
        "priority_reason": "High student traffic area; router reboot required",
        "status": IssueStatus.VERIFIED,
        "image": "https://picsum.photos/seed/wifi1027/400/250",
        "reporter": "guest@quickfix.demo",
        "created_at": "2026-09-28 09:10:00",
        "updated_at": "2026-09-28 09:30:00",
        "timeline": [
            {"status": IssueStatus.SUBMITTED, "timestamp": "28 Sep, 09:10 AM", "note": "Reported by student during lunch hour", "completed": True},
            {"status": IssueStatus.VERIFIED, "timestamp": "28 Sep, 09:30 AM", "note": "IT Helpdesk pinged switch - no response", "completed": True},
            {"status": IssueStatus.IN_PROGRESS, "timestamp": "", "note": "Network tech assigned", "completed": False},
            {"status": IssueStatus.RESOLVED, "timestamp": "", "note": "Pending resolution", "completed": False}
        ]
    },
    {
        "id": "QF1028",
        "title": "Broken Wooden Bench Near Main Gate",
        "description": "Wood splintered and detached on right side seating bench.",
        "category": "Infrastructure",
        "location": "Main Gate",
        "latitude": 20.2980,
        "longitude": 85.8210,
        "severity": "LOW",
        "impact": "HIGH",
        "priority": PriorityLevel.MEDIUM,
        "priority_score": 10,
        "priority_reason": "Public campus entrance; aesthetic and mild safety issue",
        "status": IssueStatus.RESOLVED,
        "image": "https://picsum.photos/seed/bench1028/400/250",
        "reporter": "student@quickfix.demo",
        "created_at": "2026-09-26 08:30:00",
        "updated_at": "2026-09-27 16:00:00",
        "timeline": [
            {"status": IssueStatus.SUBMITTED, "timestamp": "26 Sep, 08:30 AM", "note": "Report submitted", "completed": True},
            {"status": IssueStatus.VERIFIED, "timestamp": "26 Sep, 09:00 AM", "note": "Carpentry team inspected", "completed": True},
            {"status": IssueStatus.IN_PROGRESS, "timestamp": "26 Sep, 11:45 AM", "note": "Replaced wooden slats and secured bolts", "completed": True},
            {"status": IssueStatus.RESOLVED, "timestamp": "27 Sep, 04:00 PM", "note": "Fixed and verified by campus supervisor", "completed": True}
        ]
    }
]

class StorageService:
    def __init__(self):
        self._ensure_storage()

    def _ensure_storage(self):
        if not os.path.exists(DATA_FILE_PATH):
            self.reset_demo_data()

    def get_all(self) -> List[Issue]:
        try:
            with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
                return [Issue.from_dict(item) for item in raw_list]
        except Exception:
            return [Issue.from_dict(d) for d in DEMO_ISSUES]

    def save_all(self, issues: List[Issue]):
        with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([issue.to_dict() for issue in issues], f, indent=2)

    def get_by_id(self, issue_id: str) -> Optional[Issue]:
        for issue in self.get_all():
            if issue.id.upper() == issue_id.upper():
                return issue
        return None

    def add_issue(self, issue: Issue) -> Issue:
        issues = self.get_all()
        # Initialize default timeline if empty
        if not issue.timeline:
            now_str = datetime.now().strftime("%d %b, %I:%M %p")
            issue.timeline = [
                {"status": IssueStatus.SUBMITTED, "timestamp": now_str, "note": "Reported by Student via QuickFix", "completed": True},
                {"status": IssueStatus.VERIFIED, "timestamp": "", "note": "Awaiting admin verification", "completed": False},
                {"status": IssueStatus.IN_PROGRESS, "timestamp": "", "note": "Awaiting technician dispatch", "completed": False},
                {"status": IssueStatus.RESOLVED, "timestamp": "", "note": "Awaiting resolution", "completed": False}
            ]
        issues.insert(0, issue)
        self.save_all(issues)
        return issue

    def update_status(self, issue_id: str, new_status: str, note: str = "") -> Optional[Issue]:
        issues = self.get_all()
        target = None
        now_str = datetime.now().strftime("%d %b, %I:%M %p")

        for issue in issues:
            if issue.id == issue_id:
                issue.status = new_status
                issue.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Update timeline
                status_order = [IssueStatus.SUBMITTED, IssueStatus.VERIFIED, IssueStatus.IN_PROGRESS, IssueStatus.RESOLVED]
                current_idx = status_order.index(new_status) if new_status in status_order else 0

                for i, step in enumerate(issue.timeline):
                    step_status = step.get("status")
                    step_idx = status_order.index(step_status) if step_status in status_order else i
                    if step_idx <= current_idx:
                        step["completed"] = True
                        if not step.get("timestamp"):
                            step["timestamp"] = now_str
                    if step_status == new_status and note:
                        step["note"] = note

                target = issue
                break

        if target:
            self.save_all(issues)
        return target

    def generate_next_id(self) -> str:
        issues = self.get_all()
        max_num = 1028
        for issue in issues:
            if issue.id.startswith("QF"):
                try:
                    num = int(issue.id[2:])
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass
        return f"QF{max_num + 1}"

    def get_stats(self) -> Dict[str, Any]:
        issues = self.get_all()
        total = len(issues)
        pending = sum(1 for i in issues if i.status == IssueStatus.SUBMITTED)
        verified = sum(1 for i in issues if i.status == IssueStatus.VERIFIED)
        in_progress = sum(1 for i in issues if i.status == IssueStatus.IN_PROGRESS)
        resolved = sum(1 for i in issues if i.status == IssueStatus.RESOLVED)

        # Count by category
        cat_counts: Dict[str, int] = {}
        for i in issues:
            cat_counts[i.category] = cat_counts.get(i.category, 0) + 1

        # Count by location
        loc_counts: Dict[str, int] = {}
        for i in issues:
            loc_counts[i.location] = loc_counts.get(i.location, 0) + 1

        return {
            "total": total,
            "pending": pending,
            "verified": verified,
            "in_progress": in_progress,
            "resolved": resolved,
            "this_week": total + 8, # simulation of historical activity
            "categories": cat_counts,
            "locations": loc_counts
        }

    def reset_demo_data(self):
        with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(DEMO_ISSUES, f, indent=2)
