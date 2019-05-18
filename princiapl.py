#import RPi.GPIO as gpio
from videoget import VideoGet
from processos import processamento
from videoshow import VideoShow

def threadBoth(source=0):

    #gpio.setmode(gpio.BCM)
    #gpio.setup(18,gpio.OUT)
    video_getter = VideoGet(source).start()
    deteccao = processamento(video_getter.frame).start()
    video_shower = VideoShow(deteccao.nome,deteccao.face,video_getter.frame).start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            deteccao.stop()
            break
        frame = video_getter.frame
        deteccao.imagem = frame
        video_shower.frame = frame
        video_shower.fila=deteccao.face
        video_shower.nome = deteccao.nome
    #gpio.cleanup()
    #print(deteccao.registro)
    deteccao.gravar()


threadBoth(0)
