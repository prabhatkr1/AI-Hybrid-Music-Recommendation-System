
import streamlit as st
from weather_fetcher import get_weather
from spotify_api import get_music_recommendations
# from mood_detector import detect_emotion  # Uncomment if using webcam mood detection
import streamlit as st

st.set_page_config(page_title="AI Music Recommender", layout="wide")

# ===== ADVANCED FUTURISTIC UI =====
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Glass card */
.glass {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,255,255,0.2);
}

/* Neon Title */
.title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    color: #00ffff;
    text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
}

/* Input styling */
input, select {
    border-radius: 10px !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(45deg, #00f2fe, #4facfe);
    color: white;
    border-radius: 25px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    transition: 0.3s;
    box-shadow: 0 0 15px rgba(0,255,255,0.5);
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px rgba(0,255,255,1);
}

/* Cards */
.result-box {
    background: rgba(0,0,0,0.5);
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


st.markdown('<div class="title">🎧 AI Hybrid Music Recommender</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

with col1:
    city = st.text_input("🌍 Enter your city")
    mood = st.selectbox("😊 Select mood", ["Happy", "Sad", "Energetic", "Calm"])

    recommend = st.button("🚀 Recommend Music")

with col2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    if recommend:
        st.success(f"Selected Mood: {mood}")

        weather, temp = get_weather(city)
        st.info(f"Weather: {weather}, Temp: {temp}°C")

        songs = get_music_recommendations(mood, weather)

        st.markdown("### 🎶 Recommended Songs")
        for song in songs:
            st.markdown(f"""
            <div class="result-box">
                🎵 {song}
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
city = st.text_input("Enter your city for weather", "Delhi")
mood = st.selectbox("Select your mood", ["Happy", "Sad", "Energetic", "Calm"])

if st.button("Recommend Music"):
    # mood = detect_emotion()  # Uncomment if using webcam mood detection
    st.success(f"Selected Mood: {mood}")

    weather, temp = get_weather(city)
    st.info(f"Weather: {weather}, Temperature: {temp}°C")

    query = f"{mood} {weather} music"
    songs = get_music_recommendations(query)

    st.subheader("🎧 Recommended Songs")
    for song in songs:
        st.markdown(f"[{song['name']} - {song['artist']}]({song['url']})")
