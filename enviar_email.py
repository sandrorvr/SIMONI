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
