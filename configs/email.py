import smtplib

class Mail:

    #Email Alert
    def __init__(self):
        self.EMAIL = ""
        self.PASS = ""
        self.PORT = 465
        self.server = smtplib.SMTP_SSL('*@gmail.com', self.PORT)

    def send(self, mail):
        self.server = smtplib.SMTP_SSL('*@gmail.com', self.PORT)
        self.server.login(self.EMAIL, self.PASS)
        # message to be sent
        SUBJECT = 'ALERT!'
        TEXT = f'Social distancing rule violated!'
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

        # sending the mail
        self.server.sendmail(self.EMAIL, mail, message)
        self.server.quit()