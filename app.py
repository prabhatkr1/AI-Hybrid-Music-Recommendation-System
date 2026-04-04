import streamlit as st
from weather_fetcher import get_weather
from spotify_api import get_music_recommendations

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SoundSphere · AI Music Recommender",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# PREMIUM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #050810 !important;
    color: #e8eaf0;
    font-family: 'DM Sans', sans-serif;
}

/* Animated aurora background */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(99,102,241,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 80%, rgba(236,72,153,0.14) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 60% 30%, rgba(16,185,129,0.10) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
    animation: auroraShift 12s ease-in-out infinite alternate;
}
@keyframes auroraShift {
    0%  { filter: hue-rotate(0deg) brightness(1);   }
    100%{ filter: hue-rotate(30deg) brightness(1.1); }
}

/* ── Streamlit container cleanup ── */
[data-testid="stAppViewContainer"] > div { position: relative; z-index: 1; }
[data-testid="stHeader"]           { display: none !important; }
.block-container                   { padding: 2.5rem 3rem 4rem !important; max-width: 1300px !important; }
[data-testid="stVerticalBlock"]    { gap: 0 !important; }
div[data-testid="column"]          { padding: 0 1rem !important; }

/* ── Hero title ── */
.hero {
    text-align: center;
    padding: 3rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: .75rem;
    font-weight: 500;
    letter-spacing: .25em;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: .75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, #e8eaf0 30%, #818cf8 65%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: .95rem;
    color: #6b7280;
    margin-top: .9rem;
    letter-spacing: .02em;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(129,140,248,.35), transparent);
    margin: 1.5rem 0 2rem;
}

/* ── Glass panel ── */
.panel {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.06);
    height: 100%;
}

/* ── Labels ── */
label, [data-testid="stSelectbox"] label,
[data-testid="stTextInput"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: .78rem !important;
    font-weight: 500 !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    color: #6366f1 !important;
    margin-bottom: .35rem !important;
}

/* ── Text inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .95rem !important;
    padding: .7rem 1rem !important;
    transition: border .2s, box-shadow .2s;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(99,102,241,.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
    outline: none !important;
}

/* ── Mood pills ── */
.mood-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: .6rem;
    margin-top: .4rem;
}
.mood-pill {
    cursor: pointer;
    padding: .65rem 1rem;
    border-radius: 100px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.04);
    font-size: .88rem;
    font-weight: 500;
    color: #9ca3af;
    text-align: center;
    transition: all .2s;
    user-select: none;
}
.mood-pill:hover   { border-color: rgba(99,102,241,.5); color: #c7d2fe; background: rgba(99,102,241,.12); }
.mood-pill.active  { border-color: #6366f1; background: rgba(99,102,241,.25); color: #e0e7ff; font-weight: 600; box-shadow: 0 0 12px rgba(99,102,241,.3); }

/* ── CTA button ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    height: 54px !important;
    width: 100% !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: .06em !important;
    margin-top: 1.2rem !important;
    transition: transform .15s, box-shadow .15s !important;
    box-shadow: 0 4px 20px rgba(99,102,241,.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,.6) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Weather badge ── */
.weather-badge {
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    background: rgba(16,185,129,.12);
    border: 1px solid rgba(16,185,129,.25);
    color: #6ee7b7;
    border-radius: 100px;
    padding: .45rem 1rem;
    font-size: .85rem;
    font-weight: 500;
    margin-bottom: 1.4rem;
}

/* ── Results section ── */
.results-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #c7d2fe;
    letter-spacing: .04em;
    margin-bottom: 1rem;
}

/* ── Song card ── */
.song-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: .9rem 1.1rem;
    margin-bottom: .6rem;
    transition: background .2s, border-color .2s, transform .15s;
    text-decoration: none !important;
    cursor: pointer;
}
.song-card:hover {
    background: rgba(99,102,241,0.10);
    border-color: rgba(99,102,241,0.30);
    transform: translateX(4px);
}
.song-icon {
    width: 40px; height: 40px;
    border-radius: 10px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(99,102,241,.35);
}
.song-info { flex: 1; min-width: 0; }
.song-name {
    font-weight: 500;
    font-size: .9rem;
    color: #e8eaf0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.song-artist {
    font-size: .78rem;
    color: #6b7280;
    margin-top: .15rem;
}
.song-arrow { color: #4b5563; font-size: .9rem; transition: color .2s; }
.song-card:hover .song-arrow { color: #818cf8; }

/* ── Error / info states ── */
.state-box {
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: .9rem;
    margin-bottom: 1rem;
}
.state-error   { background: rgba(239,68,68,.10); border: 1px solid rgba(239,68,68,.25); color: #fca5a5; }
.state-info    { background: rgba(59,130,246,.10); border: 1px solid rgba(59,130,246,.25); color: #93c5fd; }
.state-empty   { text-align: center; color: #4b5563; padding: 3rem 1rem; font-size: .9rem; }

/* ── Streamlit overrides ── */
[data-testid="stSelectbox"] svg { fill: #6366f1 !important; }
[data-testid="stMarkdownContainer"] p { margin: 0; }
footer { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MOOD CONFIG
# ─────────────────────────────────────────────
MOODS = {
    "Happy":     {"emoji": "😄", "color": "#fbbf24", "genre": "pop upbeat"},
    "Sad":       {"emoji": "😢", "color": "#60a5fa", "genre": "acoustic melancholy"},
    "Energetic": {"emoji": "⚡", "color": "#f472b6", "genre": "electronic edm"},
    "Calm":      {"emoji": "🌿", "color": "#34d399", "genre": "ambient lo-fi"},
    "Romantic":  {"emoji": "💜", "color": "#a78bfa", "genre": "soul romantic"},
    "Angry":     {"emoji": "🔥", "color": "#f87171", "genre": "metal rock intense"},
}

WEATHER_EMOJI = {
    "clear": "☀️", "sunny": "☀️", "cloud": "☁️", "rain": "🌧️",
    "drizzle": "🌦️", "snow": "❄️", "storm": "⛈️", "fog": "🌫️",
    "mist": "🌫️", "haze": "🌫️",
}

def weather_icon(desc: str) -> str:
    desc_lower = desc.lower()
    for key, icon in WEATHER_EMOJI.items():
        if key in desc_lower:
            return icon
    return "🌡️"


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = "Happy"
if "results" not in st.session_state:
    st.session_state.results = None   # dict with weather + songs, or error str
if "searched" not in st.session_state:
    st.session_state.searched = False


# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Powered by AI · Weather · Spotify</div>
    <div class="hero-title">SoundSphere</div>
    <div class="hero-sub">Your mood. Your weather. Your perfect soundtrack.</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
left, right = st.columns([1, 1.15], gap="large")

# ── LEFT: controls ──────────────────────────
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    # City input
    city = st.text_input(
        "📍 Your City",
        placeholder="e.g. Mumbai, Tokyo, New York…",
        key="city_input",
    )

    # Mood picker via JS pill selection + hidden selectbox
    st.markdown("**🎭 Your Mood**", unsafe_allow_html=True)

    # Build mood pills (pure CSS, no JS needed — use selectbox underneath)
    mood_options = list(MOODS.keys())
    mood_html = '<div class="mood-grid">'
    for m in mood_options:
        active = "active" if m == st.session_state.selected_mood else ""
        mood_html += f'<div class="mood-pill {active}" onclick="void(0)">{MOODS[m]["emoji"]} {m}</div>'
    mood_html += "</div>"
    st.markdown(mood_html, unsafe_allow_html=True)

    # Actual selectbox (hidden visually via selectbox label; drives state)
    selected_mood = st.selectbox(
        "Select mood",
        options=mood_options,
        index=mood_options.index(st.session_state.selected_mood),
        label_visibility="collapsed",
        key="mood_select",
    )
    st.session_state.selected_mood = selected_mood

    go = st.button("🎧  Discover My Soundtrack", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── RIGHT: results ───────────────────────────
with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if go:
        if not city.strip():
            st.markdown('<div class="state-box state-error">⚠️ Please enter a city name first.</div>', unsafe_allow_html=True)
            st.session_state.searched = False
        else:
            with st.spinner("Tuning into your vibe…"):
                try:
                    weather_desc, temp = get_weather(city.strip())
                    query = f"{selected_mood} {MOODS[selected_mood]['genre']} {weather_desc}"
                    songs = get_music_recommendations(query)
                    st.session_state.results = {
                        "weather": weather_desc,
                        "temp": temp,
                        "songs": songs,
                        "city": city.strip(),
                    }
                    st.session_state.searched = True
                except Exception as e:
                    st.session_state.results = {"error": str(e)}
                    st.session_state.searched = True

    if st.session_state.searched and st.session_state.results:
        data = st.session_state.results

        if "error" in data:
            st.markdown(
                f'<div class="state-box state-error">❌ Something went wrong: {data["error"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            w_icon = weather_icon(data["weather"])
            mood_cfg = MOODS[st.session_state.selected_mood]

            # Weather badge
            st.markdown(
                f'<div class="weather-badge">'
                f'{w_icon} {data["city"].title()} · {data["weather"].capitalize()} · {data["temp"]}°C'
                f'  &nbsp;|&nbsp;  {mood_cfg["emoji"]} {st.session_state.selected_mood}'
                f'</div>',
                unsafe_allow_html=True,
            )

            songs: list = data["songs"]
            if not songs:
                st.markdown('<div class="state-empty">🔇 No songs found. Try a different mood or city.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="results-title">🎶 {len(songs)} Tracks Curated For You</div>', unsafe_allow_html=True)
                icons = ["🎵", "🎸", "🎹", "🎺", "🎷", "🥁", "🎻", "🎤"]
                for i, song in enumerate(songs):
                    # Support both dict {"name":…, "artist":…, "url":…} and plain strings
                    if isinstance(song, dict):
                        name   = song.get("name", "Unknown Track")
                        artist = song.get("artist", "Unknown Artist")
                        url    = song.get("url", "#")
                    else:
                        name   = str(song)
                        artist = ""
                        url    = "#"

                    icon = icons[i % len(icons)]
                    link_open  = f'<a href="{url}" target="_blank" class="song-card">' if url != "#" else '<div class="song-card">'
                    link_close = "</a>" if url != "#" else "</div>"

                    st.markdown(
                        f'{link_open}'
                        f'<div class="song-icon">{icon}</div>'
                        f'<div class="song-info">'
                        f'  <div class="song-name">{name}</div>'
                        f'  {"<div class=song-artist>" + artist + "</div>" if artist else ""}'
                        f'</div>'
                        f'<div class="song-arrow">→</div>'
                        f'{link_close}',
                        unsafe_allow_html=True,
                    )
    elif not st.session_state.searched:
        st.markdown("""
        <div class="state-empty">
            <div style="font-size:2.5rem;margin-bottom:.8rem">🎧</div>
            <div style="color:#6b7280;font-size:.9rem">
                Enter your city, pick a mood,<br>and hit <strong style="color:#818cf8">Discover</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
