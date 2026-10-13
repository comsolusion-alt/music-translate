import json
import os
import streamlit as st

# Pengaturan Halaman Streamlit
st.set_page_config(
    page_title="Modern Music & Video Translator", page_icon="🎧", layout="centered"
)

# Custom Styling CSS Menyerupai UI Pemutar Musik Modern (Dark Theme)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    /* Sembunyikan Header & Footer default Streamlit agar mirip aplikasi mobile */
    header {visibility: hidden;}
    
    /* Container Utama Kartu Pemutar */
    .player-card {
        background: #181818;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    
    /* Kartu Playlist & Trending */
    .playlist-item {
        background: #1E1E1E;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #282828;
    }
    
    .lyrics-box {
        background: #222222;
        border: 1px solid #333333;
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
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


# Fungsi untuk memuat data JSON lokal
@st.cache_data
def load_json_songs():
  if os.path.exists("songs.json"):
    with open("songs.json", "r", encoding="utf-8") as f:
      return json.load(f)
  return []


# Fungsi untuk memindai direktori lokal
def scan_local_directory(folder_path="."):
  supported_extensions = (".mp3", ".wav", ".ogg", ".m4a", ".mp4", ".webm", ".mkv")
  media_files = []
  if os.path.exists(folder_path):
    for file in os.listdir(folder_path):
      if file.lower().endswith(supported_extensions):
        media_files.append(
            {
                "title": os.path.splitext(file)[0].replace("_", " ").title(),
                "artist": "Local Storage Artist",
                "file_path": os.path.join(folder_path, file),
                "type": (
                    "video"
                    if file.lower().endswith((".mp4", ".webm", ".mkv"))
                    else "audio"
                ),
                "lyrics": [
                    {
                        "time": 0,
                        "original": (
                            "Media playback initialized from directory"
                        ),
                        "id": "Pemutaran media diinisialisasi dari direktori",
                        "en": "Media playback initialized from directory",
                        "es": (
                            "Reproducción de medios iniciada desde el"
                            " directorio"
                        ),
                        "ar": "تم تهيئة تشغيل الوسائط من الدليل",
                    },
                    {
                        "time": 5,
                        "original": "Enjoy music with real-time translation",
                        "id": (
                            "Nikmati musik dengan terjemahan bahasa secara"
                            " langsung"
                        ),
                        "en": "Enjoy music with real-time translation",
                        "es": "Disfruta de la música con traducción en tiempo real",
                        "ar": "استمتع بالموسيقى مع الترجمة في الوقت الفعلي",
                    },
                ],
            }
        )
  return media_files


# Inisialisasi Session State untuk navigasi antar halaman (Home / Player)
if "page" not in st.session_state:
  st.session_state.page = "home"
if "selected_media" not in st.session_state:
  st.session_state.selected_media = None
if "slide_idx" not in st.session_state:
  st.session_state.slide_idx = 0


# ==================== PANEL KONTROL SIDEBAR ====================
st.sidebar.markdown("### ⚙️ Pengaturan & Sumber")

# Pilihan Bahasa Terjemahan (Termasuk Bahasa Arab)
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
        "📜 Database JSON",
        "📁 Direktori Lokal (Auto-Scan)",
        "🌐 Online (Custom URL)",
    ],
)

# Kumpulkan daftar media berdasarkan sumber
media_list = []
if source_mode == "📜 Database JSON":
  json_data = load_json_songs()
  for item in json_data:
    media_list.append(
        {
            "title": item["title"],
            "artist": item["artist"],
            "file_path": item["audio_url"],
            "type": (
                "video"
                if item.get("audio_url", "").lower().endswith((".mp4", ".webm"))
                else "audio"
            ),
            "lyrics": item["lyrics"],
        }
    )
elif source_mode == "📁 Direktori Lokal (Auto-Scan)":
  target_folder = st.sidebar.text_input("Folder Direktori", ".")
  media_list = scan_local_directory(target_folder)
else:
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


# ==================== HALAMAN 1: HOME / DASHBOARD (LAYOUT TENGAH DI GAMBAR) ====================
if st.session_state.page == "home":
  # Bagian Profil Atas
  col_p1, col_p2 = st.columns([4, 1])
  with col_p1:
    st.markdown("##### 👤 Welcome back")
    st.markdown("### **Jack Fitzgerald**")
  with col_p2:
    st.markdown("<div style='font-size: 24px; text-align: right;'>🎛️</div>", unsafe_allow_html=True)

  st.write("")

  # Kotak Pencarian
  search_query = st.text_input("Cari lagu atau artis...", placeholder="🔍 Search")

  st.write("")
  st.markdown("### Playlists <span style='font-size: 14px; float: right; color: #1DB954; cursor: pointer;'>View more</span>", unsafe_allow_html=True)

  # Menampilkan Daftar Playlist / Lagu
  for idx, media in enumerate(media_list):
    if search_query.lower() in media["title"].lower() or search_query.lower() in media["artist"].lower():
      col_item1, col_item2 = st.columns([5, 1])
      with col_item1:
        if st.button(f"🎵 {media['title']} — {media['artist']}", key=f"play_btn_{idx}", use_container_width=True):
          st.session_state.selected_media = media
          st.session_state.slide_idx = 0
          st.session_state.page = "player"
          st.rerun()
      with col_item2:
        st.write("")

  st.write("")
  st.markdown("### Trending Music <span style='font-size: 14px; float: right; color: #1DB954; cursor: pointer;'>View more</span>", unsafe_allow_html=True)

  # Tampilan Kartu Trending Bergaya Modern
  col_tr1, col_tr2 = st.columns(2)
  with col_tr1:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%); padding: 20px; border-radius: 16px; height: 130px;">
            <p style="font-weight: bold; font-size: 16px; margin: 0;">Top Hits 2026</p>
            <p style="font-size: 12px; opacity: 0.8; margin-top: 5px;">Daily Global Charts</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col_tr2:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1f4037 0%, #99f2c8 100%); padding: 20px; border-radius: 16px; height: 130px; color: #000;">
            <p style="font-weight: bold; font-size: 16px; margin: 0;">Chill Vibes</p>
            <p style="font-size: 12px; opacity: 0.8; margin-top: 5px;">Relax & Translate</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================== HALAMAN 2: PEMUTAR MUSIK & LIRIK SLIDE (LAYOUT KIRI/KANAN DI GAMBAR) ====================
elif st.session_state.page == "player":
  current = st.session_state.selected_media

  if st.button("⬅️ Kembali ke Home"):
    st.session_state.page = "home"
    st.rerun()

  if current:
    st.markdown(f"## 🎶 {current['title']}")
    st.markdown(f"<p style='color: #a0a0a0;'>Artis: {current['artist']}</p>", unsafe_allow_html=True)

    # Pemutar Media (Audio / Video)
    if current.get("type") == "video":
      st.video(current["file_path"])
    else:
      st.audio(current["file_path"])

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

      # Kotak Kartu Slide Lirik
      st.markdown(
          f"""
          <div class="lyrics-box">
              <div class="original-lyrics">"{active_lyric['original']}"</div>
              <div class="translated-text {rtl_class}">🌐 {translated_text}</div>
              <p style="margin-top: 15px; color: #777777; font-size: 12px;">Slide {st.session_state.slide_idx + 1} dari {len(lyrics)}</p>
          </div>
          """,
          unsafe_allow_html=True,
      )

      # Tombol Navigasi Slide
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
      st.info("Tidak ada lirik tersedia untuk lagu ini.")
  else:
    st.warning("Belum ada media yang dipilih.")
