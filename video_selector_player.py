from PyQt6.QtCore import (Qt, QUrl, QTimer, pyqtSignal)
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QLabel)
from PyQt6.QtMultimedia import (QAudioOutput, QMediaPlayer)
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QCursor, QPixmap, QKeyEvent
import time
import sys
import os

# TODO separar esto y hacerlo mas legible


class Video(QVideoWidget):
    senal_load_and_play = pyqtSignal(int)
    senal_pause = pyqtSignal()
    senal_play = pyqtSignal()
    senal_stop = pyqtSignal()
    senal_stop_and_hide = pyqtSignal()

    def onKeyPress_Event(self, event):
        # self.activateWindow()
        # self.parent().activateWindow()
        # self.parent().raise_()

        if chr(event.key()).isnumeric():
            self.senal_load_and_play.emit(event.key())

        # TODO juntar todo esto en un solo boton
        elif event.key() == Qt.Key.Key_X:
            """ Pausa el widget de video """
            self.senal_pause.emit()

        elif event.key() == Qt.Key.Key_C:
            """ Continua la reproduccion del video """
            self.senal_play.emit()

        elif event.key() == Qt.Key.Key_Z:
            """ Cierra la app """
            self.senal_stop.emit()

        elif event.key() == Qt.Key.Key_Space:
            """ Detiene el video y esconde el widget """
            if self.isVisible():
                self.senal_stop_and_hide.emit()


class MainWindow(QWidget):
    key_pressed = pyqtSignal(QKeyEvent)

    def __init__(self, playlist_path):
        super().__init__()
        # get the current size of the window
        screen = QApplication.primaryScreen()
        size = screen.size()

        # gui
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._audio_output = QAudioOutput(self)
        self._player = QMediaPlayer(self)
        self._player.setAudioOutput(self._audio_output)

        self._video_widget = Video(self)
        self._video_widget.setGeometry(0, 0, size.width(), size.height())
        self._video_widget.showMaximized()
        self._video_widget.setHidden(True)  # aparece oculto al inicio

        # TODO, hallar la manera de siempre tener focus en la pantalla principal
        self._player.setVideoOutput(self._video_widget)

        # video info
        self._playlist_path = playlist_path
        self._videos = {}  # key y su path asociado
        self.load_videos()
        self.curr_duration = None

        # imagen de fondo
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, size.width(), size.height())
        path = os.path.join('images', 'example.jpg')
        pixmap = QPixmap(path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        # creamos un cursor y lo dejamos invisible
        self.cursor = QCursor()
        self.cursor.setShape(Qt.CursorShape.BlankCursor)
        QApplication.setOverrideCursor(self.cursor)

        self.showMaximized()

    def connect_senales(self):
        self.key_pressed.connect(self._video_widget.onKeyPress_Event)

        self._player.mediaStatusChanged.connect(self.statusChanged)

        self._video_widget.senal_load_and_play.connect(self.load_and_play)
        self._video_widget.senal_pause.connect(self._player.pause)
        self._video_widget.senal_play.connect(self._player.play)
        self._video_widget.senal_stop.connect(self.stop_and_close)
        self._video_widget.senal_stop_and_hide.connect(self.stop_and_hide)

    def load_videos(self):
        """ Lee el archivo y almacena las rutas en un diccionario"""
        # TODO hacer esto mas robusto
        try:
            with open(os.path.join(self._playlist_path)) as arch:
                lineas = arch.readlines()
                info_list = []
                for linea in lineas:
                    info_list.append(linea.strip())

                c = 0
                for video in info_list:
                    video_path = os.path.join(video)
                    self._videos[str(c)] = video_path
                    c += 1

        except FileNotFoundError:
            print(f'> Error: "{self._playlist_path}" is not a valid path')
            sys.exit()

    def keyPressEvent(self, event):
        self.key_pressed.emit(event)
        return super().keyPressEvent(event)

    def load_and_play(self, key: int) -> None:
        """ Se recibe un key, se carga y se reproduce un video """
        try:
            path = self._videos[chr(key)]

        except KeyError:
            print(f'> Error: Key "{chr(key)}" is not registered to any video')

        else:
            self._video_widget.setHidden(False)
            self.security_stop()
            url = QUrl.fromLocalFile(path)
            self._player.setSource(url)
            self._player.play()

            print(f'> Now Playing -> {path}')

    def security_stop(self):
        """ No funciona sin esto """
        self._player.stop()
        time.sleep(0.1)

    def stop_and_hide(self):
        # the player is stopped and the widget is hidden
        self._player.stop()
        self._video_widget.setHidden(True)

    def stop_and_close(self):
        self._player.stop()
        sys.exit()

    def statusChanged(self, status):
        if status == self._player.MediaStatus.EndOfMedia:
            self.stop_and_hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow(sys.argv[1])
    main_win.connect_senales()
    sys.exit(app.exec())
