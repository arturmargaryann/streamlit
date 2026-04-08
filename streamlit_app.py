import streamlit as st
import json, os, time, random
from datetime import datetime

st.set_page_config(page_title="Highway Bank", page_icon="🏦",
                   layout="centered", initial_sidebar_state="collapsed")

DB_FILE = "/tmp/hwbank_v3.json"

SEED = {
    "users": {
        "Մարինա": {
            "name": "Մարինա Մարգարյան", "initials": "ՄՄ", "pin": "7628", "color": "#a855f7",
            "amd": 13029.20, "usd": 0.0, "eur": 0.0, "rub": 0.0,
            "card_bal": 1802.0, "card_num": "0355", "card_type": "VISA",
            "has_loan": True, "loan_name": "Թանկարժեք իրեր", "loan_amt": 349000, "loan_mo": 17,
            "sav_amd": 13029, "sav_usd": 0, "sav_eur": 0,
            "txs": [
                {"icon": "🏪", "name": "CARREFOUR ARGISH...", "cat": "ԳՆում", "amt": -340, "date": "Today", "t": "18:04"},
                {"icon": "🏪", "name": "HOME GROUP",         "cat": "Գնում", "amt": -220, "date": "Today", "t": "08:52"},
                {"icon": "💼", "name": "Salary",             "cat": "Income","amt": 50000,"date": "Apr 1","t": "09:00"},
            ]
        },
        "Արթուր": {
            "name": "Արթուր Մարգարյան", "initials": "ԱՄ", "pin": "2222", "color": "#3b82f6",
            "amd": 25000.0, "usd": 50.0, "eur": 10.0, "rub": 0.0,
            "card_bal": 5500.0, "card_num": "1122", "card_type": "VISA",
            "has_loan": False, "loan_name": "", "loan_amt": 0, "loan_mo": 0,
            "sav_amd": 8000, "sav_usd": 100, "sav_eur": 0,
            "txs": [
                {"icon": "🏪", "name": "Yerevan City", "cat": "Shopping","amt": -450,"date": "Today","t": "14:30"},
                {"icon": "💼", "name": "Salary",       "cat": "Income",  "amt": 80000,"date": "Apr 1","t": "09:00"},
            ]
        },
        "Դավիթ": {
            "name": "Davit Grigoryan", "initials": "ԴԳ", "pin": "3333", "color": "#10b981",
            "amd": 50000.0, "usd": 200.0, "eur": 0.0, "rub": 500.0,
            "card_bal": 12000.0, "card_num": "9988", "card_type": "MC",
            "has_loan": True, "loan_name": "Home Loan", "loan_amt": 2500000, "loan_mo": 120,
            "sav_amd": 30000, "sav_usd": 500, "sav_eur": 200,
            "txs": [
                {"icon": "🏠", "name": "Utility bill","cat": "Utility","amt": -15000,"date": "Today","t": "10:00"},
                {"icon": "💼", "name": "Salary",      "cat": "Income", "amt": 150000,"date": "Apr 1","t": "09:00"},
            ]
        }
    }
}

ACCT = {"marina": "1001", "artur": "2001", "davit": "3001"}

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(SEED, f, ensure_ascii=False)
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False)

def find_uid_by_acct(acct):
    for uid, num in ACCT.items():
        if num == acct.strip():
            return uid
    return None

# ── Session state ─────────────────────────────────────────────────────────────
DEFAULTS = {
    "logged_in": False, "uid": None, "pin": "",
    "pin_err": False, "pin_shake": False,
    "face_scanning": False, "face_done": False,
    "tab": "home",
    "bal_vis": False,
    "send_ok": False, "send_msg": "",
    "chat_msgs": [{"r": "bot", "t": "Hello! 👋 How can I help?"}],
    "_last_toast": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Onest:wght@300;400;500;600;700;800;900&display=swap');
*{box-sizing:border-box}
:root{
  --bg:#F2F2F7;--w:#fff;--grn:#2DB34A;--dk:#1C1C1E;
  --g2:#6B7280;--g3:#9CA3AF;--g4:#E5E7EB;--g5:#F9FAFB;
  --red:#EF4444;--nav:#0f172a;--blu:#3b82f6;--pur:#7c3aed;
  --sh:0 2px 12px rgba(0,0,0,.08);--sh2:0 6px 24px rgba(0,0,0,.13);
  --r:18px;--fn:'Onest',-apple-system,sans-serif
}
html,body,[class*="css"]{font-family:var(--fn)!important;background:var(--bg)!important;color:var(--dk)!important}
.stApp{background:var(--bg)!important;max-width:430px;margin:0 auto}
.block-container{padding:0 0 88px 0!important;max-width:430px!important}
#MainMenu,footer,header,.stDeployButton,
[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"]{display:none!important}
div[data-testid="stVerticalBlock"]>div{padding:0!important}
div[data-testid="element-container"]{margin:0!important}
.stMarkdown{margin:0!important}

/* ─ All buttons reset ─ */
.stButton>button{all:unset;cursor:pointer;display:flex;align-items:center;
  justify-content:center;font-family:var(--fn)!important;width:100%;
  -webkit-tap-highlight-color:transparent}

/* ─ Keypad ─ */
.kbtn .stButton>button{
  width:76px!important;height:76px!important;border-radius:50%!important;
  background:var(--w)!important;box-shadow:var(--sh)!important;
  font-size:26px!important;font-weight:400!important;color:var(--dk)!important;
  flex-direction:column!important;gap:1px!important;
  transition:background .1s,transform .1s!important;margin:0 auto!important}
.kbtn .stButton>button:active{background:#E5E5EA!important;transform:scale(.92)!important}
.kbtn-ghost .stButton>button{background:transparent!important;box-shadow:none!important;font-size:28px!important}
.kbtn-ghost .stButton>button:active{background:#00000010!important;transform:scale(.9)!important}

/* ─ Nav ─ */
.nb .stButton>button{background:transparent!important;flex-direction:column!important;
  gap:2px!important;font-size:10px!important;color:var(--g2)!important;
  padding:4px 6px!important;border-radius:10px!important}
.nb-a .stButton>button{color:var(--grn)!important}

/* ─ Green primary ─ */
.gb .stButton>button{background:var(--grn)!important;color:#fff!important;
  border-radius:14px!important;padding:15px!important;font-size:16px!important;
  font-weight:700!important;width:100%!important;
  box-shadow:0 6px 20px rgba(45,179,74,.3)!important;transition:all .2s!important}
.gb .stButton>button:active{transform:scale(.97)!important}

/* ─ Danger ─ */
.db .stButton>button{background:#fef2f2!important;color:var(--red)!important;
  border-radius:14px!important;padding:14px!important;font-size:15px!important;
  font-weight:700!important;border:1.5px solid #fecaca!important}

/* ─ Ghost/text ─ */
.tb .stButton>button{background:transparent!important;color:var(--g2)!important;
  font-size:14px!important;text-decoration:underline!important;padding:6px!important}

/* ─ Reveal ─ */
.rb .stButton>button{background:rgba(0,0,0,.15)!important;border-radius:20px!important;
  padding:7px 16px!important;font-size:13px!important;font-weight:600!important;
  color:#fff!important;gap:6px!important;white-space:nowrap!important}

/* ─ Quick login ─ */
.qb .stButton>button{background:var(--w)!important;border-radius:14px!important;
  padding:12px 6px!important;font-size:12px!important;font-weight:700!important;
  color:var(--dk)!important;box-shadow:var(--sh)!important;
  flex-direction:column!important;gap:3px!important;line-height:1.3!important}

/* ─ Chat send ─ */
.cb .stButton>button{background:var(--grn)!important;color:#fff!important;
  border-radius:12px!important;font-size:22px!important;padding:12px!important;width:100%!important}

/* ─ Inputs ─ */
[data-testid="stTextInput"]>div>div>input{
  background:var(--g5)!important;border:1.5px solid var(--g4)!important;
  border-radius:12px!important;color:var(--dk)!important;
  font-family:var(--fn)!important;padding:14px 16px!important;font-size:16px!important}
[data-testid="stTextInput"]>label{display:none!important}
[data-testid="stTextInput"]>div>div>input:focus{border-color:var(--grn)!important}

/* ─ Animations ─ */
@keyframes shake{0%,100%{transform:translateX(0)}
  15%{transform:translateX(-9px)}30%{transform:translateX(9px)}
  45%{transform:translateX(-7px)}60%{transform:translateX(7px)}
  75%{transform:translateX(-4px)}90%{transform:translateX(3px)}}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes pop{from{opacity:0;transform:scale(.82)}to{opacity:1;transform:scale(1)}}
@keyframes scan{0%{top:8%}50%{top:84%}100%{top:8%}}
@keyframes reveal{from{filter:blur(14px);opacity:.25}to{filter:blur(0);opacity:1}}
@keyframes sring{0%{transform:scale(0);opacity:0}65%{transform:scale(1.2)}100%{transform:scale(1);opacity:1}}
@keyframes slideUp{from{transform:translateY(36px);opacity:0}to{transform:translateY(0);opacity:1}}

/* ─ PIN dots ─ */
.dots{display:flex;gap:20px;justify-content:center;margin:28px 0}
.dot{width:14px;height:14px;border-radius:50%;border:2px solid #C0C0C8;
  background:transparent;transition:all .18s cubic-bezier(.34,1.56,.64,1)}
.dot.on{background:var(--dk);border-color:var(--dk);transform:scale(1.1)}
.dot.er{background:var(--red)!important;border-color:var(--red)!important}
.dots.sh{animation:shake .42s cubic-bezier(.36,.07,.19,.97) both}

/* ─ Face ID ─ */
.fbox{width:112px;height:112px;border-radius:26px;border:2.5px solid #374151;
  position:relative;display:flex;align-items:center;justify-content:center;background:var(--g5)}
.fbox.ok{border-color:var(--grn)!important;background:#f0fdf4!important}
.sbeam{position:absolute;left:8%;right:8%;height:2px;top:10%;
  background:linear-gradient(90deg,transparent,var(--dk),transparent);
  animation:scan 1.5s ease-in-out infinite}

/* ─ Cards ─ */
.card{background:var(--w);border-radius:var(--r);box-shadow:var(--sh);
  margin:8px 16px;padding:20px;animation:fadeUp .32s ease both}
.ct{font-size:20px;font-weight:800;margin-bottom:14px}
.ri{background:var(--g5);border-radius:12px;padding:14px;
  margin-bottom:8px;display:flex;align-items:center;gap:12px}
.ag{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.ac{background:var(--g5);border-radius:14px;padding:14px;position:relative}
.acn{font-size:9px;color:var(--g3);position:absolute;top:10px;right:10px}
.acs{width:36px;height:36px;border-radius:50%;background:var(--w);box-shadow:var(--sh);
  display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;margin-bottom:10px}
.acl{font-size:11px;color:var(--g2);margin-bottom:3px}
.acb{font-size:17px;font-weight:800}

/* ─ Transactions ─ */
.tx{display:flex;align-items:center;gap:12px;padding:13px 0;border-bottom:1px solid #F3F4F6}
.txi{width:44px;height:44px;border-radius:50%;background:var(--blu);
  display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0}
.txn{font-size:14px;font-weight:600}
.txc{font-size:12px;color:var(--g2);margin-top:2px}
.txa{font-size:15px;font-weight:700;text-align:right}
.txt{font-size:11px;color:var(--g3);text-align:right;margin-top:2px}

/* ─ Header ─ */
.hdr{background:linear-gradient(150deg,#b8c0d8,#d2d6ea,#c8cedf);
  padding:50px 20px 20px;position:relative;overflow:hidden}
.hdr::before{content:'';position:absolute;top:-30%;right:-10%;width:55%;height:130%;
  background:linear-gradient(135deg,rgba(255,255,255,.18),transparent);
  transform:rotate(-15deg);pointer-events:none}
.htop{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:1}

/* ─ Balance card ─ */
.balcard{background:var(--w);border-radius:20px;margin:12px 16px;padding:22px;
  box-shadow:var(--sh2);animation:pop .3s ease}
.blr{filter:blur(10px);user-select:none;transition:filter .4s ease}
.unblr{animation:reveal .45s ease both}

/* ─ Bottom nav ─ */
.bnav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:430px;
  background:var(--nav);display:flex;justify-content:space-around;align-items:center;
  padding:10px 4px 20px;z-index:100;border-top:1px solid rgba(255,255,255,.06)}

/* ─ Toast ─ */
.toast{background:linear-gradient(135deg,#10b981,#059669);color:#fff;
  border-radius:14px;padding:14px 16px;margin:8px 16px;
  display:flex;align-items:center;gap:12px;
  box-shadow:0 4px 16px rgba(16,185,129,.35);animation:slideUp .35s ease}

/* ─ Success ─ */
.suc{text-align:center;padding:32px 16px;animation:pop .4s cubic-bezier(.34,1.56,.64,1)}
.sring{width:80px;height:80px;border-radius:50%;background:var(--grn);
  display:flex;align-items:center;justify-content:center;font-size:38px;color:#fff;
  margin:0 auto 16px;animation:sring .5s cubic-bezier(.34,1.56,.64,1)}

/* ─ Misc ─ */
.promo{background:linear-gradient(135deg,#2DB34A,#16a34a);border-radius:18px;
  padding:20px;margin:10px 16px;position:relative;overflow:hidden;
  box-shadow:0 6px 20px rgba(45,179,74,.3)}
.promo::after{content:'💳';position:absolute;bottom:-18px;right:-10px;font-size:80px;opacity:.1}
.savr{background:var(--g5);border-radius:14px;padding:14px;
  display:flex;align-items:center;gap:12px;margin-bottom:8px}
.savic{width:44px;height:44px;border-radius:50%;background:var(--pur);
  display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0}
.cg{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:14px}
.cc{background:var(--g5);border-radius:12px;padding:12px}
.ci{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:18px;margin-bottom:8px}
.cv{font-size:13px;font-weight:700}
.uch{background:var(--w);border-radius:14px;padding:14px;display:flex;
  align-items:center;gap:12px;margin-bottom:8px;box-shadow:var(--sh)}
.mr{background:var(--w);border-radius:14px;margin:0 16px 8px;padding:16px;
  display:flex;align-items:center;gap:14px;box-shadow:var(--sh)}
.mi{width:40px;height:40px;border-radius:12px;display:flex;
  align-items:center;justify-content:center;font-size:20px;flex-shrink:0}
.bb{border-radius:18px;padding:12px 16px;max-width:82%;font-size:14px;
  line-height:1.5;word-break:break-word;margin-bottom:10px}
.bbot{background:var(--g5);color:var(--dk);border-bottom-left-radius:4px}
.busr{background:var(--grn);color:#fff;border-bottom-right-radius:4px}
::-webkit-scrollbar{width:0;height:0}
</style>
""", unsafe_allow_html=True)

# Shake detection JavaScript (for mobile)
st.markdown("""
<script>
(function(){
  var last=0;
  function onMotion(e){
    var a=e.accelerationIncludingGravity;
    if(!a)return;
    var m=Math.sqrt(a.x*a.x+a.y*a.y+a.z*a.z),now=Date.now();
    if(m>13&&now-last>1000){
      last=now;
      var btns=parent.document.querySelectorAll('button');
      for(var b of btns){
        if(b.textContent&&b.textContent.trim()==='SHAKE_TRIGGER'){b.click();break;}
      }
    }
  }
  if(window.DeviceMotionEvent){
    if(typeof DeviceMotionEvent.requestPermission==='function'){
      document.addEventListener('click',function h(){
        DeviceMotionEvent.requestPermission().then(function(r){
          if(r==='granted')window.addEventListener('devicemotion',onMotion);
        });document.removeEventListener('click',h);
      },{once:true});
    }else{window.addEventListener('devicemotion',onMotion);}
  }
})();
</script>
""", unsafe_allow_html=True)

# ── PIN Screen ────────────────────────────────────────────────────────────────
def pin_screen():
    pin = st.session_state.pin
    err = st.session_state.pin_err
    shk = st.session_state.pin_shake

    # Header
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("✕", key="px"):
            st.session_state.pin = ""
            st.session_state.pin_err = False
            st.rerun()
    with c2:
        st.markdown("<div style='text-align:right;padding:10px 0;font-size:13px;"
                    "color:#6B7280;border-bottom:1px dashed #ddd;display:inline-block;float:right'>"
                    "Փokhel ogtataroyn</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:30px;font-weight:900;"
                "line-height:1.25;padding:0 32px'>Enter your<br>PIN code</div>", unsafe_allow_html=True)

    # Dots
    dots_h = ""
    for i in range(4):
        cls = "er" if (i < len(pin) and err) else ("on" if i < len(pin) else "")
        dots_h += f"<div class='dot {cls}'></div>"
    st.markdown(f"<div class='dots {'sh' if shk else ''}'>{dots_h}</div>",
                unsafe_allow_html=True)

    if err:
        st.markdown("<div style='text-align:center;color:#EF4444;font-size:14px;"
                    "margin:-16px 0 12px;font-weight:500'>Incorrect PIN</div>",
                    unsafe_allow_html=True)

    # Face ID overlay
    if st.session_state.face_scanning:
        if st.session_state.face_done:
            st.markdown("<div style='text-align:center;padding:24px'>"
                        "<div class='fbox ok' style='margin:0 auto'><span style='font-size:52px'>✅</span></div>"
                        "<div style='margin-top:14px;font-size:16px;font-weight:700;color:#2DB34A'>Recognized!</div>"
                        "</div>", unsafe_allow_html=True)
            time.sleep(0.6)
            st.session_state.uid = "marina"
            st.session_state.logged_in = True
            st.session_state.face_scanning = False
            st.session_state.face_done = False
            st.rerun()
        else:
            st.markdown("<div style='text-align:center;padding:24px'>"
                        "<div class='fbox' style='margin:0 auto'>"
                        "<div class='sbeam'></div>"
                        "<span style='font-size:52px'>🫥</span></div>"
                        "<div style='margin-top:14px;font-size:15px;color:#6B7280'>Scanning…</div>"
                        "</div>", unsafe_allow_html=True)
            time.sleep(2)
            st.session_state.face_done = True
            st.rerun()
        return

    # Keypad
    def press(digit):
        p = st.session_state.pin
        if len(p) >= 4:
            return
        p += digit
        st.session_state.pin = p
        st.session_state.pin_err = False
        st.session_state.pin_shake = False
        if len(p) == 4:
            db = load_db()
            match = next((u for u, d in db["users"].items() if d["pin"] == p), None)
            if match:
                st.session_state.uid = match
                st.session_state.logged_in = True
                st.session_state.pin = ""
                st.session_state.pin_err = False
            else:
                st.session_state.pin_shake = True
                st.session_state.pin_err = True

    ROWS = [
        [("1", ""), ("2", "ABC"), ("3", "DEF")],
        [("4", "GHI"), ("5", "JKL"), ("6", "MNO")],
        [("7", "PQRS"), ("8", "TUV"), ("9", "WXYZ")],
        [("face", ""), ("0", ""), ("del", "")],
    ]

    st.markdown("<div style='padding:0 14px'>", unsafe_allow_html=True)
    for row in ROWS:
        cols = st.columns(3)
        for i, (d, sub) in enumerate(row):
            with cols[i]:
                if d == "face":
                    st.markdown("<div class='kbtn kbtn-ghost'>", unsafe_allow_html=True)
                    if st.button("🔐", key="kface"):
                        st.session_state.face_scanning = True
                        st.session_state.face_done = False
                        st.session_state.pin = ""
                        st.session_state.pin_err = False
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                elif d == "del":
                    st.markdown("<div class='kbtn kbtn-ghost'>", unsafe_allow_html=True)
                    if st.button("⌫", key="kdel"):
                        p = st.session_state.pin
                        if p:
                            st.session_state.pin = p[:-1]
                        st.session_state.pin_err = False
                        st.session_state.pin_shake = False
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    label = f"{d}\n{sub}" if sub else d
                    st.markdown("<div class='kbtn'>", unsafe_allow_html=True)
                    if st.button(label, key=f"k{d}"):
                        press(d)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='tb' style='text-align:center'>", unsafe_allow_html=True)
    st.button("Forgot PIN?", key="forgot")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin:14px;border:none;border-top:1px solid #E5E7EB'>",
                unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:12px;color:#9CA3AF;margin-bottom:10px'>"
                "Quick login (demo)</div>", unsafe_allow_html=True)
    db = load_db()
    qcols = st.columns(len(db["users"]))
    for i, (uid, u) in enumerate(db["users"].items()):
        with qcols[i]:
            st.markdown("<div class='qb'>", unsafe_allow_html=True)
            if st.button(f"{u['initials']}\nPIN: {u['pin']}", key=f"q{uid}"):
                st.session_state.uid = uid
                st.session_state.logged_in = True
                st.session_state.pin = ""
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ── Nav Bar ───────────────────────────────────────────────────────────────────
def nav_bar():
    TABS = [("home","🏠","Home"),("history","💳","History"),
            ("transfer","🔄","Transfer"),("chat","💬","Chat"),("profile","👤","Hub")]
    cur = st.session_state.tab
    nav_html = "".join(
        f"<div style='text-align:center;{'color:#2DB34A' if cur==k else 'color:#6B7280'};"
        f"font-size:10px;padding:0 4px'><div style='font-size:22px'>{ic}</div>{lb}</div>"
        for k, ic, lb in TABS
    )
    st.markdown(f"<div class='bnav'>{nav_html}</div>", unsafe_allow_html=True)
    ncols = st.columns(5)
    for i, (k, ic, lb) in enumerate(TABS):
        with ncols[i]:
            cls = "nb-a" if cur == k else "nb"
            st.markdown(f"<div class='{cls}'>", unsafe_allow_html=True)
            if st.button(ic, key=f"nav_{k}"):
                st.session_state.tab = k
                st.session_state.send_ok = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ── Home ──────────────────────────────────────────────────────────────────────
def home_screen(uid):
    db = load_db()
    u = db["users"][uid]
    vis = st.session_state.bal_vis

    # App header
    st.markdown(f"""
    <div class='hdr'>
      <div class='htop'>
        <div style='width:42px;height:42px;border-radius:50%;background:{u["color"]};
          color:#fff;font-size:14px;font-weight:800;
          display:flex;align-items:center;justify-content:center'>{u["initials"]}</div>
        <div style='font-size:17px;font-weight:800'>Highway Bank</div>
        <div style='width:42px;height:42px;border-radius:50%;background:#fff;
          display:flex;align-items:center;justify-content:center;
          box-shadow:var(--sh);position:relative'>
          🔔
          <div style='position:absolute;top:8px;right:8px;width:8px;height:8px;
            border-radius:50%;background:#EF4444'></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Balance card
    bal_display = f"֏ {u['card_bal']:,.2f}" if vis else "֏ ● ● ● ●"
    bal_cls = "unblr" if vis else "blr"
    st.markdown(f"""
    <div class='balcard'>
      <div style='font-size:12px;color:#9CA3AF;letter-spacing:.8px;
        text-transform:uppercase;margin-bottom:4px'>
        {u["card_type"]} •••• {u["card_num"]}
      </div>
      <div class='{bal_cls}' style='font-size:32px;font-weight:900;
        letter-spacing:-1px;margin:6px 0 12px'>{bal_display}</div>
      <div style='font-size:12px;color:#9CA3AF'>{u["name"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Reveal / hide toggle + hidden shake trigger
    c1, c2 = st.columns([3, 2])
    with c1:
        lbl = "🫣  Hide balance" if vis else "👁  Ցույց տալ"
        st.markdown("<div class='rb'>", unsafe_allow_html=True)
        if st.button(lbl, key="togbal"):
            st.session_state.bal_vis = not vis
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        # Hidden button targeted by shake JS
        st.markdown("<div style='overflow:hidden;width:1px;height:1px;opacity:0;position:absolute'>",
                    unsafe_allow_html=True)
        if st.button("SHAKE_TRIGGER", key="shk_js"):
            st.session_state.bal_vis = not st.session_state.bal_vis
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Promo banner
    st.markdown("""
    <div class='promo'>
      <div style='font-size:20px;font-weight:800;color:#fff'>1 CLICK Loan</div>
      <div style='font-size:13px;color:rgba(255,255,255,.8);margin-top:4px'>Starting from 16%</div>
    </div>
    """, unsafe_allow_html=True)

    # Card section
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='ct'>Cards</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='ri'>
      <div style='width:46px;height:46px;background:#1C1C1E;border-radius:10px;
        display:flex;align-items:center;justify-content:center;
        color:#fff;font-size:10px;font-weight:700;text-align:center;flex-shrink:0'>
        {u["card_type"]}<br>*{u["card_num"]}
      </div>
      <div style='flex:1'>
        <div style='font-size:13px;color:#6B7280'>{u["card_type"]} Classic</div>
        <div style='font-size:20px;font-weight:800;margin-top:2px'>֏ {u["card_bal"]:,.0f}</div>
      </div>
      <span style='color:#9CA3AF;font-size:20px'>›</span>
    </div>
    <div style='text-align:center;color:#6B7280;font-size:13px;padding:8px;cursor:pointer'>See all</div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Accounts grid
    an = ACCT[uid]
    st.markdown("<div class='card' style='animation-delay:.07s'>", unsafe_allow_html=True)
    st.markdown("<div class='ct'>Accounts</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='ag'>
      <div class='ac'><div class='acn'>·{an}</div><div class='acs'>֏</div>
        <div class='acl'>AMD Current</div><div class='acb'>֏ {u["amd"]:,.2f}</div></div>
      <div class='ac'><div class='acn'>·{int(an)+19}</div><div class='acs'>$</div>
        <div class='acl'>USD Current</div><div class='acb'>$ {u["usd"]:,.2f}</div></div>
      <div class='ac'><div class='acn'>·{int(an)+39}</div><div class='acs'>€</div>
        <div class='acl'>EUR Current</div><div class='acb'>€ {u["eur"]:,.2f}</div></div>
      <div class='ac'><div class='acn'>·{int(an)+40}</div><div class='acs'>₽</div>
        <div class='acl'>RUB Current</div><div class='acb'>₽ {u["rub"]:,.2f}</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Loan
    if u["has_loan"]:
        st.markdown("<div class='card' style='animation-delay:.12s'>", unsafe_allow_html=True)
        st.markdown("<div class='ct'>Loans</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='ri'>
          <div style='width:46px;height:46px;border-radius:50%;background:#92400e;
            display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0'>🥇</div>
          <div style='flex:1'>
            <div style='font-size:13px;color:#6B7280'>{u["loan_name"]}</div>
            <div style='font-size:20px;font-weight:800'>֏ {u["loan_amt"]:,}</div>
            <div style='font-size:12px;color:#9CA3AF;margin-top:2px'>{u["loan_mo"]} months left</div>
          </div>
          <div style='background:#2DB34A;color:#fff;border-radius:20px;
            padding:8px 14px;font-size:13px;font-weight:700;cursor:pointer'>Pay</div>
        </div>
        <div style='text-align:center;color:#6B7280;font-size:13px;padding:8px'>Early payment</div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Savings
    st.markdown("<div class='card' style='animation-delay:.16s'>", unsafe_allow_html=True)
    st.markdown("<div class='ct'>Savings</div>", unsafe_allow_html=True)
    for sym, label, val in [("֏", "AMD Savings", f"֏ {u['sav_amd']:,}"),
                              ("$", "USD Savings", f"$ {u['sav_usd']:,}"),
                              ("€", "EUR Savings", f"€ {u['sav_eur']:,}")]:
        st.markdown(f"""
        <div class='savr'>
          <div class='savic'>🐷</div>
          <div>
            <div style='font-size:13px;color:#6B7280'>{label}</div>
            <div style='font-size:19px;font-weight:800;margin-top:2px'>{val}</div>
          </div>
        </div>
        <div style='text-align:center;color:#9CA3AF;font-size:12px;
          text-decoration:underline;cursor:pointer;margin-bottom:8px'>Add more</div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── History ───────────────────────────────────────────────────────────────────
def history_screen(uid):
    db = load_db()
    txs = db["users"][uid]["txs"]

    st.markdown("""
    <div style='background:#fff;padding:16px;box-shadow:0 1px 8px rgba(0,0,0,.06);margin-bottom:8px'>
      <div style='display:flex;gap:8px'>
        <div style='background:#fff;border:1.5px solid #E5E7EB;border-radius:20px;
          padding:7px 14px;font-size:13px;font-weight:600;white-space:nowrap;
          box-shadow:0 2px 8px rgba(0,0,0,.06)'>April ∨</div>
        <div style='background:#fff;border:1.5px solid #E5E7EB;border-radius:20px;
          padding:7px 14px;font-size:13px;font-weight:600;white-space:nowrap;
          box-shadow:0 2px 8px rgba(0,0,0,.06)'>Amount ∨</div>
        <div style='background:#fff;border:1.5px solid #E5E7EB;border-radius:20px;
          padding:7px 14px;font-size:13px;font-weight:600;white-space:nowrap;
          box-shadow:0 2px 8px rgba(0,0,0,.06)'>Accounts ∨</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Spending summary
    cats = [("💼","Work",50000,"#6366f122"),("🔄","Transfer",5950,"#3b82f622"),
            ("🏪","Shops",2250,"#3b82f622"),("🍽️","Food",300,"#6366f122"),
            ("🚌","Transport",150,"#3b82f622"),("🏛️","Other",2,"#6366f122")]
    ch = "".join(f"<div class='cc'><div class='ci' style='background:{c}'>{ic}</div>"
                 f"<div class='cv'>֏ {v:,}</div></div>" for ic,lb,v,c in cats)
    st.markdown(f"""
    <div style='background:#fff;border-radius:var(--r);padding:20px;margin:8px 16px;box-shadow:var(--sh)'>
      <div style='font-size:13px;color:#6B7280'>April</div>
      <div style='font-size:19px;font-weight:800;margin-top:2px'>Expenses</div>
      <div style='font-size:30px;font-weight:900;letter-spacing:-1px;margin:6px 0 12px'>֏ 58,652</div>
      <div style='height:6px;border-radius:3px;background:linear-gradient(90deg,#6366f1,#3b82f6);margin-bottom:16px'></div>
      <div class='cg'>{ch}</div>
    </div>
    """, unsafe_allow_html=True)

    def tx_rows(txlist):
        for t in txlist:
            color = "#2DB34A" if t["amt"] > 0 else "#1C1C1E"
            sign  = "+" if t["amt"] > 0 else "−"
            ic_bg = "#6366f1" if t["icon"] in ("💼",) else "#3b82f6"
            st.markdown(f"""
            <div class='tx'>
              <div class='txi' style='background:{ic_bg}'>{t["icon"]}</div>
              <div style='flex:1'>
                <div class='txn'>{t["name"]}</div>
                <div class='txc'>{t["cat"]}</div>
              </div>
              <div>
                <div class='txa' style='color:{color}'>{sign} ֏ {abs(t["amt"]):,}</div>
                <div class='txt'>{t["t"]}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    todays = [t for t in txs if t["date"] == "Today"]
    others = [t for t in txs if t["date"] != "Today"]

    if todays:
        neg = sum(t["amt"] for t in todays if t["amt"] < 0)
        st.markdown(f"""
        <div style='padding:12px 16px 0;display:flex;justify-content:space-between'>
          <span style='font-size:17px;font-weight:800'>Today</span>
          <span style='font-size:14px;color:#EF4444;font-weight:600'>֏ {abs(neg):,}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='background:#fff;border-radius:16px;margin:8px 16px;"
                    "padding:0 16px;box-shadow:var(--sh)'>", unsafe_allow_html=True)
        tx_rows(todays)
        st.markdown("</div>", unsafe_allow_html=True)

    by_date = {}
    for t in others:
        by_date.setdefault(t["date"], []).append(t)
    for d, dtxs in by_date.items():
        st.markdown(f"<div style='padding:12px 16px 0;font-size:17px;font-weight:800'>{d}</div>",
                    unsafe_allow_html=True)
        st.markdown("<div style='background:#fff;border-radius:16px;margin:8px 16px;"
                    "padding:0 16px;box-shadow:var(--sh)'>", unsafe_allow_html=True)
        tx_rows(dtxs)
        st.markdown("</div>", unsafe_allow_html=True)

# ── Transfer ──────────────────────────────────────────────────────────────────
def transfer_screen(uid):
    db = load_db()
    others = {k: v for k, v in db["users"].items() if k != uid}

    st.markdown("""
    <div style='background:linear-gradient(135deg,#4f46e5,#7c3aed);
      padding:48px 20px 28px;border-radius:0 0 24px 24px;
      box-shadow:0 8px 24px rgba(79,70,229,.3)'>
      <div style='font-size:24px;font-weight:900;color:#fff'>Transfer</div>
      <div style='font-size:14px;color:rgba(255,255,255,.7);margin-top:4px'>
        Send money instantly
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Recipients row
    st.markdown("<div style='padding:14px 16px 6px;font-size:15px;font-weight:700'>Send to</div>",
                unsafe_allow_html=True)
    ocols = st.columns(len(others))
    for i, (ouid, ou) in enumerate(others.items()):
        with ocols[i]:
            st.markdown(f"""
            <div style='text-align:center;padding:6px'>
              <div style='width:54px;height:54px;border-radius:50%;background:{ou["color"]};
                color:#fff;font-size:15px;font-weight:800;
                display:flex;align-items:center;justify-content:center;
                margin:0 auto 6px;box-shadow:0 4px 12px {ou["color"]}55'>{ou["initials"]}</div>
              <div style='font-size:11px;color:#6B7280;font-weight:600'>{ou["name"].split()[0]}</div>
              <div style='font-size:10px;color:#9CA3AF'>#{ACCT[ouid]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Success screen
    if st.session_state.send_ok:
        st.markdown(f"""
        <div style='background:#fff;border-radius:20px;margin:8px 16px;box-shadow:var(--sh2)'>
          <div class='suc'>
            <div class='sring'>✓</div>
            <div style='font-size:22px;font-weight:900'>Sent!</div>
            <div style='font-size:15px;color:#6B7280;margin-top:8px;white-space:pre-line'>
              {st.session_state.send_msg}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='tb' style='text-align:center;padding:8px'>", unsafe_allow_html=True)
        if st.button("← Back", key="back_ok"):
            st.session_state.send_ok = False
            st.session_state.send_msg = ""
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Transfer form
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:18px;font-weight:800;margin-bottom:16px'>Նոր ԳումարՈՒՄ</div>",
                unsafe_allow_html=True)
    recv    = st.text_input("", placeholder="Հաճախորդի ID", key="recv")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    amt_inp = st.text_input("", placeholder="Amount (֏)", key="amtinp")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    note    = st.text_input("", placeholder="Note (optional)", key="noteinp")
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    err_msg = None
    st.markdown("<div class='gb'>", unsafe_allow_html=True)
    if st.button("💸  ՈՒղարկել գումարը", key="dosend"):
        if not recv.strip():
            err_msg = "Enter recipient account"
        elif not amt_inp.strip():
            err_msg = "Գրել գումարը"
        else:
            try:
                amount = float(amt_inp.strip().replace(",", "").replace("֏", "").strip())
                if amount <= 0:
                    err_msg = "Գումարը պետք է լինի ճիշտ"
                else:
                    db2 = load_db()
                    su   = db2["users"][uid]
                    if amount > su["amd"]:
                        err_msg = f"Insufficient funds. Balance: ֏ {su['amd']:,.2f}"
                    else:
                        ru = find_uid_by_acct(recv)
                        if not ru:
                            err_msg = "Չի գտնվել"
                        elif ru == uid:
                            err_msg = "Չենք կարող ուղարկել"
                        else:
                            # Execute transfer
                            db2["users"][uid]["amd"] -= amount
                            db2["users"][ru]["amd"]  += amount
                            rname = db2["users"][ru]["name"]
                            sname = db2["users"][uid]["name"]
                            now_t = datetime.now().strftime("%H:%M")
                            ntxt  = note.strip()

                            db2["users"][uid]["txs"].insert(0, {
                                "icon": "💸",
                                "name": f"→ {rname.split()[0]}",
                                "cat":  "Transfer" + (f" · {ntxt}" if ntxt else ""),
                                "amt":  -amount,
                                "date": "Today",
                                "t":    now_t,
                            })
                            db2["users"][ru]["txs"].insert(0, {
                                "icon": "📥",
                                "name": f"← {sname.split()[0]}",
                                "cat":  "Received" + (f" · {ntxt}" if ntxt else ""),
                                "amt":  amount,
                                "date": "Today",
                                "t":    now_t,
                            })
                            save_db(db2)
                            st.session_state.send_ok  = True
                            st.session_state.send_msg = (
                                f"֏ {amount:,.0f} → {rname}" +
                                (f"\n«{ntxt}»" if ntxt else "")
                            )
                            st.rerun()
            except ValueError:
                err_msg = "Enter a valid amount"
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if err_msg:
        st.error(err_msg)

    # Account reference
    st.markdown("<div style='padding:12px 16px 6px;font-size:14px;color:#9CA3AF;font-weight:600'>"
                "Available accounts</div>", unsafe_allow_html=True)
    for ouid, ou in others.items():
        db_f = load_db()
        oudata = db_f["users"][ouid]
        st.markdown(f"""
        <div class='uch'>
          <div style='width:42px;height:42px;border-radius:50%;background:{ou["color"]};
            color:#fff;font-size:13px;font-weight:800;
            display:flex;align-items:center;justify-content:center;flex-shrink:0'>{ou["initials"]}</div>
          <div>
            <div style='font-size:15px;font-weight:700'>{ou["name"]}</div>
            <div style='font-size:13px;color:#6B7280;margin-top:2px'>
              AMD acct #{ACCT[ouid]} · ֏ {oudata["amd"]:,.2f}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Chat ──────────────────────────────────────────────────────────────────────
def chat_screen(uid):
    db = load_db()
    u  = db["users"][uid]

    st.markdown(f"""
    <div style='background:#2DB34A;padding:48px 20px 28px;border-radius:0 0 24px 24px;
      box-shadow:0 8px 24px rgba(45,179,74,.3)'>
      <div style='font-size:22px;font-weight:900;color:#fff'>≫</div>
      <div style='font-size:22px;font-weight:800;color:#fff;margin-top:14px;line-height:1.35'>
        Hi {u["name"].split()[0]} 🤍<br>Write to us here<br>
        <span style='font-size:16px;font-weight:500'>Contact us here</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding:16px'>", unsafe_allow_html=True)
    for m in st.session_state.chat_msgs:
        if m["r"] == "bot":
            st.markdown(f"<div class='bb bbot'>{m['t']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='display:flex;justify-content:flex-end'>"
                        f"<div class='bb busr'>{m['t']}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([5, 1])
    with c1:
        msg = st.text_input("", placeholder="Message...", key="chat_in", label_visibility="collapsed")
    with c2:
        st.markdown("<div class='cb'>", unsafe_allow_html=True)
        if st.button("➤", key="chat_go"):
            if msg.strip():
                st.session_state.chat_msgs.append({"r": "user", "t": msg.strip()})
                replies = [
                    "Thank you! Your request is received. 📋",
                    "We'll help you shortly. Please wait. 🙏",
                    "Message received! We'll reply soon. ✅",
                ]
                st.session_state.chat_msgs.append({"r": "bot", "t": random.choice(replies)})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='margin:8px 16px'>
      <div class='mr'>
        <span style='font-size:22px'>💬</span>
        <div style='flex:1;font-size:15px;font-weight:700'>Messages</div>
        <span style='color:#9CA3AF'>▪</span>
      </div>
      <div class='mr'>
        <span style='font-size:22px'>📞</span>
        <div style='flex:1;font-size:15px;font-weight:700'>Contact us</div>
        <span style='color:#9CA3AF'>▶</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Profile ───────────────────────────────────────────────────────────────────
def profile_screen(uid):
    db = load_db()
    u  = db["users"][uid]

    st.markdown(f"""
    <div style='background:linear-gradient(180deg,#e0e0ee,#F2F2F7);
      padding:48px 20px 24px;text-align:center'>
      <div style='width:80px;height:80px;border-radius:50%;background:{u["color"]};
        color:#fff;font-size:28px;font-weight:800;
        display:flex;align-items:center;justify-content:center;
        margin:0 auto 14px;box-shadow:0 8px 24px rgba(0,0,0,.2)'>{u["initials"]}</div>
      <div style='font-size:22px;font-weight:900'>{u["name"]}</div>
      <div style='display:inline-flex;align-items:center;gap:8px;background:#1C1C1E;
        color:#fff;border-radius:22px;padding:10px 22px;font-size:14px;font-weight:700;
        margin-top:12px;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.3)'>
        ≫ START Package ›
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    for ic, bg, lbl in [("🟢","#dcfce7","My Page"),
                         ("🔵","#dbeafe","Security"),
                         ("⚫","#F3F4F6","Settings")]:
        st.markdown(f"""
        <div class='mr'>
          <div class='mi' style='background:{bg}'>{ic}</div>
          <div style='flex:1;font-size:16px;font-weight:700'>{lbl}</div>
          <span style='color:#9CA3AF;font-size:18px'>›</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='padding:0 16px'><div class='db'>", unsafe_allow_html=True)
    if st.button("🔒  Lock / Log out", key="logout"):
        for k in list(DEFAULTS.keys()):
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;margin:20px 0;font-size:12px;color:#9CA3AF'>
      Powered by <span style='color:#F59E0B;font-weight:800;
      text-decoration:underline'>HIGHWAY</span> version 1.0.1
    </div>
    """, unsafe_allow_html=True)

# ── MAIN ──────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    pin_screen()
else:
    uid = st.session_state.uid
    db  = load_db()
    if uid not in db["users"]:
        st.session_state.logged_in = False
        st.rerun()

    # Incoming money toast notification
    txs = db["users"][uid].get("txs", [])
    if txs and txs[0].get("icon") == "📥":
        tkey = f"{txs[0]['name']}_{txs[0]['t']}"
        if st.session_state.get("_last_toast") != tkey:
            st.session_state["_last_toast"] = tkey
            st.markdown(f"""
            <div class='toast'>
              <span style='font-size:26px'>📥</span>
              <div>
                <div style='font-size:14px;font-weight:800'>Incoming Transfer</div>
                <div style='font-size:13px;opacity:.9'>
                  {txs[0]["name"]} · ֏ {abs(txs[0]["amt"]):,.0f}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    tab = st.session_state.tab
    if   tab == "home":     home_screen(uid)
    elif tab == "history":  history_screen(uid)
    elif tab == "transfer": transfer_screen(uid)
    elif tab == "chat":     chat_screen(uid)
    elif tab == "profile":  profile_screen(uid)

    nav_bar()
