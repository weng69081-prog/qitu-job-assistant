"""用户认证与个人资料 API"""
import hashlib, secrets, sqlite3, json
from datetime import datetime
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/user", tags=["user"])

from pathlib import Path
_BASE = Path(__file__).resolve().parent.parent
DB_PATH = str(_BASE / "data" / "users.db")

def init_db():
    import os
    os.makedirs(str(_BASE / "data"), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nickname TEXT DEFAULT '',
                avatar TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now','localtime'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY REFERENCES users(id),
                education TEXT DEFAULT '本科',
                city TEXT DEFAULT '北京',
                skills TEXT DEFAULT '',
                salary TEXT DEFAULT '8K-12K',
                major_category TEXT DEFAULT '',
                major TEXT DEFAULT '',
                job_targets TEXT DEFAULT '',
                gender TEXT DEFAULT '',
                age INTEGER DEFAULT 22,
                experience TEXT DEFAULT '',
                certificate TEXT DEFAULT '',
                interests TEXT DEFAULT '',
                confusion TEXT DEFAULT '',
                grade TEXT DEFAULT '大一',
                updated_at TEXT DEFAULT (datetime('now','localtime'))
            )
        """)
    conn.close()

init_db()

# ── 简单的密码加盐哈希 ──
def hash_pw(password: str, salt: str = "") -> tuple:
    if not salt:
        salt = secrets.token_hex(8)
    h = hashlib.sha256((password + salt).encode()).hexdigest()
    return h, salt

# ── 简易 token 生成 ──
SESSIONS = {}  # token -> user_id

def make_token(user_id: int) -> str:
    tok = secrets.token_hex(32)
    SESSIONS[tok] = user_id
    return tok

def get_user_id(token: str) -> int:
    return SESSIONS.get(token)


# ═══════════ 注册 ═══════════
@router.post("/register")
def register(username: str = Query(...), password: str = Query(...), nickname: str = ""):
    with sqlite3.connect(DB_PATH) as conn:
        exists = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if exists:
            raise HTTPException(400, "用户名已存在")
        h, s = hash_pw(password)
        cur = conn.execute(
            "INSERT INTO users (username, password_hash, nickname) VALUES (?,?,?)",
            (username, h + ":" + s, nickname or username)
        )
        user_id = cur.lastrowid
        # 创建默认 profile
        conn.execute("INSERT INTO profiles (user_id) VALUES (?)", (user_id,))
    return {"ok": True, "token": make_token(user_id), "user": {"id": user_id, "username": username, "nickname": nickname or username}}


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
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT password_hash FROM users WHERE id=?", (uid,)).fetchone()
        if not row:
            raise HTTPException(404, "用户不存在")
        pw_stored = row[0]
        parts = pw_stored.split(":")
        h, s = parts[0], parts[1] if len(parts) > 1 else ""
        test_h, _ = hash_pw(old_password, s)
        if test_h != h:
            raise HTTPException(400, "当前密码错误")
        if len(new_password) < 6:
            raise HTTPException(400, "新密码至少6位")
        new_h, new_s = hash_pw(new_password)
        conn.execute("UPDATE users SET password_hash=? WHERE id=?", (new_h + ":" + new_s, uid))
    # 使旧 token 失效
    SESSIONS.pop(token, None)
    return {"ok": True}


# ═══════════ 登录 ═══════════
@router.post("/login")
def login(username: str = Query(...), password: str = Query(...)):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT id, username, password_hash, nickname FROM users WHERE username=?", (username,)).fetchone()
        if not row:
            raise HTTPException(401, "用户名或密码错误")
        user_id, uname, pw_stored, nickname = row
        parts = pw_stored.split(":")
        h, s = parts[0], parts[1] if len(parts) > 1 else ""
        test_h, _ = hash_pw(password, s)
        if test_h != h:
            raise HTTPException(401, "用户名或密码错误")
    # 判断是否填过基础信息（新生版：昵称+专业大类+具体专业为必填）
    with sqlite3.connect(DB_PATH) as conn:
        user = conn.execute("SELECT nickname FROM users WHERE id=?", (user_id,)).fetchone()
        prof = conn.execute(
            "SELECT major_category, major FROM profiles WHERE user_id=?",
            (user_id,)
        ).fetchone()
    needs_profile = True
    if user and prof:
        nickname = user[0] or ''
        major_cat = prof[0] or ''
        major = prof[1] or ''
        # 昵称、专业大类、具体专业都填了才算填过
        if nickname.strip() and major_cat.strip() and major.strip():
            needs_profile = False
    return {
        "ok": True, "token": make_token(user_id),
        "needs_profile": needs_profile,
        "user": {"id": user_id, "username": uname, "nickname": nickname or uname}
    }


# ═══════════ 获取/更新个人资料 ═══════════
@router.get("/profile")
def get_profile(token: str = Query(...)):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    with sqlite3.connect(DB_PATH) as conn:
        user = conn.execute("SELECT username, nickname, avatar FROM users WHERE id=?", (uid,)).fetchone()
        prof = conn.execute("SELECT * FROM profiles WHERE user_id=?", (uid,)).fetchone()
    if not user:
        raise HTTPException(404, "用户不存在")
    return {
        "username": user[0], "nickname": user[1], "avatar": user[2],
        "profile": {
            "education": prof[1], "city": prof[2], "skills": prof[3],
            "salary": prof[4], "major_category": prof[5], "major": prof[6],
            "job_targets": prof[7], "gender": prof[8], "age": prof[9],
            "experience": prof[10], "certificate": prof[11],
            "interests": prof[13], "confusion": prof[14], "grade": prof[15],
        } if prof else {}
    }


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
    with sqlite3.connect(DB_PATH) as conn:
        if nickname:
            conn.execute("UPDATE users SET nickname=? WHERE id=?", (nickname, uid))
        conn.execute("""
            UPDATE profiles SET education=?, city=?, skills=?, salary=?,
            major_category=?, major=?, job_targets=?, gender=?, age=?,
            experience=?, certificate=?, interests=?, confusion=?, grade=?,
            updated_at=datetime('now','localtime')
            WHERE user_id=?
        """, (education, city, skills, salary, major_category, major, job_targets, gender, age or 22, experience, certificate, interests, confusion, grade, uid))
    return {"ok": True}