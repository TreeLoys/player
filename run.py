#coding: utf8
#Autor: blackzero
import sys, os

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QWidget
from browser import App
from mutagen import File, StreamInfo

def load_all_in_default_folder(DEFAULT_DIR):
	#print u"Произвожу загрузку из папки..."
	music_folder = os.listdir(DEFAULT_DIR)
	playList = QMediaPlaylist()
	trackInfo = []
	TEXT = ""
	for trac in music_folder:
		sound_path = DEFAULT_DIR +"\\"+ trac
		sound_name = trac
		try:
			if os.path.isfile(os.path.normpath(sound_path)) and sound_path[-3:] == "mp3":

				audio = File(os.path.normpath(sound_path))

				url = QUrl.fromLocalFile(os.path.normpath(sound_path))
				playList.addMedia(QMediaContent(url))
				sound_index = playList.mediaCount()
				sizeFile = os.path.getsize(os.path.normpath(sound_path))
				trackInfo.append([sound_name[:-4], sound_index, audio, sizeFile])
		except Exception as e:
			print "Error: "+e.message
			continue
	playList.setPlaybackMode(QMediaPlaylist.Loop)
	print u"Загрузка завершена."
	return (playList, trackInfo)
if __name__ == "__main__":
	app = QApplication(sys.argv)
	DEFAULT_FOL = QFileDialog.getExistingDirectory(caption=u"Выбери папушку с музычкой")
	playlist, trackInfoList = load_all_in_default_folder(os.path.normpath(DEFAULT_FOL + "/"))

	if len(trackInfoList) == 0:
		w = QWidget()
		QMessageBox.critical(w,
							 u"Нету файлов",
							 u"Здесь нету файлов *.mp3\r\nВыбери другую директорию. \r\nNot found mp3 file.",
							 defaultButton=QMessageBox.Ok)
		playlist, trackInfoList = load_all_in_default_folder(os.path.normpath(DEFAULT_FOL + "/"))
		app.exec_()
	player = QMediaPlayer()
	player.setPlaylist(playlist)
	ui = App(player, playlist, trackInfoList)
	ui.show()
	app.exec_()
