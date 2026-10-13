import json
import os
import streamlit as st

# Pengaturan Halaman Streamlit
st.set_page_config(
    page_title="Music Translator App", page_icon="🎵", layout="centered"
)

# Custom Styling CSS untuk mempercantik tampilan slide dan lirik
st.markdown(
    """
    <style>
    .lyrics-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .original-text {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 15px;
    }
    .translated-text {
        font-size: 20px;
        color: #0066cc;
        font-style: italic;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Fungsi untuk memuat lagu lokal dari file songs.json
@st.cache_data
def load_local_songs():
  if os.path.exists("songs.json"):
    with open("songs.json", "r", encoding="utf-8") as f:
      return json.load(f)
  return []


st.title("🎵 Pemutar Musik dengan Mode Terjemahan Slide")
st.write(
    "Nikmati lagu favorit Anda dengan mode lirik slide interaktif dan pilihan"
    " sumber data lokal atau online."
)

# ==================== MENU PENGATURAN (SIDEBAR) ====================
st.sidebar.header("⚙️ Pengaturan & Sumber Data")

# 1. Pilih Sumber Data (Lokal vs Online/Custom)
data_source = st.sidebar.radio(
    "Pilih Sumber Lagu:", options=["Lokal (Database JSON)", "Online (Custom URL)"]
)

# 2. Pilihan Bahasa Terjemahan
selected_lang = st.sidebar.selectbox(
    "Pilih Bahasa Terjemahan:",
    options=["id", "en", "es"],
    format_func=lambda x: {
        "id": "Bahasa Indonesia",
        "en": "English",
        "es": "Español",
    }[x],
)

current_song = {}

if data_source == "Lokal (Database JSON)":
  songs = load_local_songs()
  if songs:
    song_titles = [f"{song['title']} - {song['artist']}" for song in songs]
    selected_song_idx = st.sidebar.selectbox(
        "Pilih Lagu Lokal:",
        range(len(song_titles)),
        format_func=lambda x: song_titles[x],
    )
    current_song = songs[selected_song_idx]
  else:
    st.sidebar.warning("File songs.json tidak ditemukan atau kosong.")

else:  # Sumber Online / Custom Input
  st.sidebar.subheader("Masukkan Detail Lagu Online")
  custom_title = st.sidebar.text_input("Judul Lagu", "Lagu Baru Online")
  custom_artist = st.sidebar.text_input("Artis", "Nama Artis")
  custom_url = st.sidebar.text_input(
      "Link Audio (URL MP3)",
      "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
  )

  # Template lirik default untuk mode online kustom
  current_song = {
      "title": custom_title,
      "artist": custom_artist,
      "audio_url": custom_url,
      "lyrics": [
          {
              "time": 0,
              "original": "Welcome to custom online song stream",
              "id": "Selamat datang di streaming lagu online kustom",
              "en": "Welcome to custom online song stream",
              "es": "Bienvenido a la transmisión de canciones en línea",
          },
          {
              "time": 5,
              "original": "Enjoy the music and translation mode",
              "id": "Nikmati musik dan mode terjemahannya",
              "en": "Enjoy the music and translation mode",
              "es": "Disfruta de la música y el modo de traducción",
          },
          {
              "time": 10,
              "original": "Slide through the lyrics seamlessly",
              "id": "Geser lirik dengan mulus menggunakan mode slide",
              "en": "Slide through the lyrics seamlessly",
              "es": "Deslízate por las letras sin problemas",
          },
      ],
  }

st.divider()

# ==================== PEMUTAR AUDIO & TAMPILAN SLIDE ====================
if current_song:
  st.subheader(f"🎶 {current_song.get('title', 'Tanpa Judul')}")
  st.markdown(f"**Artis:** {current_song.get('artist', 'Unknown')}")

  # Pemutar Audio
  audio_url = current_song.get("audio_url", "")
  if audio_url:
    st.audio(audio_url)
  else:
    st.warning("URL Audio tidak valid.")

  st.markdown("### 📜 Mode Terjemahan Slide Lirik")

  lyrics_list = current_song.get("lyrics", [])

  if lyrics_list:
    # Inisialisasi state untuk navigasi slide
    if "slide_index" not in st.session_state:
      st.session_state.slide_index = 0

    # Pastikan index slide tidak out of bounds jika ganti lagu
    if st.session_state.slide_index >= len(lyrics_list):
      st.session_state.slide_index = 0

    current_lyric = lyrics_list[st.session_state.slide_index]

    # Tampilan Kartu Slide Lirik
    st.markdown(
        f"""
        <div class="lyrics-card">
            <div class="original-text">"{current_lyric['original']}"</div>
            <div class="translated-text">🌐 {current_lyric.get(selected_lang, current_lyric.get('en', 'Terjemahan tidak tersedia'))}</div>
            <p style="margin-top: 15px; color: #7f8c8d; font-size: 14px;">Slide {st.session_state.slide_index + 1} dari {len(lyrics_list)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tombol Navigasi Slide (Sebelumnya / Selanjutnya)
    col_prev, col_spacer, col_next = st.columns([1, 2, 1])

    with col_prev:
      if st.button("⬅️ Sebelumnya", use_container_width=True):
        if st.session_state.slide_index > 0:
          st.session_state.slide_index -= 1
          st.rerun()

    with col_next:
      if st.button("Selanjutnya ➡️", use_container_width=True):
        if st.session_state.slide_index < len(lyrics_list) - 1:
          st.session_state.slide_index += 1
          st.rerun()
  else:
    st.info("Tidak ada lirik yang tersedia untuk lagu ini.")
else:
  st.info(
      "Silakan pilih lagu dari menu pengaturan di sidebar untuk mulai memutar."
  )
