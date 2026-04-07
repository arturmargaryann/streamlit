import streamlit as st
import time
import random
from datetime import datetime, timedelta

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Streamlit Bank",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
CORRECT_PIN = "1234"
BALANCE = 12450.00
CARD_NUMBER = "**** **** **** 4291"
CARD_HOLDER = "Alex Johnson"

TRANSLATIONS = {
    "en": {
        "app_name": "Streamlit Bank",
        "balance_preview": "Balance Preview",
        "enter_pin": "Enter your PIN",
        "wrong_pin": "Incorrect PIN. Try again.",
        "face_id": "Face ID",
        "face_id_scanning": "Scanning…",
        "face_id_success": "Face ID recognized!",
        "good_morning": "Good morning",
        "total_balance": "Total Balance",
        "send_money": "Send Money",
        "recent_transactions": "Recent Transactions",
        "amount": "Amount ($)",
        "receiver": "Receiver name or account",
        "send": "Send",
        "success_sent": "Money sent successfully!",
        "logout": "Lock",
        "card_holder": "Card Holder",
        "valid_thru": "Valid Thru",
        "income": "Income",
        "expenses": "Expenses",
        "savings": "Savings",
        "all_transactions": "All Transactions",
        "enter_amount": "Enter amount",
        "enter_receiver": "Enter receiver",
        "dashboard": "Dashboard",
        "analytics": "Analytics",
        "settings": "Settings",
    },
    "ru": {
        "app_name": "Streamlit Банк",
        "balance_preview": "Предпросмотр баланса",
        "enter_pin": "Введите PIN-код",
        "wrong_pin": "Неверный PIN. Попробуйте снова.",
        "face_id": "Face ID",
        "face_id_scanning": "Сканирование…",
        "face_id_success": "Face ID распознан!",
        "good_morning": "Доброе утро",
        "total_balance": "Общий баланс",
        "send_money": "Отправить деньги",
        "recent_transactions": "Последние операции",
        "amount": "Сумма ($)",
        "receiver": "Получатель",
        "send": "Отправить",
        "success_sent": "Деньги успешно отправлены!",
        "logout": "Заблокировать",
        "card_holder": "Владелец карты",
        "valid_thru": "Действует до",
        "income": "Доходы",
        "expenses": "Расходы",
        "savings": "Сбережения",
        "all_transactions": "Все операции",
        "enter_amount": "Введите сумму",
        "enter_receiver": "Введите получателя",
        "dashboard": "Главная",
        "analytics": "Аналитика",
        "settings": "Настройки",
    },
}

TRANSACTIONS = [
    {"icon": "🛒", "name": "Whole Foods Market", "category": "Groceries", "amount": -84.20, "date": "Today, 10:32"},
    {"icon": "☕", "name": "Blue Bottle Coffee", "category": "Food & Drink", "amount": -6.50, "date": "Today, 08:15"},
    {"icon": "💼", "name": "Salary Deposit", "category": "Income", "amount": 4200.00, "date": "Yesterday"},
    {"icon": "🏋️", "name": "Equinox Gym", "category": "Health", "amount": -55.00, "date": "Apr 5"},
    {"icon": "🎵", "name": "Spotify Premium", "category": "Entertainment", "amount": -9.99, "date": "Apr 4"},
    {"icon": "🚕", "name": "Uber", "category": "Transport", "amount": -18.40, "date": "Apr 3"},
    {"icon": "📱", "name": "Apple Store", "category": "Shopping", "amount": -129.00, "date": "Apr 2"},
    {"icon": "💸", "name": "Transfer from Mike", "category": "Income", "amount": 250.00, "date": "Apr 1"},
]

# ─── SESSION STATE ────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "logged_in": False,
        "pin": "",
        "shake": False,
        "error": False,
        "face_id_scanning": False,
        "face_id_success": False,
        "unlock_animation": False,
        "lang": "en",
        "send_success": False,
        "active_tab": "dashboard",
        "balance": BALANCE,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def t(key):
    return TRANSLATIONS[st.session_state.lang].get(key, key)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg: #0a0a0f;
        --bg2: #111118;
        --card: #1a1a24;
        --card2: #22222e;
        --border: rgba(255,255,255,0.08);
        --text: #f0f0f5;
        --text2: #8e8ea0;
        --accent: #4f8ef7;
        --accent2: #6fa3ff;
        --success: #30d158;
        --danger: #ff453a;
        --gold: #ffd60a;
        --radius: 20px;
        --font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    html, body, [class*="css"] {
        font-family: var(--font) !important;
        background: var(--bg) !important;
        color: var(--text) !important;
    }

    .stApp {
        background: var(--bg) !important;
        max-width: 440px;
        margin: 0 auto;
    }

    .block-container {
        padding: 0 !important;
        max-width: 440px !important;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header, .stDeployButton,
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] { display: none !important; }

    .stButton > button {
        all: unset;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    div[data-testid="stVerticalBlock"] > div { padding: 0 !important; }
    div[data-testid="element-container"] { margin: 0 !important; }
    .stMarkdown { margin: 0 !important; }

    /* ── Animations ── */
    @keyframes shake {
        0%,100%{transform:translateX(0)}
        10%{transform:translateX(-8px)}
        20%{transform:translateX(8px)}
        30%{transform:translateX(-8px)}
        40%{transform:translateX(8px)}
        50%{transform:translateX(-6px)}
        60%{transform:translateX(6px)}
        70%{transform:translateX(-4px)}
        80%{transform:translateX(4px)}
        90%{transform:translateX(-2px)}
    }

    @keyframes fadeIn {
        from { opacity:0; transform:translateY(20px); }
        to   { opacity:1; transform:translateY(0); }
    }

    @keyframes slideUp {
        from { opacity:0; transform:translateY(40px); }
        to   { opacity:1; transform:translateY(0); }
    }

    @keyframes scaleIn {
        from { opacity:0; transform:scale(0.85); }
        to   { opacity:1; transform:scale(1); }
    }

    @keyframes pulse {
        0%,100%{opacity:1;transform:scale(1)}
        50%{opacity:.6;transform:scale(1.04)}
    }

    @keyframes scanLine {
        0%   { top: 8%; opacity:.8; }
        50%  { top: 88%; opacity:1; }
        100% { top: 8%; opacity:.8; }
    }

    @keyframes scanRing {
        0%   { transform:scale(1);   opacity:.8; box-shadow:0 0 0 0 rgba(79,142,247,.7); }
        70%  { transform:scale(1.06);opacity:.4; box-shadow:0 0 0 16px rgba(79,142,247,0); }
        100% { transform:scale(1);   opacity:.8; box-shadow:0 0 0 0 rgba(79,142,247,0); }
    }

    @keyframes unlockGlow {
        0%   { box-shadow:0 0 0 0 rgba(48,209,88,.5); }
        50%  { box-shadow:0 0 40px 20px rgba(48,209,88,.25); }
        100% { box-shadow:0 0 0 0 rgba(48,209,88,0); }
    }

    @keyframes checkmark {
        0%   { stroke-dashoffset:50; opacity:0; }
        100% { stroke-dashoffset:0;  opacity:1; }
    }

    @keyframes float {
        0%,100%{transform:translateY(0)}
        50%{transform:translateY(-6px)}
    }

    @keyframes shimmer {
        0%   { background-position: -200% 0; }
        100% { background-position:  200% 0; }
    }

    /* ── Components ── */
    .ios-card {
        background: linear-gradient(135deg,#1e1e2e,#252535);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 20px;
        margin: 8px 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,.4);
        animation: fadeIn .5s ease both;
    }

    .credit-card {
        background: linear-gradient(135deg,#1a1a3e 0%,#2d1b5e 50%,#1a3a5e 100%);
        border-radius: 22px;
        padding: 28px 26px;
        margin: 8px 16px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,.5), 0 0 0 1px rgba(255,255,255,.06);
        animation: scaleIn .4s cubic-bezier(.34,1.56,.64,1) both;
    }

    .credit-card::before {
        content:'';
        position:absolute;
        top:-40%;left:-20%;
        width:70%;height:180%;
        background: radial-gradient(ellipse,rgba(255,255,255,.07) 0%,transparent 70%);
        pointer-events:none;
    }

    .credit-card::after {
        content:'';
        position:absolute;
        bottom:-30%;right:-10%;
        width:55%;height:120%;
        background: radial-gradient(ellipse,rgba(79,142,247,.15) 0%,transparent 70%);
        pointer-events:none;
    }

    .pin-display {
        display:flex;
        gap:18px;
        justify-content:center;
        margin:24px 0 16px;
    }

    .pin-dot {
        width:16px;height:16px;
        border-radius:50%;
        border:2px solid rgba(255,255,255,.25);
        transition: all .2s cubic-bezier(.34,1.56,.64,1);
    }

    .pin-dot.filled {
        background: var(--accent);
        border-color: var(--accent);
        box-shadow: 0 0 12px rgba(79,142,247,.6);
        transform: scale(1.15);
    }

    .pin-dot.error {
        background: var(--danger);
        border-color: var(--danger);
        box-shadow: 0 0 12px rgba(255,69,58,.6);
    }

    .pin-container.shake {
        animation: shake .5s cubic-bezier(.36,.07,.19,.97) both;
    }

    .keypad {
        display:grid;
        grid-template-columns:repeat(3,1fr);
        gap:12px;
        padding:0 24px;
        margin-top:16px;
    }

    .key-btn {
        background: var(--card2);
        border: 1px solid var(--border);
        border-radius:50%;
        width:72px;height:72px;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        cursor:pointer;
        transition: all .15s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,.3);
        margin:0 auto;
    }

    .key-btn:active, .key-btn:hover {
        background: var(--card);
        transform: scale(.94);
        box-shadow: 0 2px 6px rgba(0,0,0,.2);
    }

    .key-btn .num {
        font-size:24px;
        font-weight:400;
        color:var(--text);
        line-height:1;
    }

    .key-btn .sub {
        font-size:8px;
        color:var(--text2);
        letter-spacing:1.5px;
        text-transform:uppercase;
        margin-top:2px;
    }

    .key-btn.special {
        background:transparent;
        border-color:transparent;
        box-shadow:none;
    }

    .balance-blur {
        filter:blur(12px);
        user-select:none;
        font-size:42px;
        font-weight:700;
        color:var(--text);
        letter-spacing:-1px;
        text-align:center;
        margin:8px 0 4px;
        animation: float 4s ease-in-out infinite;
    }

    .face-id-container {
        display:flex;
        flex-direction:column;
        align-items:center;
        gap:16px;
        padding:20px;
    }

    .face-id-frame {
        width:110px;height:110px;
        border-radius:28px;
        border:2px solid var(--accent);
        position:relative;
        display:flex;align-items:center;justify-content:center;
        animation: scanRing 1.8s ease-in-out infinite;
        background: rgba(79,142,247,.05);
    }

    .face-id-frame.success {
        border-color:var(--success);
        animation: none;
        box-shadow:0 0 30px rgba(48,209,88,.3);
    }

    .scan-line {
        position:absolute;
        left:8%;right:8%;
        height:2px;
        background:linear-gradient(90deg,transparent,var(--accent),transparent);
        border-radius:1px;
        animation: scanLine 1.8s ease-in-out infinite;
        box-shadow:0 0 8px var(--accent);
    }

    .face-icon {
        font-size:44px;
        filter:drop-shadow(0 0 8px rgba(79,142,247,.4));
    }

    .nav-bar {
        display:flex;
        justify-content:space-around;
        align-items:center;
        padding:12px 20px 20px;
        background:rgba(17,17,24,.92);
        backdrop-filter:blur(20px);
        border-top:1px solid var(--border);
        position:sticky;bottom:0;
        margin:0 -16px;
    }

    .nav-item {
        display:flex;flex-direction:column;align-items:center;
        gap:4px;cursor:pointer;padding:6px 16px;border-radius:12px;
        transition:all .2s ease;
    }

    .nav-item.active { background:rgba(79,142,247,.12); }
    .nav-item .nav-icon { font-size:22px; }
    .nav-item .nav-label { font-size:10px;color:var(--text2);font-weight:500; }
    .nav-item.active .nav-label { color:var(--accent); }

    .tx-row {
        display:flex;align-items:center;gap:14px;
        padding:14px 0;
        border-bottom:1px solid rgba(255,255,255,.04);
    }
    .tx-icon {
        width:46px;height:46px;border-radius:14px;
        background:var(--card2);
        display:flex;align-items:center;justify-content:center;
        font-size:22px;flex-shrink:0;
    }
    .tx-info { flex:1; }
    .tx-name { font-size:15px;font-weight:500;color:var(--text); }
    .tx-cat  { font-size:12px;color:var(--text2);margin-top:2px; }
    .tx-right { text-align:right; }
    .tx-amt  { font-size:15px;font-weight:600; }
    .tx-amt.pos { color:var(--success); }
    .tx-amt.neg { color:var(--text); }
    .tx-date { font-size:11px;color:var(--text2);margin-top:2px; }

    .stat-card {
        background:var(--card2);
        border-radius:16px;
        padding:16px;
        text-align:center;
        border:1px solid var(--border);
        flex:1;
    }
    .stat-label { font-size:11px;color:var(--text2);margin-bottom:6px;font-weight:500; }
    .stat-value { font-size:20px;font-weight:700; }
    .stat-value.pos { color:var(--success); }
    .stat-value.neg { color:var(--danger); }
    .stat-value.neu { color:var(--accent); }

    .send-input {
        background:var(--card2) !important;
        border:1px solid var(--border) !important;
        border-radius:14px !important;
        color:var(--text) !important;
        padding:14px 16px !important;
        font-size:16px !important;
        width:100% !important;
        outline:none !important;
        font-family:var(--font) !important;
    }

    .send-btn {
        background:linear-gradient(135deg,var(--accent),#5a7fff);
        border:none;border-radius:14px;
        color:#fff;font-size:17px;font-weight:600;
        padding:16px;width:100%;cursor:pointer;
        transition:all .2s ease;
        box-shadow:0 8px 24px rgba(79,142,247,.35);
        font-family:var(--font);
    }
    .send-btn:hover { transform:translateY(-2px); box-shadow:0 12px 30px rgba(79,142,247,.45); }
    .send-btn:active { transform:scale(.97); }

    .success-overlay {
        display:flex;flex-direction:column;align-items:center;
        justify-content:center;gap:16px;padding:32px;
        animation:scaleIn .4s cubic-bezier(.34,1.56,.64,1) both;
    }
    .success-ring {
        width:80px;height:80px;border-radius:50%;
        background:rgba(48,209,88,.15);
        border:2px solid var(--success);
        display:flex;align-items:center;justify-content:center;
        font-size:36px;
        animation:unlockGlow 1.5s ease-out;
    }

    .unlock-flash {
        position:fixed;inset:0;
        background:rgba(48,209,88,.08);
        pointer-events:none;
        animation:unlockGlow 0.8s ease-out forwards;
        z-index:9999;
    }

    .lang-btn {
        background:var(--card2);
        border:1px solid var(--border);
        border-radius:10px;
        color:var(--text);
        padding:6px 12px;
        font-size:13px;
        cursor:pointer;
        font-family:var(--font);
        transition:all .2s ease;
    }
    .lang-btn:hover { background:var(--card); }

    .lock-btn {
        background:rgba(255,69,58,.1);
        border:1px solid rgba(255,69,58,.25);
        border-radius:10px;
        color:var(--danger);
        padding:6px 12px;
        font-size:13px;
        cursor:pointer;
        font-family:var(--font);
        transition:all .2s ease;
    }
    .lock-btn:hover { background:rgba(255,69,58,.18); }

    .shimmer-bar {
        height:18px;border-radius:6px;
        background:linear-gradient(90deg,var(--card) 25%,var(--card2) 50%,var(--card) 75%);
        background-size:200% 100%;
        animation:shimmer 1.5s infinite;
    }

    input[type="text"], input[type="number"] {
        background:var(--card2) !important;
        color:var(--text) !important;
        border:1px solid var(--border) !important;
        border-radius:14px !important;
        padding:14px 16px !important;
        font-family:var(--font) !important;
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def render_header(show_lock=False):
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        lang_label = "🇷🇺 RU" if st.session_state.lang == "en" else "🇺🇸 EN"
        if st.button(lang_label, key="lang_toggle"):
            st.session_state.lang = "ru" if st.session_state.lang == "en" else "en"
            st.rerun()
    with col2:
        st.markdown(f"<div style='text-align:center;font-size:17px;font-weight:700;padding:12px 0 8px;letter-spacing:-.3px'>{t('app_name')}</div>", unsafe_allow_html=True)
    with col3:
        if show_lock:
            if st.button(t("logout"), key="logout_btn"):
                st.session_state.logged_in = False
                st.session_state.pin = ""
                st.session_state.error = False
                st.session_state.send_success = False
                st.rerun()

# ─── LOGIN SCREEN ─────────────────────────────────────────────────────────────
def login_screen():
    render_header()

    # Blurred balance
    st.markdown("""
    <div style='text-align:center;padding:20px 16px 8px'>
        <div style='font-size:12px;color:#8e8ea0;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px'>""" + t("balance_preview") + """</div>
        <div class='balance-blur'>$12,450.00</div>
        <div style='font-size:12px;color:#8e8ea0;margin-top:4px'>●●●● ●●●● ●●●● 4291</div>
    </div>
    """, unsafe_allow_html=True)

    # PIN display
    pin_len = len(st.session_state.pin)
    shake_class = "shake" if st.session_state.shake else ""
    dot_color = "error" if st.session_state.error else ""

    dots_html = ""
    for i in range(4):
        cls = "filled" if i < pin_len else ""
        if i < pin_len and st.session_state.error:
            cls = "error"
        dots_html += f"<div class='pin-dot {cls}'></div>"

    st.markdown(f"""
    <div style='text-align:center;margin-top:8px'>
        <div style='font-size:15px;font-weight:500;color:#8e8ea0'>{t("enter_pin")}</div>
        <div class='pin-container {shake_class}'>
            <div class='pin-display'>{dots_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.error:
        st.markdown(f"<div style='text-align:center;color:#ff453a;font-size:13px;margin-bottom:8px'>{t('wrong_pin')}</div>", unsafe_allow_html=True)

    # ── Numeric Keypad ──
    st.markdown("<div class='keypad'>", unsafe_allow_html=True)

    KEYS = [
        ("1",""), ("2","ABC"), ("3","DEF"),
        ("4","GHI"), ("5","JKL"), ("6","MNO"),
        ("7","PQRS"), ("8","TUV"), ("9","WXYZ"),
        ("face",""), ("0",""), ("⌫",""),
    ]

    cols = st.columns(3)
    for idx, (num, sub) in enumerate(KEYS):
        col_idx = idx % 3
        with cols[col_idx]:
            if num == "face":
                if st.button("🔐", key="key_face", help="Face ID"):
                    st.session_state.face_id_scanning = True
                    st.session_state.error = False
                    st.session_state.pin = ""
                    st.rerun()
            elif num == "⌫":
                if st.button("⌫", key="key_back"):
                    if st.session_state.pin:
                        st.session_state.pin = st.session_state.pin[:-1]
                    st.session_state.error = False
                    st.session_state.shake = False
                    st.rerun()
            else:
                btn_label = f"**{num}**" if not sub else f"**{num}**\n{sub}"
                if st.button(num, key=f"key_{num}"):
                    if len(st.session_state.pin) < 4:
                        st.session_state.pin += num
                        st.session_state.error = False
                        st.session_state.shake = False
                    if len(st.session_state.pin) == 4:
                        if st.session_state.pin == CORRECT_PIN:
                            st.session_state.unlock_animation = True
                            st.session_state.logged_in = True
                            st.session_state.pin = ""
                            st.session_state.error = False
                        else:
                            st.session_state.shake = True
                            st.session_state.error = True
                            time.sleep(0.05)
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Face ID modal
    if st.session_state.face_id_scanning:
        face_id_modal()

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

def face_id_modal():
    if st.session_state.face_id_success:
        st.markdown(f"""
        <div class='face-id-container'>
            <div class='face-id-frame success'>
                <div style='font-size:44px'>✅</div>
            </div>
            <div style='font-size:15px;color:#30d158;font-weight:600'>{t("face_id_success")}</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.8)
        st.session_state.logged_in = True
        st.session_state.face_id_scanning = False
        st.session_state.face_id_success = False
        st.session_state.unlock_animation = True
        st.rerun()
    else:
        st.markdown(f"""
        <div class='face-id-container'>
            <div class='face-id-frame'>
                <div class='scan-line'></div>
                <div class='face-icon'>🫥</div>
            </div>
            <div style='font-size:15px;color:#8e8ea0;animation:pulse 1s ease-in-out infinite'>{t("face_id_scanning")}</div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(2)
        st.session_state.face_id_success = True
        st.rerun()

# ─── DASHBOARD ────────────────────────────────────────────────────────────────
def dashboard():
    if st.session_state.unlock_animation:
        st.markdown("<div class='unlock-flash'></div>", unsafe_allow_html=True)
        st.session_state.unlock_animation = False

    render_header(show_lock=True)

    # Greeting
    hour = datetime.now().hour
    if hour < 12:
        greet_emoji = "🌅"
    elif hour < 18:
        greet_emoji = "☀️"
    else:
        greet_emoji = "🌙"
    st.markdown(f"""
    <div style='padding:8px 20px 4px;animation:fadeIn .5s ease'>
        <div style='font-size:14px;color:#8e8ea0'>{greet_emoji} {t("good_morning")}, {CARD_HOLDER.split()[0]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Credit Card Visual
    st.markdown(f"""
    <div class='credit-card' style='animation-delay:.1s'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:30px'>
            <div>
                <div style='font-size:11px;color:rgba(255,255,255,.5);letter-spacing:1px;text-transform:uppercase'>{t("app_name")}</div>
                <div style='font-size:11px;color:rgba(255,255,255,.35);margin-top:2px'>Premium</div>
            </div>
            <div style='display:flex;gap:4px'>
                <div style='width:28px;height:28px;border-radius:50%;background:rgba(255,200,0,.7)'></div>
                <div style='width:28px;height:28px;border-radius:50%;background:rgba(255,120,0,.5);margin-left:-12px'></div>
            </div>
        </div>
        <div style='font-size:13px;color:rgba(255,255,255,.5);letter-spacing:3px;font-family:monospace;margin-bottom:24px'>{CARD_NUMBER}</div>
        <div style='display:flex;justify-content:space-between;align-items:flex-end'>
            <div>
                <div style='font-size:9px;color:rgba(255,255,255,.4);letter-spacing:1px;text-transform:uppercase'>{t("card_holder")}</div>
                <div style='font-size:14px;font-weight:600;color:rgba(255,255,255,.9);margin-top:2px'>{CARD_HOLDER}</div>
            </div>
            <div style='text-align:right'>
                <div style='font-size:9px;color:rgba(255,255,255,.4);letter-spacing:1px;text-transform:uppercase'>{t("valid_thru")}</div>
                <div style='font-size:14px;font-weight:600;color:rgba(255,255,255,.9);margin-top:2px'>08 / 28</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Balance
    bal = st.session_state.balance
    st.markdown(f"""
    <div style='text-align:center;padding:20px 16px 8px;animation:slideUp .5s ease .15s both'>
        <div style='font-size:12px;color:#8e8ea0;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px'>{t("total_balance")}</div>
        <div style='font-size:48px;font-weight:800;letter-spacing:-2px;color:#f0f0f5'>${bal:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    st.markdown("""
    <div style='display:flex;gap:10px;padding:8px 16px;animation:slideUp .5s ease .2s both'>
        <div class='stat-card'>
            <div class='stat-label'>""" + t("income") + """</div>
            <div class='stat-value pos'>+$4,450</div>
        </div>
        <div class='stat-card'>
            <div class='stat-label'>""" + t("expenses") + """</div>
            <div class='stat-value neg'>-$1,203</div>
        </div>
        <div class='stat-card'>
            <div class='stat-label'>""" + t("savings") + """</div>
            <div class='stat-value neu'>$3,247</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation tabs
    tab_opts = [t("send_money"), t("recent_transactions")]
    tab_icons = ["💸", "📋"]
    active_tab = st.session_state.get("active_tab", "send")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"{tab_icons[0]} {tab_opts[0]}", key="tab_send", use_container_width=True):
            st.session_state.active_tab = "send"
            st.session_state.send_success = False
            st.rerun()
    with col2:
        if st.button(f"{tab_icons[1]} {tab_opts[1]}", key="tab_tx", use_container_width=True):
            st.session_state.active_tab = "transactions"
            st.rerun()

    st.markdown("<div style='margin:0 16px;'>", unsafe_allow_html=True)

    if st.session_state.active_tab == "send":
        send_money_panel()
    else:
        transactions_panel()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

def send_money_panel():
    if st.session_state.send_success:
        st.markdown(f"""
        <div class='ios-card success-overlay'>
            <div class='success-ring'>✓</div>
            <div style='font-size:20px;font-weight:700;color:#30d158'>{t("success_sent")}</div>
            <div style='font-size:14px;color:#8e8ea0'>Transaction completed</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Back", key="back_from_success"):
            st.session_state.send_success = False
            st.rerun()
        return

    st.markdown(f"<div class='ios-card' style='animation-delay:.3s'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:17px;font-weight:700;margin-bottom:16px'>{t('send_money')}</div>", unsafe_allow_html=True)

    amount = st.text_input("", placeholder=t("enter_amount"), key="send_amount", label_visibility="collapsed")
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    receiver = st.text_input("", placeholder=t("enter_receiver"), key="send_receiver", label_visibility="collapsed")
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if st.button(f"💸  {t('send')}", key="send_btn", use_container_width=True):
        if amount and receiver:
            try:
                amt = float(amount.replace("$","").replace(",",""))
                if amt > 0 and amt <= st.session_state.balance:
                    st.session_state.balance -= amt
                    st.session_state.send_success = True
                    st.rerun()
                elif amt > st.session_state.balance:
                    st.error("Insufficient funds.")
                else:
                    st.error("Enter a valid amount.")
            except:
                st.error("Enter a valid amount.")
        else:
            st.warning("Please fill in all fields.")

    st.markdown("</div>", unsafe_allow_html=True)

def transactions_panel():
    st.markdown(f"<div class='ios-card' style='animation-delay:.3s'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:17px;font-weight:700;margin-bottom:8px'>{t('recent_transactions')}</div>", unsafe_allow_html=True)

    for tx in TRANSACTIONS:
        amt = tx["amount"]
        amt_cls = "pos" if amt > 0 else "neg"
        amt_str = f"+${amt:,.2f}" if amt > 0 else f"-${abs(amt):,.2f}"
        st.markdown(f"""
        <div class='tx-row'>
            <div class='tx-icon'>{tx["icon"]}</div>
            <div class='tx-info'>
                <div class='tx-name'>{tx["name"]}</div>
                <div class='tx-cat'>{tx["category"]}</div>
            </div>
            <div class='tx-right'>
                <div class='tx-amt {amt_cls}'>{amt_str}</div>
                <div class='tx-date'>{tx["date"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if st.session_state.logged_in:
    dashboard()
else:
    login_screen()
