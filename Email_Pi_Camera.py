import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#label_rec --> is label_pred
#confid    --> is conf
#face      --> face (image taken by camera)
#flag      --> flag = 1 is if label_pred == label_real
#          --> flag = 2 is if label_pred != label_real
def send_email(label_rec, confid, face, flag)
    attachment = face
    msg = MIMEMultipart()
    #Use a gmail account
    msg['Subject'] = 'Face Recognition'
    msg['From'] = 'YOUR_EMAIL@gmail.com'
    msg['To'] = 'SENDER_EMAIL@gmail.com'
    if flag == 1:
        body = '{} is correctly recognized with confidence {}.'.format(label_rec, confid)
        msgText = MIMEText('<b>%s</b><br><img src="cid:%s"><br>' % (body, attachment), 'html')
        msg.attach(msgText)
    elif flag == 2:
        body = 'confidence:', confid, 'label:', label_rec
        msgText = MIMEText('<b>%s</b><br><img src="cid:%s"><br>' % (body, attachment), 'html')
        msg.attach(msgText)
    #Opening picture and attaching to msg
    fp = open(attachment, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    img.add_header('Content-ID', '<{}>'.format(attachment))
    msg.attach(img)
    #Email login
    login        =  'YOUR_LOGIN_USERNAME'
    password     =  'YOUR_PASSWORD'
    from_addr    =  'YOUR_EMAIL@gmail.com'
    to_addr_list = ['SENDER_EMAIL@gmail.com']
    subject      = 'Face Recognition'

    smtpserver='smtp.gmail.com:587'
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    server.sendmail(from_addr, to_addr_list, msg.as_string())
    server.quit()
