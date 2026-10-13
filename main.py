import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QWidget,
    QFileDialog
)

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Desktop Music Player (PyQt5)")
        self.setGeometry(100, 100, 450, 300)

        # Inisialisasi Media Player PyQt5
        self.media_player = QMediaPlayer()

        # Layout Utama
        main_layout = QVBoxLayout()

        # Label Judul Lagu
        self.title_label = QLabel("Tidak ada lagu yang diputar", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        main_layout.addWidget(self.title_label)

        # Slider Durasi
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        main_layout.addWidget(self.slider)

        # Layout Tombol Kontrol
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

        # Hubungkan Sinyal
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.slider.sliderMoved.connect(self.set_position)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih Audio", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_name:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.title_label.setText(file_name.split("/")[-1])
            self.play_music()

    def play_music(self):
        self.media_player.play()

    def pause_music(self):
        self.media_player.pause()

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
