import smtplib
import getpass
import time
import email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
c=canvas.Canvas("documento.pdf", pagesize=letter)
c.setFont("Times-Roman",12)
c.setLineWidth(.3)
c.drawString(30,750,'Solicitud de Presupuesto')
c.drawString(30, 735, 'DATOS PROPORCIONADOS POR EL USUARIO')
c.drawString(30, 750, 'Solicitud de Presupuesto')
c.drawString(500,750,'fecha de hoy')
c.line(480,747,580,747)
c.showPage()
c.save()
time.sleep(1)
destinatario= 'capibaraportesymudanzas@gmail.com'
remitente = 'capibaraportesymudanzas@gmail.com'
password = 'jacko1234@'
asunto='Nueva solicitud de presupuesto'
nombre_adjunto='Solicitud'
mensaje=MIMEMultipart()
mensaje['to']=destinatario
mensaje['asunto']=asunto

mensaje.attach(MIMEText(cuerpo,'plain'))
archivo_adjunto=open(ruta_adjunto,'rb')
adjunto_MIME=MIMEbase('application','octet-stream')
adjunto_MIME.set_payload((archivo_adjunto).read())
encoders.encode_base64(adjunto_MIME)
adjunto_MIME.add_hearder('content-disposition',"attachment;filename=%s"% nombre_adjunto)
mensaje.attach(adjunto_MIME)
sesion_smtp=smtplib.SMTP('smtp.gmail.com',587)
sesion_smtp.starttls()
sesion_smtp.login(remitente,password)
texto=mensaje.as_string()
sesion_smtp.sendmail(remitente,destinatario)
