import re
from typing import Tuple, Optional, List, Dict, Any
from models.issue import Issue, IssueStatus, PriorityLevel

# Category definitions and keyword mappings
CATEGORY_KEYWORDS = {
    "Electrical": [
        "light", "lamp", "bulb", "electric", "electricity", "wire", "switch", "short circuit",
        "power", "plug", "socket", "spark", "blackout", "fan", "fuse", "voltage", "cable", "shock"
    ],
    "Water": [
        "water", "pipe", "leak", "leaking", "flood", "tap", "faucet", "drain", "sewage", "clogged",
        "overflow", "tank", "valve", "plumbing", "dripping", "sink"
    ],
    "Cleanliness": [
        "garbage", "trash", "waste", "dust", "dirty", "dustbin", "litter", "spill", "smell",
        "odor", "sweep", "mop", "stain", "mess", "unclean"
    ],
    "Network": [
        "wifi", "wi-fi", "internet", "network", "ethernet", "lan", "router", "signal", "offline",
        "connection", "server", "bandwidth", "portal"
    ],
    "Infrastructure": [
        "chair", "bench", "desk", "table", "door", "window", "lock", "wall", "ceiling", "floor",
        "stairs", "tile", "cracked", "pavement", "glass", "gate", "road", "rail"
    ],
    "Sanitation": [
        "toilet", "washroom", "restroom", "urinal", "basin", "soap", "hygiene", "flush",
        "tissue", "bathroom"
    ],
    "Equipment": [
        "projector", "computer", "printer", "ac", "air conditioner", "speaker", "mic",
        "screen", "monitor", "lab equipment", "generator"
    ]
}

CATEGORY_WEIGHTS = {
    "Electrical": 1.4,
    "Water": 1.2,
    "Sanitation": 1.2,
    "Infrastructure": 1.1,
    "Network": 1.0,
    "Equipment": 1.0,
    "Cleanliness": 0.9,
    "Other": 0.8
}

LOCATION_IMPACT = {
    "Library Block": 5,
    "Main Gate": 5,
    "Auditorium": 4,
    "Cafeteria": 4,
    "CSE Block": 4,
    "ECE Block": 4,
    "Hostel A": 3,
    "Hostel B": 3,
    "Parking": 2,
    "Campus Grounds": 2
}

CRITICAL_HAZARD_WORDS = [
    "spark", "shock", "fire", "smoke", "exposed wire", "flooding", "emergency", "danger",
    "hazard", "burst", "collapsed", "blast", "live wire", "unconscious"
]

class SmartEngine:
    @staticmethod
    def detect_category(text: str) -> Tuple[str, float]:
        """Analyzes text to detect the most probable issue category and confidence."""
        if not text:
            return "Other", 0.0

        lower_text = text.lower()
        best_category = "Other"
        max_matches = 0

        for cat, keywords in CATEGORY_KEYWORDS.items():
            matches = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', lower_text))
            if matches > max_matches:
                max_matches = matches
                best_category = cat

        confidence = min(1.0, max_matches * 0.35) if max_matches > 0 else 0.2
        return best_category, confidence

    @staticmethod
    def calculate_priority(category: str, location: str, description: str) -> Dict[str, Any]:
        """
        Dynamically calculates priority score based on:
        Severity x Impact x Category Weight
        """
        lower_desc = description.lower() if description else ""

        # Base severity calculation (1 to 5)
        severity = 2
        reason_parts = []

        is_critical_hazard = any(w in lower_desc for w in CRITICAL_HAZARD_WORDS)
        if is_critical_hazard:
            severity = 5
            reason_parts.append("Potential immediate safety hazard detected")
        elif any(w in lower_desc for w in ["broken", "leak", "not working", "cut", "overflow", "damage"]):
            severity = 4
            reason_parts.append("Functional failure affecting operations")
        elif any(w in lower_desc for w in ["slow", "flicker", "dirty", "smell", "loose"]):
            severity = 3
            reason_parts.append("Service degradation or discomfort")
        else:
            severity = 2
            reason_parts.append("Minor maintenance or reporting request")

        # Campus impact calculation (1 to 5)
        impact = LOCATION_IMPACT.get(location, 3)
        if impact >= 4:
            reason_parts.append(f"High-traffic campus location ({location})")

        # Category Weight
        weight = CATEGORY_WEIGHTS.get(category, 1.0)

        # Priority Score formula: Severity * Impact * Weight
        raw_score = int(round(severity * impact * weight))

        if raw_score >= 18 or severity == 5:
            level = PriorityLevel.CRITICAL
        elif raw_score >= 12:
            level = PriorityLevel.HIGH
        elif raw_score >= 6:
            level = PriorityLevel.MEDIUM
        else:
            level = PriorityLevel.LOW

        severity_label = "CRITICAL" if severity == 5 else ("HIGH" if severity == 4 else ("MEDIUM" if severity == 3 else "LOW"))
        impact_label = "HIGH" if impact >= 4 else ("MEDIUM" if impact == 3 else "LOW")

        return {
            "score": raw_score,
            "level": level,
            "severity_num": severity,
            "severity_label": severity_label,
            "impact_num": impact,
            "impact_label": impact_label,
            "category_weight": weight,
            "reason": "; ".join(reason_parts)
        }

    @staticmethod
    def detect_duplicate(new_category: str, new_location: str, new_description: str, existing_issues: List[Issue]) -> Optional[Dict[str, Any]]:
        """
        Duplicate Detection Engine:
        Finds if a similar problem in the same category & location is already reported.
        """
        if not new_description or len(new_description.strip()) < 3:
            return None

        # Clean words from description
        stop_words = {"the", "a", "an", "is", "in", "at", "near", "to", "and", "of", "on", "not", "working", "for"}
        new_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', new_description.lower())) - stop_words

        for issue in existing_issues:
            # Only consider active issues (not resolved)
            if issue.status == IssueStatus.RESOLVED:
                continue

            # Same category and same location is strong signal
            same_loc = (issue.location.strip().lower() == new_location.strip().lower())
            same_cat = (issue.category.strip().lower() == new_category.strip().lower())

            if same_loc and same_cat:
                existing_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', (issue.description + " " + issue.title).lower())) - stop_words
                common = new_words.intersection(existing_words)

                if len(common) >= 1 or len(new_words) == 0:
                    return {
                        "is_duplicate": True,
                        "existing_issue": issue,
                        "matched_keywords": list(common),
                        "message": f"Issue #{issue.id} ('{issue.title}') at {issue.location} is currently {issue.status}."
                    }

        return None
