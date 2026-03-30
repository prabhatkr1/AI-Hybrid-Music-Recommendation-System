import streamlit as st
from weather_fetcher import get_weather
from spotify_api import get_music_recommendations
# from mood_detector import detect_emotion  # Uncomment if using webcam mood detection

st.title("🎵 AI-Based Hybrid Music Recommender")

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