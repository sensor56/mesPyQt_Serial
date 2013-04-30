#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Janv 2013 - Tous droits réservés
# GPLv3 - www.mon-club-elec.fr

# modules a importer 
from PyQt4.QtGui import *
from PyQt4.QtCore import *  # inclut QTimer..
import os,sys

import serial # communication serie


from tuto_pyqt_pyserial_terminal_envoi_chaine_sliderx5_record import * # fichier obtenu à partir QtDesigner et pyuic4

class myApp(QWidget, Ui_Form): # la classe reçoit le Qwidget principal ET la classe définie dans test.py obtenu avec pyuic4
	def __init__(self, parent=None):
		QWidget.__init__(self) # initialise le Qwidget principal 
		self.setupUi(parent) # Obligatoire 

		#Ici, personnalisez vos widgets si nécessaire

		#Réalisez les connexions supplémentaires entre signaux et slots
		
		# --- interface terminal série ---
		# connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		self.connect(self.pushButtonInitSerial, SIGNAL("clicked()"), self.pushButtonInitSerialClicked) 
		self.connect(self.pushButtonEnvoi, SIGNAL("clicked()"), self.pushButtonEnvoiClicked) 
		
		# --- connexions des sliders --- 
		# connecte le signal valueChanged de l'objet Slider à l'appel de la fonction voulue 
		self.connect(self.horizontalSlider_1, SIGNAL("valueChanged(int)"), self.horizontalSlider_1ValueChanged) 
		self.connect(self.horizontalSlider_2, SIGNAL("valueChanged(int)"), self.horizontalSlider_2ValueChanged) 
		self.connect(self.horizontalSlider_3, SIGNAL("valueChanged(int)"), self.horizontalSlider_3ValueChanged) 
		self.connect(self.horizontalSlider_4, SIGNAL("valueChanged(int)"), self.horizontalSlider_4ValueChanged) 
		self.connect(self.horizontalSlider_5, SIGNAL("valueChanged(int)"), self.horizontalSlider_5ValueChanged) 
		
		# connecte le signal sliderReleased de l'objet Dial à l'appel de la fonction voulue 
		self.connect(self.horizontalSlider_1, SIGNAL("sliderReleased()"), self.horizontalSlider_1Released) 
		self.connect(self.horizontalSlider_2, SIGNAL("sliderReleased()"), self.horizontalSlider_2Released) 
		self.connect(self.horizontalSlider_3, SIGNAL("sliderReleased()"), self.horizontalSlider_3Released) 
		self.connect(self.horizontalSlider_4, SIGNAL("sliderReleased()"), self.horizontalSlider_4Released) 
		self.connect(self.horizontalSlider_5, SIGNAL("sliderReleased()"), self.horizontalSlider_5Released) 

		#-- interface d'enregistrement 
		self.connect(self.pushButtonAjouter, SIGNAL("clicked()"), self.pushButtonAjouterClicked) 
		self.connect(self.pushButtonToHome, SIGNAL("clicked()"), self.pushButtonToHomeClicked) 

		#self.connect(self.pushButtonEffacer, SIGNAL("clicked()"), self.pushButtonEffacerClicked) 
		#self.connect(self.pushButtonSelectTout, SIGNAL("clicked()"), self.pushButtonSelectToutClicked) 
		#self.connect(self.pushButtonDeselect, SIGNAL("clicked()"), self.pushButtonDeselectClicked) 
		self.connect(self.pushButtonSelectPrec, SIGNAL("clicked()"), self.pushButtonSelectPrecClicked) 
		self.connect(self.pushButtonSelectSuiv, SIGNAL("clicked()"), self.pushButtonSelectSuivClicked) 
		self.connect(self.pushButtonSelectDebut, SIGNAL("clicked()"), self.pushButtonSelectDebutClicked) 
		self.connect(self.pushButtonSelectFin, SIGNAL("clicked()"), self.pushButtonSelectFinClicked) 

		# variables / objets utiles 
		self.cursor=None # objet curseur initialisé à None

		#initialisation Timer
		self.timer=QTimer() # déclare un timer Qt
		self.connect(self.timer, SIGNAL("timeout()"), self.timerEvent) # connecte le signal timeOut de l'objet timer à l'appel de la fonction voulue 

		#--- déclaration utiles --- 
		self.serialPort=None # déclaration initiale

	# les fonctions appelées, utilisées par les signaux 
	
	#----- les fonctions des signaux des boutons du Terminal série ---- 				
	def pushButtonInitSerialClicked(self): # lors appui bouton initialisation série 
		print("Bouton Init cliqué")
		if self.serialPort: # si le port existe déjà 
			self.serialPort.close() # ferme le port si existe

		# -- initialise paramètres initialisation
		if self.comboBoxPort.currentText()=="" : # si le champ d'initialisation Port est vide = initialisation par défaut 
			strPortInit="/dev/ttyACM0" # port par défaut
		else :
			strPortInit=str(self.comboBoxPort.currentText()) #sinon utilise paramètre champ texte pour le port
		
		strDebitInit=str(self.comboBoxDebit.currentText()) # paramètre champ texte pour debit 
		
		#--- initialisation série avec gestion erreur --- 			
		try: # essaie d'exécuter les instructions 
			# initialise port serie avec délai attente en réception en ms
			self.serialPort=serial.Serial(strPortInit, strDebitInit, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 0.100) 			
			#self.serialPort=serial.Serial(strPortInit, strDebitInit) # initialise port serie forme réduite 
			self.serialPort.flushInput() # vide la file d'attente série
			print("Initialisation Port Série : " + strPortInit +" @ " + strDebitInit +" = OK ") # affiche debug
			
			#-- change aspect bouton init
			self.pushButtonInitSerial.setStyleSheet(QString.fromUtf8("background-color: rgb(0, 255, 0);")) # bouton en vert
			self.pushButtonInitSerial.setText("OK")  # change titre bouton 
			
		except: # si erreur initialisation 
			print("Erreur initialisation Série")		
				
			#-- change aspect bouton init
			self.pushButtonInitSerial.setStyleSheet(QString.fromUtf8("background-color: rgb(255, 127, 0);")) # bouton en orange
			self.pushButtonInitSerial.setText(QString.fromUtf8("PB"))  # change titre bouton 

		self.timer.start(10) # lance le timer avec délai en ms - 10 pour réception rapide 

	def pushButtonEnvoiClicked(self): # lors appui bouton envoi série du champ du Terminal Série
		print("Bouton ENVOI appuyé")
		self.envoiChaineSerie(str(self.lineEditChaineEnvoi.text())) # envoi le contenu du champ texte sur le port série 

	#------- fonctions des signaux du/des sliders ----------
	def horizontalSlider_1ValueChanged(self, valeur): # fonction appelée si changement valeur slider - reçoit la valeur courante
		print("Slider 1 modifié : valeur = " + str(valeur))
		
	def horizontalSlider_1Released(self): # fonction appelée si changement souris relâchée
		print("Slider 1 : clic souris relaché")
		#self.envoiChaineSerie("servoPanTo("+str(valeur)+")") # envoi le contenu du champ texte sur le port série 
		if self.lineEditSlider_1.text()=="":
			self.envoiChaineSerie(str(self.horizontalSlider_1.value())) # envoi le contenu du champ texte + valeur + ")" sur le port série 
		else:
			self.envoiChaineSerie(str(self.lineEditSlider_1.text()) +str(self.horizontalSlider_1.value())+")") # envoi le contenu du champ texte + valeur + ")" sur le port série 

	def horizontalSlider_2ValueChanged(self, valeur): # fonction appelée si changement valeur slider - reçoit la valeur courante
		print("Slider 2 modifié : valeur = " + str(valeur))
		
	def horizontalSlider_2Released(self): # fonction appelée si changement souris relâchée
		print("Slider 2 : clic souris relaché")
		#self.envoiChaineSerie("servoPanTo("+str(valeur)+")") # envoi le contenu du champ texte sur le port série 
		if self.lineEditSlider_2.text()=="":
			self.envoiChaineSerie(str(self.horizontalSlider_2.value())) # envoi le contenu du champ texte + valeur + ")" sur le port série 
		else:
			self.envoiChaineSerie(str(self.lineEditSlider_2.text()) +str(self.horizontalSlider_2.value())+")") # envoi le contenu du champ texte + valeur + ")" sur le port série 

	def horizontalSlider_3ValueChanged(self, valeur): # fonction appelée si changement valeur slider - reçoit la valeur courante
		print("Slider 3 modifié : valeur = " + str(valeur))
		
	def horizontalSlider_3Released(self): # fonction appelée si changement souris relâchée
		print("Slider 3 : clic souris relaché")
		#self.envoiChaineSerie("servoPanTo("+str(valeur)+")") # envoi le contenu du champ texte sur le port série 
		if self.lineEditSlider_3.text()=="":
			self.envoiChaineSerie(str(self.horizontalSlider_3.value())) # envoi le contenu du champ texte + valeur + ")" sur le port série 
		else:
			self.envoiChaineSerie(str(self.lineEditSlider_3.text()) +str(self.horizontalSlider_3.value())+")") # envoi le contenu du champ texte + valeur + ")" sur le port série 

	def horizontalSlider_4ValueChanged(self, valeur): # fonction appelée si changement valeur slider - reçoit la valeur courante
		print("Slider 4 modifié : valeur = " + str(valeur))
		
	def horizontalSlider_4Released(self): # fonction appelée si changement souris relâchée
		print("Slider 4 : clic souris relaché")
		#self.envoiChaineSerie("servoPanTo("+str(valeur)+")") # envoi le contenu du champ texte sur le port série 
		if self.lineEditSlider_4.text()=="":
			self.envoiChaineSerie(str(self.horizontalSlider_4.value())) # envoi le contenu du champ texte + valeur + ")" sur le port série 
		else:
			self.envoiChaineSerie(str(self.lineEditSlider_4.text()) +str(self.horizontalSlider_4.value())+")") # envoi le contenu du champ texte + valeur + ")" sur le port série 

	def horizontalSlider_5ValueChanged(self, valeur): # fonction appelée si changement valeur slider - reçoit la valeur courante
		print("Slider 5 modifié : valeur = " + str(valeur))
		
	def horizontalSlider_5Released(self): # fonction appelée si changement souris relâchée
		print("Slider 5 : clic souris relaché")
		#self.envoiChaineSerie("servoPanTo("+str(valeur)+")") # envoi le contenu du champ texte sur le port série 
		if self.lineEditSlider_5.text()=="":
			self.envoiChaineSerie(str(self.horizontalSlider_5.value())) # envoi le contenu du champ texte + valeur + ")" sur le port série 
		else:
			self.envoiChaineSerie(str(self.lineEditSlider_5.text()) +str(self.horizontalSlider_5.value())+")") # envoi le contenu du champ texte + valeur + ")" sur le port série 
	
	# ---- fonction des signaux de l'interface d'enregistrement --- 
	def pushButtonAjouterClicked(self):
		print("Bouton Ajouter cliqué")
		self.textEditSequence.append(self.lineEditRacineAjouter.text()
		+str(self.horizontalSlider_1.value())+","
		+str(self.horizontalSlider_2.value())+","
		+str(self.horizontalSlider_3.value())+","
		+str(self.horizontalSlider_4.value())+","
		+str(self.horizontalSlider_5.value())+")"
		) # ajoute racine + valeurs au champ texte 

	def pushButtonToHomeClicked(self):
		print("Bouton ToHome cliqué")
		
		# met à jour les sliders avec les positions ToHome
		self.horizontalSlider_1.setValue(90) 
		self.horizontalSlider_2.setValue(120) 
		self.horizontalSlider_3.setValue(0) 
		self.horizontalSlider_4.setValue(0) 
		self.horizontalSlider_5.setValue(10) 
		
		"""
		self.textEditSequence.append(self.lineEditRacineAjouter.text()
		+str(self.horizontalSlider_1.value())+","
		+str(self.horizontalSlider_2.value())+","
		+str(self.horizontalSlider_3.value())+","
		+str(self.horizontalSlider_4.value())+","
		+str(self.horizontalSlider_5.value())+")"
		) # ajoute racine + valeurs au champ texte 
		"""
		
		self.textEditSequence.append("toHome()") # ajoute racine + valeurs au champ texte 
		
		self.envoiChaineSerie("toHome()") # envoie la chaine sur le port série 		
		
		"""
		self.envoiChaineSerie(self.lineEditRacineAjouter.text()
		+str(self.horizontalSlider_1.value())+","
		+str(self.horizontalSlider_2.value())+","
		+str(self.horizontalSlider_3.value())+","
		+str(self.horizontalSlider_4.value())+","
		+str(self.horizontalSlider_5.value())+")"
		) # envoie la chaine sur le port série 
		"""
		
		#---- fonctions gestion défilement dans textEdit ---- 
		
	def pushButtonSelectPrecClicked(self):
		print("Bouton Select. Prec cliqué")

		if self.cursor==None: # si self.cursor n'existe pas, on le crée - sinon on réutilise le curseur courant
			self.cursor=self.textEditSequence.textCursor() # récupère l'objet textCursor du textEdit... les opérations réalisées sur le self.cursor ne seront pas visible

		# -- se place sur la bonne ligne -- 
		if self.cursor.atEnd() and not self.cursor.hasSelection(): # si le curseur est à la fin et pas de sélection = 1ère sélection
			self.cursor.movePosition(QTextCursor.NoMove, QTextCursor.MoveAnchor) # reste sur la meme ligne - position curseur et anchor ensemble 
		else : 
			self.cursor.movePosition(QTextCursor.Up, QTextCursor.MoveAnchor) # sinon monte d'une ligne - position curseur et anchor ensemble 

		# -- sélectionne la ligne -- 
		#self.cursor.clearSelection() # déselectionne texte (au cas où...) = ramène anchor à la position du curseur
	
		self.cursor.select(QTextCursor.LineUnderCursor) # sélectionne la ligne courante 
		print ("anchor =" + str(self.cursor.anchor())) # affiche début courant - se trouve à la fin du texte par défaut
		print ("position =" + str(self.cursor.position())) # affiche position courante - se trouve à la fin du texte par défaut
		print ("texte=" + str(self.cursor.selectedText())) # affiche texte sélectionné
				
		self.textEditSequence.setTextCursor(self.cursor) # applique le curseur au texte Edit = rend visible... 	

		self.envoiChaineSerie(str(self.cursor.selectedText())) # envoie la chaine sur le port série 		
			
	def pushButtonSelectSuivClicked(self):
		print("Bouton Select. Suiv cliqué")

		if self.cursor==None: # si self.cursor n'existe pas, on le crée - sinon on réutilise le curseur courant
			self.cursor=self.textEditSequence.textCursor() # récupère l'objet textCursor du textEdit... les opérations réalisées sur le self.cursor ne seront pas visible

		# -- se place sur la bonne ligne -- 
		if self.cursor.atEnd() and not self.cursor.hasSelection(): # si le curseur est à la fin et pas de sélection = 1ère sélection
			#self.cursor.movePosition(QTextCursor.NoMove, QTextCursor.MoveAnchor) # reste sur la meme ligne - position curseur et anchor ensemble 
			self.cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor) # se place au debut du texte - position curseur et anchor ensemble 
		else : 
			self.cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor) # sinon descend d'une ligne - position curseur et anchor ensemble 

		# -- sélectionne la ligne -- 
		#self.cursor.clearSelection() # déselectionne texte (au cas où...) = ramène anchor à la position du curseur
	
		self.cursor.select(QTextCursor.LineUnderCursor) # sélectionne la ligne courante 
		print ("anchor =" + str(self.cursor.anchor())) # affiche début courant - se trouve à la fin du texte par défaut
		print ("position =" + str(self.cursor.position())) # affiche position courante - se trouve à la fin du texte par défaut
		print ("texte=" + str(self.cursor.selectedText())) # affiche texte sélectionné
				
		self.textEditSequence.setTextCursor(self.cursor) # applique le curseur au texte Edit = rend visible... 	

		self.envoiChaineSerie(str(self.cursor.selectedText())) # envoie la chaine sur le port série 		
	
	def pushButtonSelectDebutClicked(self):
		print("Bouton Select. Debut cliqué")

		if self.cursor==None: # si self.cursor n'existe pas, on le crée - sinon on réutilise le curseur courant
			self.cursor=self.textEditSequence.textCursor() # récupère l'objet textCursor du textEdit... les opérations réalisées sur le self.cursor ne seront pas visible

		self.cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor) # se place au debut du texte - position curseur et anchor ensemble 

		# -- sélectionne la ligne -- 
		#self.cursor.clearSelection() # déselectionne texte (au cas où...) = ramène anchor à la position du curseur
	
		self.cursor.select(QTextCursor.LineUnderCursor) # sélectionne la ligne courante 
		print ("anchor =" + str(self.cursor.anchor())) # affiche début courant - se trouve à la fin du texte par défaut
		print ("position =" + str(self.cursor.position())) # affiche position courante - se trouve à la fin du texte par défaut
		print ("texte=" + str(self.cursor.selectedText())) # affiche texte sélectionné

		self.textEditSequence.setTextCursor(self.cursor) # applique le curseur au texte Edit = rend visible... 	

		self.envoiChaineSerie(str(self.cursor.selectedText())) # envoie la chaine sur le port série 		

	def pushButtonSelectFinClicked(self):
		print("Bouton Select. Fin cliqué")

		if self.cursor==None: # si self.cursor n'existe pas, on le crée - sinon on réutilise le curseur courant
			self.cursor=self.textEditSequence.textCursor() # récupère l'objet textCursor du textEdit... les opérations réalisées sur le self.cursor ne seront pas visible

		self.cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor) # se place a la fin du texte - position curseur et anchor ensemble 

		# -- sélectionne la ligne -- 
		#self.cursor.clearSelection() # déselectionne texte (au cas où...) = ramène anchor à la position du curseur
	
		self.cursor.select(QTextCursor.LineUnderCursor) # sélectionne la ligne courante 
		print ("anchor =" + str(self.cursor.anchor())) # affiche début courant - se trouve à la fin du texte par défaut
		print ("position =" + str(self.cursor.position())) # affiche position courante - se trouve à la fin du texte par défaut
		print ("texte=" + str(self.cursor.selectedText())) # affiche texte sélectionné
				
		self.textEditSequence.setTextCursor(self.cursor) # applique le curseur au texte Edit = rend visible... 	

		self.envoiChaineSerie(str(self.cursor.selectedText())) # envoie la chaine sur le port série 		

	#----- fonction de classe commune d'envoi d'une chaîne sur le port série ---- 
	def envoiChaineSerie(self, chaineIn): # la fonction reçoit un objet chaîne Str correspondant à la racine à envoyer
		
		if self.serialPort: # seulement si le port série existe - n'existe pas (=None) tant que pas initialisé 

			self.timer.stop() # stoppe le timer le temps d'envoyer message sur le port série		
			
			# combobox avec index 0 = rien, 1=saut de ligne (LF), 2=retour chariot (CR), 3= les 2 LF+CR
			if self.comboBoxFinLigne.currentIndex()==0: # si rien sélectionné
				# self.serialPort.write(str(self.lineEditChaineEnvoi.text())+'\n'  ) # envoie la chaine sur le port serie		
				self.serialPort.write(chaineIn)  # envoie la chaine sur le port serie	- variante ascii	
				print("Envoi Série : " + chaineIn )
				self.textEditTraceEnvoiSerie.append(chaineIn) # ajoute texteEdit de visualisation 

			if self.comboBoxFinLigne.currentIndex()==1: # si saut de ligne sélectionné
				self.serialPort.write(chaineIn +chr(10) ) # envoie la chaine sur le port serie	- variante ascii	
				print("Envoi Série : " + chaineIn + '\n')
				self.textEditTraceEnvoiSerie.append(chaineIn) # ajoute texteEdit de visualisation 
				
			if self.comboBoxFinLigne.currentIndex()==2: # si retour chariot sélectionné
				self.serialPort.write(chaineIn+chr(13)  ) # envoie la chaine sur le port serie	- variante ascii	
				print("Envoi Série : " + chaineIn + '\r')
				self.textEditTraceEnvoiSerie.append(chaineIn) # ajoute texteEdit de visualisation 
				
			if self.comboBoxFinLigne.currentIndex()==3: # si saut de ligne + retour chariot sélectionné
				self.serialPort.write(chaineIn+chr(10)+chr(13)  ) # envoie la chaine sur le port serie	- variante ascii
				print("Envoi Série : " + chaineIn + '\n'+'\r')
				self.textEditTraceEnvoiSerie.append(chaineIn) # ajoute texteEdit de visualisation 
				
			self.timer.start() # redémarre le timer - laisse délai pour réception en réinitialisation Timer à 0
			# car sinon l'appui survient n'importe quand et si survient peu de temps avant fin délai
			# la réception est hachée
	
	#--- fin envoiChaineSerie

	#----- fonction de gestion du signal timeout du QTimer
	def timerEvent(self): # fonction appelée lors de la survenue d'un évènement Timer - nom fonction indiférrent 
		#-- variables de réception -- 
		self.chaineIn="";
		self.char="";
		
		# lecture des données reçues		
		if self.serialPort: # seulement si le port série existe 
			self.timer.stop() # stoppe le timer le temps de lire les caractères et éviter "réentrée"
			
			while (self.serialPort.inWaiting()): # tant que au moins un caractère en réception
				self.char=self.serialPort.read() # on lit le caractère
				#self.chaineIn=self.chaineIn+self.char		# forme minimale...
				
				if self.char=='\n': # si saut de ligne, on sort du while
					print("saut ligne reçu") # debug
					break # sort du while
				else: #tant que c'est pas le saut de ligne, on l'ajoute à la chaine 
					self.chaineIn=self.chaineIn+self.char					
				
			if len(self.chaineIn)>0: # ... pour ne pas avoir d'affichage si ""	
				print(self.chaineIn) # affiche la chaîne 
				self.textEditReception.append(self.chaineIn[:-1]) # ajoute le texte au textEdit en enlevant le dernier caractère 
				
			self.timer.start() # redémarre le timer
			
	#---- fin timerEvent 
			
def main(args):
	a=QApplication(args) # crée l'objet application 
	f=QWidget() # crée le QWidget racine
	c=myApp(f) # appelle la classe contenant le code de l'application 
	f.show() # affiche la fenêtre QWidget
	r=a.exec_() # lance l'exécution de l'application 
	return r

if __name__=="__main__": # pour rendre le code exécutable 
	main(sys.argv) # appelle la fonction main

