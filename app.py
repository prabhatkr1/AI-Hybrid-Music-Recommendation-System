"""
SoundSphere — Advanced 3D Premium AI Music Recommender
Run: streamlit run app.py
"""

import streamlit as st
from weather_fetcher import get_weather
from spotify_api import get_music_recommendations

# ─── PAGE CONFIG (must be first) ────────────────────────────────────────────
st.set_page_config(
    page_title="SoundSphere · AI Music",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── PREMIUM 3D CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

:root {
    --c-bg:        #06080f;
    --c-surface:   rgba(255,255,255,0.04);
    --c-border:    rgba(255,255,255,0.08);
    --c-border-hi: rgba(255,255,255,0.18);
    --c-text:      #e8eaf4;
    --c-muted:     #6b7280;
    --c-accent-1:  #7c6ef7;
    --c-accent-2:  #e05ae0;
    --c-accent-3:  #06d0c8;
    --c-glow-1:    rgba(124,110,247,0.35);
    --c-glow-2:    rgba(224,90,224,0.28);
    --radius-sm:   10px;
    --radius-md:   16px;
    --radius-lg:   24px;
    --font-main:   'Outfit', sans-serif;
    --font-mono:   'Space Mono', monospace;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: var(--c-bg) !important;
    font-family: var(--font-main) !important;
    color: var(--c-text) !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"],
#MainMenu, footer, header { display: none !important; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1280px !important; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
div[data-testid="column"] { padding: 0 .75rem !important; }

/* ── Animated background ── */
body::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 90% 70% at 15%  5%,  rgba(124,110,247,.20) 0%, transparent 55%),
        radial-gradient(ellipse 65% 55% at 85% 15%,  rgba(224,90,224,.15)  0%, transparent 50%),
        radial-gradient(ellipse 50% 45% at 50% 85%,  rgba(6,208,200,.12)   0%, transparent 50%),
        radial-gradient(ellipse 40% 35% at 75% 60%,  rgba(124,110,247,.10) 0%, transparent 45%);
    animation: bgPulse 16s ease-in-out infinite alternate;
}
@keyframes bgPulse {
    0%  { transform: scale(1)    rotate(0deg);  filter: hue-rotate(0deg);   }
    50% { transform: scale(1.04) rotate(1deg);  filter: hue-rotate(15deg);  }
    100%{ transform: scale(.98)  rotate(-1deg); filter: hue-rotate(-15deg); }
}

/* floating orb */
body::after {
    content: '';
    position: fixed; width: 500px; height: 500px;
    top: -120px; right: -120px; z-index: 0; pointer-events: none;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, rgba(124,110,247,.22), transparent 65%);
    filter: blur(60px);
    animation: orbDrift 20s ease-in-out infinite alternate;
}
@keyframes orbDrift {
    from { transform: translate(0,0) scale(1);      }
    to   { transform: translate(-60px,80px) scale(1.15); }
}

[data-testid="stAppViewContainer"] > * { position: relative; z-index: 1; }

/* mesh grid overlay */
.ss-grid {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        linear-gradient(rgba(255,255,255,.022) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.022) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 10%, transparent 80%);
}

/* ── HERO ── */
.hero-wrap {
    padding: 4rem 0 3.5rem; text-align: center; position: relative;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: .5rem;
    font-size: .7rem; font-weight: 600; letter-spacing: .2em;
    text-transform: uppercase; color: var(--c-accent-1);
    background: rgba(124,110,247,.12); border: 1px solid rgba(124,110,247,.25);
    padding: .35rem 1rem; border-radius: 100px; margin-bottom: 1.5rem;
}
.hero-badge::before {
    content: ''; display: inline-block;
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--c-accent-1); box-shadow: 0 0 8px var(--c-accent-1);
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.8)} }

.hero-title {
    font-size: clamp(3rem, 7vw, 5.5rem); font-weight: 900;
    line-height: 1; letter-spacing: -.03em;
    background: linear-gradient(135deg, #fff 20%, var(--c-accent-1) 50%, var(--c-accent-2) 80%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    position: relative;
}
.hero-title::after {
    content: 'SoundSphere'; position: absolute; inset: 0;
    background: linear-gradient(135deg, transparent 20%, var(--c-accent-1) 50%, var(--c-accent-2) 80%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    filter: blur(18px) opacity(.45); z-index: -1;
}
.hero-sub { font-size: 1rem; color: var(--c-muted); margin-top: 1rem; letter-spacing: .01em; }
.hero-divider {
    width: 80px; height: 2px; margin: 1.8rem auto 0;
    background: linear-gradient(90deg, var(--c-accent-1), var(--c-accent-2));
    border-radius: 100px; box-shadow: 0 0 12px var(--c-glow-1);
}

/* ── 3-D CARD ── */
.card-3d { perspective: 900px; width: 100%; margin-bottom: 1.5rem; }
.card-inner {
    background: rgba(12,15,28,0.75);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-lg);
    padding: 2rem;
    backdrop-filter: blur(24px) saturate(1.4);
    -webkit-backdrop-filter: blur(24px) saturate(1.4);
    box-shadow:
        0 2px 0 rgba(255,255,255,.06) inset,
        0 -1px 0 rgba(0,0,0,.6) inset,
        0 20px 60px rgba(0,0,0,.55),
        0 4px 20px rgba(124,110,247,.12);
    transform-style: preserve-3d;
    transition: transform .4s cubic-bezier(.23,1,.32,1), box-shadow .4s;
    position: relative; overflow: hidden;
}
.card-inner::before {
    content: '';
    position: absolute; top: 0; left: 5%; right: 5%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.18), transparent);
    border-radius: 100px;
}
.card-inner::after {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, var(--c-glow-1), transparent 70%);
    pointer-events: none;
}
.card-3d:hover .card-inner {
    transform: rotateX(2deg) rotateY(-2deg) translateZ(8px);
    box-shadow:
        0 2px 0 rgba(255,255,255,.08) inset,
        0 -1px 0 rgba(0,0,0,.6) inset,
        0 30px 80px rgba(0,0,0,.7),
        0 8px 30px rgba(124,110,247,.22);
}

/* ── FORM ELEMENTS ── */
label,
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label {
    font-family: var(--font-main) !important;
    font-size: .72rem !important; font-weight: 600 !important;
    letter-spacing: .16em !important; text-transform: uppercase !important;
    color: var(--c-accent-1) !important; margin-bottom: .5rem !important;
}
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid var(--c-border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--c-text) !important;
    font-family: var(--font-main) !important;
    font-size: .95rem !important; padding: .75rem 1.1rem !important;
    transition: border-color .2s, box-shadow .2s; height: 50px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(124,110,247,.6) !important;
    box-shadow: 0 0 0 3px rgba(124,110,247,.15), 0 0 20px rgba(124,110,247,.1) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #374151 !important; }
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid var(--c-border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--c-text) !important;
    font-family: var(--font-main) !important;
}
[data-testid="stSelectbox"] svg { fill: var(--c-accent-1) !important; }

/* ── MOOD PILLS ── */
.mood-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .55rem; margin: .5rem 0 1.5rem; }
.mood-pill {
    position: relative; overflow: hidden;
    padding: .7rem .9rem; border-radius: var(--radius-sm);
    border: 1px solid var(--c-border);
    background: rgba(255,255,255,.03);
    font-family: var(--font-main); font-size: .85rem; font-weight: 500;
    color: var(--c-muted); text-align: center; cursor: pointer;
    transition: all .25s cubic-bezier(.23,1,.32,1);
}
.mood-pill::before {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(135deg, var(--c-accent-1), var(--c-accent-2));
    opacity: 0; transition: opacity .25s; border-radius: inherit;
}
.mood-pill span { position: relative; z-index: 1; }
.mood-pill:hover {
    border-color: rgba(124,110,247,.4); color: #c7d2fe;
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 20px rgba(0,0,0,.3), 0 0 12px rgba(124,110,247,.2);
}
.mood-pill:hover::before { opacity: .08; }
.mood-pill.active {
    border-color: rgba(124,110,247,.5); color: #e0e7ff; font-weight: 600;
    background: rgba(124,110,247,.15);
    box-shadow: 0 4px 20px rgba(124,110,247,.25), inset 0 1px 0 rgba(255,255,255,.08);
    transform: translateY(-1px);
}
.mood-pill.active::before { opacity: .12; }

/* ── CTA BUTTON ── */
.stButton > button {
    position: relative; overflow: hidden;
    background: linear-gradient(135deg, #6d62f0, #9e49e0) !important;
    color: #fff !important; border: none !important;
    border-radius: var(--radius-md) !important;
    height: 56px !important; width: 100% !important;
    font-family: var(--font-main) !important;
    font-size: 1rem !important; font-weight: 700 !important;
    letter-spacing: .06em !important; margin-top: .5rem !important;
    transition: transform .2s cubic-bezier(.23,1,.32,1), box-shadow .2s !important;
    box-shadow: 0 4px 20px rgba(109,98,240,.45), 0 1px 0 rgba(255,255,255,.2) inset !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 8px 32px rgba(109,98,240,.65), 0 1px 0 rgba(255,255,255,.2) inset !important;
}
.stButton > button:active { transform: translateY(0) scale(.99) !important; }

/* ── WEATHER STRIP ── */
.weather-strip {
    display: flex; align-items: center; gap: 1rem;
    background: rgba(6,208,200,.07);
    border: 1px solid rgba(6,208,200,.18);
    border-radius: var(--radius-md); padding: .9rem 1.2rem;
    margin-bottom: 1.4rem; position: relative; overflow: hidden;
}
.weather-strip::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
    background: linear-gradient(180deg, var(--c-accent-3), transparent); border-radius: 100px;
}
.weather-temp {
    font-family: var(--font-mono); font-size: 1.6rem; font-weight: 700;
    color: var(--c-accent-3); line-height: 1;
    text-shadow: 0 0 20px rgba(6,208,200,.4);
}
.weather-detail { flex: 1; }
.weather-city { font-size: .9rem; font-weight: 600; color: var(--c-text); }
.weather-desc { font-size: .78rem; color: var(--c-muted); margin-top: .15rem; }
.weather-mood-badge {
    font-size: .72rem; font-weight: 600; letter-spacing: .08em;
    padding: .3rem .75rem; border-radius: 100px;
    background: rgba(124,110,247,.15); color: #c4b5fd;
    border: 1px solid rgba(124,110,247,.25);
}

/* ── SONG CARDS ── */
.songs-header {
    font-size: .72rem; font-weight: 600;
    letter-spacing: .18em; text-transform: uppercase;
    color: var(--c-muted); margin-bottom: .9rem;
    display: flex; align-items: center; gap: .6rem;
}
.songs-header::before {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, var(--c-border));
}
.songs-header::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--c-border), transparent);
}
.song-card {
    display: flex; align-items: center; gap: .9rem;
    background: rgba(255,255,255,.035);
    border: 1px solid var(--c-border); border-radius: var(--radius-md);
    padding: .85rem 1.1rem; margin-bottom: .55rem;
    text-decoration: none !important; color: inherit !important;
    cursor: pointer;
    transition: all .25s cubic-bezier(.23,1,.32,1);
    position: relative; overflow: hidden;
}
.song-card::before {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(124,110,247,.06), rgba(224,90,224,.04));
    opacity: 0; transition: opacity .25s;
}
.song-card:hover {
    border-color: rgba(124,110,247,.3);
    transform: translateX(6px);
    box-shadow: -4px 4px 20px rgba(0,0,0,.3), 0 0 12px rgba(124,110,247,.12);
}
.song-card:hover::before { opacity: 1; }

.song-num {
    font-family: var(--font-mono); font-size: .72rem;
    color: #374151; min-width: 22px; position: relative; z-index: 1;
}
.song-icon-wrap {
    width: 42px; height: 42px; border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; position: relative; z-index: 1;
    box-shadow: 0 4px 14px rgba(0,0,0,.4), 0 1px 0 rgba(255,255,255,.08) inset;
}
.song-info { flex: 1; min-width: 0; position: relative; z-index: 1; }
.song-name { font-size: .9rem; font-weight: 500; color: var(--c-text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.song-artist { font-size: .77rem; color: var(--c-muted); margin-top: .15rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.song-arrow { color: #1f2937; font-size: .9rem; transition: color .25s, transform .25s; position: relative; z-index: 1; }
.song-card:hover .song-arrow { color: var(--c-accent-1); transform: translateX(3px); }

/* ── STATES ── */
.empty-state { text-align: center; padding: 3.5rem 1.5rem; display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.empty-orb {
    width: 72px; height: 72px; border-radius: 50%;
    background: rgba(124,110,247,.08); border: 1px solid rgba(124,110,247,.15);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem; animation: floatOrb 4s ease-in-out infinite;
}
@keyframes floatOrb { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
.empty-title { font-size: 1rem; font-weight: 600; color: #374151; }
.empty-sub   { font-size: .82rem; color: #1f2937; max-width: 220px; line-height: 1.6; }
.err-box {
    background: rgba(239,68,68,.08); border: 1px solid rgba(239,68,68,.2);
    border-radius: var(--radius-md); padding: 1rem 1.2rem;
    color: #fca5a5; font-size: .88rem; margin-bottom: 1rem;
}
.stat-row { display: flex; gap: .5rem; flex-wrap: wrap; margin-bottom: 1.2rem; }
.stat-chip {
    font-size: .72rem; font-weight: 600; letter-spacing: .06em;
    padding: .35rem .85rem; border-radius: 100px;
    border: 1px solid var(--c-border); color: var(--c-muted);
    background: rgba(255,255,255,.03);
}
.stat-chip.hi { background: rgba(124,110,247,.12); border-color: rgba(124,110,247,.25); color: #c4b5fd; }

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .block-container { padding: 0 1rem 3rem !important; }
    .hero-title      { font-size: 2.6rem !important; }
    div[data-testid="column"] { padding: 0 .25rem !important; }
    .card-inner      { padding: 1.4rem; }
    .card-3d:hover .card-inner { transform: none; }
}
@media (max-width: 480px) {
    .hero-wrap  { padding: 2.5rem 0 2rem; }
    .hero-title { font-size: 2rem !important; }
    .mood-grid  { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)


# ─── CONSTANTS ───────────────────────────────────────────────────────────────
MOODS = {
    "Happy":     {"emoji": "😄", "tag": "upbeat pop funk",           "grad": "linear-gradient(135deg,#f59e0b,#f97316)"},
    "Sad":       {"emoji": "😢", "tag": "melancholic acoustic slow",  "grad": "linear-gradient(135deg,#60a5fa,#3b82f6)"},
    "Energetic": {"emoji": "⚡", "tag": "edm dance electronic",       "grad": "linear-gradient(135deg,#f472b6,#e11d48)"},
    "Calm":      {"emoji": "🌿", "tag": "ambient lo-fi chill",        "grad": "linear-gradient(135deg,#34d399,#059669)"},
    "Romantic":  {"emoji": "💜", "tag": "soul rnb romantic",          "grad": "linear-gradient(135deg,#a78bfa,#7c3aed)"},
    "Angry":     {"emoji": "🔥", "tag": "metal rock intense",         "grad": "linear-gradient(135deg,#f87171,#dc2626)"},
    "Focus":     {"emoji": "🧠", "tag": "study classical minimal",    "grad": "linear-gradient(135deg,#7c6ef7,#6d28d9)"},
    "Nostalgic": {"emoji": "🌅", "tag": "retro 80s classic hits",     "grad": "linear-gradient(135deg,#fbbf24,#d97706)"},
}

WEATHER_ICONS = {
    "clear":"☀️","sunny":"☀️","cloud":"☁️","overcast":"☁️",
    "rain":"🌧️","drizzle":"🌦️","shower":"🌦️","snow":"❄️",
    "storm":"⛈️","thunder":"⛈️","fog":"🌫️","mist":"🌫️","haze":"🌫️",
}

CARD_ICONS = ["🎵","🎸","🎹","🎺","🎷","🥁","🎻","🎤","🎼","🎙️"]


def _weather_icon(desc: str) -> str:
    d = desc.lower()
    for k, v in WEATHER_ICONS.items():
        if k in d:
            return v
    return "🌡️"


def _song_card_html(index: int, song, mood_cfg: dict) -> str:
    if isinstance(song, dict):
        name   = song.get("name",   "Unknown Track")
        artist = song.get("artist", "")
        url    = song.get("url",    "#")
    else:
        name, artist, url = str(song), "", "#"

    num   = f"{index + 1:02d}"
    icon  = CARD_ICONS[index % len(CARD_ICONS)]
    grad  = mood_cfg["grad"]
    open_ = f'<a href="{url}" target="_blank" rel="noopener" class="song-card">' if url != "#" else '<div class="song-card">'
    close = "</a>" if url != "#" else "</div>"
    artist_html = f'<div class="song-artist">{artist}</div>' if artist else ""

    return (
        f"{open_}"
        f'<div class="song-num">{num}</div>'
        f'<div class="song-icon-wrap" style="background:{grad};">{icon}</div>'
        f'<div class="song-info">'
        f'<div class="song-name">{name}</div>{artist_html}'
        f'</div>'
        f'<div class="song-arrow">&#8594;</div>'
        f"{close}"
    )


# ─── SESSION STATE ────────────────────────────────────────────────────────────
for key, default in [
    ("selected_mood", "Happy"),
    ("results", None),
    ("searched", False),
    ("last_city", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ─── MESH + HERO ──────────────────────────────────────────────────────────────
st.markdown('<div class="ss-grid"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">AI &middot; Weather &middot; Spotify</div>
    <div class="hero-title">SoundSphere</div>
    <div class="hero-sub">Your city. Your mood. Your perfect soundtrack &mdash; powered by AI.</div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)


# ─── TWO-COLUMN LAYOUT ───────────────────────────────────────────────────────
left, right = st.columns([1, 1.2], gap="large")


# ══ LEFT: INPUT CARD ══════════════════════════════════════════════════════════
with left:
    st.markdown('<div class="card-3d"><div class="card-inner">', unsafe_allow_html=True)

    city_val = st.text_input(
        "📍 Your City",
        placeholder="Mumbai, Tokyo, London…",
        key="city_input",
        value=st.session_state.last_city,
    )

    st.markdown(
        '<div style="font-size:.72rem;font-weight:600;letter-spacing:.16em;'
        'text-transform:uppercase;color:#7c6ef7;margin:.9rem 0 .1rem;">🎭 Your Mood</div>',
        unsafe_allow_html=True,
    )

    mood_options = list(MOODS.keys())

    pills_html = '<div class="mood-grid">'
    for m in mood_options:
        active = "active" if m == st.session_state.selected_mood else ""
        pills_html += (
            f'<div class="mood-pill {active}">'
            f'<span>{MOODS[m]["emoji"]} {m}</span>'
            f'</div>'
        )
    pills_html += "</div>"
    st.markdown(pills_html, unsafe_allow_html=True)

    chosen_mood = st.selectbox(
        "Mood",
        options=mood_options,
        index=mood_options.index(st.session_state.selected_mood),
        label_visibility="collapsed",
        key="mood_select",
    )
    st.session_state.selected_mood = chosen_mood

    hit = st.button("🎧  Discover My Soundtrack", use_container_width=True)

    st.markdown("""
    <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.2rem;">
        <div style="font-size:.72rem;color:#1f2937;padding:.3rem .7rem;background:rgba(255,255,255,.03);
                    border:1px solid rgba(255,255,255,.06);border-radius:100px;">🌤 Weather-aware</div>
        <div style="font-size:.72rem;color:#1f2937;padding:.3rem .7rem;background:rgba(255,255,255,.03);
                    border:1px solid rgba(255,255,255,.06);border-radius:100px;">🤖 AI-curated</div>
        <div style="font-size:.72rem;color:#1f2937;padding:.3rem .7rem;background:rgba(255,255,255,.03);
                    border:1px solid rgba(255,255,255,.06);border-radius:100px;">🎵 Spotify-linked</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


# ══ RIGHT: RESULTS CARD ═══════════════════════════════════════════════════════
with right:
    st.markdown('<div class="card-3d"><div class="card-inner">', unsafe_allow_html=True)

    if hit:
        if not city_val.strip():
            st.markdown(
                '<div class="err-box">&#9888; Please enter a city name to continue.</div>',
                unsafe_allow_html=True,
            )
            st.session_state.searched = False
        else:
            st.session_state.last_city = city_val.strip()
            with st.spinner("Tuning into your vibe…"):
                try:
                    weather_desc, temp = get_weather(city_val.strip())
                    mood_cfg = MOODS[chosen_mood]
                    query    = f"{chosen_mood} {mood_cfg['tag']} {weather_desc}"
                    songs    = get_music_recommendations(query)
                    st.session_state.results = {
                        "city":    city_val.strip(),
                        "weather": weather_desc,
                        "temp":    temp,
                        "mood":    chosen_mood,
                        "songs":   songs,
                    }
                    st.session_state.searched = True
                except Exception as exc:
                    st.session_state.results  = {"error": str(exc)}
                    st.session_state.searched = True

    if st.session_state.searched and st.session_state.results:
        data = st.session_state.results

        if "error" in data:
            st.markdown(
                f'<div class="err-box">&#10060; <strong>Error:</strong> {data["error"]}<br>'
                f'<span style="font-size:.8rem;opacity:.7">Check your API keys or city name.</span></div>',
                unsafe_allow_html=True,
            )
        else:
            mood_cfg  = MOODS[data["mood"]]
            w_icon    = _weather_icon(data["weather"])
            songs     = data["songs"] or []
            city_disp = data["city"].title()

            st.markdown(f"""
            <div class="weather-strip">
                <div class="weather-temp">{data['temp']}&deg;C</div>
                <div class="weather-detail">
                    <div class="weather-city">{w_icon} {city_disp}</div>
                    <div class="weather-desc">{data['weather'].capitalize()}</div>
                </div>
                <div class="weather-mood-badge">{mood_cfg['emoji']} {data['mood']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="stat-row">
                <div class="stat-chip hi">{len(songs)} tracks</div>
                <div class="stat-chip">AI-curated</div>
                <div class="stat-chip">Spotify</div>
            </div>
            """, unsafe_allow_html=True)

            if not songs:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-orb">&#128263;</div>
                    <div class="empty-title">No tracks found</div>
                    <div class="empty-sub">Try a different mood or city and search again.</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="songs-header">Recommended Tracks</div>', unsafe_allow_html=True)
                for i, song in enumerate(songs):
                    st.markdown(_song_card_html(i, song, mood_cfg), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-orb">&#127911;</div>
            <div class="empty-title">Ready when you are</div>
            <div class="empty-sub">Pick a city and a mood, then hit Discover.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 1rem;
            font-size:.72rem;letter-spacing:.12em;color:#111827;text-transform:uppercase;">
    SoundSphere &nbsp;&middot;&nbsp; AI &times; Weather &times; Spotify
</div>
""", unsafe_allow_html=True)
