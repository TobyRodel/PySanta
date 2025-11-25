import numpy as np
import pandas as pd
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from argparse import ArgumentParser

def defaulttext(name, giftee, hint):
    """Default email text generator

    Args:
        name (str): Name of email recipient (NOT EMAIL ADDRESS)
        giftee (str): Name of assigned giftee
        hint (str): Hint message (ASCII only)

    Returns:
        str: body text of email message
    """    
    line1 = f'Seasons greetings {name}'
    line2 = f'You are {giftee}\'s secret santa!'
    line3 = f'Struggling for ideas? They have left this hint:'
    line4 = f'Love Santa x'
    return line1 + '\n' + line2 + '\n' + line3 + '\n' + hint + '\n' + line4

def sendemail(TO,FROM,PWD,name,giftee,hint,subject='Secret Santa',bodytext=defaulttext):
    """_summary_

    Args:
        TO (str): Email address of message recipient.
        FROM (str): Email address of sender.
        PWD (str): Password of email sender.
        name (str): Name of email recipient (NOT EMAIL ADDRESS)
        giftee (str): Name of assigned giftee
        hint (str): Hint message (ASCII only)
        subject (str, optional): Subject line. Defaults to 'Secret Santa'.
        bodytext (function, optional): body text generator function, must take (name, giftee, hint) as positional arguments. Defaults to defaulttext.
    """    
    body = (bodytext(name, giftee, hint))
    msg = MIMEMultipart()
    msg['To'] = TO
    msg['From'] = FROM
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    msgtext = msg.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(FROM, PWD)
        server.sendmail(FROM, TO, msgtext)

class Santas:
    """Main class
    """    
    def __init__(self, index=None, names=None, hints=None, emails=None, assigned=None, account=None, password=None):
        """Initialise class

        Args:
            index (array_like, optional): Indexes of data. Defaults to None.
            names (array_like, optional): Names of participants. Defaults to None.
            hints (array_like, optional): Hint messages. Defaults to None.
            emails (array_like, optional): Email addresses of participants. Defaults to None.
            assigned (array_like, optional): Assigned giftee index. Defaults to None.
            account (str, optional): Email address to send emails from. Defaults to None.
            password (str, optional): Password of email account. Defaults to None.
        """        
        self.ids = index
        self.names = names
        self.hints = hints
        self.emails = emails
        self.assigned = assigned
        self.account = account
        self.password = password
    def createidx(self):
        """Creates index array based off names
        """        
        self.ids = np.arange(len(self.names))
    def assignpairs(self, generator, maxiters=1000):
        """Reshuffles index array, ensuring no element remains in the same place.

        Args:
            generator (numpy.random.Generator): numpy rng generator class
        """        
        nomatch = False
        iters = 0
        while (nomatch == False) and (iters<=maxiters):
            assigned = generator.shuffle(self.ids)
            iters += 1
            if np.count_nonzero(self.ids==assigned) > 0:
                nomatch == True
        self.assigned = assigned
    def createspoilerdf(self, path='spoilers.csv'):
        """Creates spoiler table of assignees

        Args:
            path (str, optional): path to save file. Defaults to 'spoilers.csv'.

        Returns:
            pandas.DataFrame: Dataframe object containing spoiler information
        """        
        spoilers = pd.DataFrame({'Name':self.names, 'Assigned':self.names[self.assigned]})
        spoilers.to_csv(path, index=None)
        return spoilers
    def sendemails(self, subject='Secret Santa', bodytext=defaulttext):
        """Sends assignee emails

        Args:
            subject (str, optional): Subject line. Defaults to 'Secret Santa'.
            bodytext (function, optional): body text generator function, must take (name, giftee, hint) as positional arguments.. Defaults to defaulttext.
        """        
        if self.account is None:
            self.account = input('Email address:')
        if self.password is None:
            self.password = input('Password:')
        for i in self.ids:
            try:
                sendemail(TO=self.emails[i], FROM=self.account, PWD=self.password, name=self.names[i], giftee=self.names[self.assigned[i]], hint=self.hints[self.assigned[i]], subject=subject, bodytext=bodytext)
            except Exception as e:
                print(f'Error: {e}\nSkipping')
                continue

parser = ArgumentParser(prog='PySanta', description='A Python module for organising secret Santa gift exchanges.')
parser.add_argument('-f', '--inputfile', type=str, help='Path to csv file containing participant info')
parser.add_argument('-u', '--username', type=str, help='Email address to send emails from', default=None)
parser.add_argument('-p', '--password', type=str, help='Email account password (app password for gmail)', default=None)
parser.add_argument('-o', '--spoilerfile', type=str, default='spoilers.csv', help='Path to output spoiler file, defaults to current directory.')
args = parser.parse_args()

gen = np.random.default_rng()

df = pd.read_csv(args['inputfile'])
santas = Santas(names=df['name'], emails=df['email'], hints=df['hint'], account=args['username'], password=args['password'])
santas.createidx()
santas.assignpairs()
santas.createspoilerdf(path=args['spoilerfile'])
santas.sendemails()
