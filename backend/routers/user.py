"""用户认证与个人资料 API（SQLAlchemy 统一版）"""
import hashlib, secrets, json
from datetime import datetime
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/user", tags=["user"])

from database import SessionLocal
from models import User, Profile, UserSession

# ── 简单的密码加盐哈希 ──
def hash_pw(password: str, salt: str = "") -> tuple:
    if not salt:
        salt = secrets.token_hex(8)
    h = hashlib.sha256((password + salt).encode()).hexdigest()
    return h, salt

# ── 持久化 token ──
def ensure_session_table():
    from database import engine, Base
    Base.metadata.create_all(bind=engine, tables=[UserSession.__table__])

def make_token(user_id: int) -> str:
    tok = secrets.token_hex(32)
    ensure_session_table()
    db = SessionLocal()
    try:
        db.merge(UserSession(token=tok, user_id=user_id))
        db.commit()
    finally:
        db.close()
    return tok

def get_user_id(token: str) -> int | None:
    ensure_session_table()
    db = SessionLocal()
    try:
        s = db.query(UserSession).filter(UserSession.token == token).first()
        return s.user_id if s else None
    finally:
        db.close()


# ═══════════ 注册 ═══════════
@router.post("/register")
def register(username: str = Query(...), password: str = Query(...), nickname: str = ""):
    db = SessionLocal()
    try:
        exists = db.query(User).filter(User.username == username).first()
        if exists:
            raise HTTPException(400, "用户名已存在")
        h, s = hash_pw(password)
        user = User(username=username, password_hash=h + ":" + s, nickname=nickname or username)
        db.add(user)
        db.flush()
        profile = Profile(user_id=user.id)
        db.add(profile)
        db.commit()
        return {"ok": True, "token": make_token(user.id), "user": {"id": user.id, "username": username, "nickname": nickname or username}}
    finally:
        db.close()


# ═══════════ 修改密码 ═══════════
@router.post("/change-password")
def change_password(
    token: str = Query(...),
    old_password: str = Query(...),
    new_password: str = Query(...),
):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == uid).first()
        if not user:
            raise HTTPException(404, "用户不存在")
        parts = user.password_hash.split(":")
        h, s = parts[0], parts[1] if len(parts) > 1 else ""
        test_h, _ = hash_pw(old_password, s)
        if test_h != h:
            raise HTTPException(400, "当前密码错误")
        if len(new_password) < 6:
            raise HTTPException(400, "新密码至少6位")
        new_h, new_s = hash_pw(new_password)
        user.password_hash = new_h + ":" + new_s
        # 使旧 token 失效
        db.query(UserSession).filter(UserSession.token == token).delete()
        db.commit()
    finally:
        db.close()
    return {"ok": True}


# ═══════════ 登录 ═══════════
@router.post("/login")
def login(username: str = Query(...), password: str = Query(...)):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(401, "用户名或密码错误")
        parts = user.password_hash.split(":")
        h, s = parts[0], parts[1] if len(parts) > 1 else ""
        test_h, _ = hash_pw(password, s)
        if test_h != h:
            raise HTTPException(401, "用户名或密码错误")

        # 判断是否填过基础信息
        prof = db.query(Profile).filter(Profile.user_id == user.id).first()
        needs_profile = True
        if user.nickname and prof:
            if user.nickname.strip() and (prof.major_category or "").strip() and (prof.major or "").strip():
                needs_profile = False
    finally:
        db.close()

    return {
        "ok": True, "token": make_token(user.id),
        "needs_profile": needs_profile,
        "user": {"id": user.id, "username": user.username, "nickname": user.nickname or user.username}
    }


# ═══════════ 获取/更新个人资料 ═══════════
@router.get("/profile")
def get_profile(token: str = Query(...)):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == uid).first()
        prof = db.query(Profile).filter(Profile.user_id == uid).first()
        if not user:
            raise HTTPException(404, "用户不存在")
        return {
            "username": user.username, "nickname": user.nickname, "avatar": user.avatar,
            "profile": {
                "education": prof.education, "city": prof.city, "skills": prof.skills,
                "salary": prof.salary, "major_category": prof.major_category, "major": prof.major,
                "job_targets": prof.job_targets, "gender": prof.gender, "age": prof.age,
                "experience": prof.experience, "certificate": prof.certificate,
                "interests": prof.interests, "confusion": prof.confusion, "grade": prof.grade,
            } if prof else {}
        }
    finally:
        db.close()


@router.post("/profile")
def update_profile(
    token: str = Query(...),
    nickname: str = "", education: str = "", city: str = "",
    skills: str = "", salary: str = "", major_category: str = "",
    major: str = "", job_targets: str = "", gender: str = "",
    age: int = 0, experience: str = "", certificate: str = "",
    interests: str = "", confusion: str = "", grade: str = "大一",
):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = SessionLocal()
    try:
        if nickname:
            db.query(User).filter(User.id == uid).update({"nickname": nickname})
        prof = db.query(Profile).filter(Profile.user_id == uid).first()
        if prof:
            prof.education = education or prof.education
            prof.city = city or prof.city
            prof.skills = skills or prof.skills
            prof.salary = salary or prof.salary
            prof.major_category = major_category or prof.major_category
            prof.major = major or prof.major
            prof.job_targets = job_targets or prof.job_targets
            prof.gender = gender or prof.gender
            prof.age = age or prof.age or 22
            prof.experience = experience or prof.experience
            prof.certificate = certificate or prof.certificate
            prof.interests = interests or prof.interests
            prof.confusion = confusion or prof.confusion
            prof.grade = grade or prof.grade
            prof.updated_at = datetime.utcnow()
        db.commit()
    finally:
        db.close()
    return {"ok": True}