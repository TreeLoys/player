#coding: utf8
#Autor: blackzero
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mutagen
import os, sys
from jinja2 import Template
#config
URL = os.path.dirname(os.path.abspath(__file__)) + "/static/"
URL = URL.replace("\\", "/")

class QPLAYER_COMMAND(QObject):
	def __init__(self, p, l, trackInfo):
		QObject.__init__(self)
		self.statusNextComposition = False
		self.p = p
		self.l = l
		self.trackInfo = trackInfo
		self.p.currentMediaChanged.connect(self.nextCompositionPlayed)
	@pyqtSlot()
	def play(self):
		self.p.play()

	@pyqtSlot()
	def stop(self):
		self.p.stop()
	@pyqtSlot()
	def pause(self):
		self.p.pause()
	@pyqtSlot(result=int)
	def duration(self):
		#возвращает продолжительность воспроизведения мультимедиа в миллисекундах
		return self.p.duration()
	@pyqtSlot(result=int)
	def position(self):
		#возвращает продолжительность воспроизведения мультимедиа в миллисекундах
		return self.p.position()
	@pyqtSlot(int)
	def setPosition(self, time):
		self.p.setPosition(time / 100.0 * self.duration())
	@pyqtSlot(int)
	def setIndex(self, index):
		self.l.setCurrentIndex(index)
		self.statusNextComposition = False
	@pyqtSlot(result=str)
	def getNameTrack(self):
		return "<span class='number'>" + str(self.l.currentIndex()+1) +"</span> "+\
			   self.trackInfo[self.l.currentIndex()][0]
	@pyqtSlot()
	def stop(self):
		self.p.stop()
	@pyqtSlot(result=int)
	def getCurrentIndex(self):
		return self.l.currentIndex()
	@pyqtSlot()
	def next(self):
		self.l.next()
		self.statusNextComposition = False
	@pyqtSlot()
	def prev(self):
		self.l.previous()
		self.statusNextComposition = False
	def nextCompositionPlayed(self):
		self.statusNextComposition = True
	@pyqtSlot(result=int)
	def timerNext(self):
		if (self.statusNextComposition):
			self.statusNextComposition = False
			return True
		return False
	@pyqtSlot(result=str)
	def info(self):
		pathCurrentSound = self.trackInfo[self.l.currentIndex()][2]
		sizeFile = os.path.getsize(pathCurrentSound)
		audio = mutagen.File(pathCurrentSound)
		info = """
			 <div class="left">
				 {bitrate}kbps {ch}ch {size}MB
			 </div>
			 <div class="right">
				{lengthm}:{lengths}
			 </div>
				""".format(bitrate=audio.info.bitrate//1000,
					ch=audio.info.channels,
					lengthm=int(audio.info.length // 60),
					lengths=int(audio.info.length % 60),
					size=sizeFile//1000000)
		return info
class App(QWidget):
	def __init__(self, player, playlist, trackInfoList, *args, **kwargs):
		QWidget.__init__(self, *args, **kwargs)
		view = QWebView(self)

		view.resize(800, 600)
		#для перехвата post
		page = QWebPage()
		self.qplayer = QPLAYER_COMMAND(player, playlist, trackInfoList)
		page.mainFrame().addToJavaScriptWindowObject("qplayer", self.qplayer)
		page.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
		view.setPage(page)

		with open(URL + "index.html", "rb") as f:
			template = Template(f.read().decode("utf8"))
		template_compos = ""
		#генерируем список воспроизведения
		for name in trackInfoList:
			template_compos += """
			<div class="composition" onclick="select_music(%s, this)" valued="%s">
			 <div class="picture" >
				 <div class="picture-play">
					 <div class="picture-play-span">
						 <span class="glyphicon glyphicon-play"></span>
					 </div>
				 </div>
			 </div>
			 <div class="composition_text">%s</div>
			</div>""" % (str(name[1]-1),
					  str(name[1]-1),
					  "<span class='number'>"+str(name[1])+"</span> "+name[0])

		view.setHtml(template.render(URL=URL, COMPOS=template_compos), QUrl("file:///"+URL))
		self.setWindowTitle('VK Player')
		self.setWindowIcon(QIcon(os.path.dirname(os.path.abspath(__file__))+"./icon.png"))


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = App()
	ui.show()
	app.exec_()