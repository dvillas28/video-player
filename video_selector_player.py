from PyQt6.QtCore import (Qt, QUrl)
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout)
from PyQt6.QtMultimedia import (QAudioOutput, QMediaPlayer)
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QCursor
import time
import sys
import os

# TODO separar esto y hacerlo mas legible

# TODO ocultar el widget reproductor si es que termina un video, esto se podria resolver si
# en el archivo tenemos la duraccion de cada video


# class MainWindow(QMainWindow):
class MainWindow(QWidget):

    def __init__(self, playlist_path):
        super().__init__()
        # gui
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)

        self.layout = QHBoxLayout(self)
        self._video_widget = QVideoWidget(self)
        self._video_widget.showMaximized()

        # para poder controlarlo con las teclas inmediatamente al comenzar
        # TODO mantener en todo momento un focus a la ventana exterior, de modo que
        # los keypress event funcionen, buscar una manera de quitar el focus al widget
        self._video_widget.setFocus()
        self._player.setVideoOutput(self._video_widget)
        # self._video_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # self._player.errorOccurred.connect(self._player_error)

        # TODO, poner una imagen de fondo en el widget central, luego que los videos se superpongan

        # video info
        self._playlist_path = playlist_path
        self._videos = {}  # key y su path asociado
        self.load_videos()

        # creamos un cursor y lo dejamos invisible
        self.cursor = QCursor()
        self.cursor.setShape(Qt.CursorShape.BlankCursor)
        QApplication.setOverrideCursor(self.cursor)

        self.layout.addWidget(self._video_widget)
        self.setLayout(self.layout)

    # def _player_error(self, error, error_string):
    #     print(error_string, file=sys.stderr)
    #     # self.show_status_message(error_string)

    def keyPressEvent(self, event):
        # TODO repensar la implementacion de esto
        # selected a video from the playlist
        if chr(event.key()).isnumeric():
            self.security_stop()
            self.load_and_play(event.key())

        elif event.key() == Qt.Key.Key_Z:
            """ Cierra la app """
            self._player.stop()
            # QApplication.quit()
            sys.exit()

        # TODO juntar todo esto en un solo boton
        elif event.key() == Qt.Key.Key_X:
            """ Pausa el widget de video """
            self._player.pause()

        elif event.key() == Qt.Key.Key_C:
            """ Continua la reproduccion del video """
            self._player.play()

    def load_and_play(self, key: int) -> None:
        """ Se recibe un key, se carga y se reproduce un video """
        path = self._videos[chr(key)]
        url = QUrl.fromLocalFile(path)
        self._player.setSource(url)
        self._player.play()

    def security_stop(self):
        """ No funciona sin esto """
        self._player.stop()
        time.sleep(0.1)

    def load_videos(self):
        """ Lee el archivo y almacena las rutas en un diccionario"""
        # TODO hacer esto mas robusto
        try:
            with open(os.path.join(self._playlist_path)) as arch:
                lineas = arch.readlines()
                for linea in lineas:
                    linea = os.path.join(linea.strip())

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
