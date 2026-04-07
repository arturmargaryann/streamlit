import streamlit as st
from datetime import datetime, timedelta
import hashlib

st.set_page_config(page_title="Streamlit Bank", page_icon="🏦", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:1.5rem;padding-bottom:5rem;max-width:440px;}
.bank-header{background:linear-gradient(135deg,#C0392B 0%,#7B241C 100%);border-radius:24px;padding:24px 28px 22px;color:white;margin-bottom:18px;position:relative;overflow:hidden;}
.bank-header::before{content:'';position:absolute;top:-50px;right:-50px;width:180px;height:180px;background:rgba(255,255,255,0.07);border-radius:50%;}
.bank-name{font-family:'DM Serif Display',serif;font-size:28px;letter-spacing:-0.5px;}
.bank-tagline{font-size:13px;opacity:0.75;margin-top:2px;}
.balance-label{font-size:11px;opacity:0.8;margin-top:20px;letter-spacing:1px;text-transform:uppercase;}
.balance-amount{font-size:36px;font-weight:600;letter-spacing:-1px;margin-top:4px;}
.shake-hint{background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.3);border-radius:10px;padding:7px 13px;font-size:12px;margin-top:12px;display:inline-block;}
@keyframes shake{0%,100%{transform:translateX(0);}20%{transform:translateX(-10px) rotate(-1deg);}40%{transform:translateX(10px) rotate(1deg);}60%{transform:translateX(-6px);}80%{transform:translateX(6px);}}
.bank-card{background:linear-gradient(135deg,#C0392B 0%,#7B241C 100%);border-radius:22px;padding:28px 26px 22px;color:white;position:relative;overflow:hidden;margin-bottom:12px;}
.bank-card::after{content:'';position:absolute;bottom:-30px;right:-30px;width:140px;height:140px;background:rgba(255,255,255,0.06);border-radius:50%;}
.card-chip{width:38px;height:30px;background:linear-gradient(135deg,#f0c060,#c8960a);border-radius:6px;margin-bottom:18px;}
.card-number{font-size:18px;letter-spacing:3px;font-weight:500;}
.card-footer{display:flex;justify-content:space-between;margin-top:16px;}
.card-fl{font-size:10px;opacity:0.7;text-transform:uppercase;letter-spacing:0.5px;}
.card-fv{font-size:15px;font-weight:600;margin-top:2px;}
.frozen-badge{position:absolute;top:14px;right:16px;background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.4);border-radius:8px;padding:4px 12px;font-size:12px;font-weight:600;}
.cw{background:#fff;border-radius:16px;padding:18px 20px;border:1px solid rgba(0,0,0,0.08);margin-bottom:12px;}
.wt{font-size:12px;color:#7a736d;font-weight:500;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;}
.txn-row{display:flex;align-items:center;padding:12px 0;border-bottom:1px solid rgba(0,0,0,0.06);}
.txn-row:last-child{border-bottom:none;}
.txn-icon{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;margin-right:12px;}
.txn-icon.out{background:#fdf0ef;}.txn-icon.in{background:#eaf7f1;}
.txn-desc{font-size:14px;font-weight:500;color:#1a1410;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.txn-date{font-size:12px;color:#7a736d;margin-top:2px;}
.txn-amt{margin-left:auto;font-size:15px;font-weight:600;white-space:nowrap;padding-left:8px;}
.txn-amt.out{color:#C0392B;}.txn-amt.in{color:#1a9e6b;}
.badge{display:inline-block;padding:2px 8px;border-radius:20px;font-size:11px;font-weight:600;}
.badge.success{background:#eaf7f1;color:#1a9e6b;}.badge.pending{background:#fef3c7;color:#d97706;}.badge.failed{background:#fdf0ef;color:#C0392B;}
.qg{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:12px 0 20px;}
.qb{background:#fff;border:1px solid rgba(0,0,0,0.08);border-radius:14px;padding:14px 6px;text-align:center;}
.qi{font-size:22px;display:block;}.ql{font-size:11px;color:#7a736d;margin-top:5px;display:block;}
.ni{border-radius:14px;padding:14px 16px;margin-bottom:8px;border:1px solid rgba(0,0,0,0.07);display:flex;align-items:center;gap:12px;}
.ni.unread{background:#fdf0ef;}.ni.read{background:#fff;}
.stTabs [data-baseweb="tab-list"]{background:#f0ece8;border-radius:12px;padding:4px;gap:2px;}
.stTabs [data-baseweb="tab"]{border-radius:9px;padding:8px 16px;font-size:14px;font-weight:500;}
.stTabs [aria-selected="true"]{background:#C0392B!important;color:white!important;}
.stTextInput>div>div>input{border-radius:12px!important;}
.stTextInput>div>div>input:focus{border-color:#C0392B!important;box-shadow:0 0 0 2px rgba(192,57,43,0.15)!important;}
.stButton>button{background:#C0392B!important;color:white!important;border:none!important;border-radius:14px!important;padding:12px 24px!important;font-size:15px!important;font-weight:600!important;width:100%!important;}
.stButton>button:hover{background:#922B21!important;}
.login-wrap{background:#fff;border-radius:24px;padding:32px 28px;border:1px solid rgba(0,0,0,0.08);box-shadow:0 4px 24px rgba(192,57,43,0.08);}
.st{font-size:18px;font-weight:600;margin:18px 0 12px;color:#1a1410;}
</style>
""", unsafe_allow_html=True)

# ── USERS ──
USERS = {
    "demo": {
        "pw": hashlib.sha256(b"1234").hexdigest(),
        "name": "Արամ Ավետисян", "name_en": "Aram Avetisyan",
        "balance": 1_250_000, "card_num": "4580 •••• •••• 7342",
        "expiry": "09/28", "phone": "+374 91 234 567", "id": "DEMO001", "student": False,
    },
    "student": {
        "pw": hashlib.sha256(b"5678").hexdigest(),
        "name": "Ани Акобян", "name_en": "Ani Hakobyan",
        "balance": 85_000, "card_num": "4580 •••• •••• 9911",
        "expiry": "12/27", "phone": "+374 93 765 432", "id": "STU001", "student": True,
    },
}

def seed_txns():
    return [
        {"desc":"Yerevan City gnumner","amount":-12500,"date":datetime.now()-timedelta(hours=2),"status":"success","icon":"🛒"},
        {"desc":"Aram H.-ic poxancum","amount":+50000,"date":datetime.now()-timedelta(hours=5),"status":"success","icon":"⬇️"},
        {"desc":"Netflix bajandordagrutyun","amount":-3990,"date":datetime.now()-timedelta(days=1),"status":"success","icon":"🎬"},
        {"desc":"Komunal vcharumner","amount":-18000,"date":datetime.now()-timedelta(days=2),"status":"success","icon":"🏠"},
        {"desc":"Ashkhatavaraj","amount":+350000,"date":datetime.now()-timedelta(days=3),"status":"success","icon":"💼"},
        {"desc":"Jazzve surj","amount":-1500,"date":datetime.now()-timedelta(days=4),"status":"success","icon":"☕"},
        {"desc":"Mane G.-in poxancum","amount":-25000,"date":datetime.now()-timedelta(days=5),"status":"pending","icon":"⬆️"},
        {"desc":"Bzhshkakan tsarayutyun","amount":-8000,"date":datetime.now()-timedelta(days=6),"status":"success","icon":"🏥"},
        {"desc":"Amazon gnumner","amount":-45200,"date":datetime.now()-timedelta(days=7),"status":"failed","icon":"📦"},
        {"desc":"Avtobus kart","amount":-5000,"date":datetime.now()-timedelta(days=8),"status":"success","icon":"🚌"},
    ]

NOTIFS = [
    {"icon":"💸","msg":"Stacvats e 50,000 AMD Aram H.-ic","time":"2 jam araj","read":False},
    {"icon":"⚠️","msg":"Ansvor gorcoghoutun Amazon-um","time":"7 or araj","read":False},
    {"icon":"💸","msg":"Vcharvel Netflix 3,990 AMD","time":"1 or araj","read":True},
    {"icon":"ℹ️","msg":"Qarti jamkety avartvoum e 3 amsum","time":"3 or araj","read":True},
    {"icon":"💸","msg":"Stacvats ashkhatavaraj 350,000 AMD","time":"3 or araj","read":True},
]

# ── STATE ──
for k,v in {"logged_in":False,"username":"","balance_visible":False,"card_frozen":False,
            "txns":seed_txns(),"notifs":[n.copy() for n in NOTIFS],"page":"dashboard"}.items():
    if k not in st.session_state: st.session_state[k]=v

def u(): return USERS[st.session_state.username]
def fmt(n): return f"{n:,.0f} AMD"
def unread(): return sum(1 for n in st.session_state.notifs if not n["read"])

# ════════ LOGIN ════════
def login_page():
    st.markdown("""
    <div style='text-align:center;margin-bottom:28px;'>
      <div style='font-family:"DM Serif Display",serif;font-size:42px;color:#C0392B;letter-spacing:-1px;'>Streamlit</div>
      <div style='font-size:13px;color:#7a736d;margin-top:4px;'>Dzery vstaheli bank — Ваш надёжный банк</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:19px;font-weight:600;margin-bottom:18px;'>Mutq gorccel</div>", unsafe_allow_html=True)
    username = st.text_input("👤  Andznakanin kody", placeholder="demo  kam  student")
    password = st.text_input("🔒  Gaghtnabary", type="password", placeholder="••••")
    c1,c2 = st.columns(2)
    with c1:
        if st.button("▶  Mutq", key="lgn"):
            ud = USERS.get(username)
            if ud and hashlib.sha256(password.encode()).hexdigest()==ud["pw"]:
                st.session_state.logged_in=True; st.session_state.username=username; st.session_state.card_frozen=False; st.rerun()
            else: st.error("Sxal tvaynabar kam gaghtnabary")
    with c2:
        if st.button("🧪  Demo", key="dm"):
            st.session_state.logged_in=True; st.session_state.username="demo"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#fdf0ef;border-radius:14px;padding:14px 16px;margin-top:14px;font-size:13px;'>
      <b style='color:#C0392B;'>🧪 Test hashivner</b><br>
      <code>demo</code> / <code>1234</code> — Sovorakan ogtatar<br>
      <code>student</code> / <code>5678</code> — Usanoghi / Education mode
    </div>""", unsafe_allow_html=True)

# ════════ DASHBOARD ════════
def dashboard_page():
    usr = u()
    first = usr["name_en"].split()[0]
    bal_real   = fmt(usr["balance"])
    bal_hidden = "●●●●●●  AMD"
    shown = bal_real if st.session_state.balance_visible else bal_hidden

    st.markdown(f"""
    <div class="bank-header" id="bkh">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div><div class="bank-name">Streamlit</div><div class="bank-tagline">Barev, {first} 👋</div></div>
        <div style="font-size:32px;">🏦</div>
      </div>
      <div class="balance-label">Yntacik mnacord</div>
      <div class="balance-amount" id="bld">{shown}</div>
      <div class="shake-hint">📱 Herakhosy tapy tves · gumare tesnel hamar</div>
    </div>
    <script>
    (function(){{
      var vis={'true' if st.session_state.balance_visible else 'false'};
      var real="{bal_real}",hid="{bal_hidden}";
      var el=document.getElementById('bld'),hdr=document.getElementById('bkh');
      function toggle(){{vis=!vis;el.textContent=vis?real:hid;hdr.style.animation='none';void hdr.offsetWidth;hdr.style.animation='shake 0.45s ease';}}
      var lx,ly,lz,cd=false,th=16;
      function onM(e){{if(cd)return;var a=e.accelerationIncludingGravity;if(!a)return;
        if(lx!==undefined){{var d=Math.abs(a.x-lx)+Math.abs(a.y-ly)+Math.abs(a.z-lz);if(d>th){{toggle();cd=true;setTimeout(function(){{cd=false;}},1200);}}}}
        lx=a.x;ly=a.y;lz=a.z;}}
      if(window.DeviceMotionEvent){{
        if(typeof DeviceMotionEvent.requestPermission==='function'){{
          document.addEventListener('click',function ask(){{DeviceMotionEvent.requestPermission().then(function(s){{if(s==='granted')window.addEventListener('devicemotion',onM);}});document.removeEventListener('click',ask);}},{{once:true}});
        }}else{{window.addEventListener('devicemotion',onM);}}
      }}
    }})();
    </script>""", unsafe_allow_html=True)

    if st.button("👁  Tsuyts tal / Takctsel  bal", key="tglb"):
        st.session_state.balance_visible = not st.session_state.balance_visible; st.rerun()

    st.markdown("<div class='st'>Aragi gorcoghoutunner</div>", unsafe_allow_html=True)
    st.markdown("""<div class="qg">
      <div class="qb"><span class="qi">💸</span><span class="ql">Poxancum</span></div>
      <div class="qb"><span class="qi">📲</span><span class="ql">Vcharum</span></div>
      <div class="qb"><span class="qi">💳</span><span class="ql">Kart</span></div>
      <div class="qb"><span class="qi">📊</span><span class="ql">Hashvet.</span></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='st'>Tzakser (7 or)</div>", unsafe_allow_html=True)
    days=[(datetime.now()-timedelta(days=i)).strftime("%d/%m") for i in range(6,-1,-1)]
    vals=[12500,3990,18000,1500,0,25000,8000]
    fig=go.Figure(go.Bar(x=days,y=vals,marker_color=["#C0392B" if v==max(vals) else "#f0b0aa" for v in vals],
        text=[f"{v//1000}K" if v else "" for v in vals],textposition="outside"))
    fig.update_layout(margin=dict(t=10,b=10,l=0,r=0),height=165,paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",xaxis=dict(showgrid=False,tickfont=dict(size=11)),yaxis=dict(visible=False),showlegend=False)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    st.markdown("<div class='st'>Verjin gorcoghoutunner</div>", unsafe_allow_html=True)
    txns=st.session_state.txns[:5]
    html="<div class='cw'>"
    for t in txns:
        cls="out" if t["amount"]<0 else "in"; sign="−" if t["amount"]<0 else "+"; amt=abs(t["amount"]); date=t["date"].strftime("%d %b, %H:%M")
        html+=f'<div class="txn-row"><div class="txn-icon {cls}">{t["icon"]}</div><div style="flex:1;min-width:0;"><div class="txn-desc">{t["desc"]}</div><div class="txn-date">{date} <span class="badge {t["status"]}">{t["status"]}</span></div></div><div class="txn-amt {cls}">{sign}{amt:,.0f}֏</div></div>'
    html+="</div>"
    st.markdown(html,unsafe_allow_html=True)

    if u()["student"]:
        st.markdown("""<div style='background:linear-gradient(135deg,#1a9e6b,#0f6e56);border-radius:16px;padding:16px 18px;color:white;margin-top:14px;'>
          <div style='font-size:16px;font-weight:600;'>🎓 Education Mode</div>
          <div style='font-size:13px;opacity:0.85;margin-top:3px;'>Usanoghi rezim active e</div></div>""", unsafe_allow_html=True)

# ════════ TRANSACTIONS ════════
def transactions_page():
    st.markdown("<div style='font-size:20px;font-weight:600;margin-bottom:16px;'>💸 Gorcoghoutunner</div>", unsafe_allow_html=True)
    th, ts = st.tabs(["📋  Patmutyun","➕  Nuyn Ughark"])
    with th:
        search=st.text_input("🔍",placeholder="Gorcoghoutun pntr...")
        sf=st.selectbox("",["Bolor","success","pending","failed"],label_visibility="collapsed")
        txns=st.session_state.txns
        if search: txns=[t for t in txns if search.lower() in t["desc"].lower()]
        if sf!="Bolor": txns=[t for t in txns if t["status"]==sf]
        if not txns: st.info("Gorcoghoutunner chka")
        else:
            html="<div class='cw'>"
            for t in txns:
                cls="out" if t["amount"]<0 else "in"; sign="−" if t["amount"]<0 else "+"; amt=abs(t["amount"]); date=t["date"].strftime("%d %b %Y, %H:%M")
                html+=f'<div class="txn-row"><div class="txn-icon {cls}">{t["icon"]}</div><div style="flex:1;min-width:0;"><div class="txn-desc">{t["desc"]}</div><div class="txn-date">{date} <span class="badge {t["status"]}">{t["status"]}</span></div></div><div class="txn-amt {cls}">{sign}{amt:,.0f}֏</div></div>'
            html+="</div>"; st.markdown(html,unsafe_allow_html=True)
    with ts:
        st.markdown("<div class='cw'>", unsafe_allow_html=True)
        recipient=st.text_input("👤  Stolagoli ID kam herakhosy")
        amount=st.number_input("💰  Chap (֏)",min_value=100,max_value=1000000,value=5000,step=1000)
        st.text_input("📝  Canutaguir (optional)")
        if st.button("💸  Oughark",key="snd"):
            if recipient.strip():
                st.session_state.txns.insert(0,{"desc":f"Poxancum → {recipient}","amount":-amount,"date":datetime.now(),"status":"pending","icon":"⬆️"})
                st.session_state.notifs.insert(0,{"icon":"💸","msg":f"Poxancum {amount:,}֏ → {recipient}","time":"Hima","read":False})
                st.success(f"✅  Ougharkved e {amount:,}֏"); st.rerun()
            else: st.error("Nshe stolagoly")
        st.markdown("</div>", unsafe_allow_html=True)

# ════════ CARD ════════
def card_page():
    usr=u(); frozen=st.session_state.card_frozen
    st.markdown("<div style='font-size:20px;font-weight:600;margin-bottom:16px;'>💳 Imy Kart</div>", unsafe_allow_html=True)
    badge="<div class='frozen-badge'>❄️ FROZEN</div>" if frozen else ""
    num="•••• •••• •••• ••••" if frozen else usr["card_num"]
    st.markdown(f"""<div class="bank-card">{badge}
      <div class="card-chip"></div>
      <div class="card-number">{num}</div>
      <div class="card-footer">
        <div><div class="card-fl">Card Holder</div><div class="card-fv">{usr['name_en']}</div></div>
        <div><div class="card-fl">Expires</div><div class="card-fv">{usr['expiry']}</div></div>
        <div><div class="card-fl">Type</div><div class="card-fv">VISA</div></div>
      </div></div>""", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        if st.button("🔥 Bac" if frozen else "❄️ Sarel",key="frz"):
            st.session_state.card_frozen=not frozen
            st.session_state.notifs.insert(0,{"icon":"⚠️","msg":"Karty baccvel e" if frozen else "Karty saravel e","time":"Hima","read":False}); st.rerun()
    with c2:
        if st.button("📋  Details",key="dtl"): st.info(f"Phone: {usr['phone']}\nID: {usr['id']}")
    rows=[("Nomery",usr["card_num"]),("Jamkety",usr["expiry"]),("Status","❄️ Saraccel" if frozen else "✅ Activ"),("Tipos","Visa Debit"),("CVV","•••")]
    html="<div class='cw' style='margin-top:14px;'><div class='wt'>Manaramsutyunner</div><table style='width:100%;font-size:14px;border-collapse:collapse;'>"
    for l,v in rows: html+=f"<tr style='border-top:1px solid rgba(0,0,0,0.06);'><td style='padding:10px 0;color:#7a736d;'>{l}</td><td style='text-align:right;font-weight:500;'>{v}</td></tr>"
    html+="</table></div>"; st.markdown(html,unsafe_allow_html=True)

# ════════ NOTIFICATIONS ════════
def notifications_page():
    uc=unread(); title=f"🔔 Tegutyanner ({uc} new)" if uc else "🔔 Tegutyanner"
    st.markdown(f"<div style='font-size:20px;font-weight:600;margin-bottom:16px;'>{title}</div>", unsafe_allow_html=True)
    if uc:
        if st.button("✓  Bolor karcac",key="mar"): 
            for n in st.session_state.notifs: n["read"]=True
            st.rerun()
    for n in st.session_state.notifs:
        cls="unread" if not n["read"] else "read"
        dot="<span style='width:8px;height:8px;background:#C0392B;border-radius:50%;display:inline-block;margin-right:6px;'></span>" if not n["read"] else ""
        st.markdown(f"""<div class="ni {cls}"><div style="font-size:22px;">{n['icon']}</div>
          <div style="flex:1;"><div style="font-size:14px;font-weight:500;">{dot}{n['msg']}</div>
          <div style="font-size:12px;color:#7a736d;margin-top:3px;">{n['time']}</div></div></div>""", unsafe_allow_html=True)

# ════════ SETTINGS ════════
def settings_page():
    usr=u(); initials="".join(w[0].upper() for w in usr["name_en"].split())
    st.markdown("<div style='font-size:20px;font-weight:600;margin-bottom:16px;'>⚙️ Kayustabanutyan</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='cw'><div class='wt'>👤 Anvagir</div>
      <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:54px;height:54px;border-radius:50%;background:#fdf0ef;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:600;color:#C0392B;flex-shrink:0;">{initials}</div>
        <div><div style="font-size:16px;font-weight:600;">{usr['name_en']}</div>
        <div style="font-size:13px;color:#7a736d;">{usr['phone']}</div>
        <div style="font-size:13px;color:#7a736d;">ID: {usr['id']}</div></div></div></div>""", unsafe_allow_html=True)
    st.markdown("<div class='cw'><div class='wt'>🌐 Lezva</div>", unsafe_allow_html=True)
    st.selectbox("",["🇦🇲 Hayeren (Armenian)","🇬🇧 English","🇷🇺 Русский"],label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='cw'><div class='wt'>🔒 Anvtangutyan</div>", unsafe_allow_html=True)
    np=st.text_input("Nor gaghthnabary",type="password",key="np"); cp=st.text_input("Hashtutel",type="password",key="cp")
    tfa=st.toggle("2FA - Erkerord hashtutel")
    if tfa: st.info("📱 SMS kod kugharkvni amena mutqin")
    if st.button("💾  Pahel",key="savs"):
        if np and np==cp: st.success("✅ Gaghthnabary pvokhokhvel e")
        elif np: st.error("Gaghthnabarnery chi hamapat")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='cw'><div class='wt'>🎓 Education Mode</div>", unsafe_allow_html=True)
    edu=st.toggle("Usanoghi rezim",value=usr["student"])
    if edu: st.info("📚 Pathured interface usanogneri hamar")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪  Logout",key="lgt"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ════════ NAV ════════
def bottom_nav():
    uc=unread()
    items=[("🏠","Dash","dashboard"),("💸","Txns","transactions"),("💳","Kart","cards"),(f"🔔{'·' if uc else ''}","Notifs","notifications"),("⚙️","Settings","settings")]
    st.markdown("<hr style='border:none;border-top:1px solid rgba(0,0,0,0.08);margin:20px 0 8px;'>", unsafe_allow_html=True)
    cols=st.columns(5)
    for i,(icon,label,page) in enumerate(items):
        with cols[i]:
            active=st.session_state.page==page; color="#C0392B" if active else "#7a736d"; fw="600" if active else "400"
            st.markdown(f"<div style='text-align:center;'><span style='font-size:20px;'>{icon}</span><br><span style='font-size:10px;color:{color};font-weight:{fw};'>{label}</span></div>", unsafe_allow_html=True)
            if st.button("",key=f"nv_{page}",help=label):
                st.session_state.page=page; st.rerun()
    st.markdown("""<style>
    div[data-testid="stHorizontalBlock"] button{background:transparent!important;border:none!important;height:8px!important;padding:0!important;min-height:8px!important;}
    </style>""", unsafe_allow_html=True)

# ════════ MAIN ════════
if not st.session_state.logged_in:
    login_page()
else:
    p=st.session_state.page
    if p=="dashboard": dashboard_page()
    elif p=="transactions": transactions_page()
    elif p=="cards": card_page()
    elif p=="notifications": notifications_page()
    elif p=="settings": settings_page()
    bottom_nav()
