import streamlit as st
import requests
import random
from PIL import Image, ImageEnhance
from io import BytesIO

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

st.set_page_config(page_title="Who's That Pokémon?", page_icon="⚡")

# -----------------------------
# Utility Functions
# -----------------------------
def get_random_pokemon():
    pokemon_id = random.randint(1, 151)  # Gen 1 Pokémon
    response = requests.get(f"{POKEAPI_URL}{pokemon_id}")
    data = response.json()
    name = data["name"].capitalize()
    image_url = data["sprites"]["other"]["official-artwork"]["front_default"]
    return name, image_url


def get_silhouette(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")

    # Darken image to create silhouette
    enhancer = ImageEnhance.Brightness(img)
    silhouette = enhancer.enhance(0.0)
    return silhouette


# -----------------------------
# Session State Initialization
# -----------------------------
if "pokemon_name" not in st.session_state:
    st.session_state.pokemon_name, st.session_state.image_url = get_random_pokemon()
    st.session_state.revealed = False
    st.session_state.score = 0

# -----------------------------
# UI
# -----------------------------
st.title("⚡ Who’s That Pokémon?")
st.markdown("Guess the Pokémon from the silhouette!")

if not st.session_state.revealed:
    silhouette_img = get_silhouette(st.session_state.image_url)
    st.image(silhouette_img, use_container_width=True)

    guess = st.text_input("Your Guess:")

    if st.button("Submit Guess"):
        if guess.strip().lower() == st.session_state.pokemon_name.lower():
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! It was **{st.session_state.pokemon_name}**.")
        st.session_state.revealed = True

else:
    st.image(st.session_state.image_url, caption=st.session_state.pokemon_name, use_container_width=True)

    if st.button("Next Pokémon"):
        st.session_state.pokemon_name, st.session_state.image_url = get_random_pokemon()
        st.session_state.revealed = False

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("📊 Score")
st.sidebar.metric("Correct Guesses", st.session_state.score)