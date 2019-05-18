from tkinter import*
from functools import partial
import cv2
from threading import Thread
from queue import Queue
import os
import numpy as np

def monitorar():
    #CRIA O ARQUIVO ROTULO.TXT COM O ENDERECO DA IMAGEM E UM ROTULO(QUEM A FOTO REPRESENTA) SEPARADOS POR PONTO E VIRGULA      
    def rotular():
        label=0
        rotulo=open('C:\\Users\\sandro\\Documents\\Python Scripts\\reconhecimento_face\\rotulo.txt','w')
        path='C:\\Users\\sandro\\Documents\\Python Scripts\\reconhecimento_face\\treinamento'
        for pdir,subdir,arq in os.walk(path):
            for name in arq:
                rotulo.write(pdir+'\\'+name+';'+str(label)+'\n')
            label=label+1
        rotulo.close()
    
    #ENTRA O ARQUIVO COM OS ENDERECOS DAS IMAGENS E OS ROTULOS E RETORNA DOS VETORES UM CONTENDO TODAS AS FACES E OUTRO CONTENDO TODOS OS ROTULOS 
    def agrupar(arquivo):
        fotos_label=arquivo.readlines()
        arquivo.close()
        face=[]
        chave=[]
        for linha in fotos_label:
            foto,label = linha.rstrip().split(';')
            face.append(cv2.imread(foto,0))
            chave.append(int(label))
        return face, chave
    
    #TREINA A BASE DE FOTOS, POSSUI COMO PARAMETROS UM VETOS CONTENDO DAS AS FACES E OUTRO VETOR CONTENDO OS RECTIVOS ROTULOS
    def treinamento(face,label):
        model = cv2.face.createLBPHFaceRecognizer()
        model.train(face, np.array(label))
        return model
    
    # FAZ A CLASSIFICACAO EM TEMPO REAL, DISCIMINA A PESSOA QUE ESTA EM VIDEO
    def aovivo(model):
        video= cv2.VideoCapture(0)
        classificador_face=cv2.CascadeClassifier('C:\\Users\\sandro\\Documents\\Python Scripts\\detector\\cascades\\haarcascade_frontalface_default.xml')
        classificador_olho=cv2.CascadeClassifier('C:\\Users\\sandro\\Documents\\Python Scripts\\detector\\cascades\\haarcascade_eye.xml')
        path='C:\\Users\\sandro\\Documents\\Python Scripts\\reconhecimento_face\\treinamento'
        identificacao=os.listdir(path)                                                          #PESSOAS CADASTRADAS NO BANCO DE DADOS
        while True:
            conec,frame=video.read()
            framecinza=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            face=classificador_face.detectMultiScale(framecinza)
            for (x,y,l,h) in face:
                mascara=framecinza[y:y+h,x:x+l]
                olho=classificador_olho.detectMultiScale(mascara,scaleFactor=1.1)
                if len(olho)!=0:
                    mascara=cv2.resize(mascara,(255,255))                                       #REDIMENSIONA A IMAGEM PARA PODER COMPARAR COM O MODELO GERADO 
                    
                    label = modelo.predict(mascara)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    print(label)
                    for i in range(len(identificacao)):
                        if (label-1)==i:
                            cv2.putText(frame,identificacao[i],(x - 20,y + h+30), font, 1,(255,0,0),1,cv2.LINE_AA)
                            cv2.rectangle(frame,(x,y),(x+l,y+h),(255,0,0),2)
                    
                cv2.imshow('video',frame)
            #print(len(q.queue))
            if cv2.waitKey(1)==ord('q') or len(q.queue)!=0:
            	break
        video.release()
        cv2.destroyAllWindows()
    
    rotular()
    rotulos=open('C:\\Users\\sandro\\Documents\\Python Scripts\\reconhecimento_face\\rotulo.txt','r')
    face,chave=agrupar(rotulos)
    modelo=treinamento(face,chave)
    aovivo(modelo)

def armazenar(): 
    q.put(caixa.get())      #ARMAZENA NA POSICAO 0 DA FILA
    q.put(caixanumero.get())
    os.chdir('C:\\Users\\sandro\\Documents\\Python Scripts\\reconhecimento_face')
    
    #VERIRIFICA SE UMA PESSOA COM O MESMO NOME CADASTRADO
    def verificacao(nome):
        chave=1
        cadastrados= open('cadastrados.txt','r')
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
        cadastrar_nome = open('cadastrados.txt','a')
        cadastrar_nome.write(nome+'\n')
        cadastrar_nome.close()
        
    
    #SALVA CADA FFRAME EM UMA PASTA,PASTA ESTA QUE POSSUI O MESMO NOME DA PESSOA, DENTRO DA PASTRA TREINAMENTO
    def salvar(frame,nome,cont):
        try:
            os.chdir('C:\\Users\\sandro\\Documents\\Python Scripts\\reconhecimento_face\\treinamento\\'+nome)
        except FileNotFoundError:
            os.mkdir('C:\\Users\\sandro\\Documents\\Python Scripts\\reconhecimento_face\\treinamento\\'+nome)
            os.chdir('C:\\Users\\sandro\\Documents\\Python Scripts\\reconhecimento_face\\treinamento\\'+nome)
        img=cv2.resize(frame,(255,255))
        cv2.imwrite(nome+str(cont)+'.jpg',img)
    
    aux=0   #VARIAVEL AUXILIAR DO LOOP WHILE
    while aux==0:   #LOOP QUE FORCA A PESSOA A CADASTRAR UM NOME QUE NAO EXISTA NO BANCO DE DADOS
        nome=q.get()
        aux=verificacao(nome)
    
    cadastrar(nome) # QUANDO SAI DO LOOP, CADASTRA O NOME NO BANCO DE DADOS
    ncadastrados=int(q.get())
    #PARTE PRINCIPAL
    #INFORMA QUAL UBCAM USAR (0=PADRAO)
    #OS CLASSIFICADORES AMAZENAM OS HAARCASCADE(VIOLA-JONES)
    video= cv2.VideoCapture(0)
    classificador_face=cv2.CascadeClassifier('C:\\Users\\sandro\\Documents\\Python Scripts\\detector\\cascades\\haarcascade_frontalface_default.xml')
    classificador_olho=cv2.CascadeClassifier('C:\\Users\\sandro\\Documents\\Python Scripts\\detector\\cascades\\haarcascade_eye.xml')
    cont=0
    while True:
        conec,frame=video.read()    #OBTEM INFORMACOES DA WEBCAM
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
        if cv2.waitKey(1)==ord('q') or len(q.queue)>ncadastrados:
            break
    video.release()
    cv2.destroyAllWindows()
    

def startthread():
    thread=Thread(target=armazenar)
    thread.start()

def startthread1():
    thread=Thread(target=monitorar)
    thread.start()

def fecharvideo():
    q.put('q')

q=Queue()      #CRIMA UMA FILA PARA COMUNICAR UMA THREAD COM OUTRA
janela=Tk()
janela.title('HOME')

label=Label(janela,text='Escreva sua identificacao')
label.grid(row=0, column=1)

label=Label(janela,text='Numero de cadastros')
label.grid(row=0, column=2)

caixa=Entry(janela, width=30)
caixa.grid(row=1, column=1)

caixanumero=Entry(janela, width=10)
caixanumero.grid(row=1, column=2)

btcadastro=Button(janela,width=20,text='CADASTRAR',command=startthread)
#btcadastro['command']=partial(startthread,armazenar)
btcadastro.grid(row=3, column=1)

btfechar=Button(janela,width=20,text='FECHAR CADASTRO',command=fecharvideo)
btfechar.grid(row=4, column=1)

btmonitorar=Button(janela,width=20,text='MONITORAR',command=startthread1)
btmonitorar.grid(row=3, column=2)

btfechar=Button(janela,width=20,text='FECHAR MONITOR',command=fecharvideo)
btfechar.grid(row=4, column=2)

janela.geometry('370x120')

janela.mainloop()