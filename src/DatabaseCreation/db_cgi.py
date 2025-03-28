# 23/04/2014
# import time
import sqlite3
from datetime import date, datetime
from xls import XlsControl
# from writer import XlsWriter


class DB_cgi(object):

    def __init__(self):
        # {cgi: [latitude, longitude, morada, local, nome, cp, azimute,
        # tecnologia, data]}
        self.db = sqlite3.connect('cgi.db')
        self.cur = self.db.cursor()
        db = sqlite3.connect("cgi.db")
        cur = db.cursor()
        cur.execute('''
        CREATE TABLE cgi(
            cgi TEXT,
            latitude REAL,
            longitude REAL,
            morada TEXT,
            local TEXT,
            nome TEXT,
            cp TEXT,
            azimute INTEGER,
            tecnologia TEXT,
            date TEXT, 
            PRIMARY KEY (cgi, azimute, date)
            )''') # alterei o data type de date de DATE para TEXT
        

    def update(self, excel_file):
        # [[[1st sheet name][1st row data][2nd row data][...][Nth row data]]]

        # new_data = [tuple(x) for x in XlsReader(excel_file).read_excel()[0]]
        new_data = []
        #print(XlsControl(excel_file).read_excel())
        for x in XlsControl(excel_file).read_excel()[0]:
            #x.append(date.today()) -> comentei esta linha
            new_data.append(tuple(x))
        # new_data[0] - the leave name
        new_data.pop(0)
        # new_data[1] - titles row
        new_data.pop(0)
        # new_data[2:] - value rows
        print(new_data[0])

        self.cur.executemany('''INSERT INTO cgi(cgi, latitude, longitude,
            morada, local, nome, cp, azimute, tecnologia, date) VALUES(?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?)''', new_data)  # falta um IF DOESN'T EXIST
        self.db.commit()

    def search(self, query_list):
        # 2G = 2G, GSM
        # 3G = 3G, UMTS, HSDPA(3,5G)
        # 4G = 4G, LTE, FDD_1
        # query_list será qq coisa como:
        # [cgi, lat, lon, morada, local, nome, cp, azimute, tecnologia, data]
        self.cur.execute('''SELECT * FROM cgi WHERE
                            cgi=? AND
                            latitude=? AND
                            longitude=? AND
                            morada=? AND
                            local=? AND
                            nome=? AND
                            cp=? AND
                            azimute=? AND
                            tecnologia=? AND
                            data=?'''(
            query_list[0], query_list[1], query_list[2], query_list[3],
            query_list[4], query_list[5], query_list[6], query_list[7],
            query_list[8], query_list[9],))
        result = self.cur.fetchall()
        return result

    def export(self, export_file):
        # deve estar ligado ao self.search
        pass

    def close(self):
        self.db.close()
