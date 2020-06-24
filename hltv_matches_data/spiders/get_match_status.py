# -*- coding: utf-8 -*-
import scrapy
from mysql.connector import (connection)
import time
from datetime import date
import sqlalchemy as db
import pandas as pd

class GetMatchStatusSpider(scrapy.Spider):
    name = 'get_match_status'
    allowed_domains = ['hltv.org']
    start_urls = ['http://hltv.org/']
    

    def parse(self, response):

        def read_todays_matches():
            cnx = connection.MySQLConnection(user='30851648_csgo_prediction', password='csgo_prediction_pass',
                                        host='serwer1968658.home.pl',
                                        database='30851648_csgo_prediction')
            df = pd.read_sql('SELECT * FROM upcoming_matches_prediction', con=cnx)
            return df
        
        def split(df, headSize) :
            hd = df.head(headSize)
            hd = hd.reset_index().drop('index', axis=1)
            tl = df.tail(len(df)-headSize)
            return hd, tl
        
        todays_matches = read_todays_matches()
        while len(todays_matches) >= 1:
            match_to_check, todays_matches  = split(todays_matches, 1)
            match_link = match_to_check['match_link'][0]
        
            yield scrapy.Request(match_link,
                                    callback=self.parse_match_status,
                                    meta={'data_frame':match_to_check,
                                          'match_link': match_link})
            pass

    def parse_match_status(self, response):
        #TODO