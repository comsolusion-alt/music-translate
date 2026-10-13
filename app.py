import json
import streamlit as st

# Pengaturan Halaman Streamlit
st.set_page_config(
    page_title="Music Translator App", page_icon="🎵", layout="centered"
)


# Fungsi untuk memuat data lagu dari JSON
@st.cache_data
def load_songs():
  with open("songs.json", "r", encoding="utf-8") as f:
    return json.load(f)


songs = load_songs()

# Judul Aplikasi
st.title("🎵 Pemutar Musik dengan Terjemahan Lirik")
st.write(
    "Nikmati lagu favorit Anda sekaligus pahami artinya dalam berbagai bahasa"
    " secara real-time."
)

# Sidebar untuk Navigasi & Pengaturan
st.sidebar.header("⚙️ Pengaturan")
selected_lang = st.sidebar.selectbox(
    "Pilih Bahasa Terjemahan:",
    options=["id", "en"],
    format_func=lambda x: "Bahasa Indonesia" if x == "id" else "English",
)

# Pilih Lagu
song_titles = [f"{song['title']} - {song['artist']}" for song in songs]
selected_song_idx = st.sidebar.selectbox(
    "Pilih Lagu:", range(len(song_titles)), format_func=lambda x: song_titles[x]
)

current_song = songs[selected_song_idx]

st.divider()

# Tampilan Info Lagu
st.subheader(f"🎶 {current_song['title']}")
st.markdown(f"**Artis:** {current_song['artist']}")

# Pemutar Audio Bawaan Streamlit
# Anda bisa mengganti URL di songs.json dengan link file .mp3 Anda sendiri
st.audio(current_song["audio_url"])

st.markdown("### 📜 Lirik & Terjemahan Berjalan")
st.info(
    "Tips: Putar audio di atas. Karena keterbatasan kontrol waktu real-time di"
    " Streamlit murni tanpa komponen kustom berat, bagian lirik di bawah ini"
    " menampilkan seluruh lirik interaktif."
)

# Menampilkan Daftar Lirik
for line in current_song["lyrics"]:
  # Kotak kecil untuk setiap baris lirik
  col1, col2 = st.columns([1, 10])
  with col1:
    st.text(f"[{int(line['time'])}s]")
  with col2:
    st.markdown(f"**{line['original']}**")
    # Menampilkan terjemahan sesuai bahasa yang dipilih di sidebar
    st.markdown(
        f"<p style='color: #0066cc;'>{line.get(selected_lang, line['en'])}</p>",
        unsafe_allow_html=True,
    )
  st.write("---")
