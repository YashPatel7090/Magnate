import ctypes
import os
import math
import csv
import sqlite3
import smtplib
import hashlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
C = ctypes.CDLL('services/C_Functions/c_functions.so')


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hashed_password = hashlib.sha256(password.encode('ascii')).hexdigest()
        self.hashed_email_url = hashlib.sha256(email.encode('ascii')).hexdigest()
    
    def is_verified(self):
        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command = "SELECT COUNT(*) FROM verified WHERE email = '{}'".format(self.email)

        db.execute(sql_command)
        data = db.fetchall()
        connection.close()

        One_or_Zero = data[0][0]

        if One_or_Zero == 0:
            return False
        else:
            return True
    
    def is_unverified(self):
        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command = "SELECT COUNT(*) FROM unverified WHERE email = '{}'".format(self.email)

        db.execute(sql_command)
        data = db.fetchall()
        connection.close()

        One_or_Zero = data[0][0]

        if One_or_Zero == 0:
            return False
        else:
            return True

    def send_verification_email(self):
        PERSONAL_EMAIL = os.environ.get('PERSONAL_EMAIL')
        PERSONAL_PASSWORD = os.environ.get('PERSONAL_PASSWORD')

        plain_text = open('services/email_files/plaintext_email', 'r').read().replace('(username)', self.username).replace(
        '(url)', self.hashed_email_url)
        html_text = open('services/email_files/htmltext_email.html', 'r').read().replace('(username)', self.username).replace(
        '(url)', self.hashed_email_url)
    
        verification_email = MIMEMultipart('alternative')
        verification_email['Subject'] = 'Magnate: Verify Account'
        verification_email['From'] = PERSONAL_EMAIL
        verification_email['To'] = self.email
        verification_email.attach(MIMEText(plain_text, 'plain'))
        verification_email.attach(MIMEText(html_text, 'html'))
    
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(PERSONAL_EMAIL, PERSONAL_PASSWORD)
            server.sendmail(PERSONAL_EMAIL, self.email, verification_email.as_string())
            server.quit()
            sent_or_error = True
        except:
            sent_or_error = False

        if sent_or_error == True:
            connection = sqlite3.connect('services/databases/magnate.db')
            db = connection.cursor()

            sql_command = '''INSERT INTO unverified 
            (username, email, hashed_password, hashed_email_url) 
            VALUES ('{}', '{}', '{}', '{}');'''.format(self.username, self.email, self.hashed_password, 
            self.hashed_email_url).replace('\n', '').replace('            ', '')
    
            db.execute(sql_command)
            connection.commit()
            connection.close()

            return True
        else:
            return False

    def secure_login(self):
        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command = '''SELECT COUNT(*) FROM verified 
        WHERE username = '{}' AND email = '{}' AND 
        hashed_password = '{}';'''.format(self.username, self.email, self.hashed_password).replace(
        '\n', '').replace('        ', '')

        db.execute(sql_command)
        data = db.fetchall()
        connection.close()

        secure_or_insecure = data[0][0]

        if secure_or_insecure == 0:
            return False
        else:
            return True

    def update_data(self, name, value):
        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command = "SELECT user_id FROM verified WHERE email = '{}';".format(self.email)

        db.execute(sql_command)
        data = db.fetchall()
        connection.close()

        userid = data[0][0]

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command = "UPDATE data SET {} = '{}' WHERE userid = '{}';".format(name, value, userid)

        try:
            db.execute(sql_command)
            connection.commit()
        except:
            connection.close()
            return False
        
        connection.close()

        return True

    def extract_data(self):
        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command = "SELECT user_id FROM verified WHERE email = '{}';".format(self.email)

        db.execute(sql_command)
        data = db.fetchall()
        connection.close()

        userid = data[0][0]

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command = "SELECT name FROM PRAGMA_TABLE_INFO('data');"

        db.execute(sql_command)
        data_2 = db.fetchall()
        connection.close()

        lis = []
        for row in data_2:
            lis.append(row[0])
        lis.remove('userid')

        length = len(lis)
        column_names = ''
        for i in range(length):
            if i == length - 1:
                column_names = column_names + lis[i]
            else:
                column_names = column_names + lis[i] + ', '

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command = "SELECT {} FROM data WHERE userid = '{}';".format(column_names, userid)

        db.execute(sql_command)
        data_3 = db.fetchall()
        connection.close()

        user_data = {}
        for x in range(length):
            user_data[f'{lis[x]}'] = data_3[0][x]

        return user_data

    @classmethod
    def url_is_unverified(cls, url):
        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command = '''SELECT COUNT(*) FROM unverified WHERE 
        hashed_email_url = '{}';'''.format(url).replace('\n', '').replace('        ', '')

        db.execute(sql_command)
        data = db.fetchall()
        connection.close()

        true_or_false = data[0][0]

        if true_or_false == 0:
            return False
        else:
            return True

    @classmethod
    def verify_user(cls, url):
        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command_1 = '''SELECT username, email, hashed_password, hashed_email_url 
        FROM unverified WHERE hashed_email_url = '{}';'''.format(url).replace('\n', '').replace('        ', '')

        db.execute(sql_command_1)
        data = db.fetchall()
        connection.close()

        username = data[0][0]
        email = data[0][1]
        hashed_password = data[0][2]
        hashed_email_url = data[0][3]

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command_2 = '''INSERT INTO verified 
        (username, email, hashed_password, hashed_email_url) 
        VALUES ('{}', '{}', '{}', '{}');'''.format(username, email, hashed_password, hashed_email_url).replace(
        '\n', '').replace('        ', '')

        db.execute(sql_command_2)
        connection.commit()
        connection.close()

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command_3 = "SELECT user_id FROM verified WHERE email = '{}';".format(email)

        db.execute(sql_command_3)
        data_2 = db.fetchall()
        connection.close()

        userid = data_2[0][0]

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command_4 = '''INSERT INTO data 
        (userid, username, email) 
        VALUES ('{}', '{}', '{}');'''.format(userid, username, email).replace(
        '\n', '').replace('        ', '')

        db.execute(sql_command_4)
        connection.commit()
        connection.close()

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command_5 = '''DELETE FROM unverified 
        WHERE hashed_email_url = '{}';'''.format(url).replace('\n', '').replace('        ', '')

        db.execute(sql_command_5)
        connection.commit()
        connection.close()

        return

    @classmethod
    def reset_database(cls):
        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()
        sql_command = ('''DROP TABLE IF EXISTS 
        verified;'''.replace('\n', '')).replace('        ', '')
        print(sql_command)
        db.execute(sql_command)
        connection.commit()
        connection.close()

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()
        sql_command = ('''DROP TABLE IF EXISTS 
        unverified;'''.replace('\n', '')).replace('        ', '')
        print(sql_command)
        db.execute(sql_command)
        connection.commit()
        connection.close()

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()
        sql_command = ('''DROP TABLE IF EXISTS 
        data;'''.replace('\n', '')).replace('        ', '')
        print(sql_command)
        db.execute(sql_command)
        connection.commit()
        connection.close()

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()
        sql_command = ('''CREATE TABLE verified 
        (user_id INTEGER PRIMARY KEY, 
        username VARCHAR(1000), 
        email VARCHAR(1000), 
        hashed_password VARCHAR(1000), 
        hashed_email_url VARCHAR(1000));'''.replace('\n', '')).replace('        ', '')
        print(sql_command)
        db.execute(sql_command)
        connection.commit()
        connection.close()

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()
        sql_command = ('''CREATE TABLE unverified 
        (id INTEGER PRIMARY KEY, 
        username VARCHAR(1000), 
        email VARCHAR(1000), 
        hashed_password VARCHAR(1000), 
        hashed_email_url VARCHAR(1000));'''.replace('\n', '')).replace('        ', '')
        print(sql_command)
        db.execute(sql_command)
        connection.commit()
        connection.close()

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()
        sql_command = ('''CREATE TABLE data 
        (userid INTEGER, 
        username VARCHAR(1000), 
        email VARCHAR(1000), 
        FOREIGN KEY(userid) REFERENCES verified(user_id));'''.replace('\n', '')).replace('        ', '')
        print(sql_command)
        db.execute(sql_command)
        connection.commit()
        connection.close()

        return

    @classmethod
    def add_data(cls, name, datatype, confirm):
        if confirm != True:
            return

        connection = sqlite3.connect('services/databases/magnate.db')
        db = connection.cursor()

        sql_command = '''ALTER TABLE data 
        ADD COLUMN {} {};'''.format(name, datatype).replace('\n', '').replace('        ', '')

        try:
            db.execute(sql_command)
            connection.commit()
        except:
            print('Error executing add_data')
        finally:
            connection.close()

        return


def main():
    pass


if __name__ == "__main__":
    main()

