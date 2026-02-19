"""
EONIX Analytics API — App usage stats and productivity metrics.
"""
from fastapi import APIRouter
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from memory.db import SessionLocal, AppUsage
from tools.usage_tracker import classify_app

router = APIRouter()


def _db():
    return SessionLocal()


@router.get("/analytics/today")
async def analytics_today():
    """Today's per-app breakdown with total minutes."""
    db = _db()
    today = datetime.now().strftime("%Y-%m-%d")
    rows = (
        db.query(
            AppUsage.app_name,
            func.sum(AppUsage.duration_seconds).label("total_secs"),
            func.count(AppUsage.id).label("sessions"),
        )
        .filter(AppUsage.date == today)
        .group_by(AppUsage.app_name)
        .order_by(desc("total_secs"))
        .all()
    )
    db.close()

    apps = []
    for r in rows:
        mins = round(r.total_secs / 60, 1)
        apps.append({
            "app": r.app_name,
            "minutes": mins,
            "sessions": r.sessions,
            "category": classify_app(r.app_name),
        })

    total_min = round(sum(a["minutes"] for a in apps), 1)
    return {"date": today, "total_minutes": total_min, "apps": apps}


@router.get("/analytics/weekly")
async def analytics_weekly():
    """Last 7 days summary with daily totals and productive/distraction split."""
    db = _db()
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    rows = (
        db.query(
            AppUsage.date,
            AppUsage.app_name,
            func.sum(AppUsage.duration_seconds).label("total_secs"),
        )
        .filter(AppUsage.date >= week_ago)
        .group_by(AppUsage.date, AppUsage.app_name)
        .all()
    )
    db.close()

    days = {}
    for r in rows:
        if r.date not in days:
            days[r.date] = {"date": r.date, "total_min": 0, "productive_min": 0, "distraction_min": 0}
        mins = round(r.total_secs / 60, 1)
        cat = classify_app(r.app_name)
        days[r.date]["total_min"] = round(days[r.date]["total_min"] + mins, 1)
        if cat == "productive":
            days[r.date]["productive_min"] = round(days[r.date]["productive_min"] + mins, 1)
        elif cat == "distraction":
            days[r.date]["distraction_min"] = round(days[r.date]["distraction_min"] + mins, 1)

    sorted_days = sorted(days.values(), key=lambda d: d["date"])

    # Find most focused day
    best = max(sorted_days, key=lambda d: d["productive_min"]) if sorted_days else None

    return {
        "days": sorted_days,
        "best_focus_day": best["date"] if best else None,
    }


@router.get("/analytics/focus")
async def analytics_focus():
    """Productive vs distraction time + score for today."""
    db = _db()
    today = datetime.now().strftime("%Y-%m-%d")
    rows = (
        db.query(
            AppUsage.app_name,
            func.sum(AppUsage.duration_seconds).label("total_secs"),
        )
        .filter(AppUsage.date == today)
        .group_by(AppUsage.app_name)
        .all()
    )
    db.close()

    productive = 0.0
    distraction = 0.0
    neutral = 0.0
    for r in rows:
        mins = r.total_secs / 60
        cat = classify_app(r.app_name)
        if cat == "productive":
            productive += mins
        elif cat == "distraction":
            distraction += mins
        else:
            neutral += mins

    total = productive + distraction + neutral
    score = round((productive / total) * 100) if total > 0 else 0

    return {
        "productive_min": round(productive, 1),
        "distraction_min": round(distraction, 1),
        "neutral_min": round(neutral, 1),
        "total_min": round(total, 1),
        "score": min(score, 100),
    }


@router.get("/analytics/top")
async def analytics_top():
    """Top 10 most used apps this month."""
    db = _db()
    month_start = datetime.now().replace(day=1).strftime("%Y-%m-%d")
    rows = (
        db.query(
            AppUsage.app_name,
            func.sum(AppUsage.duration_seconds).label("total_secs"),
            func.count(AppUsage.id).label("sessions"),
        )
        .filter(AppUsage.date >= month_start)
        .group_by(AppUsage.app_name)
        .order_by(desc("total_secs"))
        .limit(10)
        .all()
    )
    db.close()

    apps = []
    for r in rows:
        apps.append({
            "app": r.app_name,
            "hours": round(r.total_secs / 3600, 2),
            "minutes": round(r.total_secs / 60, 1),
            "sessions": r.sessions,
            "category": classify_app(r.app_name),
        })

    return {"month": month_start[:7], "top_apps": apps}
