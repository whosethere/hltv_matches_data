# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
from datetime import timedelta
from scrapy.loader import ItemLoader
from matches_data.items import Matches_Results

class GetResultsSpider(scrapy.Spider):
    name = 'get_results'
    allowed_domains = ['hltv.org']
    start_urls = ['https://www.hltv.org/results?startDate=2019-08-25&endDate=2019-11-21']

    def parse(self, response):
        links_grid = response.xpath('//div[@class="results-holder"]')
        matches_links = links_grid.xpath('//div[@class="result-con"]')
        link_to_match = matches_links.xpath('./a/@href').extract()
        for match_link in link_to_match:
            caly = 'http://hltv.org' + str(match_link)
            yield scrapy.Request(caly,
                                 callback = self.parse_listing,
                                 meta = {'match_link':match_link})


        next_page =  response.xpath('//a[@class="pagination-next"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback = self.parse)


    def parse_listing(self, response):

        def get_id(link, pozycja):
            link = str(link)
            link = link.split("/")
            id = link[pozycja]
            return id

        def replace_char(do_zmiany, znak):
            do_zmiany = do_zmiany.replace(znak, "")
            if znak == "(":
                znak = ")"
                do_zmiany = do_zmiany.replace(znak, "")
            do_zmiany = do_zmiany.replace("[", "")
            do_zmiany = do_zmiany.replace("]", "")
            do_zmiany = do_zmiany.replace("'", "")
            do_zmiany = do_zmiany.replace("u", "")

            return do_zmiany

        match_link = response.meta['match_link']



        #####################

        match_box = response.xpath('//div[@class="standard-box teamsBox"]')
        teams = match_box.xpath('./div[@class="team"]')
        teams_names = teams.xpath('//div[@class="teamName"]/text()').extract()

        # HOME TEAM INFO
        ##################

        home_team_name = teams_names[0]
        home_team_country = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/img/@alt').extract()
        home_team_link = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/a/@href').extract()
        home_team_score = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/text()').extract()
        home_team_id = get_id(home_team_link, 2)

        # AWAY TEAM INFO
        ##################
        away_team_name = teams_names[1]
        away_team_country = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[3]/img/@alt').extract()
        away_team_link = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/a/@href').extract()
        away_team_score = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div/text()').extract()
        away_team_id = get_id(away_team_link, 2)

        # TOURNAMENT AND MATCH INFO
        ##################
        match_date_time = response.xpath('//div[@class="time"]/@data-unix').extract()
        match_date_time = int(match_date_time[0]) / 1000
        match_date_time = datetime.datetime.fromtimestamp(match_date_time)
        match_time = datetime.datetime.now().time().replace(hour=match_date_time.hour, minute=match_date_time.minute, second=0, microsecond=0)
        match_time = match_time.strftime("%H:%M:%S")
        match_date = match_date_time.strftime("%Y-%m-%d")
        vote_ban = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[1]/div[2]/div/div/text()').extract()
        tournament_link = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/a/@href').extract()
        tournament_id = get_id(tournament_link, 2)
        match_notes = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div/text()').extract()
        match_demo_link = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div/div[1]/a/@href').extract()


        stats = response.xpath('//a[@class="results-stats"]/@href').extract()
        for stats_link_pre in stats:
            stats_link = 'http://hltv.org' + str(stats_link_pre)
            yield scrapy.Request(stats_link,
                                 callback=self.parse_listing_again,
                                 meta={'match_link': match_link,
                                       'match_date_time':match_date_time,
                                       'match_date':match_date,
                                       'match_time':match_time,
                                       'stats_link':stats_link,
                                       'home_team_name':home_team_name,
                                       'home_team_country':home_team_country,
                                       'home_team_link':home_team_link,
                                       'home_team_score':home_team_score,
                                       'away_team_name':away_team_name,
                                       'away_team_country':away_team_country,
                                       'away_team_link':away_team_link,
                                       'away_team_score':away_team_score,
                                       'match_notes':match_notes,
                                       'match_demo_link':match_demo_link,
                                       'vote_ban':vote_ban,
                                       'home_team_id':home_team_id,
                                       'away_team_id':away_team_id,
                                       'tournament_id':tournament_id,
                                       'tournament_link':tournament_link
                                       })


    def parse_listing_again(self, response):

        def replace_char(do_zmiany, znak):
            do_zmiany = do_zmiany.replace(znak, "")
            if znak == "(":
                znak = ")"
                do_zmiany = do_zmiany.replace(znak, "")
            do_zmiany = do_zmiany.replace("[", "")
            do_zmiany = do_zmiany.replace("]", "")
            do_zmiany = do_zmiany.replace("'", "")
            do_zmiany = do_zmiany.replace("u", "")
            do_zmiany = do_zmiany.replace(",", "")
            return do_zmiany

        def get_id(link, pozycja):
            link = str(link)
            link = link.split("/")
            id = link[pozycja]
            return id
            
        match_date_time = response.meta['match_date_time']
        home_team_id = response.meta['home_team_id']
        away_team_id = response.meta['away_team_id']
        tournament_id = response.meta['tournament_id']
        tournament_link = response.meta['tournament_link']
        match_link = response.meta['match_link']
        match_date = response.meta['match_date']
        match_time = response.meta['match_time']
        stats_link = response.meta['stats_link']
        vote_ban = response.meta['vote_ban']
        match_id = get_id(str(match_link), 2)
        home_team_name = response.meta['home_team_name']
        home_team_country = response.meta['home_team_country']
        home_team_link = response.meta['home_team_link']
        home_team_score = response.meta['home_team_score']
        away_team_name = response.meta['away_team_name']
        away_team_country = response.meta['away_team_country']
        away_team_link = response.meta['away_team_link']
        away_team_score = response.meta['away_team_score']
        match_notes = response.meta['match_notes']
        match_demo_link = response.meta['match_demo_link']

        gracz = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[1]/a/text()').extract()

        # GAME STATS INFO
        ##################
        maps = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/div/div[1]/text()').extract()
        maps = replace_char(maps[1], "")
        home_team_side = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/div/div[2]/div[1]/span[3]/@class').extract()
        away_team_side = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/div/div[2]/div[1]/span[4]/@class').extract()
        home_first_score = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/div/div[2]/div[1]/span[3]/text()').extract()
        away_first_score = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/div/div[2]/div[1]/span[4]/text()').extract()
        home_second_score = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/div/div[2]/div[1]/span[5]/text()').extract()
        away_second_score = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/div/div[2]/div[1]/span[6]/text()').extract()
        first_kills = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/text()').extract()
        first_kills = str(first_kills)
        first_kills = first_kills.split(":")
        clutches_won = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/div/div[5]/div[1]/text()').extract()
        clutches_won = str(clutches_won)
        clutches_won = clutches_won.split(":")
        home_first_kills = first_kills[0]
        home_first_kills = replace_char(home_first_kills, "")
        away_first_kills = first_kills[1]
        away_first_kills = replace_char(away_first_kills, "")
        home_clutches_won = clutches_won[0]
        home_clutches_won = replace_char(home_clutches_won, "")
        away_clutches_won = clutches_won[1]
        away_clutches_won = replace_char(away_clutches_won, "")

        ht_p1_name = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[1]/a/text()').extract()
        ht_p1_link = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[1]/a/@href').extract()
        ht_p1_kills = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[2]/text()').extract()
        ht_p1_headshots = response.xpath("/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[2]/span/text()").extract()
        ht_p1_asists = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[3]/text()').extract()
        ht_p1_deaths = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[4]/text()').extract()
        ht_p1_kast = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[5]/text()').extract()
        ht_p1_kast = str(ht_p1_kast)
        ht_p1_kast = replace_char(ht_p1_kast, "%")
        ht_p1_adr =response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[7]/text()').extract()
        ht_p1_fk_diff =response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[8]/text()').extract()
        ht_p1_rating20 =response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[9]/text()').extract()

        #ht_p2_id =
        ht_p2_name = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[2]/td[1]/a/text()').extract()
        ht_p2_link =response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[2]/td[1]/a/@href').extract()
        ht_p2_kills = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[2]/td[2]/text()').extract()
        ht_p2_headshots = response.xpath("/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[2]/td[2]/span/text()").extract()
        ht_p2_asists = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[2]/td[3]/text()').extract()
        ht_p2_deaths = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[2]/td[4]/text()').extract()
        ht_p2_kast = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[2]/td[5]/text()').extract()
        ht_p2_kast = str(ht_p2_kast)
        ht_p2_kast = replace_char(ht_p2_kast, "%")
        ht_p2_adr = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[2]/td[7]/text()').extract()
        ht_p2_fk_diff = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[2]/td[8]/text()').extract()
        ht_p2_rating20 = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[2]/td[9]/text()').extract()


        ht_p3_name = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[3]/td[1]/a/text()').extract()
        ht_p3_link = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[3]/td[1]/a/@href').extract()
        ht_p3_kills = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[3]/td[2]/text()').extract()
        ht_p3_headshots = response.xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[3]/td[2]/span/text()").extract()
        ht_p3_asists = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[3]/td[3]/text()').extract()
        ht_p3_deaths = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[3]/td[4]/text()').extract()
        ht_p3_kast = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[3]/td[5]/text()').extract()
        ht_p3_kast = str(ht_p3_kast)
        ht_p3_kast = replace_char(ht_p3_kast, "%")
        ht_p3_adr = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[3]/td[7]/text()').extract()
        ht_p3_fk_diff = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[3]/td[8]/text()').extract()
        ht_p3_rating20 = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[3]/td[9]/text()').extract()

        ht_p4_name = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[4]/td[1]/a/text()').extract()
        ht_p4_link = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[4]/td[1]/a/@href').extract()
        ht_p4_kills = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[4]/td[2]/text()').extract()
        ht_p4_headshots = response.xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[4]/td[2]/span/text()").extract()
        ht_p4_asists = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[4]/td[3]/text()').extract()
        ht_p4_deaths = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[4]/td[4]/text()').extract()
        ht_p4_kast = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[4]/td[5]/text()').extract()
        ht_p4_kast = str(ht_p4_kast)
        ht_p4_kast = replace_char(ht_p4_kast, "%")
        ht_p4_adr = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[4]/td[7]/text()').extract()
        ht_p4_fk_diff = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[4]/td[8]/text()').extract()
        ht_p4_rating20 = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[4]/td[9]/text()').extract()

        ht_p5_name = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[5]/td[1]/a/text()').extract()
        ht_p5_link = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[5]/td[1]/a/@href').extract()
        ht_p5_kills = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[5]/td[2]/text()').extract()
        ht_p5_headshots = response.xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[5]/td[2]/span/text()").extract()
        ht_p5_asists = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[5]/td[3]/text()').extract()
        ht_p5_deaths = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[5]/td[4]/text()').extract()
        ht_p5_kast = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[5]/td[5]/text()').extract()
        ht_p5_kast = str(ht_p5_kast)
        ht_p5_kast = replace_char(ht_p5_kast, "%")
        ht_p5_adr = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[5]/td[7]/text()').extract()
        ht_p5_fk_diff = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[5]/td[8]/text()').extract()
        ht_p5_rating20 = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[5]/td[9]/text()').extract()


        ###########################################################################################3

        at_p1_name = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[1]/td[1]/a/text()').extract()
        at_p1_link = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[1]/td[1]/a/@href').extract()
        at_p1_kills = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[1]/td[2]/text()').extract()
        at_p1_headshots = response.xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[1]/td[2]/span/text()").extract()
        at_p1_asists = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[1]/td[3]/text()').extract()
        at_p1_deaths = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[1]/td[4]/text()').extract()
        at_p1_kast = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[1]/td[5]/text()').extract()
        at_p1_kast = str(at_p1_kast)
        at_p1_kast = replace_char(at_p1_kast, "%")
        at_p1_adr = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[1]/td[7]/text()').extract()
        at_p1_fk_diff = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[1]/td[8]/text()').extract()
        at_p1_rating20 = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[1]/td[9]/text()').extract()

        at_p2_name = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[1]/a/text()').extract()
        at_p2_link = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[1]/a/@href').extract()
        at_p2_kills = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[2]/text()').extract()
        at_p2_headshots = response.xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[2]/span/text()").extract()
        at_p2_asists = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[3]/text()').extract()
        at_p2_deaths = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[4]/text()').extract()
        at_p2_kast = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[5]/text()').extract()
        at_p2_kast = str(at_p2_kast)
        at_p2_kast = replace_char(at_p2_kast, "%")
        at_p2_adr = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[7]/text()').extract()
        at_p2_fk_diff = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[8]/text()').extract()
        at_p2_rating20 = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[9]/text()').extract()

        at_p3_name = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[3]/td[1]/a/text()').extract()
        at_p3_link = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[3]/td[1]/a/@href').extract()
        at_p3_kills = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[3]/td[2]/text()').extract()
        at_p3_headshots = response.xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[3]/td[2]/span/text()").extract()
        at_p3_asists = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[3]/td[3]/text()').extract()
        at_p3_deaths = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[3]/td[4]/text()').extract()
        at_p3_kast = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[3]/td[5]/text()').extract()
        at_p3_kast = str(at_p3_kast)
        at_p3_kast = replace_char(at_p3_kast, "%")
        at_p3_adr = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[3]/td[7]/text()').extract()
        at_p3_fk_diff = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[3]/td[8]/text()').extract()
        at_p3_rating20 = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[3]/td[9]/text()').extract()

        at_p4_name = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[1]/a/text()').extract()
        at_p4_link = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[1]/a/@href').extract()
        at_p4_kills = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[2]/text()').extract()
        at_p4_headshots = response.xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[2]/span/text()").extract()
        at_p4_asists = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[3]/text()').extract()
        at_p4_deaths = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[4]/text()').extract()
        at_p4_kast = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[5]/text()').extract()
        at_p4_kast = str(at_p4_kast)
        at_p4_kast = replace_char(at_p4_kast, "%")
        at_p4_adr = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[7]/text()').extract()
        at_p4_fk_diff = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[8]/text()').extract()
        at_p4_rating20 = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[9]/text()').extract()

        at_p5_name = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[5]/td[1]/a/text()').extract()
        at_p5_link = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[5]/td[1]/a/@href').extract()
        at_p5_kills = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[5]/td[2]/text()').extract()
        at_p5_headshots = response.xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[5]/td[2]/span/text()").extract()
        at_p5_asists = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[5]/td[3]/text()').extract()
        at_p5_deaths = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[5]/td[4]/text()').extract()
        at_p5_kast = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[5]/td[5]/text()').extract()
        at_p5_kast = str(at_p5_kast)
        at_p5_kast = replace_char(at_p5_kast, "%")
        at_p5_adr = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[5]/td[7]/text()').extract()
        at_p5_fk_diff = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[5]/td[8]/text()').extract()
        at_p5_rating20 = response.xpath(
            '/html/body/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[5]/td[9]/text()').extract()

        ht_p1_headshots = str(ht_p1_headshots)
        ht_p2_headshots = str(ht_p2_headshots)
        ht_p3_headshots = str(ht_p3_headshots)
        ht_p4_headshots = str(ht_p4_headshots)
        ht_p5_headshots = str(ht_p5_headshots)
        at_p1_headshots = str(at_p1_headshots)
        at_p2_headshots = str(at_p2_headshots)
        at_p3_headshots = str(at_p3_headshots)
        at_p4_headshots = str(at_p4_headshots)
        at_p5_headshots = str(at_p5_headshots)


        ht_p1_headshots = replace_char(ht_p1_headshots, "(")
        ht_p2_headshots = replace_char(ht_p2_headshots, "(")
        ht_p3_headshots = replace_char(ht_p3_headshots, "(")
        ht_p4_headshots = replace_char(ht_p4_headshots, "(")
        ht_p5_headshots = replace_char(ht_p5_headshots, "(")
        at_p1_headshots = replace_char(at_p1_headshots, "(")
        at_p2_headshots = replace_char(at_p2_headshots, "(")
        at_p3_headshots = replace_char(at_p3_headshots, "(")
        at_p4_headshots = replace_char(at_p4_headshots, "(")
        at_p5_headshots = replace_char(at_p5_headshots, "(")
        ht_p1_id = get_id(ht_p1_link, 3)
        ht_p2_id = get_id(ht_p2_link, 3)
        ht_p3_id = get_id(ht_p3_link, 3)
        ht_p4_id = get_id(ht_p4_link, 3)
        ht_p5_id = get_id(ht_p5_link, 3)
        at_p1_id = get_id(at_p1_link, 3)
        at_p2_id = get_id(at_p2_link, 3)
        at_p3_id = get_id(at_p3_link, 3)
        at_p4_id = get_id(at_p4_link, 3)
        at_p5_id = get_id(at_p5_link, 3)


        loader = ItemLoader(item=Matches_Results(), response=response)

        loader.add_value('match_date_time', match_date_time)
        loader.add_value('match_date', match_date)
        loader.add_value('match_time', match_time)
        loader.add_value('match_id', match_id)
        loader.add_value('match_link', match_link)
        loader.add_value('stats_link', stats_link)
        loader.add_value('vote_ban',vote_ban)
        loader.add_value('maps',maps)
        loader.add_value('home_team_side',home_team_side)
        loader.add_value('away_team_side',away_team_side)
        loader.add_value('home_first_score',home_first_score)
        loader.add_value('away_first_score',away_first_score)
        loader.add_value('home_second_score',home_second_score)
        loader.add_value('away_second_score',away_second_score)
        loader.add_value('home_team_name',home_team_name)
        loader.add_value('home_team_country',home_team_country)
        loader.add_value('home_team_link',home_team_link)
        loader.add_value('home_team_score',home_team_score)
        loader.add_value('away_team_name',away_team_name)
        loader.add_value('away_team_country',away_team_country)
        loader.add_value('away_team_link',away_team_link)
        loader.add_value('away_team_score',away_team_score)
        loader.add_value('match_notes',match_notes)
        loader.add_value('match_demo_link',match_demo_link)
        loader.add_value('at_p1_name', at_p1_name)
        loader.add_value('at_p1_link', at_p1_link)
        loader.add_value('at_p1_kills', at_p1_kills)
        loader.add_value('at_p1_headshots', at_p1_headshots)
        loader.add_value('at_p1_asists', at_p1_asists)
        loader.add_value('at_p1_deaths', at_p1_deaths)
        loader.add_value('at_p1_kast', at_p1_kast)
        loader.add_value('at_p1_adr', at_p1_adr)
        loader.add_value('at_p1_fk_diff', at_p1_fk_diff)
        loader.add_value('at_p1_rating20', at_p1_rating20)
        loader.add_value('at_p2_name', at_p2_name)
        loader.add_value('at_p2_link', at_p2_link)
        loader.add_value('at_p2_kills', at_p2_kills)
        loader.add_value('at_p2_headshots', at_p2_headshots)
        loader.add_value('at_p2_asists', at_p2_asists)
        loader.add_value('at_p2_deaths', at_p2_deaths)
        loader.add_value('at_p2_kast', at_p2_kast)
        loader.add_value('at_p2_adr', at_p2_adr)
        loader.add_value('at_p2_fk_diff', at_p2_fk_diff)
        loader.add_value('at_p2_rating20', at_p2_rating20)
        loader.add_value('at_p3_name', at_p3_name)
        loader.add_value('at_p3_link', at_p3_link)
        loader.add_value('at_p3_kills', at_p3_kills)
        loader.add_value('at_p3_headshots', at_p3_headshots)
        loader.add_value('at_p3_asists', at_p3_asists)
        loader.add_value('at_p3_deaths', at_p3_deaths)
        loader.add_value('at_p3_kast', at_p3_kast)
        loader.add_value('at_p3_adr', at_p3_adr)
        loader.add_value('at_p3_fk_diff', at_p3_fk_diff)
        loader.add_value('at_p3_rating20', at_p3_rating20)
        loader.add_value('at_p4_name', at_p4_name)
        loader.add_value('at_p4_link', at_p4_link)
        loader.add_value('at_p4_kills', at_p4_kills)
        loader.add_value('at_p4_headshots', at_p4_headshots)
        loader.add_value('at_p4_asists', at_p4_asists)
        loader.add_value('at_p4_deaths', at_p4_deaths)
        loader.add_value('at_p4_kast', at_p4_kast)
        loader.add_value('at_p4_adr', at_p4_adr)
        loader.add_value('at_p4_fk_diff', at_p4_fk_diff)
        loader.add_value('at_p4_rating20', at_p4_rating20)
        loader.add_value('at_p5_name', at_p5_name)
        loader.add_value('at_p5_link', at_p5_link)
        loader.add_value('at_p5_kills', at_p5_kills)
        loader.add_value('at_p5_headshots', at_p5_headshots)
        loader.add_value('at_p5_asists', at_p5_asists)
        loader.add_value('at_p5_deaths', at_p5_deaths)
        loader.add_value('at_p5_kast', at_p5_kast)
        loader.add_value('at_p5_adr', at_p5_adr)
        loader.add_value('at_p5_fk_diff', at_p5_fk_diff)
        loader.add_value('at_p5_rating20', at_p5_rating20)
        loader.add_value('ht_p1_name', ht_p1_name)
        loader.add_value('ht_p1_link', ht_p1_link)
        loader.add_value('ht_p1_kills', ht_p1_kills)
        loader.add_value('ht_p1_headshots', ht_p1_headshots)
        loader.add_value('ht_p1_asists', ht_p1_asists)
        loader.add_value('ht_p1_deaths', ht_p1_deaths)
        loader.add_value('ht_p1_kast', ht_p1_kast)
        loader.add_value('ht_p1_adr', ht_p1_adr)
        loader.add_value('ht_p1_fk_diff', ht_p1_fk_diff)
        loader.add_value('ht_p1_rating20', ht_p1_rating20)
        loader.add_value('ht_p2_name', ht_p2_name)
        loader.add_value('ht_p2_link', ht_p2_link)
        loader.add_value('ht_p2_kills', ht_p2_kills)
        loader.add_value('ht_p2_headshots', ht_p2_headshots)
        loader.add_value('ht_p2_asists', ht_p2_asists)
        loader.add_value('ht_p2_deaths', ht_p2_deaths)
        loader.add_value('ht_p2_kast', ht_p2_kast)
        loader.add_value('ht_p2_adr', ht_p2_adr)
        loader.add_value('ht_p2_fk_diff', ht_p2_fk_diff)
        loader.add_value('ht_p2_rating20', ht_p2_rating20)
        loader.add_value('ht_p3_name', ht_p3_name)
        loader.add_value('ht_p3_link', ht_p3_link)
        loader.add_value('ht_p3_kills', ht_p3_kills)
        loader.add_value('ht_p3_headshots', ht_p3_headshots)
        loader.add_value('ht_p3_asists', ht_p3_asists)
        loader.add_value('ht_p3_deaths', ht_p3_deaths)
        loader.add_value('ht_p3_kast', ht_p3_kast)
        loader.add_value('ht_p3_adr', ht_p3_adr)
        loader.add_value('ht_p3_fk_diff', ht_p3_fk_diff)
        loader.add_value('ht_p3_rating20', ht_p3_rating20)
        loader.add_value('ht_p4_name', ht_p4_name)
        loader.add_value('ht_p4_link', ht_p4_link)
        loader.add_value('ht_p4_kills', ht_p4_kills)
        loader.add_value('ht_p4_headshots', ht_p4_headshots)
        loader.add_value('ht_p4_asists', ht_p4_asists)
        loader.add_value('ht_p4_deaths', ht_p4_deaths)
        loader.add_value('ht_p4_kast', ht_p4_kast)
        loader.add_value('ht_p4_adr', ht_p4_adr)
        loader.add_value('ht_p4_fk_diff', ht_p4_fk_diff)
        loader.add_value('ht_p4_rating20', ht_p4_rating20)
        loader.add_value('ht_p5_name', ht_p5_name)
        loader.add_value('ht_p5_link', ht_p5_link)
        loader.add_value('ht_p5_kills', ht_p5_kills)
        loader.add_value('ht_p5_headshots', ht_p5_headshots)
        loader.add_value('ht_p5_asists', ht_p5_asists)
        loader.add_value('ht_p5_deaths', ht_p5_deaths)
        loader.add_value('ht_p5_kast', ht_p5_kast)
        loader.add_value('ht_p5_adr', ht_p5_adr)
        loader.add_value('ht_p5_fk_diff', ht_p5_fk_diff)
        loader.add_value('ht_p5_rating20', ht_p5_rating20)
        loader.add_value('tournament_link',tournament_link)
        loader.add_value('home_team_id',home_team_id)
        loader.add_value('away_team_id',away_team_id)
        loader.add_value('tournament_id',tournament_id)
        loader.add_value('home_first_kills',home_first_kills)
        loader.add_value('away_first_kills',away_first_kills)
        loader.add_value('home_clutches_won',home_clutches_won)
        loader.add_value('away_clutches_won',away_clutches_won)
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

        yield loader.load_item()