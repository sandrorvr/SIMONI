# -*- coding: utf-8 -*-
import cv2
import os


#VERIRIFICA SE UMA PESSOA COM O MESMO NOME CADASTRADO
def verificacao(nome):
    chave=1
    cadastrados= open('recursos/cadastrados.txt','r')
    arquivo=cadastrados.readlines()
    cadastrados.close()
    for linha in arquivo:
        if nome!=linha:
            chave=1
        else:
            chave=0
            
    return chave
#CADASTRA O NOME DA PESSOA A UM BANCO DE DADOS
def cadastrar(nome):
    cadastrar_nome = open('recursos/cadastrados.txt','a')
    cadastrar_nome.write(nome+'\n')
    cadastrar_nome.close()
    

#SALVA CADA FFRAME EM UMA PASTA,PASTA ESTA QUE POSSUI O MESMO NOME DA PESSOA, DENTRO DA PASTRA TREINAMENTO
def salvar(frame,nome,cont):
    img=cv2.resize(frame,(255,255))
    cv2.imwrite('treinamento/'+nome+'_'+str(cont)+'.jpg',img)

def principal():
	aux=0   #VARIAVEL AUXILIAR DO LOOP WHILE
	while aux==0:   #LOOP QUE FORCA A PESSOA A CADASTRAR UM NOME QUE NAO EXISTA NO BANCO DE DADOS
		
		print('Digite sua identificação')
		nome=input()
		aux=verificacao(nome)

	cadastrar(nome) # QUANDO SAI DO LOOP, CADASTRA O NOME NO BANCO DE DADOS

	#PARTE PRINCIPAL
	#INFORMA QUAL UBCAM USAR (0=PADRAO)
	#OS CLASSIFICADORES AMAZENAM OS HAARCASCADE(VIOLA-JONES)
	cap = cv2.VideoCapture(0)
	classificador_face=cv2.CascadeClassifier('recursos/face.xml')
	classificador_olho=cv2.CascadeClassifier('recursos/olho.xml')
	cont=0
	while True:
		conec,frame=cap.read()    #OBTEM INFORMACOES DA WEBCAM
		framecinza=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   #CONVERTE DE BGR PARA CIMZA
		face=classificador_face.detectMultiScale(framecinza) #DETECTA A FACE
		for (x,y,l,h) in face:
		    mascara=framecinza[y:y+h,x:x+l]     #CRIA UMA MASCACARA DE CORTE COM LOCALIZACAO DA FACE
		    olho=classificador_olho.detectMultiScale(mascara,scaleFactor=1.1)       #DETECTA OS OLHOS DENTRO DA MASCARA
		    if len(olho)!=0:                                                        #SE FOI POSSIVEL DETECTAR OLHOS DENTRO DA FACE ENTAO E FACE.GARANTE QUE A FACE E UMA FACE
		        cv2.rectangle(frame,(x,y),(x+l,y+h),(255,0,0),2)
		        salvar(frame[y:y+h,x:x+l],nome,cont)                                #SALVA A FACE NO BANCO DE DADOS
		cv2.imshow('video',frame)
		cont=cont+1
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

principal()
