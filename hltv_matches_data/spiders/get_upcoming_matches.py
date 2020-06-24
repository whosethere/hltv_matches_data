import scrapy

from matches_data.items import Upcoming_Matches_Data
from scrapy.loader import ItemLoader
import time
from datetime import *
from matches_data.mongo_connection import get_connection, match_in_database

class GetUpcomingMatchesSpider(scrapy.Spider):
    name = 'get_upcoming_matches'
    allowed_domains = ['hltv.org']
    start_urls = ['https://www.hltv.org/matches']

    def parse(self, response):

        upcoming_matches = response.xpath('//div[@class="match-day"]')[:3]
        base_url = 'http://hltv.org'
        
        for match_day in upcoming_matches: 
            match_day = match_day.xpath('./div[@class="upcoming-match standard-box"]') 
            for match  in match_day: 
                match_link = match.xpath('./div/a/@href')[0].extract()
                match_link = base_url +  str(match_link)
                if match_in_database(match_link):
                    continue
                yield scrapy.Request(match_link,
                                        callback=self.parse_matches_data,
                                        meta={'match_link':match_link})
                pass

    def parse_matches_data(self, response):

        def get_id(link, pozycja):
            link = str(link)
            link = link.split("/")
            _id = link[pozycja]
            _id = int(_id)
            return _id
        
        match_link = response.meta['match_link']
        match_id = int(match_link.split("/")[4])
        match_date_time = response.xpath('//div[@class="time"]/@data-unix').extract_first()
        match_unix_time = int(match_date_time) / 1000
        match_date_time = int(match_date_time) / 1000
        match_date_time = datetime.fromtimestamp(match_date_time)
        match_date = match_date_time.strftime("%Y-%m-%d")
        match_time = match_date_time.strftime("%H:%M")
        

        match_box = response.xpath('//div[@class="standard-box teamsBox"]')
        teams = match_box.xpath('./div[@class="team"]')
        teams_names = teams.xpath('//div[@class="teamName"]/text()').extract()
        home_team_link = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/a/@href').extract_first()
        away_team_link = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/a/@href').extract_first()
        
        home_team_name = teams_names[0]
        home_team_id = "get it yrself"

        away_team_name = teams_names[1]
        away_team_id = "get it yrself"

        players = response.xpath('//td[@class="player player-image"]')

        ht_p1_id = players[0].xpath('./div/@data-player-id').extract_first()
        ht_p2_id = players[1].xpath('./div/@data-player-id').extract_first()
        ht_p3_id = players[2].xpath('./div/@data-player-id').extract_first()
        ht_p4_id = players[3].xpath('./div/@data-player-id').extract_first()
        ht_p5_id = players[4].xpath('./div/@data-player-id').extract_first()
        at_p1_id = players[5].xpath('./div/@data-player-id').extract_first()
        at_p2_id = players[6].xpath('./div/@data-player-id').extract_first()
        at_p3_id = players[7].xpath('./div/@data-player-id').extract_first()
        at_p4_id = players[8].xpath('./div/@data-player-id').extract_first()
        at_p5_id = players[9].xpath('./div/@data-player-id').extract_first()
        
        players_nicks = response.xpath('//td[@class="player"]')
        
        ht_p1_nick = players_nicks[0].xpath('./div/div/text()')[0].extract()
        ht_p2_nick = players_nicks[1].xpath('./div/div/text()')[0].extract()
        ht_p3_nick = players_nicks[2].xpath('./div/div/text()')[0].extract()
        ht_p4_nick = players_nicks[3].xpath('./div/div/text()')[0].extract()
        ht_p5_nick = players_nicks[4].xpath('./div/div/text()')[0].extract()
        at_p1_nick = players_nicks[5].xpath('./div/div/text()')[0].extract()
        at_p2_nick = players_nicks[6].xpath('./div/div/text()')[0].extract()
        at_p3_nick = players_nicks[7].xpath('./div/div/text()')[0].extract()
        at_p4_nick = players_nicks[8].xpath('./div/div/text()')[0].extract()
        at_p5_nick = players_nicks[9].xpath('./div/div/text()')[0].extract()
        

        

        ht_p1_link = "https://www.hltv.org/player/" + str(ht_p1_id) + "/" + str(ht_p1_nick)
        ht_p2_link = "https://www.hltv.org/player/" + str(ht_p2_id) + "/" + str(ht_p2_nick)
        ht_p3_link = "https://www.hltv.org/player/" + str(ht_p3_id) + "/" + str(ht_p3_nick)
        ht_p4_link = "https://www.hltv.org/player/" + str(ht_p4_id) + "/" + str(ht_p4_nick)
        ht_p5_link = "https://www.hltv.org/player/" + str(ht_p5_id) + "/" + str(ht_p5_nick)
        at_p1_link = "https://www.hltv.org/player/" + str(at_p1_id) + "/" + str(at_p1_nick)
        at_p2_link = "https://www.hltv.org/player/" + str(at_p2_id) + "/" + str(at_p2_nick)
        at_p3_link = "https://www.hltv.org/player/" + str(at_p3_id) + "/" + str(at_p3_nick)
        at_p4_link = "https://www.hltv.org/player/" + str(at_p4_id) + "/" + str(at_p4_nick)
        at_p5_link = "https://www.hltv.org/player/" + str(at_p5_id) + "/" + str(at_p5_nick)
        


        loader = ItemLoader(item=Upcoming_Matches_Data(), response=response)
        loader.add_value('home_team_id', home_team_id)
        loader.add_value('away_team_id', away_team_id)
        loader.add_value('ht_p1_link',ht_p1_link)
        loader.add_value('ht_p2_link',ht_p2_link)
        loader.add_value('ht_p3_link',ht_p3_link)
        loader.add_value('ht_p4_link',ht_p4_link)
        loader.add_value('ht_p5_link',ht_p5_link)
        loader.add_value('at_p1_link',at_p1_link)
        loader.add_value('at_p2_link',at_p2_link)
        loader.add_value('at_p3_link',at_p3_link)
        loader.add_value('at_p4_link',at_p4_link)
        loader.add_value('at_p5_link',at_p5_link)
        loader.add_value('ht_p1_id',ht_p1_id)
        loader.add_value('ht_p2_id',ht_p2_id)
        loader.add_value('ht_p3_id',ht_p3_id)
        loader.add_value('ht_p4_id',ht_p4_id)
        loader.add_value('ht_p5_id',ht_p5_id)
        loader.add_value('at_p1_id',at_p1_id)
        loader.add_value('at_p2_id',at_p2_id)
        loader.add_value('at_p3_id',at_p3_id)
        loader.add_value('at_p4_id',at_p4_id)
        loader.add_value('at_p5_id',at_p5_id)
        loader.add_value('match_link',match_link)
        loader.add_value('match_id',match_id)
        loader.add_value('match_unix_time',match_unix_time)
        loader.add_value('match_date',match_date)
        loader.add_value('match_time',match_time)

        yield loader.load_item()
