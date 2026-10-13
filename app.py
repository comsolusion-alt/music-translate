import json
import os
import streamlit as st

# Pengaturan Halaman Streamlit
st.set_page_config(
    page_title="Modern Music & Video Translator", page_icon="🎧", layout="centered"
)

# Custom Styling CSS untuk Tampilan Modern & Elegan
st.markdown(
    """
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .lyrics-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    .original-text {
        font-size: 26px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 20px;
        letter-spacing: -0.025em;
    }
    .translated-text {
        font-size: 22px;
        color: #38bdf8;
        font-weight: 500;
    }
    .arabic-text {
        direction: rtl;
        font-family: 'Amiri', 'Traditional Arabic', sans-serif;
    }
    /* Styling Sidebar */
    .css-1d391kg {
        background-color: #1e293b;
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


# Fungsi untuk memindai direktori lokal (misal folder 'media/' atau root folder)
def scan_local_directory(folder_path="."):
  supported_extensions = (".mp3", ".wav", ".ogg", ".m4a", ".mp4", ".webm", ".mkv")
  media_files = []
  if os.path.exists(folder_path):
    for file in os.listdir(folder_path):
      if file.lower().endswith(supported_extensions):
        media_files.append(
            {
                "title": os.path.splitext(file)[0].replace("_", " ").title(),
                "artist": "Local Directory File",
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
                            "Media playback started from local directory"
                        ),
                        "id": "Pemutaran media dimulai dari direktori lokal",
                        "en": "Media playback started from local directory",
                        "es": (
                            "Reproducción de medios iniciada desde el"
                            " directorio local"
                        ),
                        "ar": "بدأ تشغيل الوسائط من الدليل المحلي",
                    },
                    {
                        "time": 5,
                        "original": (
                            "Enjoy your music or video with multi-language"
                            " translation"
                        ),
                        "id": (
                            "Nikmati musik atau video Anda dengan terjemahan"
                            " multi-bahasa"
                        ),
                        "en": (
                            "Enjoy your music or video with multi-language"
                            " translation"
                        ),
                        "es": (
                            "Disfruta de tu música o video con traducción en"
                            " varios idiomas"
                        ),
                        "ar": "استمتع بموسيقاك أو فيديو الخاص بك مع الترجمة متعددة اللغات",
                    },
                ],
            }
        )
  return media_files


# Judul Utama Dashboard
st.markdown(
    "<h1 style='text-align: center; color: #38bdf8;'>🎧 Media & Lyrics Translator</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #94a3b8;'>Pemutar Musik & Video Modern"
    " dengan Dukungan Terjemahan Multi-Bahasa Real-Time</p>",
    unsafe_allow_html=True,
)
st.divider()

# ==================== MENU PENGATURAN MODERN (SIDEBAR) ====================
st.sidebar.markdown(
    "### 🎛️ Panel Kontrol", help="Atur sumber media dan bahasa di sini"
)

# 1. Pilih Sumber Data
source_mode = st.sidebar.radio(
    "Sumber Media:",
    options=[
        "📁 Direktori Lokal (Auto-Scan)",
        "📜 Database JSON",
        "🌐 Online (Custom URL)",
    ],
)

# 2. Pilihan Bahasa Terjemahan (Termasuk Bahasa Arab)
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

current_media = {}

# Logika Pengambilan Data Berdasarkan Sumber
if source_mode == "📁 Direktori Lokal (Auto-Scan)":
  # Membuat sub-input folder jika ingin menskan folder khusus (default: folder saat ini)
  target_folder = st.sidebar.text_input(
      "Nama Folder Direktori",
      ".",
      help="Letakkan file mp3/mp4 di folder ini",
  )
  local_media_list = scan_local_directory(target_folder)

  if local_media_list:
    media_titles = [m["title"] for m in local_media_list]
    selected_idx = st.sidebar.selectbox(
        "Pilih File Media:", range(len(media_titles)), format_func=lambda x: media_titles[x]
    )
    current_media = local_media_list[selected_idx]
  else:
    st.sidebar.warning(
        "Tidak ditemukan file audio/video (.mp3, .mp4, dll) di direktori"
        f" '{target_folder}'."
    )

elif source_mode == "📜 Database JSON":
  json_songs = load_json_songs()
  if json_songs:
    song_titles = [f"{s['title']} - {s['artist']}" for s in json_songs]
    selected_idx = st.sidebar.selectbox(
        "Pilih Lagu JSON:", range(len(song_titles)), format_func=lambda x: song_titles[x]
    )
    item = json_songs[selected_idx]
    current_media = {
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
  else:
    st.sidebar.warning(
        "File 'songs.json' kosong atau tidak ditemukan di direktori."
    )

else:  # Online / Custom URL
  st.sidebar.markdown("---")
  custom_title = st.sidebar.text_input("Judul Media", "Media Streaming Online")
  custom_artist = st.sidebar.text_input("Kreator / Artis", "Unknown Creator")
  media_type_choice = st.sidebar.selectbox(
      "Tipe Media", options=["Audio (MP3/URL)", "Video (MP4/URL)"]
  )
  custom_url = st.sidebar.text_input(
      "Link URL Media",
      (
          "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
          if "Audio" in media_type_choice
          else "https://www.w3schools.com/html/mov_bbb.mp4"
      ),
  )

  current_media = {
      "title": custom_title,
      "artist": custom_artist,
      "file_path": custom_url,
      "type": "video" if "Video" in media_type_choice else "audio",
      "lyrics": [
          {
              "time": 0,
              "original": "Online streaming media initialized",
              "id": "Media streaming online diinisialisasi",
              "en": "Online streaming media initialized",
              "es": "Medios de transmisión en línea inicializados",
              "ar": "تم تهيئة وسائط البث عبر الإنترنت",
          },
          {
              "time": 5,
              "original": "Navigate through slides to view translated lyrics",
              "id": (
                  "Geser slide untuk melihat terjemahan lirik secara interaktif"
              ),
              "en": "Navigate through slides to view translated lyrics",
              "es": "Navega por las diapositivas para ver las letras traducidas",
              "ar": "تنقل عبر الشرائح لعرض الكلمات المترجمة",
          },
      ],
  }

st.divider()

# ==================== PEMUTAR MEDIA & TAMPILAN SLIDE MODERN ====================
if current_media:
  # Header Info
  col_info1, col_info2 = st.columns([3, 1])
  with col_info1:
    st.markdown(f"### 🎵 {current_media.get('title')}")
    st.markdown(f"<span style='color: #94a3b8;'>Artis: {current_media.get('artist')}</span>", unsafe_allow_html=True)
  with col_info2:
    media_badge = "🎥 Video Player" if current_media.get("type") == "video" else "🎧 Audio Player"
    st.markdown(f"<div style='text-align: right;'><span style='background: #334155; padding: 6px 12px; border-radius: 8px; font-size: 12px;'>{media_badge}</span></div>", unsafe_allow_html=True)

  st.write("")

  # Eksekusi Pemutar Media (Audio vs Video)
  media_source = current_media.get("file_path")
  if media_source:
    if current_media.get("type") == "video":
      st.video(media_source)
    else:
      st.audio(media_source)
  else:
    st.warning("Sumber file media tidak ditemukan.")

  st.markdown("### 📜 Mode Slide Terjemahan Interaktif")

  lyrics_list = current_media.get("lyrics", [])

  if lyrics_list:
    # State manajemen slide
    if "slide_idx" not in st.session_state:
      st.session_state.slide_idx = 0

    if st.session_state.slide_idx >= len(lyrics_list):
      st.session_state.slide_idx = 0

    active_lyric = lyrics_list[st.session_state.slide_idx]

    # Cek apakah bahasa target adalah Bahasa Arab untuk menerapkan gaya RTL (Right-to-Left)
    is_arabic = selected_lang == "ar"
    extra_class = "arabic-text" if is_arabic else ""
    translated_content = active_lyric.get(selected_lang, active_lyric.get("en", "Terjemahan tidak tersedia"))

    # Kartu Slide Modern
    st.markdown(
        f"""
        <div class="lyrics-card">
            <div class="original-text">"{active_lyric['original']}"</div>
            <div class="translated-text {extra_class}">🌐 {translated_content}</div>
            <p style="margin-top: 20px; color: #64748b; font-size: 13px; font-weight: 500;">
                Slide {st.session_state.slide_idx + 1} dari {len(lyrics_list)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tombol Navigasi Slide Modern
    c_prev, c_space, c_next = st.columns([1, 2, 1])

    with c_prev:
      if st.button("⬅️ Sebelumnya", use_container_width=True):
        if st.session_state.slide_idx > 0:
          st.session_state.slide_idx -= 1
          st.rerun()

    with c_next:
      if st.button("Selanjutnya ➡️", use_container_width=True):
        if st.session_state.slide_idx < len(lyrics_list) - 1:
          st.session_state.slide_idx += 1
          st.rerun()
  else:
    st.info("Tidak ada lirik atau teks terjemahan yang tersedia untuk media ini.")
else:
  st.info("Silakan tentukan sumber media melalui panel kontrol di sidebar.")
