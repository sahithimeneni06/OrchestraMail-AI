import streamlit as st
import time
import requests
st.set_page_config(
    page_title="OrchestraMail AI",
    page_icon="💌",
    layout="wide",
    initial_sidebar_state="collapsed"
)
import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
  --gold:#c9a84c; --gold-lt:#e8cc7e;
  --violet:#6c4a9e; --violet-lt:#9b72d0;
  --teal:#2a9d8f; --teal-lt:#52c4b5;
  --blush:#e8b4b8; --cream:#f7f3ec;
  --bg:#08071a;
}

#MainMenu{visibility:hidden !important}
footer{visibility:hidden !important}
header{visibility:hidden !important}
[data-testid="stToolbar"]{display:none !important}
[data-testid="stDecoration"]{display:none !important}
[data-testid="stStatusWidget"]{display:none !important}
.stDeployButton{display:none !important}

.stApp {
  background: var(--bg) !important;
  font-family: 'DM Sans', sans-serif !important;
  overflow-x: hidden;
}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.stApp > div {
  background: transparent !important;
}
.main .block-container {
  padding: 1rem 2rem 3rem !important;
  max-width: 100% !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: rgba(255,255,255,0.06) !important;
  color: rgba(247,243,236,0.82) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  border-radius: 50px !important;
  padding: 10px 26px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  width: auto !important;
  transition: all 0.25s ease !important;
  box-shadow: none !important;
  letter-spacing: 0.2px !important;
}
.stButton > button:hover {
  background: rgba(255,255,255,0.12) !important;
  border-color: rgba(255,255,255,0.32) !important;
  color: #f7f3ec !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
}
.stButton > button:focus:not(:hover) {
  box-shadow: none !important;
  border-color: rgba(255,255,255,0.2) !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > textarea {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.11) !important;
  border-radius: 12px !important;
  color: #f7f3ec !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.94rem !important;
  caret-color: #e8cc7e;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > textarea:focus {
  border-color: rgba(201,168,76,0.55) !important;
  box-shadow: 0 0 0 3px rgba(201,168,76,0.1) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
  color: rgba(247,243,236,0.5) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.84rem !important;
}
p { color: rgba(247,243,236,0.65) !important; font-family: 'DM Sans', sans-serif !important; }

/* ── SELECTBOX ── */
.stSelectbox > div > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.11) !important;
  border-radius: 12px !important;
}
.stSelectbox > div > div > div { color: #f7f3ec !important; }

/* ── EXPANDER ── */
details > summary {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 10px !important;
  color: rgba(247,243,236,0.65) !important;
  padding: 10px 16px !important;
  font-family: 'DM Sans', sans-serif !important;
}
.streamlit-expanderHeader {
  background: rgba(255,255,255,0.04) !important;
  border-radius: 10px !important;
  color: rgba(247,243,236,0.65) !important;
}

/* ── INFO ── */
.stAlert {
  background: rgba(42,157,143,0.1) !important;
  border: 1px solid rgba(42,157,143,0.2) !important;
  border-radius: 12px !important;
}
.stAlert p { color: rgba(82,196,181,0.9) !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.02)}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:3px}

.bg-orb {
  position: fixed; border-radius: 50%;
  filter: blur(90px); pointer-events: none;
  z-index: 0; animation: bgOrbFloat 10s ease-in-out infinite;
}
.bg-orb-1 {
  width:520px;height:520px;top:-160px;left:-160px;
  background: radial-gradient(circle, rgba(108,74,158,0.28) 0%, transparent 70%);
  animation-duration:12s;
}
.bg-orb-2 {
  width:420px;height:420px;top:25%;right:-120px;
  background: radial-gradient(circle, rgba(201,168,76,0.2) 0%, transparent 70%);
  animation-duration:15s;animation-delay:-5s;
}
.bg-orb-3 {
  width:480px;height:480px;bottom:-120px;left:32%;
  background: radial-gradient(circle, rgba(42,157,143,0.22) 0%, transparent 70%);
  animation-duration:11s;animation-delay:-3s;
}
@keyframes bgOrbFloat {
  0%,100%{transform:translateY(0) scale(1)}
  50%{transform:translateY(-55px) scale(1.1)}
}

.bg-noise {
  position:fixed;top:0;left:0;width:100%;height:100%;
  opacity:0.032;pointer-events:none;z-index:1;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size:300px;
}

.lp-center {
  text-align: center;
  padding: 64px 0 12px;
  position: relative; z-index: 2;
}
.om-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(201,168,76,0.1);
  border: 1px solid rgba(201,168,76,0.28);
  border-radius: 100px; padding: 7px 20px;
  color: #e8cc7e;
  font-family: 'Space Mono', monospace;
  font-size: 0.67rem; letter-spacing: 2px; text-transform: uppercase;
  margin-bottom: 30px;
  animation: fadeup 0.6s ease 0.05s both;
}
.om-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(3.2rem, 8vw, 7rem);
  font-weight: 300; line-height: 0.98;
  color: #f7f3ec; letter-spacing: -1.5px;
  margin-bottom: 16px;
  animation: fadeup 0.65s ease 0.12s both;
}
.om-title .grad {
  font-style: italic;
  background: linear-gradient(135deg, #e8cc7e 0%, #e8b4b8 45%, #9b72d0 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.om-sub {
  font-size: 1.08rem; font-weight: 300;
  color: rgba(247,243,236,0.42);
  max-width: 500px; margin: 0 auto 42px; line-height: 1.72;
  animation: fadeup 0.65s ease 0.2s both;
}
.chips-wrap {
  display: flex; flex-wrap: wrap; justify-content: center;
  gap: 11px; margin-bottom: 46px;
}
.om-chip {
  display: flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px; padding: 10px 16px;
  color: rgba(247,243,236,0.72);
  font-family: 'DM Sans', sans-serif; font-size: 0.86rem;
  transition: all 0.3s ease;
  animation: fadeup 0.6s ease both;
}
.om-chip:nth-child(1){animation-delay:0.28s}
.om-chip:nth-child(2){animation-delay:0.34s;border-color:rgba(42,157,143,0.25)}
.om-chip:nth-child(3){animation-delay:0.40s;border-color:rgba(108,74,158,0.25)}
.om-chip:nth-child(4){animation-delay:0.46s;border-color:rgba(232,180,184,0.25)}
.om-chip:nth-child(5){animation-delay:0.52s;border-color:rgba(201,168,76,0.25)}
.om-chip:nth-child(6){animation-delay:0.58s}

/* Landing sign-in btn */
.lp-btn .stButton > button {
  background: linear-gradient(135deg, rgba(201,168,76,0.22) 0%, rgba(108,74,158,0.28) 100%) !important;
  border: 1.5px solid rgba(201,168,76,0.5) !important;
  color: #f7f3ec !important;
  font-size: 1.06rem !important;
  padding: 14px 38px !important;
  border-radius: 100px !important;
  box-shadow: 0 0 40px rgba(201,168,76,0.18), inset 0 1px 0 rgba(255,255,255,0.08) !important;
  letter-spacing: 0.3px !important;
  animation: fadeup 0.65s ease 0.65s both;
}
.lp-btn .stButton > button:hover {
  box-shadow: 0 18px 55px rgba(201,168,76,0.35), 0 0 80px rgba(108,74,158,0.22) !important;
  transform: translateY(-4px) scale(1.025) !important;
  border-color: #c9a84c !important;
}

.modal-bg {
  position: fixed; top:0;left:0;width:100%;height:100%;
  background: rgba(8,7,26,0.88);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  z-index: 9998;
  display: flex; align-items: center; justify-content: center;
  animation: fadeIn 0.25s ease both;
}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.modal-card {
  background: linear-gradient(145deg, #141030, #0c1825);
  border: 1px solid rgba(201,168,76,0.22);
  border-radius: 26px; padding: 50px 46px;
  width: 100%; max-width: 400px;
  position: relative; overflow: hidden;
  box-shadow: 0 40px 100px rgba(0,0,0,0.7), 0 0 80px rgba(108,74,158,0.2);
  animation: cardIn 0.45s cubic-bezier(0.34,1.56,0.64,1) both;
}
@keyframes cardIn{
  from{opacity:0;transform:scale(0.82) translateY(28px)}
  to{opacity:1;transform:scale(1) translateY(0)}
}
.modal-card::after{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(201,168,76,0.7),transparent);
}
.modal-logo {
  font-size: 2.7rem; display: block; text-align: center;
  margin-bottom: 8px;
  filter: drop-shadow(0 0 22px rgba(201,168,76,0.65));
  animation: iconPulse 3s ease infinite;
}
@keyframes iconPulse{
  0%,100%{filter:drop-shadow(0 0 18px rgba(201,168,76,0.55))}
  50%{filter:drop-shadow(0 0 38px rgba(201,168,76,0.95))}
}
.modal-brand {
  font-family:'Cormorant Garamond',serif;
  font-size:1.9rem;font-weight:600;color:#f7f3ec;text-align:center;margin-bottom:4px;
}
.modal-tag {
  font-family:'Space Mono',monospace;font-size:0.67rem;
  letter-spacing:1.8px;text-transform:uppercase;
  color:rgba(247,243,236,0.3);text-align:center;margin-bottom:30px;
}
.modal-info {
  background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
  border-radius:11px;padding:13px 16px;
  color:rgba(247,243,236,0.38);font-size:0.81rem;line-height:1.62;
  text-align:center;margin-bottom:22px;
  font-family:'DM Sans',sans-serif;
}
.modal-div {
  display:flex;align-items:center;gap:13px;
  color:rgba(247,243,236,0.2);font-size:0.74rem;
  font-family:'Space Mono',monospace;letter-spacing:1px;margin-bottom:18px;
}
.modal-div::before,.modal-div::after{content:'';flex:1;height:1px;background:rgba(255,255,255,0.07);}
.g-btn {
  display:flex;align-items:center;justify-content:center;gap:12px;
  width:100%;padding:15px 22px;
  background:rgba(255,255,255,0.055);
  border:1.5px solid rgba(255,255,255,0.12);
  border-radius:13px;
  color:#f7f3ec !important;text-decoration:none !important;
  font-size:0.96rem;font-weight:500;font-family:'DM Sans',sans-serif;
  transition:all 0.28s ease;cursor:pointer;box-sizing:border-box;
}
.g-btn:hover{
  background:rgba(255,255,255,0.1);border-color:rgba(255,255,255,0.26);
  transform:translateY(-2px);box-shadow:0 10px 28px rgba(0,0,0,0.35);
}
.g-circle{
  width:22px;height:22px;background:white;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  color:#4285F4;font-weight:800;font-size:0.72rem;flex-shrink:0;
  font-family:'DM Sans',sans-serif;
}
.sec-note{
  display:flex;align-items:center;justify-content:center;gap:7px;
  margin-top:22px;color:rgba(247,243,236,0.2);
  font-size:0.72rem;font-family:'Space Mono',monospace;
}

.nav-wrap{
  display:flex;align-items:center;justify-content:space-between;
  padding:16px 0 14px;
  border-bottom:1px solid rgba(255,255,255,0.06);
  margin-bottom:32px;position:relative;z-index:10;
}
.nav-brand{display:flex;align-items:center;gap:12px;}
.nav-icon{font-size:1.5rem;filter:drop-shadow(0 0 12px rgba(201,168,76,0.7));}
.nav-name{font-family:'Cormorant Garamond',serif;font-size:1.55rem;font-weight:600;color:#f7f3ec;}
.nav-name span{
  background:linear-gradient(135deg,#e8cc7e,#9b72d0);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.nav-user{
  display:flex;align-items:center;gap:10px;
  background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
  border-radius:100px;padding:7px 15px 7px 7px;
  color:rgba(247,243,236,0.6);font-size:0.84rem;font-family:'DM Sans',sans-serif;
}
.nav-avatar{
  width:27px;height:27px;border-radius:50%;
  background:linear-gradient(135deg,#c9a84c,#6c4a9e);
  display:flex;align-items:center;justify-content:center;
  color:white;font-size:0.74rem;font-weight:700;
}

.hero-wrap{text-align:center;margin-bottom:50px;position:relative;z-index:2;}
.hero-greeting{
  font-family:'Space Mono',monospace;font-size:0.67rem;
  color:#52c4b5;letter-spacing:3px;text-transform:uppercase;
  margin-bottom:13px;opacity:0.85;
}
.hero-h{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(2rem,4.5vw,3.6rem);
  font-weight:300;color:#f7f3ec;line-height:1.08;margin-bottom:13px;
}
.hero-h em{
  font-style:italic;
  background:linear-gradient(135deg,#e8cc7e 0%,#e8b4b8 55%,#9b72d0 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-sub{color:rgba(247,243,236,0.35);font-size:0.94rem;max-width:400px;margin:0 auto;line-height:1.65;}

.cards-row{
  display:flex;gap:22px;
  max-width:1080px;margin:0 auto 46px;
  position:relative;z-index:2;
}
.feat-card{
  flex:1;border-radius:22px;padding:32px 26px;
  position:relative;overflow:hidden;cursor:pointer;
  transition:transform 0.4s cubic-bezier(0.175,0.885,0.32,1.275), box-shadow 0.4s ease, border-color 0.3s ease;
  min-height:320px;display:flex;flex-direction:column;justify-content:space-between;
  border:1px solid rgba(255,255,255,0.06);
}
.feat-card:hover{transform:translateY(-10px) scale(1.015);}
.feat-card:nth-child(1){animation:fadeup 0.65s ease 0.1s both}
.feat-card:nth-child(2){animation:fadeup 0.65s ease 0.2s both}
.feat-card:nth-child(3){animation:fadeup 0.65s ease 0.3s both}

.card-v{background:linear-gradient(148deg,#180a2c,#110725);box-shadow:0 16px 48px rgba(108,74,158,0.12);}
.card-v:hover{box-shadow:0 28px 72px rgba(108,74,158,0.35);border-color:rgba(155,114,208,0.45);}
.card-t{background:linear-gradient(148deg,#061829,#08202f);box-shadow:0 16px 48px rgba(42,157,143,0.1);}
.card-t:hover{box-shadow:0 28px 72px rgba(42,157,143,0.3);border-color:rgba(82,196,181,0.42);}
.card-r{background:linear-gradient(148deg,#1c0810,#1e0b14);box-shadow:0 16px 48px rgba(200,80,110,0.08);}
.card-r:hover{box-shadow:0 28px 72px rgba(200,80,110,0.24);border-color:rgba(232,180,184,0.42);}

/* Card internal orbs */
.card-orb{
  position:absolute;border-radius:50%;
  filter:blur(55px);pointer-events:none;
  animation:orbPulse 6s ease-in-out infinite;
}
.orb-v1{width:190px;height:190px;top:-65px;right:-65px;background:rgba(108,74,158,0.5);}
.orb-v2{width:130px;height:130px;bottom:-40px;left:-40px;background:rgba(201,168,76,0.22);animation-delay:-3s;}
.orb-t1{width:190px;height:190px;top:-65px;right:-65px;background:rgba(42,157,143,0.45);}
.orb-t2{width:130px;height:130px;bottom:-40px;left:-40px;background:rgba(10,80,100,0.35);animation-delay:-2s;}
.orb-r1{width:190px;height:190px;top:-65px;right:-65px;background:rgba(185,60,90,0.4);animation-delay:-1s;}
.orb-r2{width:130px;height:130px;bottom:-40px;left:-40px;background:rgba(232,180,184,0.22);animation-delay:-4s;}
@keyframes orbPulse{0%,100%{transform:scale(1);opacity:0.6}50%{transform:scale(1.18);opacity:0.95}}

.card-icon-box{
  width:52px;height:52px;border-radius:14px;
  display:flex;align-items:center;justify-content:center;
  font-size:1.5rem;margin-bottom:16px;
  position:relative;z-index:2;border:1px solid rgba(255,255,255,0.1);
}
.icon-v{background:rgba(108,74,158,0.32);}
.icon-t{background:rgba(42,157,143,0.3);}
.icon-r{background:rgba(232,180,184,0.18);}

.card-num{font-family:'Space Mono',monospace;font-size:0.62rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:5px;position:relative;z-index:2;opacity:0.5;}
.num-v{color:#9b72d0} .num-t{color:#52c4b5} .num-r{color:#e8b4b8}
.card-title{font-family:'Cormorant Garamond',serif;font-size:1.85rem;font-weight:600;color:#f7f3ec;line-height:1.05;margin-bottom:11px;position:relative;z-index:2;}
.card-desc{font-size:0.83rem;font-weight:300;line-height:1.66;position:relative;z-index:2;margin-bottom:20px;}
.desc-v{color:rgba(155,114,208,0.88)} .desc-t{color:rgba(82,196,181,0.88)} .desc-r{color:rgba(232,180,184,0.82)}
.card-pills{display:flex;flex-direction:column;gap:7px;margin-bottom:22px;position:relative;z-index:2;}
.card-pill{display:flex;align-items:center;gap:9px;font-size:0.79rem;color:rgba(247,243,236,0.38);}
.pill-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;}
.dot-v{background:#9b72d0} .dot-t{background:#52c4b5} .dot-r{background:#e8b4b8}
.card-cta{display:inline-flex;align-items:center;gap:8px;font-size:0.84rem;font-weight:500;padding:9px 18px;border-radius:100px;border:1px solid;width:fit-content;position:relative;z-index:2;transition:all 0.3s ease;}
.cta-v{color:#9b72d0;border-color:rgba(155,114,208,0.38);background:rgba(108,74,158,0.12);}
.cta-t{color:#52c4b5;border-color:rgba(82,196,181,0.38);background:rgba(42,157,143,0.1);}
.cta-r{color:#e8b4b8;border-color:rgba(232,180,184,0.32);background:rgba(232,180,184,0.08);}
.feat-card:hover .cta-v{background:rgba(108,74,158,0.28);border-color:#9b72d0;}
.feat-card:hover .cta-t{background:rgba(42,157,143,0.25);border-color:#52c4b5;}
.feat-card:hover .cta-r{background:rgba(232,180,184,0.2);border-color:#e8b4b8;}
.lp-btn {
    display: flex;
    justify-content: center;
    margin-top: 30px;
}


/* MAIN BUTTON */
.stButton > button {
    position: relative;
    padding: 0.95rem 2.4rem;
    font-size: 1.08rem;
    font-weight: 600;
    color: #ffffff;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.18);
    background: rgba(20, 25, 35, 0.45);
    backdrop-filter: blur(18px);
    overflow: hidden;
    z-index: 1;
    transition: 0.35s ease;
}

/* 🌊 FLOWING RGB GLOSS */
.stButton > button::before {
    content: "";
    position: absolute;
    inset: -2px;
    border-radius: 16px;

    background: linear-gradient(
        120deg,
        rgba(0,255,170,0.35),
        rgba(0,140,255,0.35),
        rgba(255,60,60,0.35),
        rgba(0,255,170,0.35)
    );

    background-size: 300% 300%;
    animation: rgbFlow 8s ease infinite;
    z-index: -1;
}

/* ✨ INNER SOFT LIGHT */
.stButton > button::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 16px;
    background: radial-gradient(circle at 50% 50%,
        rgba(255,255,255,0.15),
        transparent 70%);
}

/* HOVER */
.stButton > button:hover {
    transform: translateY(-3px) scale(1.04);
    box-shadow:
        0 0 25px rgba(0,255,170,0.35),
        0 0 45px rgba(0,140,255,0.35),
        0 0 65px rgba(255,60,60,0.25);
}

/* ANIMATION */
@keyframes rgbFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Stats */
.stats-wrap{display:flex;justify-content:center;gap:54px;padding:26px 0;border-top:1px solid rgba(255,255,255,0.05);max-width:600px;margin:0 auto;position:relative;z-index:2;}
.stat-n{font-family:'Cormorant Garamond',serif;font-size:2.1rem;font-weight:600;background:linear-gradient(135deg,#e8cc7e,#f7f3ec);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;text-align:center;line-height:1;margin-bottom:5px;}
.stat-l{color:rgba(247,243,236,0.27);font-size:0.69rem;letter-spacing:1.5px;text-transform:uppercase;font-family:'Space Mono',monospace;text-align:center;}

.fp-header{display:flex;align-items:center;gap:15px;margin-bottom:28px;padding-bottom:20px;border-bottom:1px solid rgba(255,255,255,0.06);position:relative;z-index:2;}
.fp-icon{width:50px;height:50px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:1.45rem;flex-shrink:0;}
.fp-title{font-family:'Cormorant Garamond',serif;font-size:1.85rem;font-weight:600;color:#f7f3ec;}
.fp-sub{color:rgba(247,243,236,0.3);font-size:0.82rem;margin-top:2px;}
.panel{background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:17px;padding:26px;margin-bottom:16px;position:relative;z-index:2;}
.msg-ok{background:rgba(42,157,143,0.14);border:1px solid rgba(42,157,143,0.28);color:#52c4b5;padding:11px 17px;border-radius:11px;font-size:0.87rem;font-weight:500;margin:10px 0;}
.msg-warn{background:rgba(201,168,76,0.11);border:1px solid rgba(201,168,76,0.28);color:#e8cc7e;padding:11px 17px;border-radius:11px;font-size:0.87rem;font-weight:500;margin:10px 0;}
.email-item{background:rgba(255,255,255,0.028);border:1px solid rgba(255,255,255,0.07);border-left:3px solid #2a9d8f;border-radius:11px;padding:13px 17px;margin:9px 0;color:rgba(247,243,236,0.7);font-size:0.87rem;transition:all 0.2s ease;font-family:'DM Sans',sans-serif;}
[data-testid="stToast"]{
    background: #b91c1c !important;   /* red */
    color: #3b82f6 !important;        /* blue text */
    border-radius: 12px !important;
    border: 1px solid #1e3a8a !important;

    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    font-weight: 500;
    padding: 14px 18px;
}
/* Only card nav buttons — full overlay, invisible */
.card-btn-wrap {
    position: relative !important;
    margin-top: -100% !important;
    height: 100% !important;
    z-index: 10 !important;
}

.card-btn-wrap .stButton > button {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    opacity: 0 !important;
    cursor: pointer !important;
    border-radius: 22px !important;
    z-index: 10 !important;
    margin: 0 !important;
    padding: 0 !important;
}
/* icon color */
[data-testid="stToast"] svg{
    fill: #3b82f6 !important;
}
/* Footer */
.foot{text-align:center;padding:16px 0 8px;border-top:1px solid rgba(255,255,255,0.04);color:rgba(247,243,236,0.17);font-family:'Space Mono',monospace;font-size:0.67rem;letter-spacing:1px;position:relative;z-index:2;}
.stTextInput > div > div > input {
    color: #e8cc7e !important;
}
/* Animations */
@keyframes fadeup{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
.anim-1{animation:fadeup 0.6s ease 0.05s both}
.anim-2{animation:fadeup 0.6s ease 0.15s both}
.anim-3{animation:fadeup 0.6s ease 0.25s both}
.anim-4{animation:fadeup 0.6s ease 0.38s both}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="bg-orb bg-orb-1"></div>
<div class="bg-orb bg-orb-2"></div>
<div class="bg-orb bg-orb-3"></div>
<div class="bg-noise"></div>
""", unsafe_allow_html=True)

# ── SESSION STATE DEFAULTS ──
defaults = {
    "user": None,
    "page": "landing",
    "show_login": False,
    "emails": None,
    "generated_email": None,
    "ai_reply": None,
    "intent": "",
    "sender": "",
    "recipient_type": "",
    "recipient_name": "",
    "login_toast": False,
    "cookies": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── HANDLE OAUTH REDIRECT: ?user=email ──
if "user" in st.query_params:
    user_val = st.query_params["user"]
    if isinstance(user_val, list):
        user_val = user_val[0]
    st.session_state.user = user_val
    st.session_state.page = "home"
    st.query_params.clear()
    st.rerun()

# ── HANDLE NAV PARAM ──
if "nav" in st.query_params:
    st.session_state.page = st.query_params["nav"]
    st.query_params.clear()
    st.rerun()

# ── FIX 1: LANDING CHECK — use not st.session_state.user ──
if not st.session_state.user:
    _, col, _ = st.columns([1, 2.5, 1])
    with col:
        st.markdown("""
<div class="lp-center">
  <div class="om-badge">◆ Multi-Agent Intelligence &nbsp;·&nbsp; Email Orchestration</div>
  <div class="om-title">Orchestra<span class="grad">Mail</span> AI</div>
  <p class="om-sub">A symphony of AI agents composing, refining and dispatching your emails - intelligently, contextually, professionally.</p>
  <div class="chips-wrap">
    <div class="om-chip">✦ Multi-Agent Drafting</div>
    <div class="om-chip">⟳ Context-Aware Replies</div>
    <div class="om-chip">◈ Tone Intelligence</div>
    <div class="om-chip">✉ Gmail Integration</div>
    <div class="om-chip">⚡ One-Click Send</div>
    <div class="om-chip">🔒 OAuth2 Secured</div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="lp-btn">', unsafe_allow_html=True)
        if st.button("✦  Sign in with Google", key="open_login", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.show_login:
        st.markdown("""
<div class="modal-bg">
  <div class="modal-card">
    <span class="modal-logo">💌</span>
    <div class="modal-brand">OrchestraMail AI</div>
    <div class="modal-tag">Intelligent Email Orchestration</div>
    <div class="modal-info">Connect Gmail to let AI agents compose, reply and manage your emails with full context awareness.</div>
    <div class="modal-div">Continue with</div>
    <a href=""" + f'{BACKEND_URL}/login' + """ target="_self" class="g-btn">
      <div class="g-circle">G</div>
      Sign in with Google
      <span style="margin-left:auto;opacity:0.38;">→</span>
    </a>
    <div class="sec-note">🔒 &nbsp;OAuth2 Secured &nbsp;·&nbsp; We never store your password</div>
  </div>
</div>
""", unsafe_allow_html=True)
        _, mc, _ = st.columns([2, 1, 2])
        with mc:
            if st.button("✕  Close", key="close_modal", use_container_width=True):
                st.session_state.show_login = False
                st.rerun()

    st.stop()

# ── SIGNED-IN AREA ──

if not st.session_state.login_toast:
    st.toast("✦ Signed in!", icon="💌")
    st.session_state.login_toast = True

user_raw = st.session_state.user
user_display = user_raw.split("@")[0] if "@" in user_raw else user_raw
user_initial = user_display[0].upper()

st.markdown(f"""
<div class="nav-wrap">
  <div class="nav-brand">
    <span class="nav-icon">💌</span>
    <span class="nav-name">Orchestra<span>Mail</span></span>
  </div>
  <div class="nav-user">
    <div class="nav-avatar">{user_initial}</div>
    {user_raw}
  </div>
</div>
""", unsafe_allow_html=True)

n1, n2, n3, n4, _ = st.columns([1.05, 1.05, 1.05, 1.05, 4.8])
with n1:
    if st.button("🏠 Home", key="nav_home"): st.session_state.page = "home"; st.rerun()
with n2:
    if st.button("✦ New Mail", key="nav_new"): st.session_state.page = "new"; st.rerun()
with n3:
    if st.button("⟳ Inbox", key="nav_inbox"): st.session_state.page = "inbox"; st.rerun()
with n4:
    if st.button("↩ Reply", key="nav_reply"): st.session_state.page = "reply"; st.rerun()
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

if st.session_state.page in ("home", "landing"):
    st.markdown(f"""
<div class="hero-wrap anim-1">
  <div class="hero-greeting">Good day, {user_raw}</div>
  <div class="hero-h">What would you like to<br><em>orchestrate</em> today?</div>
  <p class="hero-sub">Your AI agents are ready. Pick a workflow below.</p>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
<div class="feat-card card-v" style="cursor:pointer;">
  <div class="card-orb orb-v1"></div><div class="card-orb orb-v2"></div>
  <div>
    <div class="card-icon-box icon-v">✦</div>
    <div class="card-num num-v">01 · Compose</div>
    <div class="card-title">New<br>Email</div>
  </div>
  <div>
    <p class="card-desc desc-v">Describe your intent in plain language. Agents craft a perfectly toned, context-aware email in seconds.</p>
    <div class="card-pills">
      <div class="card-pill"><div class="pill-dot dot-v"></div>Intent-to-email generation</div>
      <div class="card-pill"><div class="pill-dot dot-v"></div>Role-aware tone calibration</div>
      <div class="card-pill"><div class="pill-dot dot-v"></div>Edit before sending</div>
    </div>
    
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown('<div class="card-btn-wrap">', unsafe_allow_html=True)
        if st.button("✦  Compose New Email", key="card_new", use_container_width=True):
            st.session_state.page = "new"
            st.rerun()

    with col2:
        st.markdown("""
<div class="feat-card card-t" style="cursor:pointer;">
  <div class="card-orb orb-t1"></div><div class="card-orb orb-t2"></div>
  <div>
    <div class="card-icon-box icon-t">⟳</div>
    <div class="card-num num-t">02 · Inbox</div>
    <div class="card-title">Smart<br>Inbox</div>
  </div>
  <div>
    <p class="card-desc desc-t">Load your latest emails, browse threads and let AI generate perfectly contextual replies.</p>
    <div class="card-pills">
      <div class="card-pill"><div class="pill-dot dot-t"></div>100 latest emails</div>
      <div class="card-pill"><div class="pill-dot dot-t"></div>Thread-aware AI replies</div>
      <div class="card-pill"><div class="pill-dot dot-t"></div>Search by sender</div>
    </div>
    
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown('<div class="card-btn-wrap">', unsafe_allow_html=True)
        if st.button("⟳  Open Smart Inbox", key="card_inbox", use_container_width=True):
            st.session_state.page = "inbox"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown("""
<div class="feat-card card-r" style="cursor:pointer;">
  <div class="card-orb orb-r1"></div><div class="card-orb orb-r2"></div>
  <div>
    <div class="card-icon-box icon-r">↩</div>
    <div class="card-num num-r">03 · Reply</div>
    <div class="card-title">Smart<br>Reply</div>
  </div>
  <div>
    <p class="card-desc desc-r">Enter any email address to fetch your conversation history and craft a thoughtful AI response.</p>
    <div class="card-pills">
      <div class="card-pill"><div class="pill-dot dot-r"></div>Fetch by email address</div>
      <div class="card-pill"><div class="pill-dot dot-r"></div>Full conversation context</div>
      <div class="card-pill"><div class="pill-dot dot-r"></div>One-click send</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown('<div class="card-btn-wrap">', unsafe_allow_html=True)
        if st.button("↩  Smart Reply", key="card_reply", use_container_width=True):
            st.session_state.page = "reply"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="stats-wrap anim-4">
  <div><div class="stat-n">∞</div><div class="stat-l">Emails Possible</div></div>
  <div><div class="stat-n">5</div><div class="stat-l">AI Agents</div></div>
  <div><div class="stat-n">0 sec</div><div class="stat-l">Setup Time</div></div>
</div>
""", unsafe_allow_html=True)

elif st.session_state.page == "new":
    st.markdown("""
<div class="fp-header anim-1">
  <div class="fp-icon" style="background:rgba(108,74,158,0.22);border:1px solid rgba(155,114,208,0.3);">✦</div>
  <div>
    <div class="fp-title">Compose New Email</div>
    <div class="fp-sub">Describe your intent — agents do the rest</div>
  </div>
</div>
""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        to = st.text_input("📧 Recipient Email", placeholder="colleague@company.com")
        sender = st.text_input("👤 Your Name", placeholder="Your name")
    with c2:
        recipient_type = st.text_input("🎯 Recipient Role", placeholder="HR / Professor / Manager / Client")
        recipient_name = st.text_input("🙋 Recipient Name (optional)")
    intent = st.text_area("💭 Email Intent", placeholder="e.g. Follow up on Q3 budget and ask about next steps…", height=110)

    if st.button("✦  Generate Email Draft", use_container_width=True):
        st.session_state.intent = intent
        st.session_state.sender = sender
        st.session_state.recipient_type = recipient_type
        st.session_state.recipient_name = recipient_name
        if to and sender and intent and recipient_type:
            with st.spinner("AI agents drafting…"):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/generate-email",
                        json={
                            "to": to,
                            "intent": intent,
                            "sender": sender,
                            "recipient_type": recipient_type,
                            "recipient_name": recipient_name
                        },
                        cookies=st.session_state.get("cookies", {})
                    )
                    if res.status_code == 200:
                        st.session_state.generated_email = res.json()
                    else:
                        st.error("Failed to generate email")
                except Exception as e:
                    st.session_state.generated_email = {"subject": "Draft Subject", "email": f"[Draft body]\n\nNote: {e}", "to": to}
            st.markdown("<div class='msg-ok'>✦ Draft ready — review below</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='msg-warn'>⚠ Please fill all required fields</div>", unsafe_allow_html=True)

    if st.session_state.generated_email:
        gen = st.session_state.generated_email
        st.markdown("---")
        subject = st.text_input("Subject Line", value=gen.get("subject", ""), key="gen_subj")
        body = st.text_area("Email Body", value=gen.get("email", ""), height=210, key="gen_body")
        if st.button("📤  Send Email", use_container_width=True):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/send-email",
                    json={
                        "to": gen["to"],
                        "subject": subject,
                        "body": body
                    },
                    cookies=st.session_state.get("cookies", {})
                )
                if res.status_code == 200:
                    st.markdown("<div class='msg-ok'>✦ Email sent!</div>", unsafe_allow_html=True)
                    st.session_state.generated_email = None
                else:
                    st.error("Send failed")
            except Exception as e:
                st.error(f"Send error: {e}")

elif st.session_state.page == "inbox":
    st.markdown("""
<div class="fp-header anim-1">
  <div class="fp-icon" style="background:rgba(42,157,143,0.2);border:1px solid rgba(82,196,181,0.3);">⟳</div>
  <div>
    <div class="fp-title">Smart Inbox</div>
    <div class="fp-sub">Browse, preview and reply with AI</div>
  </div>
</div>
""", unsafe_allow_html=True)

    search_email = st.text_input("🔍 Search by email address", placeholder="sender@example.com")
    b1, b2 = st.columns(2)

    with b1:
        # FIX 5: clean up double-assignment; Search Conversations → /search
        if st.button("Search Conversations", use_container_width=True):
            if search_email:
                with st.spinner("Loading…"):
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/search",
                            json={"email": search_email},
                            cookies=st.session_state.get("cookies", {})
                        )
                        st.session_state.emails = res.json()
                    except:
                        st.session_state.emails = []
                st.markdown("<div class='msg-ok'>✦ Loaded</div>", unsafe_allow_html=True)

    with b2:
        # FIX 5: clean up double-assignment; Load Latest → /inbox
        if st.button("📨 Load 100 Latest", use_container_width=True):
            with st.spinner("Fetching inbox…"):
                try:
                    res = requests.get(
                        f"{BACKEND_URL}/inbox",
                        cookies=st.session_state.get("cookies", {})
                    )
                    st.session_state.emails = res.json()
                except:
                    st.session_state.emails = []
            st.markdown("<div class='msg-ok'>✦ Inbox loaded</div>", unsafe_allow_html=True)

    if st.session_state.emails:
        opts = {f"{e['subject']} — {e['from']}": e for e in st.session_state.emails}
        sel_lbl = st.selectbox("Select Email Thread", list(opts.keys()))
        sel = opts[sel_lbl]
        st.markdown(f"<div class='email-item'><strong>From:</strong> {sel['from']}<br><strong>Subject:</strong> {sel['subject']}</div>", unsafe_allow_html=True)
        with st.expander("📜 Full email body"):
            st.write(sel.get("body", "No content"))

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("**✏ Generate AI Reply**")
        ri = st.text_area("What should the reply say?", key="i_intent")
        rc1, rc2 = st.columns(2)
        with rc1:
            rs = st.text_input("Your Name", key="i_sender")
            rt = st.text_input("Recipient Role", placeholder="HR / Manager…", key="i_type")
        with rc2:
            rn = st.text_input("Recipient Name (optional)", key="i_name")
        if st.button("⟳  Generate AI Reply", use_container_width=True, key="i_gen"):
            if ri and rs and rt:
                with st.spinner("Generating…"):
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/generate-reply",
                            json={
                                "selected_email": sel,
                                "intent": ri,
                                "sender": rs,
                                "recipient_type": rt,
                                "recipient_name": rn
                            },
                            cookies=st.session_state.get("cookies", {})
                        )
                        st.session_state.ai_reply = res.json()
                    except Exception as e:
                        st.session_state.ai_reply = {"subject": "Re: " + sel.get("subject", ""), "email": f"[Reply]\n{e}", "to": sel.get("from", "")}
                st.markdown("<div class='msg-ok'>✦ Reply generated</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='msg-warn'>⚠ Fill intent, name and role</div>", unsafe_allow_html=True)

        if st.session_state.ai_reply:
            rep = st.session_state.ai_reply
            rs2 = st.text_input("Subject", value=rep.get("subject", ""), key="i_rsubj")
            rb2 = st.text_area("Reply Body", value=rep.get("email", ""), height=200, key="i_rbody")
            if st.button("📤  Send Reply", use_container_width=True, key="i_send"):
                try:
                    rep["subject"] = rs2
                    rep["email"] = rb2
                    res = requests.post(
                        f"{BACKEND_URL}/send-reply",
                        json=rep,
                        cookies=st.session_state.get("cookies", {})
                    )
                    if res.status_code == 200:
                        st.markdown("<div class='msg-ok'>✦ Reply sent!</div>", unsafe_allow_html=True)
                        st.session_state.ai_reply = None
                    else:
                        st.error("Reply failed")
                except Exception as e:
                    st.error(f"Send error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Load emails above to get started.")

elif st.session_state.page == "reply":
    st.markdown("""
<div class="fp-header anim-1">
  <div class="fp-icon" style="background:rgba(232,180,184,0.15);border:1px solid rgba(232,180,184,0.3);">↩</div>
  <div>
    <div class="fp-title">Smart Reply</div>
    <div class="fp-sub">Fetch any conversation and reply with AI context</div>
  </div>
</div>
""", unsafe_allow_html=True)

    target = st.text_input("📧 Email Address", placeholder="Enter sender/recipient email")

    # FIX 6: replaced local function calls with backend API calls
    if st.button("↩  Fetch Conversations", use_container_width=True):
        if target:
            with st.spinner("Loading…"):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/search",
                        json={"email": target},
                        cookies=st.session_state.get("cookies", {})
                    )
                    st.session_state.emails = res.json()
                except:
                    st.session_state.emails = []
            st.markdown("<div class='msg-ok'>✦ Conversations loaded</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='msg-warn'>⚠ Enter an email address first</div>", unsafe_allow_html=True)

    if st.session_state.emails:
        opts = {f"{e['subject']} — {e['from']}": e for e in st.session_state.emails}
        sel_lbl = st.selectbox("Select Thread", list(opts.keys()), key="r_sel")
        sel = opts[sel_lbl]
        st.markdown(f"<div class='email-item'><strong>From:</strong> {sel['from']}<br><strong>Subject:</strong> {sel['subject']}</div>", unsafe_allow_html=True)
        with st.expander("📜 Full email"):
            st.write(sel.get("body", "No content"))

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        ri = st.text_area("Reply Intent", placeholder="What should AI write?", key="r_intent")
        rc1, rc2 = st.columns(2)
        with rc1:
            rs = st.text_input("Your Name", key="r_sender")
            rt = st.text_input("Recipient Role", key="r_role")
        with rc2:
            rn = st.text_input("Recipient Name (optional)", key="r_name")

        if st.button("⟳  Generate AI Reply", use_container_width=True, key="r_gen"):
            if ri and rs and rt:
                with st.spinner("Generating…"):
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/generate-reply",
                            json={
                                "selected_email": sel,
                                "intent": ri,
                                "sender": rs,
                                "recipient_type": rt,
                                "recipient_name": rn
                            },
                            cookies=st.session_state.get("cookies", {})
                        )
                        st.session_state.ai_reply = res.json()
                    except Exception as e:
                        st.session_state.ai_reply = {"subject": "Re: " + sel.get("subject", ""), "email": "[Reply]", "to": sel.get("from", "")}
                st.markdown("<div class='msg-ok'>✦ Reply ready</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='msg-warn'>⚠ Fill intent, name and role</div>", unsafe_allow_html=True)

        if st.session_state.ai_reply:
            rep = st.session_state.ai_reply
            rs2 = st.text_input("Subject", value=rep.get("subject", ""), key="r_subj")
            rb2 = st.text_area("Reply Body", value=rep.get("email", ""), height=200, key="r_body")
            if st.button("📤  Send Reply", use_container_width=True, key="r_send"):
                try:
                    rep["subject"] = rs2
                    rep["email"] = rb2
                    res = requests.post(
                        f"{BACKEND_URL}/send-reply",
                        json=rep,
                        cookies=st.session_state.get("cookies", {})
                    )
                    if res.status_code == 200:
                        st.markdown("<div class='msg-ok'>✦ Reply sent!</div>", unsafe_allow_html=True)
                        st.session_state.ai_reply = None
                    else:
                        st.error("Reply failed")
                except Exception as e:
                    st.error(f"Send error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Enter an email address above and fetch conversations.")

# ── FOOTER + LOGOUT ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="foot">OrchestraMail AI &nbsp;·&nbsp; Multi-Agent Email Intelligence &nbsp;·&nbsp; Built with ♦ and care</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
_, lc, _ = st.columns([4, 1, 4])
with lc:
    if st.button("⎋  Sign Out", key="logout", use_container_width=True):
        try:
            requests.get(f"{BACKEND_URL}/logout", cookies=st.session_state.get("cookies", {}))
        except:
            pass
        st.session_state.clear()
        st.rerun()








# import streamlit as st
# import time
# import requests
# st.set_page_config(
#     page_title="OrchestraMail AI",
#     page_icon="💌",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )
# import os
# BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

# :root {
#   --gold:#c9a84c; --gold-lt:#e8cc7e;
#   --violet:#6c4a9e; --violet-lt:#9b72d0;
#   --teal:#2a9d8f; --teal-lt:#52c4b5;
#   --blush:#e8b4b8; --cream:#f7f3ec;
#   --bg:#08071a;
# }

# #MainMenu{visibility:hidden !important}
# footer{visibility:hidden !important}
# header{visibility:hidden !important}
# [data-testid="stToolbar"]{display:none !important}
# [data-testid="stDecoration"]{display:none !important}
# [data-testid="stStatusWidget"]{display:none !important}
# .stDeployButton{display:none !important}

# .stApp {
#   background: var(--bg) !important;
#   font-family: 'DM Sans', sans-serif !important;
#   overflow-x: hidden;
# }
# [data-testid="stAppViewContainer"],
# [data-testid="stMain"],
# .stApp > div {
#   background: transparent !important;
# }
# .main .block-container {
#   padding: 1rem 2rem 3rem !important;
#   max-width: 100% !important;
# }

# /* ── BUTTONS ── */
# .stButton > button {
#   background: rgba(255,255,255,0.06) !important;
#   color: rgba(247,243,236,0.82) !important;
#   border: 1px solid rgba(255,255,255,0.14) !important;
#   border-radius: 50px !important;
#   padding: 10px 26px !important;
#   font-family: 'DM Sans', sans-serif !important;
#   font-size: 0.9rem !important;
#   font-weight: 500 !important;
#   width: auto !important;
#   transition: all 0.25s ease !important;
#   box-shadow: none !important;
#   letter-spacing: 0.2px !important;
# }
# .stButton > button:hover {
#   background: rgba(255,255,255,0.12) !important;
#   border-color: rgba(255,255,255,0.32) !important;
#   color: #f7f3ec !important;
#   transform: translateY(-2px) !important;
#   box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
# }
# .stButton > button:focus:not(:hover) {
#   box-shadow: none !important;
#   border-color: rgba(255,255,255,0.2) !important;
# }

# /* ── INPUTS ── */
# .stTextInput > div > div > input,
# .stTextArea > div > textarea {
#   background: rgba(255,255,255,0.04) !important;
#   border: 1px solid rgba(255,255,255,0.11) !important;
#   border-radius: 12px !important;
#   color: #f7f3ec !important;
#   font-family: 'DM Sans', sans-serif !important;
#   font-size: 0.94rem !important;
#   caret-color: #e8cc7e;
# }
# .stTextInput > div > div > input:focus,
# .stTextArea > div > textarea:focus {
#   border-color: rgba(201,168,76,0.55) !important;
#   box-shadow: 0 0 0 3px rgba(201,168,76,0.1) !important;
# }
# .stTextInput label, .stTextArea label, .stSelectbox label {
#   color: rgba(247,243,236,0.5) !important;
#   font-family: 'DM Sans', sans-serif !important;
#   font-size: 0.84rem !important;
# }
# p { color: rgba(247,243,236,0.65) !important; font-family: 'DM Sans', sans-serif !important; }

# /* ── SELECTBOX ── */
# .stSelectbox > div > div {
#   background: rgba(255,255,255,0.04) !important;
#   border: 1px solid rgba(255,255,255,0.11) !important;
#   border-radius: 12px !important;
# }
# .stSelectbox > div > div > div { color: #f7f3ec !important; }

# /* ── EXPANDER ── */
# details > summary {
#   background: rgba(255,255,255,0.04) !important;
#   border: 1px solid rgba(255,255,255,0.08) !important;
#   border-radius: 10px !important;
#   color: rgba(247,243,236,0.65) !important;
#   padding: 10px 16px !important;
#   font-family: 'DM Sans', sans-serif !important;
# }
# .streamlit-expanderHeader {
#   background: rgba(255,255,255,0.04) !important;
#   border-radius: 10px !important;
#   color: rgba(247,243,236,0.65) !important;
# }

# /* ── INFO ── */
# .stAlert {
#   background: rgba(42,157,143,0.1) !important;
#   border: 1px solid rgba(42,157,143,0.2) !important;
#   border-radius: 12px !important;
# }
# .stAlert p { color: rgba(82,196,181,0.9) !important; }

# /* ── SCROLLBAR ── */
# ::-webkit-scrollbar{width:5px}
# ::-webkit-scrollbar-track{background:rgba(255,255,255,0.02)}
# ::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:3px}

# .bg-orb {
#   position: fixed; border-radius: 50%;
#   filter: blur(90px); pointer-events: none;
#   z-index: 0; animation: bgOrbFloat 10s ease-in-out infinite;
# }
# .bg-orb-1 {
#   width:520px;height:520px;top:-160px;left:-160px;
#   background: radial-gradient(circle, rgba(108,74,158,0.28) 0%, transparent 70%);
#   animation-duration:12s;
# }
# .bg-orb-2 {
#   width:420px;height:420px;top:25%;right:-120px;
#   background: radial-gradient(circle, rgba(201,168,76,0.2) 0%, transparent 70%);
#   animation-duration:15s;animation-delay:-5s;
# }
# .bg-orb-3 {
#   width:480px;height:480px;bottom:-120px;left:32%;
#   background: radial-gradient(circle, rgba(42,157,143,0.22) 0%, transparent 70%);
#   animation-duration:11s;animation-delay:-3s;
# }
# @keyframes bgOrbFloat {
#   0%,100%{transform:translateY(0) scale(1)}
#   50%{transform:translateY(-55px) scale(1.1)}
# }

# .bg-noise {
#   position:fixed;top:0;left:0;width:100%;height:100%;
#   opacity:0.032;pointer-events:none;z-index:1;
#   background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E");
#   background-size:300px;
# }

# .lp-center {
#   text-align: center;
#   padding: 64px 0 12px;
#   position: relative; z-index: 2;
# }
# .om-badge {
#   display: inline-flex; align-items: center; gap: 8px;
#   background: rgba(201,168,76,0.1);
#   border: 1px solid rgba(201,168,76,0.28);
#   border-radius: 100px; padding: 7px 20px;
#   color: #e8cc7e;
#   font-family: 'Space Mono', monospace;
#   font-size: 0.67rem; letter-spacing: 2px; text-transform: uppercase;
#   margin-bottom: 30px;
#   animation: fadeup 0.6s ease 0.05s both;
# }
# .om-title {
#   font-family: 'Cormorant Garamond', serif;
#   font-size: clamp(3.2rem, 8vw, 7rem);
#   font-weight: 300; line-height: 0.98;
#   color: #f7f3ec; letter-spacing: -1.5px;
#   margin-bottom: 16px;
#   animation: fadeup 0.65s ease 0.12s both;
# }
# .om-title .grad {
#   font-style: italic;
#   background: linear-gradient(135deg, #e8cc7e 0%, #e8b4b8 45%, #9b72d0 100%);
#   -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
# }
# .om-sub {
#   font-size: 1.08rem; font-weight: 300;
#   color: rgba(247,243,236,0.42);
#   max-width: 500px; margin: 0 auto 42px; line-height: 1.72;
#   animation: fadeup 0.65s ease 0.2s both;
# }
# .chips-wrap {
#   display: flex; flex-wrap: wrap; justify-content: center;
#   gap: 11px; margin-bottom: 46px;
# }
# .om-chip {
#   display: flex; align-items: center; gap: 8px;
#   background: rgba(255,255,255,0.04);
#   border: 1px solid rgba(255,255,255,0.1);
#   border-radius: 10px; padding: 10px 16px;
#   color: rgba(247,243,236,0.72);
#   font-family: 'DM Sans', sans-serif; font-size: 0.86rem;
#   transition: all 0.3s ease;
#   animation: fadeup 0.6s ease both;
# }
# .om-chip:nth-child(1){animation-delay:0.28s}
# .om-chip:nth-child(2){animation-delay:0.34s;border-color:rgba(42,157,143,0.25)}
# .om-chip:nth-child(3){animation-delay:0.40s;border-color:rgba(108,74,158,0.25)}
# .om-chip:nth-child(4){animation-delay:0.46s;border-color:rgba(232,180,184,0.25)}
# .om-chip:nth-child(5){animation-delay:0.52s;border-color:rgba(201,168,76,0.25)}
# .om-chip:nth-child(6){animation-delay:0.58s}

# /* Landing sign-in btn */
# .lp-btn .stButton > button {
#   background: linear-gradient(135deg, rgba(201,168,76,0.22) 0%, rgba(108,74,158,0.28) 100%) !important;
#   border: 1.5px solid rgba(201,168,76,0.5) !important;
#   color: #f7f3ec !important;
#   font-size: 1.06rem !important;
#   padding: 14px 38px !important;
#   border-radius: 100px !important;
#   box-shadow: 0 0 40px rgba(201,168,76,0.18), inset 0 1px 0 rgba(255,255,255,0.08) !important;
#   letter-spacing: 0.3px !important;
#   animation: fadeup 0.65s ease 0.65s both;
# }
# .lp-btn .stButton > button:hover {
#   box-shadow: 0 18px 55px rgba(201,168,76,0.35), 0 0 80px rgba(108,74,158,0.22) !important;
#   transform: translateY(-4px) scale(1.025) !important;
#   border-color: #c9a84c !important;
# }

# .modal-bg {
#   position: fixed; top:0;left:0;width:100%;height:100%;
#   background: rgba(8,7,26,0.88);
#   backdrop-filter: blur(18px);
#   -webkit-backdrop-filter: blur(18px);
#   z-index: 9998;
#   display: flex; align-items: center; justify-content: center;
#   animation: fadeIn 0.25s ease both;
# }
# @keyframes fadeIn{from{opacity:0}to{opacity:1}}
# .modal-card {
#   background: linear-gradient(145deg, #141030, #0c1825);
#   border: 1px solid rgba(201,168,76,0.22);
#   border-radius: 26px; padding: 50px 46px;
#   width: 100%; max-width: 400px;
#   position: relative; overflow: hidden;
#   box-shadow: 0 40px 100px rgba(0,0,0,0.7), 0 0 80px rgba(108,74,158,0.2);
#   animation: cardIn 0.45s cubic-bezier(0.34,1.56,0.64,1) both;
# }
# @keyframes cardIn{
#   from{opacity:0;transform:scale(0.82) translateY(28px)}
#   to{opacity:1;transform:scale(1) translateY(0)}
# }
# .modal-card::after{
#   content:'';position:absolute;top:0;left:0;right:0;height:1px;
#   background:linear-gradient(90deg,transparent,rgba(201,168,76,0.7),transparent);
# }
# .modal-logo {
#   font-size: 2.7rem; display: block; text-align: center;
#   margin-bottom: 8px;
#   filter: drop-shadow(0 0 22px rgba(201,168,76,0.65));
#   animation: iconPulse 3s ease infinite;
# }
# @keyframes iconPulse{
#   0%,100%{filter:drop-shadow(0 0 18px rgba(201,168,76,0.55))}
#   50%{filter:drop-shadow(0 0 38px rgba(201,168,76,0.95))}
# }
# .modal-brand {
#   font-family:'Cormorant Garamond',serif;
#   font-size:1.9rem;font-weight:600;color:#f7f3ec;text-align:center;margin-bottom:4px;
# }
# .modal-tag {
#   font-family:'Space Mono',monospace;font-size:0.67rem;
#   letter-spacing:1.8px;text-transform:uppercase;
#   color:rgba(247,243,236,0.3);text-align:center;margin-bottom:30px;
# }
# .modal-info {
#   background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
#   border-radius:11px;padding:13px 16px;
#   color:rgba(247,243,236,0.38);font-size:0.81rem;line-height:1.62;
#   text-align:center;margin-bottom:22px;
#   font-family:'DM Sans',sans-serif;
# }
# .modal-div {
#   display:flex;align-items:center;gap:13px;
#   color:rgba(247,243,236,0.2);font-size:0.74rem;
#   font-family:'Space Mono',monospace;letter-spacing:1px;margin-bottom:18px;
# }
# .modal-div::before,.modal-div::after{content:'';flex:1;height:1px;background:rgba(255,255,255,0.07);}
# .g-btn {
#   display:flex;align-items:center;justify-content:center;gap:12px;
#   width:100%;padding:15px 22px;
#   background:rgba(255,255,255,0.055);
#   border:1.5px solid rgba(255,255,255,0.12);
#   border-radius:13px;
#   color:#f7f3ec !important;text-decoration:none !important;
#   font-size:0.96rem;font-weight:500;font-family:'DM Sans',sans-serif;
#   transition:all 0.28s ease;cursor:pointer;box-sizing:border-box;
# }
# .g-btn:hover{
#   background:rgba(255,255,255,0.1);border-color:rgba(255,255,255,0.26);
#   transform:translateY(-2px);box-shadow:0 10px 28px rgba(0,0,0,0.35);
# }
# .g-circle{
#   width:22px;height:22px;background:white;border-radius:50%;
#   display:flex;align-items:center;justify-content:center;
#   color:#4285F4;font-weight:800;font-size:0.72rem;flex-shrink:0;
#   font-family:'DM Sans',sans-serif;
# }
# .sec-note{
#   display:flex;align-items:center;justify-content:center;gap:7px;
#   margin-top:22px;color:rgba(247,243,236,0.2);
#   font-size:0.72rem;font-family:'Space Mono',monospace;
# }

# .nav-wrap{
#   display:flex;align-items:center;justify-content:space-between;
#   padding:16px 0 14px;
#   border-bottom:1px solid rgba(255,255,255,0.06);
#   margin-bottom:32px;position:relative;z-index:10;
# }
# .nav-brand{display:flex;align-items:center;gap:12px;}
# .nav-icon{font-size:1.5rem;filter:drop-shadow(0 0 12px rgba(201,168,76,0.7));}
# .nav-name{font-family:'Cormorant Garamond',serif;font-size:1.55rem;font-weight:600;color:#f7f3ec;}
# .nav-name span{
#   background:linear-gradient(135deg,#e8cc7e,#9b72d0);
#   -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
# }
# .nav-user{
#   display:flex;align-items:center;gap:10px;
#   background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
#   border-radius:100px;padding:7px 15px 7px 7px;
#   color:rgba(247,243,236,0.6);font-size:0.84rem;font-family:'DM Sans',sans-serif;
# }
# .nav-avatar{
#   width:27px;height:27px;border-radius:50%;
#   background:linear-gradient(135deg,#c9a84c,#6c4a9e);
#   display:flex;align-items:center;justify-content:center;
#   color:white;font-size:0.74rem;font-weight:700;
# }

# .hero-wrap{text-align:center;margin-bottom:50px;position:relative;z-index:2;}
# .hero-greeting{
#   font-family:'Space Mono',monospace;font-size:0.67rem;
#   color:#52c4b5;letter-spacing:3px;text-transform:uppercase;
#   margin-bottom:13px;opacity:0.85;
# }
# .hero-h{
#   font-family:'Cormorant Garamond',serif;
#   font-size:clamp(2rem,4.5vw,3.6rem);
#   font-weight:300;color:#f7f3ec;line-height:1.08;margin-bottom:13px;
# }
# .hero-h em{
#   font-style:italic;
#   background:linear-gradient(135deg,#e8cc7e 0%,#e8b4b8 55%,#9b72d0 100%);
#   -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
# }
# .hero-sub{color:rgba(247,243,236,0.35);font-size:0.94rem;max-width:400px;margin:0 auto;line-height:1.65;}

# .cards-row{
#   display:flex;gap:22px;
#   max-width:1080px;margin:0 auto 46px;
#   position:relative;z-index:2;
# }
# .feat-card{
#   flex:1;border-radius:22px;padding:32px 26px;
#   position:relative;overflow:hidden;cursor:pointer;
#   transition:transform 0.4s cubic-bezier(0.175,0.885,0.32,1.275), box-shadow 0.4s ease, border-color 0.3s ease;
#   min-height:320px;display:flex;flex-direction:column;justify-content:space-between;
#   border:1px solid rgba(255,255,255,0.06);
# }
# .feat-card:hover{transform:translateY(-10px) scale(1.015);}
# .feat-card:nth-child(1){animation:fadeup 0.65s ease 0.1s both}
# .feat-card:nth-child(2){animation:fadeup 0.65s ease 0.2s both}
# .feat-card:nth-child(3){animation:fadeup 0.65s ease 0.3s both}

# .card-v{background:linear-gradient(148deg,#180a2c,#110725);box-shadow:0 16px 48px rgba(108,74,158,0.12);}
# .card-v:hover{box-shadow:0 28px 72px rgba(108,74,158,0.35);border-color:rgba(155,114,208,0.45);}
# .card-t{background:linear-gradient(148deg,#061829,#08202f);box-shadow:0 16px 48px rgba(42,157,143,0.1);}
# .card-t:hover{box-shadow:0 28px 72px rgba(42,157,143,0.3);border-color:rgba(82,196,181,0.42);}
# .card-r{background:linear-gradient(148deg,#1c0810,#1e0b14);box-shadow:0 16px 48px rgba(200,80,110,0.08);}
# .card-r:hover{box-shadow:0 28px 72px rgba(200,80,110,0.24);border-color:rgba(232,180,184,0.42);}

# /* Card internal orbs */
# .card-orb{
#   position:absolute;border-radius:50%;
#   filter:blur(55px);pointer-events:none;
#   animation:orbPulse 6s ease-in-out infinite;
# }
# .orb-v1{width:190px;height:190px;top:-65px;right:-65px;background:rgba(108,74,158,0.5);}
# .orb-v2{width:130px;height:130px;bottom:-40px;left:-40px;background:rgba(201,168,76,0.22);animation-delay:-3s;}
# .orb-t1{width:190px;height:190px;top:-65px;right:-65px;background:rgba(42,157,143,0.45);}
# .orb-t2{width:130px;height:130px;bottom:-40px;left:-40px;background:rgba(10,80,100,0.35);animation-delay:-2s;}
# .orb-r1{width:190px;height:190px;top:-65px;right:-65px;background:rgba(185,60,90,0.4);animation-delay:-1s;}
# .orb-r2{width:130px;height:130px;bottom:-40px;left:-40px;background:rgba(232,180,184,0.22);animation-delay:-4s;}
# @keyframes orbPulse{0%,100%{transform:scale(1);opacity:0.6}50%{transform:scale(1.18);opacity:0.95}}

# .card-icon-box{
#   width:52px;height:52px;border-radius:14px;
#   display:flex;align-items:center;justify-content:center;
#   font-size:1.5rem;margin-bottom:16px;
#   position:relative;z-index:2;border:1px solid rgba(255,255,255,0.1);
# }
# .icon-v{background:rgba(108,74,158,0.32);}
# .icon-t{background:rgba(42,157,143,0.3);}
# .icon-r{background:rgba(232,180,184,0.18);}

# .card-num{font-family:'Space Mono',monospace;font-size:0.62rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:5px;position:relative;z-index:2;opacity:0.5;}
# .num-v{color:#9b72d0} .num-t{color:#52c4b5} .num-r{color:#e8b4b8}
# .card-title{font-family:'Cormorant Garamond',serif;font-size:1.85rem;font-weight:600;color:#f7f3ec;line-height:1.05;margin-bottom:11px;position:relative;z-index:2;}
# .card-desc{font-size:0.83rem;font-weight:300;line-height:1.66;position:relative;z-index:2;margin-bottom:20px;}
# .desc-v{color:rgba(155,114,208,0.88)} .desc-t{color:rgba(82,196,181,0.88)} .desc-r{color:rgba(232,180,184,0.82)}
# .card-pills{display:flex;flex-direction:column;gap:7px;margin-bottom:22px;position:relative;z-index:2;}
# .card-pill{display:flex;align-items:center;gap:9px;font-size:0.79rem;color:rgba(247,243,236,0.38);}
# .pill-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;}
# .dot-v{background:#9b72d0} .dot-t{background:#52c4b5} .dot-r{background:#e8b4b8}
# .card-cta{display:inline-flex;align-items:center;gap:8px;font-size:0.84rem;font-weight:500;padding:9px 18px;border-radius:100px;border:1px solid;width:fit-content;position:relative;z-index:2;transition:all 0.3s ease;}
# .cta-v{color:#9b72d0;border-color:rgba(155,114,208,0.38);background:rgba(108,74,158,0.12);}
# .cta-t{color:#52c4b5;border-color:rgba(82,196,181,0.38);background:rgba(42,157,143,0.1);}
# .cta-r{color:#e8b4b8;border-color:rgba(232,180,184,0.32);background:rgba(232,180,184,0.08);}
# .feat-card:hover .cta-v{background:rgba(108,74,158,0.28);border-color:#9b72d0;}
# .feat-card:hover .cta-t{background:rgba(42,157,143,0.25);border-color:#52c4b5;}
# .feat-card:hover .cta-r{background:rgba(232,180,184,0.2);border-color:#e8b4b8;}
# .lp-btn {
#     display: flex;
#     justify-content: center;
#     margin-top: 30px;
# }


# /* MAIN BUTTON */
# .stButton > button {
#     position: relative;
#     padding: 0.95rem 2.4rem;
#     font-size: 1.08rem;
#     font-weight: 600;
#     color: #ffffff;
#     border-radius: 16px;
#     border: 1px solid rgba(255,255,255,0.18);
#     background: rgba(20, 25, 35, 0.45);
#     backdrop-filter: blur(18px);
#     overflow: hidden;
#     z-index: 1;
#     transition: 0.35s ease;
# }

# /* 🌊 FLOWING RGB GLOSS */
# .stButton > button::before {
#     content: "";
#     position: absolute;
#     inset: -2px;
#     border-radius: 16px;

#     background: linear-gradient(
#         120deg,
#         rgba(0,255,170,0.35),
#         rgba(0,140,255,0.35),
#         rgba(255,60,60,0.35),
#         rgba(0,255,170,0.35)
#     );

#     background-size: 300% 300%;
#     animation: rgbFlow 8s ease infinite;
#     z-index: -1;
# }

# /* ✨ INNER SOFT LIGHT */
# .stButton > button::after {
#     content: "";
#     position: absolute;
#     inset: 0;
#     border-radius: 16px;
#     background: radial-gradient(circle at 50% 50%,
#         rgba(255,255,255,0.15),
#         transparent 70%);
# }

# /* HOVER */
# .stButton > button:hover {
#     transform: translateY(-3px) scale(1.04);
#     box-shadow:
#         0 0 25px rgba(0,255,170,0.35),
#         0 0 45px rgba(0,140,255,0.35),
#         0 0 65px rgba(255,60,60,0.25);
# }

# /* ANIMATION */
# @keyframes rgbFlow {
#     0% { background-position: 0% 50%; }
#     50% { background-position: 100% 50%; }
#     100% { background-position: 0% 50%; }
# }

# /* Stats */
# .stats-wrap{display:flex;justify-content:center;gap:54px;padding:26px 0;border-top:1px solid rgba(255,255,255,0.05);max-width:600px;margin:0 auto;position:relative;z-index:2;}
# .stat-n{font-family:'Cormorant Garamond',serif;font-size:2.1rem;font-weight:600;background:linear-gradient(135deg,#e8cc7e,#f7f3ec);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;text-align:center;line-height:1;margin-bottom:5px;}
# .stat-l{color:rgba(247,243,236,0.27);font-size:0.69rem;letter-spacing:1.5px;text-transform:uppercase;font-family:'Space Mono',monospace;text-align:center;}

# .fp-header{display:flex;align-items:center;gap:15px;margin-bottom:28px;padding-bottom:20px;border-bottom:1px solid rgba(255,255,255,0.06);position:relative;z-index:2;}
# .fp-icon{width:50px;height:50px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:1.45rem;flex-shrink:0;}
# .fp-title{font-family:'Cormorant Garamond',serif;font-size:1.85rem;font-weight:600;color:#f7f3ec;}
# .fp-sub{color:rgba(247,243,236,0.3);font-size:0.82rem;margin-top:2px;}
# .panel{background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:17px;padding:26px;margin-bottom:16px;position:relative;z-index:2;}
# .msg-ok{background:rgba(42,157,143,0.14);border:1px solid rgba(42,157,143,0.28);color:#52c4b5;padding:11px 17px;border-radius:11px;font-size:0.87rem;font-weight:500;margin:10px 0;}
# .msg-warn{background:rgba(201,168,76,0.11);border:1px solid rgba(201,168,76,0.28);color:#e8cc7e;padding:11px 17px;border-radius:11px;font-size:0.87rem;font-weight:500;margin:10px 0;}
# .email-item{background:rgba(255,255,255,0.028);border:1px solid rgba(255,255,255,0.07);border-left:3px solid #2a9d8f;border-radius:11px;padding:13px 17px;margin:9px 0;color:rgba(247,243,236,0.7);font-size:0.87rem;transition:all 0.2s ease;font-family:'DM Sans',sans-serif;}
# [data-testid="stToast"]{
#     background: #b91c1c !important;   /* red */
#     color: #3b82f6 !important;        /* blue text */
#     border-radius: 12px !important;
#     border: 1px solid #1e3a8a !important;

#     box-shadow: 0 10px 30px rgba(0,0,0,0.6);
#     font-weight: 500;
#     padding: 14px 18px;
# }
# /* Only card nav buttons — full overlay, invisible */
# .card-btn-wrap {
#     position: relative !important;
#     margin-top: -100% !important;
#     height: 100% !important;
#     z-index: 10 !important;
# }

# .card-btn-wrap .stButton > button {
#     position: absolute !important;
#     top: 0 !important;
#     left: 0 !important;
#     width: 100% !important;
#     height: 100% !important;
#     opacity: 0 !important;
#     cursor: pointer !important;
#     border-radius: 22px !important;
#     z-index: 10 !important;
#     margin: 0 !important;
#     padding: 0 !important;
# }
# /* icon color */
# [data-testid="stToast"] svg{
#     fill: #3b82f6 !important;
# }
# /* Footer */
# .foot{text-align:center;padding:16px 0 8px;border-top:1px solid rgba(255,255,255,0.04);color:rgba(247,243,236,0.17);font-family:'Space Mono',monospace;font-size:0.67rem;letter-spacing:1px;position:relative;z-index:2;}
# .stTextInput > div > div > input {
#     color: #e8cc7e !important;
# }
# /* Animations */
# @keyframes fadeup{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
# .anim-1{animation:fadeup 0.6s ease 0.05s both}
# .anim-2{animation:fadeup 0.6s ease 0.15s both}
# .anim-3{animation:fadeup 0.6s ease 0.25s both}
# .anim-4{animation:fadeup 0.6s ease 0.38s both}
# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <div class="bg-orb bg-orb-1"></div>
# <div class="bg-orb bg-orb-2"></div>
# <div class="bg-orb bg-orb-3"></div>
# <div class="bg-noise"></div>
# """, unsafe_allow_html=True)

# if "user" not in st.session_state:
#     st.stop()

# if "page" not in st.session_state:
#     st.session_state.page = "landing"

# if "login_toast" not in st.session_state:
#     st.session_state.login_toast = False

# query_params = st.query_params
# if "user" in st.query_params:
#     user_val = st.query_params["user"]

#     if isinstance(user_val, list):
#         user_val = user_val[0]

#     st.session_state.user = user_val
#     st.query_params.clear()
#     st.rerun()
# if "session" not in st.session_state:
#     st.session_state.cookies = {}

# defaults = {
#     "page": "home" if st.session_state.get("user") else "landing", "show_login": False,
#     "emails": None, "generated_email": None, "ai_reply": None,
#     "intent": "", "sender": "", "recipient_type": "", "recipient_name": "",
#     "login_toast": False,
# }
# for k, v in defaults.items():
#     if k not in st.session_state:
#         st.session_state[k] = v

# if "user" not in st.session_state:

#     _, col, _ = st.columns([1, 2.5, 1])
#     with col:
#         st.markdown("""
# <div class="lp-center">
#   <div class="om-badge">◆ Multi-Agent Intelligence &nbsp;·&nbsp; Email Orchestration</div>
#   <div class="om-title">Orchestra<span class="grad">Mail</span> AI</div>
#   <p class="om-sub">A symphony of AI agents composing, refining and dispatching your emails - intelligently, contextually, professionally.</p>
#   <div class="chips-wrap">
#     <div class="om-chip">✦ Multi-Agent Drafting</div>
#     <div class="om-chip">⟳ Context-Aware Replies</div>
#     <div class="om-chip">◈ Tone Intelligence</div>
#     <div class="om-chip">✉ Gmail Integration</div>
#     <div class="om-chip">⚡ One-Click Send</div>
#     <div class="om-chip">🔒 OAuth2 Secured</div>
#   </div>
# </div>
# """, unsafe_allow_html=True)

#         st.markdown('<div class="lp-btn">', unsafe_allow_html=True)
#         if st.button("✦  Sign in with Google", key="open_login", use_container_width=True):
#             st.session_state.show_login = True
#             st.rerun()
#         st.markdown("</div>", unsafe_allow_html=True)

#     if st.session_state.show_login:
#         st.markdown("""
# <div class="modal-bg">
#   <div class="modal-card">
#     <span class="modal-logo">💌</span>
#     <div class="modal-brand">OrchestraMail AI</div>
#     <div class="modal-tag">Intelligent Email Orchestration</div>
#     <div class="modal-info">Connect Gmail to let AI agents compose, reply and manage your emails with full context awareness.</div>
#     <div class="modal-div">Continue with</div>
#     <a href=""" + f'{BACKEND_URL}/login' + """ target="_self" class="g-btn">
#       <div class="g-circle">G</div>
#       Sign in with Google
#       <span style="margin-left:auto;opacity:0.38;">→</span>
#     </a>
#     <div class="sec-note">🔒 &nbsp;OAuth2 Secured &nbsp;·&nbsp; We never store your password</div>
#   </div>
# </div>
# """, unsafe_allow_html=True)
#         _, mc, _ = st.columns([2, 1, 2])
#         with mc:
#             if st.button("✕  Close", key="close_modal", use_container_width=True):
#                 st.session_state.show_login = False
#                 st.rerun()

#     st.stop()

# if not st.session_state.login_toast:
#     st.toast("✦ Signed in!", icon="💌")
#     st.session_state.login_toast = True

# user_raw = st.session_state.get("user")

# if not user_raw:
#     st.session_state.page = "landing"
#     st.stop()

# user_display = user_raw.split("@")[0] if "@" in user_raw else user_raw
# user_initial = user_display[0].upper()

# st.markdown(f"""
# <div class="nav-wrap">
#   <div class="nav-brand">
#     <span class="nav-icon">💌</span>
#     <span class="nav-name">Orchestra<span>Mail</span></span>
#   </div>
#   <div class="nav-user">
#     <div class="nav-avatar">{user_initial}</div>
#     {user_raw}
#   </div>
# </div>
# """, unsafe_allow_html=True)
# query = st.query_params

# if "nav" in query:
#     st.session_state.page = query["nav"]
#     st.query_params.clear()
#     st.rerun()

# n1, n2, n3, n4, _ = st.columns([1.05, 1.05, 1.05, 1.05, 4.8])
# with n1:
#     if st.button("🏠 Home", key="nav_home"): st.session_state.page = "home"; st.rerun()
# with n2:
#     if st.button("✦ New Mail", key="nav_new"): st.session_state.page = "new"; st.rerun()
# with n3:
#     if st.button("⟳ Inbox", key="nav_inbox"): st.session_state.page = "inbox"; st.rerun()
# with n4:
#     if st.button("↩ Reply", key="nav_reply"): st.session_state.page = "reply"; st.rerun()
# st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# if st.session_state.page in ("home", "landing"):
#     st.markdown(f"""
# <div class="hero-wrap anim-1">
#   <div class="hero-greeting">Good day, {user_raw}</div>
#   <div class="hero-h">What would you like to<br><em>orchestrate</em> today?</div>
#   <p class="hero-sub">Your AI agents are ready. Pick a workflow below.</p>
# </div>
# """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.markdown("""
# <div class="feat-card card-v" style="cursor:pointer;">
#   <div class="card-orb orb-v1"></div><div class="card-orb orb-v2"></div>
#   <div>
#     <div class="card-icon-box icon-v">✦</div>
#     <div class="card-num num-v">01 · Compose</div>
#     <div class="card-title">New<br>Email</div>
#   </div>
#   <div>
#     <p class="card-desc desc-v">Describe your intent in plain language. Agents craft a perfectly toned, context-aware email in seconds.</p>
#     <div class="card-pills">
#       <div class="card-pill"><div class="pill-dot dot-v"></div>Intent-to-email generation</div>
#       <div class="card-pill"><div class="pill-dot dot-v"></div>Role-aware tone calibration</div>
#       <div class="card-pill"><div class="pill-dot dot-v"></div>Edit before sending</div>
#     </div>
    
#   </div>
# </div>
# """, unsafe_allow_html=True)
#         st.markdown('<div class="card-btn-wrap">', unsafe_allow_html=True)
#         if st.button("✦  Compose New Email", key="card_new", use_container_width=True):
#             st.session_state.page = "new"
#             st.rerun()

#     with col2:
#         st.markdown("""
# <div class="feat-card card-t" style="cursor:pointer;">
#   <div class="card-orb orb-t1"></div><div class="card-orb orb-t2"></div>
#   <div>
#     <div class="card-icon-box icon-t">⟳</div>
#     <div class="card-num num-t">02 · Inbox</div>
#     <div class="card-title">Smart<br>Inbox</div>
#   </div>
#   <div>
#     <p class="card-desc desc-t">Load your latest emails, browse threads and let AI generate perfectly contextual replies.</p>
#     <div class="card-pills">
#       <div class="card-pill"><div class="pill-dot dot-t"></div>100 latest emails</div>
#       <div class="card-pill"><div class="pill-dot dot-t"></div>Thread-aware AI replies</div>
#       <div class="card-pill"><div class="pill-dot dot-t"></div>Search by sender</div>
#     </div>
    
#   </div>
# </div>
# """, unsafe_allow_html=True)
#         st.markdown('<div class="card-btn-wrap">', unsafe_allow_html=True)
#         if st.button("⟳  Open Smart Inbox", key="card_inbox", use_container_width=True):
#             st.session_state.page = "inbox"
#             st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col3:
#         st.markdown("""
# <div class="feat-card card-r" style="cursor:pointer;">
#   <div class="card-orb orb-r1"></div><div class="card-orb orb-r2"></div>
#   <div>
#     <div class="card-icon-box icon-r">↩</div>
#     <div class="card-num num-r">03 · Reply</div>
#     <div class="card-title">Smart<br>Reply</div>
#   </div>
#   <div>
#     <p class="card-desc desc-r">Enter any email address to fetch your conversation history and craft a thoughtful AI response.</p>
#     <div class="card-pills">
#       <div class="card-pill"><div class="pill-dot dot-r"></div>Fetch by email address</div>
#       <div class="card-pill"><div class="pill-dot dot-r"></div>Full conversation context</div>
#       <div class="card-pill"><div class="pill-dot dot-r"></div>One-click send</div>
#     </div>
#   </div>
# </div>
# """, unsafe_allow_html=True)
#         st.markdown('<div class="card-btn-wrap">', unsafe_allow_html=True)
#         if st.button("↩  Smart Reply", key="card_reply", use_container_width=True):
#             st.session_state.page = "reply"
#             st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown("""
# <div class="stats-wrap anim-4">
#   <div><div class="stat-n">∞</div><div class="stat-l">Emails Possible</div></div>
#   <div><div class="stat-n">5</div><div class="stat-l">AI Agents</div></div>
#   <div><div class="stat-n">0 sec</div><div class="stat-l">Setup Time</div></div>
# </div>
# """, unsafe_allow_html=True)

# elif st.session_state.page == "new":
#     st.markdown("""
# <div class="fp-header anim-1">
#   <div class="fp-icon" style="background:rgba(108,74,158,0.22);border:1px solid rgba(155,114,208,0.3);">✦</div>
#   <div>
#     <div class="fp-title">Compose New Email</div>
#     <div class="fp-sub">Describe your intent — agents do the rest</div>
#   </div>
# </div>
# """, unsafe_allow_html=True)

    
#     c1, c2 = st.columns(2)
#     with c1:
#         to = st.text_input("📧 Recipient Email", placeholder="colleague@company.com")
#         sender = st.text_input("👤 Your Name", placeholder="Your name")
#     with c2:
#         recipient_type = st.text_input("🎯 Recipient Role", placeholder="HR / Professor / Manager / Client")
#         recipient_name = st.text_input("🙋 Recipient Name (optional)")
#     intent = st.text_area("💭 Email Intent", placeholder="e.g. Follow up on Q3 budget and ask about next steps…", height=110)

#     if st.button("✦  Generate Email Draft", use_container_width=True):
#         st.session_state.intent = intent
#         st.session_state.sender = sender
#         st.session_state.recipient_type = recipient_type
#         st.session_state.recipient_name = recipient_name
#         if to and sender and intent and recipient_type:
#             with st.spinner("AI agents drafting…"):
#                 try:
#                     import requests

#                     res = requests.post(
#                         f"{BACKEND_URL}/generate-email",
#                         json={
#                             "to": to,
#                             "intent": intent,
#                             "sender": sender,
#                             "recipient_type": recipient_type,
#                             "recipient_name": recipient_name
#                         },
#                         cookies=st.session_state.get("cookies", {})
#                     )

#                     if res.status_code == 200:
#                         st.session_state.generated_email = res.json()
#                     else:
#                         st.error("Failed to generate email")
#                     result = res.json()
#                     st.session_state.generated_email = result
#                 except Exception as e:
#                     st.session_state.generated_email = {"subject": "Draft Subject", "email": f"[Draft body]\n\nNote: {e}", "to": to}
#             st.markdown("<div class='msg-ok'>✦ Draft ready — review below</div>", unsafe_allow_html=True)
#         else:
#             st.markdown("<div class='msg-warn'>⚠ Please fill all required fields</div>", unsafe_allow_html=True)

#     if st.session_state.generated_email:
#         gen = st.session_state.generated_email
#         st.markdown("---")
#         subject = st.text_input("Subject Line", value=gen.get("subject", ""), key="gen_subj")
#         body = st.text_area("Email Body", value=gen.get("email", ""), height=210, key="gen_body")
#         if st.button("📤  Send Email", use_container_width=True):
#             try:
#                 res = requests.post(
#                     f"{BACKEND_URL}/send-email",
#                     json={
#                         "to": gen["to"],
#                         "subject": subject,
#                         "body": body
#                     },
#                     cookies=st.session_state.get("cookies", {})
#                 )

#                 if res.status_code == 200:
#                     st.markdown("<div class='msg-ok'>✦ Email sent!</div>", unsafe_allow_html=True)
#                 else:
#                     st.error("Send failed")
#                 result = res.json()
#             except: pass
#             st.markdown("<div class='msg-ok'>✦ Email sent!</div>", unsafe_allow_html=True)
#             st.session_state.generated_email = None
#     st.markdown("</div>", unsafe_allow_html=True)

# elif st.session_state.page == "inbox":
#     st.markdown("""
# <div class="fp-header anim-1">
#   <div class="fp-icon" style="background:rgba(42,157,143,0.2);border:1px solid rgba(82,196,181,0.3);">⟳</div>
#   <div>
#     <div class="fp-title">Smart Inbox</div>
#     <div class="fp-sub">Browse, preview and reply with AI</div>
#   </div>
# </div>
# """, unsafe_allow_html=True)

    
#     search_email = st.text_input("🔍 Search by email address", placeholder="sender@example.com")
#     b1, b2 = st.columns(2)
#     with b1:
#         if st.button("Search Conversations", use_container_width=True):
#             if search_email:
#                 with st.spinner("Loading…"):
#                     try:
                        
#                         st.session_state.emails = res = requests.get(
#                             f"{BACKEND_URL}/inbox",
#                             cookies=st.session_state.get("cookies", {})
#                         )

#                         st.session_state.emails = res.json()
#                     except: st.session_state.emails = []
#                 st.markdown("<div class='msg-ok'>✦ Loaded</div>", unsafe_allow_html=True)
#     with b2:
#         if st.button("📨 Load 100 Latest", use_container_width=True):
#             with st.spinner("Fetching inbox…"):
#                 try:
                    
#                     st.session_state.emails = res = requests.post(
#                         f"{BACKEND_URL}/search",
#                         json={"email": search_email},
#                         cookies=st.session_state.get("cookies", {})
#                     )

#                     st.session_state.emails = res.json()
#                 except: st.session_state.emails = []
#             st.markdown("<div class='msg-ok'>✦ Inbox loaded</div>", unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

#     if st.session_state.emails:
#         opts = {f"{e['subject']} — {e['from']}": e for e in st.session_state.emails}
#         sel_lbl = st.selectbox("Select Email Thread", list(opts.keys()))
#         sel = opts[sel_lbl]
#         st.markdown(f"<div class='email-item'><strong>From:</strong> {sel['from']}<br><strong>Subject:</strong> {sel['subject']}</div>", unsafe_allow_html=True)
#         with st.expander("📜 Full email body"):
#             st.write(sel.get("body", "No content"))

#         st.markdown('<div class="panel">', unsafe_allow_html=True)
#         st.markdown("**✏ Generate AI Reply**")
#         ri = st.text_area("What should the reply say?", key="i_intent")
#         rc1, rc2 = st.columns(2)
#         with rc1:
#             rs = st.text_input("Your Name", key="i_sender")
#             rt = st.text_input("Recipient Role", placeholder="HR / Manager…", key="i_type")
#         with rc2:
#             rn = st.text_input("Recipient Name (optional)", key="i_name")
#         if st.button("⟳  Generate AI Reply", use_container_width=True, key="i_gen"):
#             if ri and rs and rt:
#                 with st.spinner("Generating…"):
#                     try:
                        
#                         st.session_state.ai_reply = res = requests.post(
#                             f"{BACKEND_URL}/generate-reply",
#                             json={
#                                 "selected_email": sel,
#                                 "intent": ri,
#                                 "sender": rs,
#                                 "recipient_type": rt,
#                                 "recipient_name": rn
#                             },
#                             cookies=st.session_state.get("cookies", {})
#                         )

#                         st.session_state.ai_reply = res.json()
#                     except Exception as e:
#                         st.session_state.ai_reply = {"subject":"Re: "+sel.get("subject",""),"email":f"[Reply]\n{e}","to":sel.get("from","")}
#                 st.markdown("<div class='msg-ok'>✦ Reply generated</div>", unsafe_allow_html=True)
#             else:
#                 st.markdown("<div class='msg-warn'>⚠ Fill intent, name and role</div>", unsafe_allow_html=True)
#         if st.session_state.ai_reply:
#             rep = st.session_state.ai_reply
#             rs2 = st.text_input("Subject", value=rep.get("subject",""), key="i_rsubj")
#             rb2 = st.text_area("Reply Body", value=rep.get("email",""), height=200, key="i_rbody")
#             if st.button("📤  Send Reply", use_container_width=True, key="i_send"):
#                 try:
                    
#                     rep["subject"] = rs2; rep["email"] = rb2
#                     res = requests.post(
#                         f"{BACKEND_URL}/send-reply",
#                         json=rep,
#                         cookies=st.session_state.get("cookies", {})
#                     )

#                     if res.status_code == 200:
#                         st.markdown("<div class='msg-ok'>✦ Reply sent!</div>", unsafe_allow_html=True)
#                     else:
#                         st.error("Reply failed")
#                 except: pass
#                 st.markdown("<div class='msg-ok'>✦ Reply sent!</div>", unsafe_allow_html=True)
#                 st.session_state.ai_reply = None
#         st.markdown("</div>", unsafe_allow_html=True)
#     else:
#         st.info("Load emails above to get started.")

# elif st.session_state.page == "reply":
#     st.markdown("""
# <div class="fp-header anim-1">
#   <div class="fp-icon" style="background:rgba(232,180,184,0.15);border:1px solid rgba(232,180,184,0.3);">↩</div>
#   <div>
#     <div class="fp-title">Smart Reply</div>
#     <div class="fp-sub">Fetch any conversation and reply with AI context</div>
#   </div>
# </div>
# """, unsafe_allow_html=True)

#     target = st.text_input("📧 Email Address", placeholder="Enter sender/recipient email")
#     if st.button("↩  Fetch Conversations", use_container_width=True):
#         if target:
#             with st.spinner("Loading…"):
#                 try:
                    
#                     st.session_state.emails = reply_using_email_flow(st.session_state.user, target, 100)
#                 except: st.session_state.emails = []
#             st.markdown("<div class='msg-ok'>✦ Conversations loaded</div>", unsafe_allow_html=True)
#         else:
#             st.markdown("<div class='msg-warn'>⚠ Enter an email address first</div>", unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

#     if st.session_state.emails:
#         opts = {f"{e['subject']} — {e['from']}": e for e in st.session_state.emails}
#         sel_lbl = st.selectbox("Select Thread", list(opts.keys()), key="r_sel")
#         sel = opts[sel_lbl]
#         st.markdown(f"<div class='email-item'><strong>From:</strong> {sel['from']}<br><strong>Subject:</strong> {sel['subject']}</div>", unsafe_allow_html=True)
#         with st.expander("📜 Full email"):
#             st.write(sel.get("body","No content"))

#         st.markdown('<div class="panel">', unsafe_allow_html=True)
#         ri = st.text_area("Reply Intent", placeholder="What should AI write?", key="r_intent")
#         rc1, rc2 = st.columns(2)
#         with rc1:
#             rs = st.text_input("Your Name", key="r_sender")
#             rt = st.text_input("Recipient Role", key="r_role")
#         with rc2:
#             rn = st.text_input("Recipient Name (optional)", key="r_name")
#         if st.button("⟳  Generate AI Reply", use_container_width=True, key="r_gen"):
#             if ri and rs and rt:
#                 with st.spinner("Generating…"):
#                     try:
                        
#                         st.session_state.ai_reply = generate_reply(selected_email=sel, user_intent=ri, sender_name=rs, recipient_type=rt, recipient_name=rn)
#                     except Exception as e:
#                         st.session_state.ai_reply = {"subject":"Re: "+sel.get("subject",""),"email":"[Reply]","to":sel.get("from","")}
#                 st.markdown("<div class='msg-ok'>✦ Reply ready</div>", unsafe_allow_html=True)
#         if st.session_state.ai_reply:
#             rep = st.session_state.ai_reply
#             rs2 = st.text_input("Subject", value=rep.get("subject",""), key="r_subj")
#             rb2 = st.text_area("Reply Body", value=rep.get("email",""), height=200, key="r_body")
#             if st.button("📤  Send Reply", use_container_width=True, key="r_send"):
#                 try:
                    
#                     rep["subject"] = rs2; rep["email"] = rb2
#                     send_reply_flow(st.session_state.user, rep)
#                 except: pass
#                 st.markdown("<div class='msg-ok'>✦ Reply sent!</div>", unsafe_allow_html=True)
#                 st.session_state.ai_reply = None
#         st.markdown("</div>", unsafe_allow_html=True)
#     else:
#         st.info("Enter an email address above and fetch conversations.")

# # ── FOOTER + LOGOUT ──
# st.markdown("<br>", unsafe_allow_html=True)
# st.markdown('<div class="foot">OrchestraMail AI &nbsp;·&nbsp; Multi-Agent Email Intelligence &nbsp;·&nbsp; Built with ♦ and care</div>', unsafe_allow_html=True)
# st.markdown("<br>", unsafe_allow_html=True)
# _, lc, _ = st.columns([4, 1, 4])
# with lc:
#     if st.button("⎋  Sign Out", key="logout", use_container_width=True):
#         st.link_button("⎋  Sign Out", f"{BACKEND_URL}/logout", use_container_width=True)
#         st.session_state.clear()
#         st.rerun()
