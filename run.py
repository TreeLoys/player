#coding: utf8
#Autor: blackzero
import sys, os

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QWidget
from browser import App

def load_all_in_default_folder(DEFAULT_DIR):
	#print u"Произвожу загрузку из папки..."
	music_folder = os.listdir(DEFAULT_DIR)
	play_list = QMediaPlaylist()
	dName_index = []
	for trac in music_folder:
		sound_path = DEFAULT_DIR +"\\"+ trac
		sound_name = trac
		#print os.path.normpath(sound_path)
		try:
			if os.path.isfile(os.path.normpath(sound_path)) and sound_path[-3:] == "mp3":
				url = QUrl.fromLocalFile(os.path.normpath(sound_path))
				play_list.addMedia(QMediaContent(url))
				sound_index = play_list.mediaCount()
				dName_index.append([sound_name[:-4], sound_index])
		except Exception as e:
			print "Error: "+e.message
			continue
	play_list.setPlaybackMode(QMediaPlaylist.Loop)
	#print u"Загрузка завершена."
	return (play_list, dName_index)
if __name__ == "__main__":
	app = QApplication(sys.argv)
	DEFAULT_FOL = QFileDialog.getExistingDirectory(caption=u"Выбери папушку с музычкой")
	playlist, dName_index = load_all_in_default_folder(os.path.normpath(DEFAULT_FOL+"/"))

	if len(dName_index) == 0:
		w = QWidget()
		QMessageBox.critical(w,
							 u"Нету файлов",
							 u"Здесь нету файлов *.mp3\r\nВыбери другую директорию.",
							 defaultButton=QMessageBox.Ok)
		playlist, dName_index = load_all_in_default_folder(os.path.normpath(DEFAULT_FOL + "/"))
		app.exec_()
	player = QMediaPlayer()
	player.setPlaylist(playlist)
	#player.play()
	ui = App(player, playlist, dName_index)
	ui.show()
	app.exec_()
