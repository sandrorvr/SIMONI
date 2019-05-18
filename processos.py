from threading import Thread
import cv2
import dlib
import os
import numpy as np
import datetime
import csv

class processamento:

	def __init__(self, imagem):
		self.imagem=imagem
		self.stopped = False
		self.face=None
		self.nome=None
		self.dicionario={}
		self.registro=[]

	def start(self):
		Thread(target=self.detector, args=()).start()
		return self

	def gravar(self):
		data = datetime.datetime.now()
		arquivo = open('registros/regsitro '+str((data.day,data.month))+'.csv','w')
		escrever = csv.writer(arquivo)
		escrever.writerow(['id','ano','mes','dia','hora','minuto'])
		for pessoa in self.registro:
			escrever.writerow(pessoa)
		arquivo.close()

	def detector(self):
		detectorFace = dlib.get_frontal_face_detector()
		detectorPontos = dlib.shape_predictor("recursos/shape_predictor_68_face_landmarks.dat")
		reconhecimentoFacial = dlib.face_recognition_model_v1("recursos/dlib_face_recognition_resnet_model_v1.dat")
		indices = np.load("recursos/indices_rn.pickle")
		descritoresFaciais = np.load("recursos/descritores_rn.npy")
		limiar = 0.5
		classificador_face = cv2.CascadeClassifier('recursos/face.xml')
		while not self.stopped:
			data = datetime.datetime.now()
			gray = cv2.cvtColor(self.imagem, cv2.COLOR_BGR2GRAY)
			facesDetectadas = classificador_face.detectMultiScale(gray)
			self.face=facesDetectadas
			facesDetectadas = detectorFace(self.imagem)
			#if len(facesDetectadas)!=0:
			#    gpio.output(18,gpio.HIGH)
			#else:
			#    gpio.output(18,gpio.LOW)
			self.nome = ' '
			for face in facesDetectadas:
				pontosFaciais = detectorPontos(self.imagem, face)
				descritorFacial = reconhecimentoFacial.compute_face_descriptor(self.imagem, pontosFaciais)
				listaDescritorFacial = [fd for fd in descritorFacial]
				npArrayDescritorFacial = np.asarray(listaDescritorFacial, dtype=np.float64)
				npArrayDescritorFacial = npArrayDescritorFacial[np.newaxis, :]
				distancias = np.linalg.norm(npArrayDescritorFacial - descritoresFaciais, axis=1)
				minimo = np.argmin(distancias)
				distanciaMinima = distancias[minimo]
				if distanciaMinima <= limiar:
					self.nome = os.path.split(indices[minimo])[1].split("_")[0]
					self.dicionario[self.nome]=[str(self.nome),str(data.day),str(data.month),str(data.year),str(data.hour),str(data.minute)]
					if self.dicionario[self.nome] not in self.registro:
						self.registro.append(self.dicionario[self.nome])
				else:
					self.nome = ' '
			print(self.nome)
			if cv2.waitKey(1) == ord("q"):
				self.stopped = True


	def stop(self):
		self.stopped = True

