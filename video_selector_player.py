
import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow)
from PyQt6.QtMultimedia import (QAudioOutput, QMediaPlayer)
from PyQt6.QtMultimediaWidgets import QVideoWidget
import time
import os


class MainWindow(QMainWindow):

    def __init__(self, playlist_path):
        super().__init__()

        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)

        self._video_widget = QVideoWidget()
        self.setCentralWidget(self._video_widget)
        self._player.setVideoOutput(self._video_widget)

        self._player.errorOccurred.connect(self._player_error)

        self._playlist_path = playlist_path

        self._videos = {}  # key y su path asociado
        self.load_videos()

    def _player_error(self, error, error_string):
        print(error_string, file=sys.stderr)
        # self.show_status_message(error_string)

    def keyPressEvent(self, event):

        # selected a video from the playlist
        if chr(event.key()).isnumeric():
            self.security_stop()
            self.load_and_play(event.key())

        # closes
        elif event.key() == Qt.Key.Key_Z:
            self._player.stop()
            QApplication.quit()

        # pauses
        elif event.key() == Qt.Key.Key_X:
            self._player.pause()

        # reanudates
        elif event.key() == Qt.Key.Key_C:
            self._player.play()

    def load_and_play(self, key: int) -> None:
        path = self._videos[chr(key)]
        url = QUrl.fromLocalFile(path)
        self._player.setSource(url)
        self._player.play()

    def security_stop(self):
        """ No funciona sin esto """
        self._player.stop()
        time.sleep(0.1)

    def load_videos(self):
        try:
            with open(os.path.join(self._playlist_path)) as arch:
                lineas = arch.readlines()
                for linea in lineas:
                    linea = linea.strip()

                c = 0
                for linea in lineas:
                    self._videos[str(c)] = linea
                    c += 1

        except FileNotFoundError:
            print(f'> Error: "{self._playlist_path}" is not a valid path')
            sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow(sys.argv[1])
    available_geometry = main_win.screen().availableGeometry()
    main_win.resize(300, 300)
    main_win.showMaximized()
    sys.exit(app.exec())
