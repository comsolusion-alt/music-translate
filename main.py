import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame

# Inisialisasi pemutar audio pygame
pygame.mixer.init()


class MusicPlayerApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Python Desktop Music Player")
    self.root.geometry("420x220")
    self.root.configure(bg="#121212")

    self.current_file = ""
    self.is_paused = False

    # Label Judul Lagu
    self.title_label = tk.Label(
        root,
        text="🎵 Tidak ada lagu yang dipilih",
        font=("Arial", 11, "bold"),
        bg="#121212",
        fg="#FFFFFF",
        wraplength=380,
    )
    self.title_label.pack(pady=25)

    # Frame Tombol Kontrol
    btn_frame = tk.Frame(root, bg="#121212")
    btn_frame.pack(pady=10)

    # Tombol Buka File
    self.btn_open = tk.Button(
        btn_frame,
        text="📂 Buka",
        command=self.open_file,
        bg="#1DB954",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=12,
        pady=6,
        relief="flat",
    )
    self.btn_open.grid(row=0, column=0, padx=6)

    # Tombol Play
    self.btn_play = tk.Button(
        btn_frame,
        text="▶️ Play",
        command=self.play_music,
        bg="#282828",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=12,
        pady=6,
        relief="flat",
    )
    self.btn_play.grid(row=0, column=1, padx=6)

    # Tombol Pause / Resume
    self.btn_pause = tk.Button(
        btn_frame,
        text="⏸️ Pause",
        command=self.pause_music,
        bg="#282828",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=12,
        pady=6,
        relief="flat",
    )
    self.btn_pause.grid(row=0, column=2, padx=6)

    # Tombol Stop
    self.btn_stop = tk.Button(
        btn_frame,
        text="⏹️ Stop",
        command=self.stop_music,
        bg="#282828",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=12,
        pady=6,
        relief="flat",
    )
    self.btn_stop.grid(row=0, column=3, padx=6)

  def open_file(self):
    """Membuka jendela direktori komputer untuk memilih file musik."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
    )
    if file_path:
      self.current_file = file_path
      file_name = os.path.basename(file_path)
      self.title_label.config(text=f"🎵 {file_name}")
      self.play_music()

  def play_music(self):
    """Memuat dan memutar file musik."""
    if self.current_file:
      if self.is_paused:
        pygame.mixer.music.unpause()
        self.is_paused = False
      else:
        try:
          pygame.mixer.music.load(self.current_file)
          pygame.mixer.music.play()
          self.is_paused = False
        except Exception as e:
          messagebox.showerror("Error", f"Gagal memutar audio: {e}")
    else:
      messagebox.showwarning(
          "Peringatan", "Silakan pilih file lagu terlebih dahulu!"
      )

  def pause_music(self):
    """Menjeda atau melanjutkan pemutaran musik."""
    if self.is_paused:
      pygame.mixer.music.unpause()
      self.is_paused = False
      self.btn_pause.config(text="⏸️ Pause")
    else:
      pygame.mixer.music.pause()
      self.is_paused = True
      self.btn_pause.config(text="▶️ Resume")

  def stop_music(self):
      """Menghentikan total pemutaran musik."""
      pygame.mixer.music.stop()
      self.is_paused = False
      self.btn_pause.config(text="⏸️ Pause")


if __name__ == "__main__":
  root = tk.Tk()
  app = MusicPlayerApp(root)
  root.mainloop()
