from dataclasses import dataclass
from typing import List, Callable, Optional
from datetime import datetime

@dataclass
class InAppNotification:
    id: str
    title: str
    message: str
    timestamp: str
    read: bool = False
    issue_id: Optional[str] = None
    status: Optional[str] = None

class NotificationService:
    def __init__(self):
        self._notifications: List[InAppNotification] = [
            InAppNotification(
                id="notif_init_1",
                title="QuickFix System Ready",
                message="Welcome to QuickFix Smart Campus Issue Management.",
                timestamp="Just now",
                read=False
            )
        ]
        self._listeners: List[Callable[[InAppNotification], None]] = []

    def subscribe(self, callback: Callable[[InAppNotification], None]):
        if callback not in self._listeners:
            self._listeners.append(callback)

    def unsubscribe(self, callback: Callable[[InAppNotification], None]):
        if callback in self._listeners:
            self._listeners.remove(callback)

    def notify(self, title: str, message: str, issue_id: Optional[str] = None, status: Optional[str] = None):
        notif = InAppNotification(
            id=f"notif_{datetime.now().timestamp()}",
            title=title,
            message=message,
            timestamp=datetime.now().strftime("%I:%M %p"),
            read=False,
            issue_id=issue_id,
            status=status
        )
        self._notifications.insert(0, notif)
        for listener in self._listeners:
            try:
                listener(notif)
            except Exception:
                pass

    def notify_status_change(self, issue_id: str, new_status: str):
        msg = f"Your issue #{issue_id} is now updated to {new_status}."
        if new_status == "IN_PROGRESS":
            msg = f"Your issue #{issue_id} is now being handled by the maintenance crew."
        elif new_status == "RESOLVED":
            msg = f"Good news! Your issue #{issue_id} has been successfully resolved."
        elif new_status == "VERIFIED":
            msg = f"Your issue #{issue_id} has been inspected and verified by campus staff."

        self.notify(
            title="QuickFix Update",
            message=msg,
            issue_id=issue_id,
            status=new_status
        )

    def get_all(self) -> List[InAppNotification]:
        return self._notifications

    def get_unread_count(self) -> int:
        return sum(1 for n in self._notifications if not n.read)

    def mark_all_read(self):
        for n in self._notifications:
            n.read = True
