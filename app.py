import json
import os
import streamlit as st

# Pengaturan Halaman Streamlit
st.set_page_config(
    page_title="Modern Music & Video Translator", page_icon="🎧", layout="centered"
)

# Custom Styling CSS Tema Gelap Elegan
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    header {visibility: hidden;}
    
    .lyrics-box {
        background: #1E1E1E;
        border: 1px solid #282828;
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    
    .original-lyrics {
        font-size: 20px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 12px;
    }
    
    .translated-lyrics {
        font-size: 18px;
        color: #1DB954;
        font-weight: 500;
    }
    
    .arabic-text {
        direction: rtl;
        font-family: 'Amiri', 'Traditional Arabic', sans-serif;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Fungsi untuk memuat data JSON lokal dengan aman
@st.cache_data
def load_json_songs():
  if os.path.exists("songs.json"):
    try:
      with open("songs.json", "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      return []
  return []


# Fungsi untuk memindai direktori lokal dengan aman
def scan_local_directory(folder_path="."):
  supported_extensions = (".mp3", ".wav", ".ogg", ".m4a", ".mp4", ".webm", ".mkv")
  media_files = []
  try:
    if os.path.exists(folder_path):
      for file in os.listdir(folder_path):
        if file.lower().endswith(supported_extensions):
          media_files.append(
              {
                  "title": os.path.splitext(file)[0].replace("_", " ").title(),
                  "artist": "Local Storage",
                  "file_path": os.path.join(folder_path, file),
                  "type": (
                      "video"
                      if file.lower().endswith((".mp4", ".webm", ".mkv"))
                      else "audio"
                  ),
                  "lyrics": [
                      {
                          "time": 0,
                          "original": "Media file loaded from local directory",
                          "id": "File media dimuat dari direktori lokal",
                          "en": "Media file loaded from local directory",
                          "es": (
                              "Archivo multimedia cargado desde el directorio"
                              " local"
                          ),
                          "ar": "تم تحميل ملف الوسائط من الدليل المحلي",
                      },
                      {
                          "time": 5,
                          "original": "Enjoy translation features seamlessly",
                          "id": "Nikmati fitur terjemahan dengan mulus",
                          "en": "Enjoy translation features seamlessly",
                          "es": (
                              "Disfruta de las funciones de traducción sin"
                              " problemas"
                          ),
                          "ar": "استمتع بميزات الترجمة بسلاسة",
                      },
                  ],
              }
          )
  except Exception:
    pass
  return media_files


# Inisialisasi Session State
if "page" not in st.session_state:
  st.session_state.page = "home"
if "selected_media" not in st.session_state:
  st.session_state.selected_media = None
if "slide_idx" not in st.session_state:
  st.session_state.slide_idx = 0


# ==================== PANEL KONTROL SIDEBAR ====================
st.sidebar.markdown("### ⚙️ Pengaturan & Sumber")

# Pilihan Bahasa Terjemahan
selected_lang = st.sidebar.selectbox(
    "Bahasa Terjemahan:",
    options=["id", "en", "es", "ar"],
    format_func=lambda x: {
        "id": "🇮🇩 Bahasa Indonesia",
        "en": "🇬🇧 English",
        "es": "🇪🇸 Español",
        "ar": "🇸🇦 العربية (Arabic)",
    }[x],
)

source_mode = st.sidebar.selectbox(
    "Sumber Media:",
    options=[
        "🌐 Online (Demo Streaming)",
        "📜 Database JSON",
        "📁 Direktori Lokal",
    ],
)

# Kumpulkan daftar media
media_list = []

if source_mode == "📜 Database JSON":
  json_data = load_json_songs()
  if json_data:
    for item in json_data:
      media_list.append(
          {
              "title": item.get("title", "Unknown Title"),
              "artist": item.get("artist", "Unknown Artist"),
              "file_path": item.get("audio_url", ""),
              "type": (
                  "video"
                  if item.get("audio_url", "").lower().endswith((".mp4", ".webm"))
                  else "audio"
              ),
              "lyrics": item.get("lyrics", []),
          }
      )
  else:
    st.sidebar.warning(
        "File 'songs.json' tidak ditemukan. Menggunakan mode online."
    )

elif source_mode == "📁 Direktori Lokal":
  target_folder = st.sidebar.text_input("Nama Folder", ".")
  media_list = scan_local_directory(target_folder)

# Fallback ke Online jika data kosong
if not media_list:
  media_list = [
      {
          "title": "Demo Online Stream Track",
          "artist": "Featured Artist",
          "file_path": (
              "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
          ),
          "type": "audio",
          "lyrics": [
              {
                  "time": 0,
                  "original": "Welcome to online music streaming",
                  "id": "Selamat datang di streaming musik online",
                  "en": "Welcome to online music streaming",
                  "es": "Bienvenido a la transmisión de música en línea",
                  "ar": "مرحبًا بك في بث الموسيقى عبر الإنترنت",
              },
              {
                  "time": 5,
                  "original": "Select language from sidebar to translate",
                  "id": "Pilih bahasa dari sidebar untuk menerjemahkan",
                  "en": "Select language from sidebar to translate",
                  "es": (
                      "Selecciona el idioma de la barra lateral para traducir"
                  ),
                  "ar": "اختر اللغة من الشريط الجانبي للترجمة",
              },
          ],
      }
  ]


# ==================== HALAMAN 1: HOME ====================
if st.session_state.page == "home":
  col_p1, col_p2 = st.columns([4, 1])
  with col_p1:
    st.markdown("##### 👤 Welcome back")
    st.markdown("### **Jack Fitzgerald**")
  with col_p2:
    st.markdown(
        "<div style='font-size: 24px; text-align: right;'>🎛️</div>",
        unsafe_allow_html=True,
    )

  st.write("")
  search_query = st.text_input(
      "Cari lagu atau artis...", placeholder="🔍 Search", key="search_box"
  )

  st.write("")
  st.markdown(
      "### Playlists <span style='font-size: 14px; float: right; color:"
      " #1DB954;'>View more</span>",
      unsafe_allow_html=True,
  )

  # Daftar Playlist
  for idx, media in enumerate(media_list):
    if (
        not search_query
        or search_query.lower() in media["title"].lower()
        or search_query.lower() in media["artist"].lower()
    ):
      if st.button(
          f"🎵 {media['title']} — {media['artist']}",
          key=f"play_btn_{idx}",
          use_container_width=True,
      ):
        st.session_state.selected_media = media
        st.session_state.slide_idx = 0
        st.session_state.page = "player"
        st.rerun()

  st.write("")
  st.markdown(
      "### Trending Music <span style='font-size: 14px; float: right; color:"
      " #1DB954;'>View more</span>",
      unsafe_allow_html=True,
  )

  col_tr1, col_tr2 = st.columns(2)
  with col_tr1:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%); padding: 20px; border-radius: 16px; height: 120px;">
            <p style="font-weight: bold; font-size: 16px; margin: 0;">Top Hits 2026</p>
            <p style="font-size: 12px; opacity: 0.8; margin-top: 5px;">Daily Global Charts</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col_tr2:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1f4037 0%, #99f2c8 100%); padding: 20px; border-radius: 16px; height: 120px; color: #000;">
            <p style="font-weight: bold; font-size: 16px; margin: 0;">Chill Vibes</p>
            <p style="font-size: 12px; opacity: 0.8; margin-top: 5px;">Relax & Translate</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================== HALAMAN 2: PEMUTAR & LIRIK SLIDE ====================
elif st.session_state.page == "player":
  current = st.session_state.selected_media

  if st.button("⬅️ Kembali ke Home"):
    st.session_state.page = "home"
    st.rerun()

  if current:
    st.markdown(f"## 🎶 {current.get('title', 'Unknown Title')}")
    st.markdown(
        f"<p style='color: #a0a0a0;'>Artis:"
        f" {current.get('artist', 'Unknown')}</p>",
        unsafe_allow_html=True,
    )

    # Pemutar Media
    file_path = current.get("file_path", "")
    if file_path:
      if current.get("type") == "video":
        st.video(file_path)
      else:
        st.audio(file_path)
    else:
      st.warning("File media tidak ditemukan.")

    st.markdown("---")
    st.markdown("### 📜 Mode Terjemahan Lirik (Slide)")

    lyrics = current.get("lyrics", [])
    if lyrics:
      if st.session_state.slide_idx >= len(lyrics):
        st.session_state.slide_idx = 0

      active_lyric = lyrics[st.session_state.slide_idx]
      is_arabic = selected_lang == "ar"
      rtl_class = "arabic-text" if is_arabic else ""
      translated_text = active_lyric.get(
          selected_lang, active_lyric.get("en", "Terjemahan tidak tersedia")
      )

      st.markdown(
          f"""
          <div class="lyrics-box">
              <div class="original-lyrics">"{active_lyric.get('original', '')}"</div>
              <div class="translated-lyrics {rtl_class}">🌐 {translated_text}</div>
              <p style="margin-top: 15px; color: #777777; font-size: 12px;">Slide {st.session_state.slide_idx + 1} dari {len(lyrics)}</p>
          </div>
          """,
          unsafe_allow_html=True,
      )

      col_prev, col_space, col_next = st.columns([1, 2, 1])
      with col_prev:
        if st.button("⬅️ Prev", use_container_width=True):
          if st.session_state.slide_idx > 0:
            st.session_state.slide_idx -= 1
            st.rerun()
      with col_next:
        if st.button("Next ➡️", use_container_width=True):
          if st.session_state.slide_idx < len(lyrics) - 1:
            st.session_state.slide_idx += 1
            st.rerun()
    else:
      st.info("Tidak ada lirik tersedia.")
  else:
    st.warning("Belum ada media yang dipilih.")
