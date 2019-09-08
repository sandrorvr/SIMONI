import cv2
import dlib
import numpy as np
import os
import datetime
import csv
import datetime
import smtplib

def eviar_email(texto):
	eemail = 'projetosimoni@gmail.com'
	ssenha = 'ivetesangalo'

	data = datetime.datetime.now()
	assunto = str(data.day)+'-'+str(data.month)+'-'+str(data.year)+'-'+str(data.hour)

	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpObj.ehlo()
	smtpObj.starttls()

	smtpObj.login(e, s)

	conteudo = texto

	smtpObj.sendmail(eemail, eemail,'Subject:'+assunto+'.\n'+conteudo)

	smtpObj.quit()



def gravar(registrados):
	data = datetime.datetime.now()
	arquivo = open('registros/regsitro '+str(data.day)+'_'+str(data.month)+'.csv','a')
	escrever = csv.writer(arquivo)
	if 'regsitro '+str(data.day)+'_'+str(data.month)+'.csv' not in os.listdir('./registros'):
		escrever.writerow(['id','ano','mes','dia','hora','minuto'])
	for pessoa in registrados:
		escrever.writerow(pessoa)
	arquivo.close()


Detectado=0
nome=None
registro=[]
dicionario={}


detectorFace = dlib.get_frontal_face_detector()
detectorPontos = dlib.shape_predictor("recursos/shape_predictor_68_face_landmarks.dat")
reconhecimentoFacial = dlib.face_recognition_model_v1("recursos/dlib_face_recognition_resnet_model_v1.dat")
indices = np.load("recursos/indices_rn.pickle")
descritoresFaciais = np.load("recursos/descritores_rn.npy")
limiar = 0.5

video = cv2.VideoCapture(0)
while 1:
	_, frame =video.read()

	#classificador_face = cv2.CascadeClassifier('recursos/face.xml')   #metodo haarcascade
	
	data = datetime.datetime.now()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#facesDetectadas = classificador_face.detectMultiScale(gray)       #lista de vetores, cada vetor = 4 pontos retangulo
	#faces=facesDetectadas
	facesDetectadas = detectorFace(frame)
	if not len(facesDetectadas)>=1:
		Detectado=0
	
	nome = ' '
	for face in facesDetectadas:
		
		if Detectado>1:
			continue
		else:
			e, t, d, b = (int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))
			pontosFaciais = detectorPontos(frame, face)
			descritorFacial = reconhecimentoFacial.compute_face_descriptor(frame, pontosFaciais)
			listaDescritorFacial = [fd for fd in descritorFacial]
			npArrayDescritorFacial = np.asarray(listaDescritorFacial, dtype=np.float64)
			npArrayDescritorFacial = npArrayDescritorFacial[np.newaxis, :]
			distancias = np.linalg.norm(npArrayDescritorFacial - descritoresFaciais, axis=1)
			minimo = np.argmin(distancias)
			distanciaMinima = distancias[minimo]
			if distanciaMinima <= limiar:
				nome = os.path.split(indices[minimo])[1].split("_")[0]
				dicionario[nome]=[str(nome),str(data.day),str(data.month),str(data.year),str(data.hour),str(data.minute)]
				if dicionario[nome] not in registro:
					registro.append(dicionario[nome])

				Detectado=Detectado+1

			else:
				nome = ' '
			cv2.rectangle(frame, (e, t), (d, b), (0, 255, 255), 2)
			cv2.putText(frame, nome, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0),2,cv2.LINE_AA)


	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video.release()
cv2.destroyAllWindows()

gravar(registro)