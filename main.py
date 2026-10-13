import sys
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class MusicPlayer(QMainWindow):

  def __init__(self):
    super().__init__()
    self.setWindowTitle("Python Desktop Music Player")
    self.setGeometry(100, 100, 450, 300)

    # Inisialisasi Media Player dan Audio Output
    self.media_player = QMediaPlayer()
    self.audio_output = QAudioOutput()
    self.media_player.setAudioOutput(self.audio_output)

    # Layout Utama
    main_layout = QVBoxLayout()

    # Label Judul Lagu / Status
    self.title_label = QLabel("Tidak ada lagu yang diputar", self)
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
    main_layout.addWidget(self.title_label)

    # Slider Durasi / Progress Bar
    self.slider = QSlider(Qt.Orientation.Horizontal, self)
    self.slider.setRange(0, 100)
    main_layout.addWidget(self.slider)

    # Layout Tombol Kontrol (Play, Pause, Open)
    btn_layout = QHBoxLayout()

    self.btn_open = QPushButton("📂 Buka File", self)
    self.btn_open.clicked.connect(self.open_file)
    btn_layout.addWidget(self.btn_open)

    self.btn_play = QPushButton("▶️ Play", self)
    self.btn_play.clicked.connect(self.play_music)
    btn_layout.addWidget(self.btn_play)

    self.btn_pause = QPushButton("⏸️ Pause", self)
    self.btn_pause.clicked.connect(self.pause_music)
    btn_layout.addWidget(self.btn_pause)

    main_layout.addLayout(btn_layout)

    # Widget Utama
    container = QWidget()
    container.setLayout(main_layout)
    self.setCentralWidget(container)

    # Hubungkan sinyal durasi media player
    self.media_player.positionChanged.connect(self.position_changed)
    self.media_player.durationChanged.connect(self.duration_changed)
    self.slider.sliderMoved.connect(self.set_position)

  def open_file(self):
    """Membuka dialog file explorer untuk memilih file audio MP3/WAV."""
    file_name, _ = QFileDialog.getOpenFileName(
        self, "Pilih Audio", "", "Audio Files (*.mp3 *.wav *.ogg)"
    )
    if file_name:
      self.media_player.setSource(QUrl.fromLocalFile(file_name))
      self.title_label.setText(file_name.split("/")[-1])
      self.play_music()

  def play_music(self):
    """Memutar musik."""
    self.media_player.play()

  def pause_music(self):
    """Menjeda musik."""
    self.media_player.pause()

  def position_changed(self, position):
    """Memperbarui posisi slider seiring berjalannya lagu."""
    self.slider.setValue(position)

  def duration_changed(self, duration):
    """Mengatur rentang maksimum slider berdasarkan durasi lagu."""
    self.slider.setRange(0, duration)

  def set_position(self, position):
    """Mengatur posisi lagu saat slider digeser secara manual oleh pengguna."""
    self.media_player.setPosition(position)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  player = MusicPlayer()
  player.show()
  sys.exit(app.exec())
