import streamlit as st
import json
import os
import time
from datetime import datetime

# ─── CONFIG ──────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Highway Bank", page_icon="🏦", layout="centered",
                   initial_sidebar_state="collapsed")

DB_FILE = "/tmp/highway_bank_db.json"

# ─── SHARED DATABASE ──────────────────────────────────────────────────────────
INITIAL_DB = {
    "users": {
        "marina": {
            "name": "Մարինա Մարգարյան",
            "initials": "ՄՄ",
            "pin": "1111",
            "color": "#a855f7",
            "accounts": {
                "AMD": {"number": "1001", "balance": 13029.20, "currency": "֏"},
                "USD": {"number": "1020", "balance": 0.00, "currency": "$"},
                "EUR": {"number": "1040", "balance": 0.00, "currency": "€"},
                "RUB": {"number": "1041", "balance": 0.00, "currency": "₽"},
            },
            "cards": [{"type": "VISA", "last4": "0355", "name": "Visa Classic",
                        "balance": 1802.00, "currency": "֏", "expiry": "08/28"}],
            "loans": [{"name": "Թանկարժեք իրերի գրա...", "amount": 349000,
                        "currency": "֏", "months_left": 17, "icon": "🥇"}],
            "savings": [
                {"name": "AMD Խնայողական հաշիվ", "balance": 13029, "currency": "֏"},
                {"name": "USD Խնայողական հաշիվ", "balance": 0, "currency": "$"},
                {"name": "EUR Խնայողական հաշիվ", "balance": 0, "currency": "€"},
            ],
            "transactions": [
                {"id": "t1", "name": "CARREFOUR ARGISH...", "category": "Գնում", "amount": -340, "currency": "֏", "date": "Այսօր", "time": "18:04", "icon": "🏪"},
                {"id": "t2", "name": "HOME GROUP", "category": "Գնում", "amount": -220, "currency": "֏", "date": "Այսօր", "time": "08:52", "icon": "🏪"},
                {"id": "t3", "name": "Աշխատավարձ", "category": "Եկամուտ", "amount": 50000, "currency": "֏", "date": "Ապրիլ 1", "time": "09:00", "icon": "💼"},
            ],
            "monthly_spending": {"total": 58652, "categories": [
                {"name": "Աշխ.", "icon": "💼", "amount": 50000, "color": "#6366f1"},
                {"name": "Փոխ.", "icon": "🔄", "amount": 5950, "color": "#3b82f6"},
                {"name": "Խան.", "icon": "🏪", "amount": 2250, "color": "#3b82f6"},
                {"name": "Սնունդ", "icon": "🍽️", "amount": 300, "color": "#6366f1"},
                {"name": "Տրան.", "icon": "🚌", "amount": 150, "color": "#3b82f6"},
                {"name": "Այլ", "icon": "🏛️", "amount": 2, "color": "#6366f1"},
            ]},
        },
        "artur": {
            "name": "Արթուր Պետրոսյան",
            "initials": "ԱՊ",
            "pin": "2222",
            "color": "#3b82f6",
            "accounts": {
                "AMD": {"number": "2001", "balance": 25000.00, "currency": "֏"},
                "USD": {"number": "2020", "balance": 50.00, "currency": "$"},
                "EUR": {"number": "2040", "balance": 10.00, "currency": "€"},
                "RUB": {"number": "2041", "balance": 0.00, "currency": "₽"},
            },
            "cards": [{"type": "VISA", "last4": "1122", "name": "Visa Gold",
                        "balance": 5500.00, "currency": "֏", "expiry": "12/26"}],
            "loans": [],
            "savings": [
                {"name": "AMD Խնայողական հաշիվ", "balance": 8000, "currency": "֏"},
                {"name": "USD Խնայողական հաշիվ", "balance": 100, "currency": "$"},
                {"name": "EUR Խնայողական հաշիվ", "balance": 0, "currency": "€"},
            ],
            "transactions": [
                {"id": "t1", "name": "Yerevan City", "category": "Գնում", "amount": -450, "currency": "֏", "date": "Այսօր", "time": "14:30", "icon": "🏪"},
                {"id": "t2", "name": "Աշխատավարձ", "category": "Եկամուտ", "amount": 80000, "currency": "֏", "date": "Ապրիլ 1", "time": "09:00", "icon": "💼"},
            ],
            "monthly_spending": {"total": 80450, "categories": [
                {"name": "Աշխ.", "icon": "💼", "amount": 80000, "color": "#6366f1"},
                {"name": "Գնում", "icon": "🏪", "amount": 450, "color": "#3b82f6"},
            ]},
        },
        "davit": {
            "name": "Դավիթ Գրիգորյան",
            "initials": "ԴԳ",
            "pin": "3333",
            "color": "#10b981",
            "accounts": {
                "AMD": {"number": "3001", "balance": 50000.00, "currency": "֏"},
                "USD": {"number": "3020", "balance": 200.00, "currency": "$"},
                "EUR": {"number": "3040", "balance": 0.00, "currency": "€"},
                "RUB": {"number": "3041", "balance": 500.00, "currency": "₽"},
            },
            "cards": [{"type": "MASTER", "last4": "9988", "name": "Mastercard Platinum",
                        "balance": 12000.00, "currency": "֏", "expiry": "06/27"}],
            "loans": [{"name": "Բնակարանային վարկ", "amount": 2500000,
                        "currency": "֏", "months_left": 120, "icon": "🏠"}],
            "savings": [
                {"name": "AMD Խնայողական հաշիվ", "balance": 30000, "currency": "֏"},
                {"name": "USD Խնայողական հաշիվ", "balance": 500, "currency": "$"},
                {"name": "EUR Խնայողական հաշիվ", "balance": 200, "currency": "€"},
            ],
            "transactions": [
                {"id": "t1", "name": "Բնակ. վճար", "category": "Կոմունալ", "amount": -15000, "currency": "֏", "date": "Այսօր", "time": "10:00", "icon": "🏠"},
                {"id": "t2", "name": "Աշխատավարձ", "category": "Եկամուտ", "amount": 150000, "currency": "֏", "date": "Ապրիլ 1", "time": "09:00", "icon": "💼"},
            ],
            "monthly_spending": {"total": 165000, "categories": [
                {"name": "Աշխ.", "icon": "💼", "amount": 150000, "color": "#6366f1"},
                {"name": "Կոմ.", "icon": "🏠", "amount": 15000, "color": "#10b981"},
            ]},
        },
    }
}

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump(INITIAL_DB, f, ensure_ascii=False, indent=2)
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def get_user(uid):
    db = load_db()
    return db["users"].get(uid)

def find_user_by_account(acct_num):
    db = load_db()
    for uid, u in db["users"].items():
        for cur, acct in u["accounts"].items():
            if acct["number"] == acct_num:
                return uid, cur
    return None, None

# ─── SESSION STATE ────────────────────────────────────────────────────────────
def init():
    for k, v in {
        "logged_in": False, "user_id": None, "pin": "", "shake": False,
        "error": False, "face_scanning": False, "face_done": False,
        "tab": "home", "send_success": False, "send_msg": "",
        "pay_success": False, "chat_msgs": [], "notif_count": 2,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

# ─── CSS ─────────────────────────────────────────────────────────────────────
def css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Onest:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg: #F2F2F7;
    --white: #FFFFFF;
    --green: #2DB34A;
    --green2: #25a041;
    --blue: #3b82f6;
    --purple: #8b5cf6;
    --dark: #111827;
    --nav: #0f172a;
    --text: #1C1C1E;
    --text2: #6B7280;
    --text3: #9CA3AF;
    --danger: #EF4444;
    --gold: #F59E0B;
    --radius: 18px;
    --shadow: 0 2px 16px rgba(0,0,0,.08);
    --shadow2: 0 4px 24px rgba(0,0,0,.12);
    --font: 'Onest', -apple-system, sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--font) !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg) !important; max-width: 430px; margin: 0 auto; }
.block-container { padding: 0 0 80px 0 !important; max-width: 430px !important; }
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display:none !important; }
.stButton>button { all:unset; cursor:pointer; width:100%; display:block; }
div[data-testid="stVerticalBlock"]>div { padding:0 !important; }
div[data-testid="element-container"] { margin:0 !important; }
.stMarkdown { margin:0 !important; }
[data-testid="stTextInput"]>div>div>input {
    background: #F9FAFB !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: var(--font) !important;
    padding: 14px 16px !important;
    font-size: 16px !important;
}
[data-testid="stTextInput"]>label { display:none !important; }

/* ── Animations ── */
@keyframes shake {
    0%,100%{transform:translateX(0)}10%{transform:translateX(-9px)}
    20%{transform:translateX(9px)}30%{transform:translateX(-7px)}
    40%{transform:translateX(7px)}50%{transform:translateX(-5px)}
    60%{transform:translateX(5px)}70%{transform:translateX(-3px)}
    80%{transform:translateX(3px)}90%{transform:translateX(-1px)}
}
@keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
@keyframes pop { from{opacity:0;transform:scale(.85)} to{opacity:1;transform:scale(1)} }
@keyframes scanLine {
    0%{top:10%;opacity:.9}50%{top:85%;opacity:1}100%{top:10%;opacity:.9}
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(1.05)} }
@keyframes successPop {
    0%{transform:scale(0);opacity:0}
    60%{transform:scale(1.15);opacity:1}
    100%{transform:scale(1);opacity:1}
}
@keyframes slideIn { from{transform:translateX(100%);opacity:0} to{transform:translateX(0);opacity:1} }

/* ── PIN Screen ── */
.pin-screen {
    min-height: 100vh;
    background: #F2F2F7;
    display: flex; flex-direction: column; align-items: center;
    padding: 24px 0;
}
.pin-title {
    font-size: 28px; font-weight: 800; color: var(--text);
    text-align: center; line-height: 1.2; margin: 32px 0 40px;
    letter-spacing: -0.5px;
}
.pin-dots {
    display: flex; gap: 20px; justify-content: center;
    margin: 0 0 40px;
}
.dot {
    width: 14px; height: 14px; border-radius: 50%;
    border: 2px solid #C0C0C8;
    transition: all .2s cubic-bezier(.34,1.56,.64,1);
    background: transparent;
}
.dot.filled { background: var(--text); border-color: var(--text); transform: scale(1.1); }
.dot.error { background: var(--danger); border-color: var(--danger); }
.shake { animation: shake .5s cubic-bezier(.36,.07,.19,.97) both; }
.key-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 14px; padding: 0 40px; width: 100%; max-width: 380px;
}
.key {
    width: 80px; height: 80px; border-radius: 50%;
    background: white; box-shadow: var(--shadow);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    cursor: pointer; margin: 0 auto;
    transition: all .12s ease; user-select: none;
    border: none;
}
.key:active, .key.pressed { background: #E8E8ED; transform: scale(.93); box-shadow: none; }
.key-num { font-size: 28px; font-weight: 400; color: var(--text); line-height: 1; }
.key-sub { font-size: 9px; color: var(--text2); letter-spacing: 1.8px; margin-top: 2px; font-weight: 500; }
.key.ghost { background: transparent; box-shadow: none; }
.key.ghost:active { background: transparent; transform: scale(.9); }
.forgot-pin { font-size: 15px; color: var(--text); margin-top: 28px; text-decoration: underline; cursor: pointer; }

/* ── Top bar (PIN) ── */
.top-bar-pin {
    display: flex; justify-content: space-between; align-items: center;
    width: 100%; padding: 12px 20px 0;
}
.top-x { font-size: 20px; color: var(--text); cursor: pointer; padding: 8px; }
.top-save { font-size: 14px; color: var(--text); cursor: pointer; padding: 8px; border-bottom: 1px dashed var(--text2); }

/* ── App Header ── */
.app-header {
    background: linear-gradient(160deg, #b8c0d8 0%, #c8cfe8 40%, #d4d8ea 70%, #bcc4da 100%);
    padding: 52px 20px 20px;
    position: relative; overflow: hidden;
}
.app-header::before {
    content:''; position:absolute; top:-30%; right:-10%;
    width: 55%; height: 120%;
    background: linear-gradient(135deg, rgba(255,255,255,.15), transparent);
    transform: rotate(-15deg);
}
.app-header::after {
    content:''; position:absolute; bottom:-20%; left:10%;
    width: 45%; height: 90%;
    background: linear-gradient(135deg, rgba(255,255,255,.08), transparent);
    transform: rotate(20deg);
}
.header-top {
    display: flex; justify-content: space-between; align-items: center;
    position: relative; z-index: 1;
}
.avatar {
    width: 42px; height: 42px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700; color: white;
    cursor: pointer; flex-shrink: 0;
}
.notif-btn {
    width: 42px; height: 42px; border-radius: 50%;
    background: white; display: flex; align-items: center; justify-content: center;
    cursor: pointer; position: relative; box-shadow: var(--shadow);
}
.notif-badge {
    position: absolute; top: 6px; right: 6px;
    width: 8px; height: 8px; border-radius: 50%; background: var(--danger);
}

/* ── Cards ── */
.card {
    background: white; border-radius: var(--radius);
    box-shadow: var(--shadow); margin: 8px 16px;
    padding: 20px; animation: fadeUp .4s ease both;
}
.card-title { font-size: 20px; font-weight: 700; margin-bottom: 14px; color: var(--text); }
.card-row {
    background: #F9FAFB; border-radius: 12px;
    display: flex; align-items: center; gap: 14px;
    padding: 14px; margin-bottom: 10px; cursor: pointer;
    transition: background .15s;
}
.card-row:hover { background: #F3F4F6; }
.card-icon {
    width: 44px; height: 44px; border-radius: 10px;
    background: #1C1C1E; display: flex; align-items: center;
    justify-content: center; flex-shrink: 0; color: white;
    font-size: 11px; font-weight: 700;
}
.card-info { flex: 1; }
.card-name { font-size: 14px; font-weight: 500; color: var(--text); }
.card-bal { font-size: 20px; font-weight: 700; color: var(--text); margin-top: 2px; }
.show-all { text-align: center; color: var(--text2); font-size: 14px; padding: 10px; cursor: pointer; }

/* ── Account rows ── */
.acct-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.acct-item {
    background: #F9FAFB; border-radius: 14px; padding: 16px;
    position: relative; cursor: pointer; transition: background .15s;
}
.acct-item:hover { background: #F3F4F6; }
.acct-num { font-size: 11px; color: var(--text3); position: absolute; top: 12px; right: 12px; }
.acct-symbol {
    width: 40px; height: 40px; border-radius: 50%;
    background: white; box-shadow: var(--shadow);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: 700; color: var(--text); margin-bottom: 14px;
}
.acct-name { font-size: 12px; color: var(--text2); margin-bottom: 4px; }
.acct-bal { font-size: 17px; font-weight: 700; color: var(--text); }

/* ── Savings ── */
.savings-item {
    background: #F9FAFB; border-radius: 14px; padding: 16px;
    margin-bottom: 8px; display: flex; align-items: center; gap: 14px;
}
.savings-icon {
    width: 46px; height: 46px; border-radius: 50%;
    background: #7c3aed; display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
}
.add-savings {
    text-align: center; font-size: 13px; color: var(--text2);
    padding: 6px; text-decoration: underline; cursor: pointer;
}

/* ── Transaction History ── */
.history-header {
    background: white; padding: 20px 16px 12px;
    position: sticky; top: 0; z-index: 10;
    box-shadow: 0 1px 8px rgba(0,0,0,.06);
}
.filter-row { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 4px; }
.filter-btn {
    background: white; border: 1px solid #E5E7EB; border-radius: 20px;
    padding: 6px 14px; font-size: 13px; font-weight: 500; color: var(--text);
    cursor: pointer; white-space: nowrap; flex-shrink: 0; box-shadow: var(--shadow);
    display: flex; align-items: center; gap: 4px;
}
.spending-card { background: white; border-radius: var(--radius); padding: 20px; margin: 8px 16px; }
.spending-title { font-size: 18px; font-weight: 700; color: var(--text); }
.spending-period { font-size: 13px; color: var(--text2); margin-bottom: 4px; }
.spending-total { font-size: 28px; font-weight: 800; color: var(--text); margin-bottom: 14px; }
.progress-bar {
    height: 6px; border-radius: 3px;
    background: linear-gradient(90deg, #6366f1 0%, #3b82f6 100%);
    margin-bottom: 16px;
}
.cat-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; }
.cat-item {
    background: #F9FAFB; border-radius: 12px; padding: 12px;
    display: flex; flex-direction: column; gap: 8px;
}
.cat-icon {
    width: 38px; height: 38px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.cat-amt { font-size: 13px; font-weight: 600; color: var(--text); }
.tx-section-title {
    font-size: 17px; font-weight: 700; color: var(--text);
    padding: 12px 16px 0;
}
.tx-total { font-size: 14px; color: var(--danger); float: right; }
.tx-item {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 16px; border-bottom: 1px solid #F3F4F6; cursor: pointer;
}
.tx-icon-wrap {
    width: 46px; height: 46px; border-radius: 50%;
    background: #3b82f6; display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.tx-info { flex: 1; }
.tx-name { font-size: 15px; font-weight: 600; color: var(--text); }
.tx-cat { font-size: 12px; color: var(--text2); margin-top: 2px; }
.tx-right { text-align: right; }
.tx-amt { font-size: 15px; font-weight: 700; }
.tx-time { font-size: 11px; color: var(--text3); margin-top: 2px; }

/* ── Transfers ── */
.transfer-header {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    padding: 20px 16px 24px;
}
.transfer-section { font-size: 18px; font-weight: 700; color: var(--text); padding: 16px 16px 8px; }
.transfer-option {
    background: white; border-radius: var(--radius); margin: 0 16px 10px;
    padding: 18px; display: flex; align-items: center; gap: 14px;
    cursor: pointer; box-shadow: var(--shadow); transition: all .15s;
}
.transfer-option:hover { transform: translateY(-1px); box-shadow: var(--shadow2); }
.to-icon {
    width: 52px; height: 52px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-size: 24px;
    flex-shrink: 0;
}
.to-label { font-size: 16px; font-weight: 600; color: var(--text); }
.to-sub { font-size: 13px; color: var(--text2); margin-top: 2px; }
.to-arrow { margin-left: auto; font-size: 18px; color: var(--text3); }
.modal-overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,.4);
    z-index: 100; display: flex; align-items: flex-end;
}
.modal-sheet {
    background: white; border-radius: 24px 24px 0 0;
    width: 100%; padding: 20px; max-height: 80vh;
    animation: slideIn .3s ease;
}
.modal-title { font-size: 20px; font-weight: 800; margin-bottom: 20px; }
.success-sheet {
    display: flex; flex-direction: column; align-items: center;
    padding: 32px 20px; text-align: center;
    animation: pop .4s cubic-bezier(.34,1.56,.64,1) both;
}
.success-icon {
    width: 80px; height: 80px; border-radius: 50%;
    background: var(--green); display: flex; align-items: center;
    justify-content: center; font-size: 36px; color: white;
    animation: successPop .5s cubic-bezier(.34,1.56,.64,1) both;
    margin-bottom: 16px;
}
.notify-badge {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white; border-radius: 14px; padding: 14px 16px;
    margin: 8px 16px; display: flex; align-items: center; gap: 12px;
    animation: fadeUp .4s ease; box-shadow: 0 4px 16px rgba(16,185,129,.3);
}

/* ── Payments ── */
.pay-section-banner {
    border-radius: 18px; padding: 20px;
    margin: 8px 16px; position: relative; overflow: hidden;
    min-height: 100px; display: flex; flex-direction: column; justify-content: flex-end;
}
.pay-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; padding: 0 16px; }
.pay-item {
    background: white; border-radius: 14px; padding: 16px 10px;
    display: flex; flex-direction: column; align-items: center; gap: 8px;
    cursor: pointer; box-shadow: var(--shadow); transition: all .15s;
    text-align: center;
}
.pay-item:hover { transform: translateY(-2px); box-shadow: var(--shadow2); }
.pay-icon { width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; }
.pay-label { font-size: 12px; font-weight: 500; color: var(--text); line-height: 1.3; }

/* ── Profile ── */
.profile-bg {
    background: linear-gradient(180deg, #e8e8f0 0%, #F2F2F7 100%);
    padding: 40px 20px 20px; text-align: center; position: relative;
}
.profile-avatar {
    width: 80px; height: 80px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; font-weight: 800; color: white;
    margin: 0 auto 14px; box-shadow: 0 8px 24px rgba(0,0,0,.2);
}
.profile-name { font-size: 22px; font-weight: 800; color: var(--text); }
.profile-btn {
    background: #1C1C1E; color: white; border-radius: 22px;
    padding: 10px 24px; font-size: 14px; font-weight: 600;
    display: inline-flex; align-items: center; gap: 8px; margin-top: 12px;
    cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,.3);
}
.menu-item {
    background: white; border-radius: 14px; margin: 0 16px 8px;
    padding: 18px 16px; display: flex; align-items: center; gap: 14px;
    cursor: pointer; box-shadow: var(--shadow); transition: all .15s;
}
.menu-item:hover { background: #F9FAFB; }
.menu-item-icon {
    width: 40px; height: 40px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center; font-size: 20px;
}
.menu-item-label { font-size: 16px; font-weight: 600; color: var(--text); flex: 1; }
.menu-arrow { color: var(--text3); font-size: 16px; }

/* ── Chat ── */
.chat-header {
    background: var(--green); padding: 40px 20px 24px;
    border-radius: 0 0 24px 24px; position: relative;
}
.chat-logo { font-size: 28px; font-weight: 800; color: white; }
.chat-title { font-size: 22px; font-weight: 700; color: white; margin: 16px 0 8px; }
.chat-sub { font-size: 14px; color: rgba(255,255,255,.8); }
.chat-option {
    background: white; border-radius: 14px; padding: 18px 16px;
    margin: 0 16px 10px; display: flex; align-items: center; gap: 12px;
    cursor: pointer; box-shadow: var(--shadow); transition: all .15s;
}
.chat-option:hover { background: #F9FAFB; }
.chat-bubble {
    border-radius: 18px; padding: 12px 16px; max-width: 80%; word-break: break-word;
    font-size: 14px; line-height: 1.5;
}
.bubble-in { background: #F3F4F6; color: var(--text); border-bottom-left-radius: 4px; }
.bubble-out { background: var(--green); color: white; border-bottom-right-radius: 4px; margin-left: auto; }
.chat-row { display: flex; margin-bottom: 10px; }
.chat-row.out { justify-content: flex-end; }
.chat-time { font-size: 10px; color: var(--text3); margin-top: 4px; text-align: right; }

/* ── Nav ── */
.bottom-nav {
    position: fixed; bottom: 0; left: 50%; transform: translateX(-50%);
    width: 430px; max-width: 430px;
    background: #0f172a; display: flex; justify-content: space-around;
    align-items: center; padding: 12px 8px 20px; z-index: 50;
    border-top: 1px solid rgba(255,255,255,.05);
}
.nav-item {
    display: flex; flex-direction: column; align-items: center;
    gap: 4px; cursor: pointer; padding: 4px 12px; border-radius: 10px;
    transition: all .2s; min-width: 52px;
}
.nav-icon { font-size: 22px; }
.nav-label { font-size: 10px; color: #6B7280; font-weight: 500; white-space: nowrap; }
.nav-item.active .nav-label { color: var(--green); }

/* ── Face ID ── */
.faceid-wrap {
    display: flex; flex-direction: column; align-items: center;
    padding: 32px 20px; gap: 16px;
}
.faceid-frame {
    width: 110px; height: 110px; border-radius: 24px;
    border: 2.5px solid #374151; position: relative;
    display: flex; align-items: center; justify-content: center;
    background: #F9FAFB;
}
.scan-beam {
    position: absolute; left: 8%; right: 8%; height: 2px;
    background: linear-gradient(90deg, transparent, #1C1C1E, transparent);
    top: 10%; border-radius: 1px;
    animation: scanLine 1.6s ease-in-out infinite;
}
.faceid-face { font-size: 48px; }

/* ── Loan ── */
.loan-item {
    background: #F9FAFB; border-radius: 14px; padding: 16px;
    margin-bottom: 10px; display: flex; align-items: flex-start; gap: 14px;
    position: relative;
}
.loan-icon {
    width: 46px; height: 46px; border-radius: 50%;
    background: #92400e; display: flex; align-items: center;
    justify-content: center; font-size: 22px; flex-shrink: 0;
}
.pay-btn-green {
    background: var(--green); color: white; border-radius: 20px;
    padding: 8px 16px; font-size: 13px; font-weight: 600; cursor: pointer;
    border: none; font-family: var(--font);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 0; height: 0; }
</style>
""", unsafe_allow_html=True)
css()

# ─── COMPONENTS ──────────────────────────────────────────────────────────────
def bottom_nav():
    tab = st.session_state.tab
    tabs = [
        ("home", "🏠", "Գլխավոր"),
        ("history", "💳", "Պատմ..."),
        ("transfer", "🔄", "Վճարում..."),
        ("chat", "💬", "Չատ"),
        ("profile", "👤", "Hub"),
    ]
    html = "<div class='bottom-nav'>"
    for key, icon, label in tabs:
        active = "active" if tab == key else ""
        html += f"""
        <div class='nav-item {active}' onclick='void(0)'>
            <span class='nav-icon'>{icon}</span>
            <span class='nav-label'>{label}</span>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (key, icon, label) in enumerate(tabs):
        with cols[i]:
            if st.button(icon, key=f"nav_{key}", help=label):
                st.session_state.tab = key
                st.session_state.send_success = False
                st.session_state.pay_success = False
                st.rerun()

# ─── PIN SCREEN ───────────────────────────────────────────────────────────────
def pin_screen():
    pin = st.session_state.pin
    shake = st.session_state.shake
    err = st.session_state.error
    face = st.session_state.face_scanning

    # Top bar
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("✕", key="pin_close"):
            st.session_state.pin = ""
            st.session_state.error = False
    with col2:
        st.markdown("<div style='text-align:right;padding:8px 0'><span style='border-bottom:1px dashed #888;font-size:14px;cursor:pointer'>Փոխել օգտատիրոջը</span></div>", unsafe_allow_html=True)

    # Title
    st.markdown("<div class='pin-title'>Մուտքագրեք<br>ծածկագիրը</div>", unsafe_allow_html=True)

    # Dots
    dot_html = ""
    for i in range(4):
        cls = ""
        if i < len(pin):
            cls = "error" if err else "filled"
        dot_html += f"<div class='dot {cls}'></div>"

    shake_cls = "shake" if shake else ""
    st.markdown(f"<div class='pin-dots {shake_cls}'>{dot_html}</div>", unsafe_allow_html=True)

    if err:
        st.markdown(f"<div style='text-align:center;color:#EF4444;font-size:14px;margin:-28px 0 20px'>Սխալ ծածկագիր: Կրկին փորձեք</div>", unsafe_allow_html=True)

    # Face ID overlay
    if face:
        if st.session_state.face_done:
            st.markdown("""
            <div class='faceid-wrap'>
                <div class='faceid-frame' style='border-color:#2DB34A;background:#f0fdf4'>
                    <span style='font-size:48px'>✅</span>
                </div>
                <div style='font-size:16px;font-weight:600;color:#2DB34A'>Ճանաչված է</div>
            </div>""", unsafe_allow_html=True)
            time.sleep(0.7)
            db = load_db()
            # Default to marina for face ID
            st.session_state.user_id = "marina"
            st.session_state.logged_in = True
            st.session_state.face_scanning = False
            st.session_state.face_done = False
            st.rerun()
        else:
            st.markdown("""
            <div class='faceid-wrap'>
                <div class='faceid-frame'>
                    <div class='scan-beam'></div>
                    <span class='faceid-face'>🫥</span>
                </div>
                <div style='font-size:15px;color:#6B7280;animation:pulse 1s ease infinite'>Սկանավորում…</div>
            </div>""", unsafe_allow_html=True)
            time.sleep(2)
            st.session_state.face_done = True
            st.rerun()
        return

    # Keypad
    KEYS = [
        ("1",""), ("2","ABC"), ("3","DEF"),
        ("4","GHI"), ("5","JKL"), ("6","MNO"),
        ("7","PQRS"), ("8","TUV"), ("9","WXYZ"),
        ("face",""), ("0",""), ("⌫",""),
    ]
    st.markdown("<div class='key-grid'>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (num, sub) in enumerate(KEYS):
        with cols[i % 3]:
            if num == "face":
                if st.button("🔐", key="k_face"):
                    st.session_state.face_scanning = True
                    st.session_state.face_done = False
                    st.session_state.pin = ""
                    st.session_state.error = False
                    st.rerun()
            elif num == "⌫":
                if st.button("⌫", key="k_back"):
                    if pin:
                        st.session_state.pin = pin[:-1]
                    st.session_state.error = False
                    st.session_state.shake = False
                    st.rerun()
            else:
                if st.button(num, key=f"k_{num}"):
                    if len(pin) < 4:
                        new_pin = pin + num
                        st.session_state.pin = new_pin
                        st.session_state.error = False
                        st.session_state.shake = False
                        if len(new_pin) == 4:
                            db = load_db()
                            matched = None
                            for uid, u in db["users"].items():
                                if u["pin"] == new_pin:
                                    matched = uid
                                    break
                            if matched:
                                st.session_state.user_id = matched
                                st.session_state.logged_in = True
                                st.session_state.pin = ""
                            else:
                                st.session_state.shake = True
                                st.session_state.error = True
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;margin-top:24px'><span class='forgot-pin'>Մոռացե՞լ եք ծածկագիրը</span></div>", unsafe_allow_html=True)

    # Quick user selector (helper)
    st.markdown("<hr style='margin:20px 16px;border:none;border-top:1px solid #E5E7EB'>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:13px;color:#9CA3AF;margin-bottom:10px'>Արագ մուտք (demo)</div>", unsafe_allow_html=True)
    db = load_db()
    ucols = st.columns(len(db["users"]))
    for i, (uid, u) in enumerate(db["users"].items()):
        with ucols[i]:
            if st.button(f"{u['initials']}\n{u['pin']}", key=f"quick_{uid}"):
                st.session_state.user_id = uid
                st.session_state.logged_in = True
                st.session_state.pin = ""
                st.rerun()

# ─── HOME SCREEN ─────────────────────────────────────────────────────────────
def home_screen(user, uid):
    # Header
    st.markdown(f"""
    <div class='app-header'>
        <div class='header-top'>
            <div class='avatar' style='background:{user["color"]}'>{user["initials"]}</div>
            <div class='notif-btn'>🔔<div class='notif-badge'></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Promo banner
    st.markdown("""
    <div style='background:linear-gradient(135deg,#2DB34A,#16a34a);border-radius:18px;
                padding:20px;margin:10px 16px;position:relative;overflow:hidden;
                box-shadow:0 6px 20px rgba(45,179,74,.3)'>
        <div style='font-size:22px;font-weight:800;color:white'>1 CLICK վարկ</div>
        <div style='font-size:14px;color:rgba(255,255,255,.85);margin-top:4px'>Սկսած 16%-ից</div>
        <div style='position:absolute;bottom:-20px;right:-20px;font-size:80px;opacity:.15'>💳</div>
    </div>
    """, unsafe_allow_html=True)

    # Cards section
    st.markdown("<div class='card' style='animation-delay:.05s'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Քարտեր</div>", unsafe_allow_html=True)
    for card in user["cards"]:
        ctype = "VISA" if card["type"] == "VISA" else "MC"
        bal_fmt = f"{card['currency']} {card['balance']:,.0f}"
        st.markdown(f"""
        <div class='card-row'>
            <div class='card-icon'>{ctype}<br>*{card["last4"]}</div>
            <div class='card-info'>
                <div class='card-name'>{card["name"]}</div>
                <div class='card-bal'>{bal_fmt}</div>
            </div>
            <span style='color:#9CA3AF;font-size:18px'>›</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<div class='show-all'>Կանխավճարել</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Accounts
    st.markdown("<div class='card' style='animation-delay:.1s'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Հաշիվներ</div>", unsafe_allow_html=True)
    st.markdown("<div class='acct-grid'>", unsafe_allow_html=True)
    db = load_db()
    fresh_user = db["users"][uid]
    for cur, acct in fresh_user["accounts"].items():
        bal_fmt = f"{acct['currency']} {acct['balance']:,.2f}".rstrip("0").rstrip(".")
        if bal_fmt.endswith("."):
            bal_fmt = bal_fmt[:-1]
        st.markdown(f"""
        <div class='acct-item'>
            <div class='acct-num'>·{acct["number"]}</div>
            <div class='acct-symbol'>{acct["currency"]}</div>
            <div class='acct-name'>{cur} Ընթացիկ հ...</div>
            <div class='acct-bal'>{acct["currency"]} {acct["balance"]:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Loans
    if user["loans"]:
        st.markdown("<div class='card' style='animation-delay:.15s'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Վարկեր</div>", unsafe_allow_html=True)
        for loan in user["loans"]:
            st.markdown(f"""
            <div class='loan-item'>
                <div class='loan-icon'>{loan["icon"]}</div>
                <div style='flex:1'>
                    <div style='font-size:15px;font-weight:600;color:#1C1C1E'>{loan["name"]}</div>
                    <div style='font-size:20px;font-weight:800;color:#1C1C1E;margin:4px 0'>
                        {loan["currency"]} {loan["amount"]:,}
                    </div>
                    <div style='font-size:12px;color:#6B7280'>Մինչև {loan["months_left"]} ամիս</div>
                </div>
                <button class='pay-btn-green'>Վճարել</button>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div class='show-all'>Կանխավճարել</div></div>", unsafe_allow_html=True)

    # Savings
    st.markdown("<div class='card' style='animation-delay:.2s'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Խնայողություններ</div>", unsafe_allow_html=True)
    for sav in user["savings"]:
        st.markdown(f"""
        <div class='savings-item'>
            <div class='savings-icon'>🐷</div>
            <div>
                <div style='font-size:14px;color:#6B7280'>{sav["name"]}</div>
                <div style='font-size:20px;font-weight:700;color:#1C1C1E'>{sav["currency"]} {sav["balance"]:,}</div>
            </div>
        </div>
        <div class='add-savings'>Ավելեք խնայելու</div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ─── HISTORY SCREEN ───────────────────────────────────────────────────────────
def history_screen(user, uid):
    db = load_db()
    fresh = db["users"][uid]
    ms = fresh["monthly_spending"]

    st.markdown("""
    <div class='history-header'>
        <div class='filter-row'>
            <div class='filter-btn'>Ապրիլ ∨</div>
            <div class='filter-btn'>Գումար ∨</div>
            <div class='filter-btn'>Հաշիվներ ∨</div>
            <div class='filter-btn'>Դրա... ∨</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Spending summary
    cat_html = ""
    for c in ms["categories"]:
        cat_html += f"""
        <div class='cat-item'>
            <div class='cat-icon' style='background:{c["color"]}22'>{c["icon"]}</div>
            <div class='cat-amt'>֏ {c["amount"]:,}</div>
        </div>"""

    st.markdown(f"""
    <div class='spending-card'>
        <div class='spending-period'>Ապրիլ ամսին</div>
        <div class='spending-title'>Ծախսեր</div>
        <div class='spending-total'>֏ {ms["total"]:,}</div>
        <div class='progress-bar' style='width:100%'></div>
        <div class='cat-grid'>{cat_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # Group by date
    today_txs = [t for t in fresh["transactions"] if t["date"] == "Այսօր"]
    other_txs = [t for t in fresh["transactions"] if t["date"] != "Այսօր"]

    if today_txs:
        total_today = sum(t["amount"] for t in today_txs)
        sign = "+" if total_today > 0 else ""
        st.markdown(f"""
        <div class='tx-section-title'>
            Այսօր <span class='tx-total'>{sign}֏ {abs(total_today):,}</span>
        </div>
        """, unsafe_allow_html=True)
        for tx in today_txs:
            amt = tx["amount"]
            color = "#2DB34A" if amt > 0 else "#1C1C1E"
            sign = "+" if amt > 0 else "-"
            st.markdown(f"""
            <div class='tx-item'>
                <div class='tx-icon-wrap' style='background:#3b82f6'>{tx["icon"]}</div>
                <div class='tx-info'>
                    <div class='tx-name'>{tx["name"]}</div>
                    <div class='tx-cat'>{tx["category"]}</div>
                </div>
                <div class='tx-right'>
                    <div class='tx-amt' style='color:{color}'>{sign} ֏ {abs(amt):,}</div>
                    <div class='tx-time'>{tx["time"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if other_txs:
        for tx in other_txs:
            amt = tx["amount"]
            color = "#2DB34A" if amt > 0 else "#1C1C1E"
            sign = "+" if amt > 0 else "-"
            st.markdown(f"""
            <div class='tx-section-title'>{tx["date"]}</div>
            <div class='tx-item'>
                <div class='tx-icon-wrap' style='background:#6366f1'>{tx["icon"]}</div>
                <div class='tx-info'>
                    <div class='tx-name'>{tx["name"]}</div>
                    <div class='tx-cat'>{tx["category"]}</div>
                </div>
                <div class='tx-right'>
                    <div class='tx-amt' style='color:{color}'>{sign} ֏ {abs(amt):,}</div>
                    <div class='tx-time'>{tx["time"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─── TRANSFER SCREEN ──────────────────────────────────────────────────────────
def transfer_screen(user, uid):
    db = load_db()

    # Check for incoming notifications
    if "pending_notify" not in st.session_state:
        st.session_state.pending_notify = []

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#4f46e5,#7c3aed);
                padding:48px 20px 28px;border-radius:0 0 24px 24px;
                box-shadow:0 8px 24px rgba(79,70,229,.3)'>
        <div style='font-size:22px;font-weight:800;color:white;margin-bottom:6px'>Փոխանցել</div>
        <div style='font-size:14px;color:rgba(255,255,255,.7)'>Ուղարկեք գումար ակնթարթորեն</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Favorites banner (send to known users)
    st.markdown("<div style='padding:0 16px 8px;font-size:16px;font-weight:700;color:#1C1C1E'>Ում փոխանցել</div>", unsafe_allow_html=True)

    other_users = {k: v for k, v in db["users"].items() if k != uid}
    ucols = st.columns(len(other_users))
    for i, (ouid, ou) in enumerate(other_users.items()):
        with ucols[i]:
            st.markdown(f"""
            <div style='text-align:center;padding:8px'>
                <div style='width:56px;height:56px;border-radius:50%;
                            background:{ou["color"]};color:white;
                            font-size:16px;font-weight:700;
                            display:flex;align-items:center;justify-content:center;
                            margin:0 auto 6px;box-shadow:0 4px 12px {ou["color"]}44'>
                    {ou["initials"]}
                </div>
                <div style='font-size:12px;color:#6B7280;font-weight:500'>
                    {ou["name"].split()[0]}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:17px;font-weight:700;margin-bottom:16px'>Գումար ուղարկել</div>", unsafe_allow_html=True)

    if st.session_state.send_success:
        st.markdown(f"""
        <div class='success-sheet'>
            <div class='success-icon'>✓</div>
            <div style='font-size:22px;font-weight:800;color:#1C1C1E'>Հաջողություն</div>
            <div style='font-size:15px;color:#6B7280;margin-top:6px'>{st.session_state.send_msg}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Վերադառնալ", key="back_success"):
            st.session_state.send_success = False
            st.session_state.send_msg = ""
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Receiver account number
    recv_acct = st.text_input("", placeholder="Ստացողի հաշիվ (օր․ 2001, 3001)", key="recv_acct")
    amt_str = st.text_input("", placeholder="Գումար (֏)", key="send_amt")
    note = st.text_input("", placeholder="Նկատողություն (կամընտիր)", key="send_note")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.button("💸  Ուղարկել", key="do_send", use_container_width=True):
        if not recv_acct.strip() or not amt_str.strip():
            st.warning("Լրացրեք բոլոր դաշտերը")
        else:
            try:
                amount = float(amt_str.strip().replace(",", "").replace("֏", ""))
                if amount <= 0:
                    st.error("Գումարը պետք է դրական լինի")
                else:
                    db2 = load_db()
                    sender = db2["users"][uid]
                    sender_amd = sender["accounts"]["AMD"]["balance"]

                    if amount > sender_amd:
                        st.error(f"Անբավարար միջոցներ. ձեր մնացորդն է ֏ {sender_amd:,.2f}")
                    else:
                        recv_uid, recv_cur = find_user_by_account(recv_acct.strip())
                        if not recv_uid:
                            st.error("Հաշիվը չի գտնվել")
                        elif recv_uid == uid:
                            st.error("Չեք կարող ուղարկել ձեր սեփական հաշվին")
                        else:
                            # Deduct from sender
                            db2["users"][uid]["accounts"]["AMD"]["balance"] -= amount
                            # Add to receiver
                            db2["users"][recv_uid]["accounts"][recv_cur]["balance"] += amount

                            now = datetime.now()
                            time_str = now.strftime("%H:%M")
                            recv_name = db2["users"][recv_uid]["name"]
                            sender_name = db2["users"][uid]["name"]

                            # Add tx to sender
                            db2["users"][uid]["transactions"].insert(0, {
                                "id": f"tx_{now.timestamp()}",
                                "name": f"Փոխ. → {recv_name.split()[0]}",
                                "category": "Փոխանցում",
                                "amount": -amount,
                                "currency": "֏",
                                "date": "Այսօր",
                                "time": time_str,
                                "icon": "💸",
                            })
                            db2["users"][uid]["monthly_spending"]["total"] += amount

                            # Add tx to receiver
                            db2["users"][recv_uid]["transactions"].insert(0, {
                                "id": f"tx_in_{now.timestamp()}",
                                "name": f"Ստացված ← {sender_name.split()[0]}",
                                "category": "Փոխանցում",
                                "amount": amount,
                                "currency": "֏",
                                "date": "Այսօր",
                                "time": time_str,
                                "icon": "📥",
                            })

                            note_txt = f" · {note}" if note.strip() else ""
                            db2["users"][recv_uid]["monthly_spending"]["total"] += amount

                            save_db(db2)
                            st.session_state.send_success = True
                            st.session_state.send_msg = f"֏ {amount:,.0f} ուղարկվեց {recv_name}-ին{note_txt}"
                            st.rerun()
            except ValueError:
                st.error("Մուտքագրեք վավեր գումար")

    st.markdown("</div>", unsafe_allow_html=True)

    # Show all accounts for reference
    st.markdown("<div style='padding:16px 16px 8px;font-size:15px;font-weight:600;color:#6B7280'>Հասանելի հաշիվներ</div>", unsafe_allow_html=True)
    for ouid, ou in other_users.items():
        for cur, acct in ou["accounts"].items():
            if cur == "AMD":
                st.markdown(f"""
                <div style='background:white;border-radius:14px;margin:0 16px 8px;
                            padding:14px 16px;display:flex;align-items:center;gap:12px;
                            box-shadow:0 2px 8px rgba(0,0,0,.06)'>
                    <div style='width:40px;height:40px;border-radius:50%;background:{ou["color"]};
                                color:white;font-size:13px;font-weight:700;
                                display:flex;align-items:center;justify-content:center'>
                        {ou["initials"]}
                    </div>
                    <div style='flex:1'>
                        <div style='font-size:14px;font-weight:600;color:#1C1C1E'>{ou["name"]}</div>
                        <div style='font-size:13px;color:#6B7280'>Հաշիվ #{acct["number"]} · {cur}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ─── CHAT SCREEN ─────────────────────────────────────────────────────────────
def chat_screen(user, uid):
    st.markdown(f"""
    <div class='chat-header'>
        <div style='display:flex;justify-content:space-between;align-items:center'>
            <div style='font-size:24px;font-weight:800;color:white'>≫</div>
            <div style='color:white;font-size:20px;cursor:pointer'>✕</div>
        </div>
        <div class='chat-title'>Բարև {user["name"].split()[0]} 🤍<br>Գրեք մեզ այստեղ<br><span style='font-size:18px'>Contact us here</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if not st.session_state.chat_msgs:
        st.session_state.chat_msgs = [
            {"role": "in", "text": "Բարև! Ինչպե՞ս կարող եմ օգնել ձեզ 😊", "time": "22:40"},
        ]

    # Chat bubbles
    for msg in st.session_state.chat_msgs:
        align = "out" if msg["role"] == "out" else ""
        bubble_cls = "bubble-out" if msg["role"] == "out" else "bubble-in"
        st.markdown(f"""
        <div class='chat-row {align}'>
            <div>
                <div class='chat-bubble {bubble_cls}'>{msg["text"]}</div>
                <div class='chat-time'>{msg["time"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        msg_input = st.text_input("", placeholder="Հաղորդագրություն...", key="chat_input", label_visibility="collapsed")
    with col2:
        if st.button("➤", key="chat_send"):
            if msg_input.strip():
                now = datetime.now().strftime("%H:%M")
                st.session_state.chat_msgs.append({"role": "out", "text": msg_input.strip(), "time": now})
                # Auto reply
                replies = [
                    "Շնորհակալություն հարցի համար: Կատարում ենք...",
                    "Ձեր հարցն ընդունված է: Մի քանի րոպեում կպատասխանենք:",
                    "Կօգնենք ձեզ: Խնդրում ենք սպասել:",
                ]
                import random
                st.session_state.chat_msgs.append({
                    "role": "in",
                    "text": random.choice(replies),
                    "time": now
                })
                st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='chat-option'><span style='font-size:20px'>💬</span>
        <div style='flex:1;font-size:15px;font-weight:600'>Messages</div>
        <span style='color:#9CA3AF'>▪</span>
    </div>
    <div class='chat-option'><span style='font-size:20px'>📞</span>
        <div style='flex:1;font-size:15px;font-weight:600'>Contact us</div>
        <span style='color:#9CA3AF'>▶</span>
    </div>
    """, unsafe_allow_html=True)

# ─── PROFILE SCREEN ──────────────────────────────────────────────────────────
def profile_screen(user, uid):
    st.markdown(f"""
    <div class='profile-bg'>
        <div class='profile-avatar' style='background:{user["color"]}'>{user["initials"]}</div>
        <div class='profile-name'>{user["name"]}</div>
        <div style='margin-top:12px;display:inline-flex;align-items:center;gap:8px;
                    background:#1C1C1E;color:white;border-radius:22px;
                    padding:10px 20px;font-size:14px;font-weight:600;cursor:pointer;
                    box-shadow:0 4px 12px rgba(0,0,0,.3)'>
            ≫ START Փաթեթ ›
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    menu = [
        ("🟢", "#dcfce7", "Իմ էջը", ">"),
        ("🔵", "#dbeafe", "Անվտանգություն", ">"),
        ("⚫", "#f3f4f6", "Կարգավորումներ", ">"),
    ]
    for icon, bg, label, arrow in menu:
        st.markdown(f"""
        <div class='menu-item'>
            <div class='menu-item-icon' style='background:{bg}'>{icon}</div>
            <div class='menu-item-label'>{label}</div>
            <div class='menu-arrow'>{arrow}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.button("🔒  Դուրս գալ", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.pin = ""
        st.session_state.tab = "home"
        st.rerun()

    st.markdown("""
    <div style='text-align:center;margin-top:20px;font-size:12px;color:#9CA3AF'>
        Powered by <span style='color:#F59E0B;font-weight:700;text-decoration:underline'>HIGHWAY</span> version 1.0.1
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    pin_screen()
else:
    uid = st.session_state.user_id
    db = load_db()
    user = db["users"].get(uid)
    if not user:
        st.session_state.logged_in = False
        st.rerun()

    tab = st.session_state.tab

    # Check for new incoming transactions (notify)
    fresh = db["users"][uid]
    recent = fresh["transactions"][:1] if fresh["transactions"] else []
    if recent and recent[0].get("icon") == "📥":
        if not st.session_state.get("last_notif_id") or st.session_state.last_notif_id != recent[0]["id"]:
            st.session_state.last_notif_id = recent[0]["id"]
            st.markdown(f"""
            <div class='notify-badge'>
                <span style='font-size:22px'>📥</span>
                <div>
                    <div style='font-size:14px;font-weight:700'>Ստացված փոխանցում</div>
                    <div style='font-size:13px;opacity:.9'>{recent[0]["name"]} — ֏ {abs(recent[0]["amount"]):,.0f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if tab == "home":
        home_screen(user, uid)
    elif tab == "history":
        history_screen(user, uid)
    elif tab == "transfer":
        transfer_screen(user, uid)
    elif tab == "chat":
        chat_screen(user, uid)
    elif tab == "profile":
        profile_screen(user, uid)

    bottom_nav()
