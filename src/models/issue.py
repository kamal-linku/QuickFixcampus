from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any

class IssueStatus:
    SUBMITTED = "SUBMITTED"
    VERIFIED = "VERIFIED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"

    ALL = [SUBMITTED, VERIFIED, IN_PROGRESS, RESOLVED]

class PriorityLevel:
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class TimelineStep:
    status: str
    timestamp: str
    note: str
    completed: bool = False

@dataclass
class Issue:
    id: str
    title: str
    description: str
    category: str
    location: str
    latitude: float = 20.2961
    longitude: float = 85.8245
    severity: str = "MEDIUM"      # LOW, MEDIUM, HIGH, CRITICAL
    impact: str = "MEDIUM"        # LOW, MEDIUM, HIGH
    priority: str = "MEDIUM"      # LOW, MEDIUM, HIGH, CRITICAL
    priority_score: int = 6
    priority_reason: str = "Standard maintenance priority"
    status: str = IssueStatus.SUBMITTED
    image: str = ""
    reporter: str = "student@quickfix.demo"
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    timeline: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Issue":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            category=data.get("category", "Other"),
            location=data.get("location", "Campus"),
            latitude=float(data.get("latitude", 20.2961)),
            longitude=float(data.get("longitude", 85.8245)),
            severity=data.get("severity", "MEDIUM"),
            impact=data.get("impact", "MEDIUM"),
            priority=data.get("priority", "MEDIUM"),
            priority_score=int(data.get("priority_score", data.get("priorityScore", 6))),
            priority_reason=data.get("priority_reason", "Standard priority assessment"),
            status=data.get("status", IssueStatus.SUBMITTED),
            image=data.get("image", ""),
            reporter=data.get("reporter", "student@quickfix.demo"),
            created_at=data.get("created_at", data.get("createdAt", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
            updated_at=data.get("updated_at", data.get("updatedAt", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
            timeline=data.get("timeline", [])
        )
