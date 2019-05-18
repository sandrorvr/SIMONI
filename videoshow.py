from threading import Thread
import cv2
import dlib

class VideoShow:

    def __init__(self, nome, fila, frame=None):
        self.frame = frame
        self.stopped = False
        self.fila = fila
        self.nome = nome

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

#ESTA FUNCAO USA A TECNICA HOG
    '''def show(self):
        while not self.stopped:
            #print(self.fila)
            try:
                for face in self.fila:
                    e, t, d, b = (int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))
                    cv2.rectangle(self.frame, (e, t), (d, b), (0, 255, 255), 2)
            except TypeError:
                print('DEU MERDA NEGAO')
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True'''

    def show(self):
        classificador_olho = cv2.CascadeClassifier('recursos/olho.xml')
        while not self.stopped:
            #print(self.fila)
            try:
                for (x,y,l,h) in self.fila:
                    mascara=self.frame[y:y+h,x:x+l]
                    olho = classificador_olho.detectMultiScale(mascara)
                    if len(olho)!=0:
                        cv2.rectangle(self.frame,(x,y),(x+l,y+h),(255,0,0),2)
            except TypeError:
                print('BOTA A CARA NEGAO')
            cv2.putText(self.frame, self.nome, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0),2,cv2.LINE_AA)
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True


    def stop(self):
        self.stopped = True


