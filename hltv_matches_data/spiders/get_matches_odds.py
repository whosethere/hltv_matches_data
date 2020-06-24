# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
import time
from matches_data.items import Betting_Odds
from scrapy.loader import ItemLoader
import pprint
from matches_data.mongo_connection import get_upcoming_links, odds_added


class GetOddsSpider(scrapy.Spider):
    name = 'get_matches_odds'
    allowed_domains = ['hltv.org']
    start_urls = ['http://hltv.org/']

    def parse(self, response):
        upcoming_matches = get_upcoming_links()

        for match in upcoming_matches:
            if odds_added(match['match_id']):
                continue
            
            odds_match_link = match['match_link']
            yield scrapy.Request(odds_match_link,
                                 callback = self.parse_odds,
                                 meta = {'match_link':odds_match_link})
        
        pass

    def parse_odds(self, response):

        def get_ods_home(row):
            if len(row.xpath('.//td[@class="odds-cell border-left"]/a/text()').extract()) > 0:
                home_team_odds = str(row.xpath('.//td[@class="odds-cell border-left"]/a/text()')[0].extract())
                home_team_odds = home_team_odds.replace("%", "")
                home_team_odds = float(home_team_odds)
            else:
                home_team_odds = None
            return home_team_odds

        def get_ods_away(row):
            if len(row.xpath('.//td[@class="odds-cell border-left"]/a/text()').extract()) > 0:
                away_team_odds = str(row.xpath('.//td[@class="odds-cell border-left"]/a/text()')[2].extract())
                away_team_odds = away_team_odds.replace("%", "")
                away_team_odds = float(away_team_odds)
            else:
                away_team_odds = None
            return away_team_odds


        match_link = response.meta['match_link']
        match_id = int(match_link.split("/")[4])

        pick_a_winner_home = response.xpath("//div[@class='pick-a-winner-team team1 canvote']/div[2]/text()").extract_first()
        pick_a_winner_away = response.xpath("//div[@class='pick-a-winner-team team2 canvote']/div[2]/text()").extract_first()
        
        # table = response.xpath('//div[@class="compare standard-box"]/table')
        egb_com_home = get_ods_home(response.xpath('.//tr[@class=" gprov_egb provider"]'))
        egb_com_away = get_ods_away(response.xpath('.//tr[@class=" gprov_egb provider"]'))
        
        betway_com_home = get_ods_home(response.xpath('.//tr[@class=" gprov_p2g0jzml provider"]'))
        betway_com_away = get_ods_away(response.xpath('.//tr[@class=" gprov_p2g0jzml provider"]'))
        
        loot_bet_home = get_ods_home(response.xpath('.//tr[@class=" gprov_nz6cnayl provider"]'))
        loot_bet_away = get_ods_away(response.xpath('.//tr[@class=" gprov_nz6cnayl provider"]'))
        
        gg_bet_home = get_ods_home(response.xpath('.//tr[@class=" gprov_gv4nx914 provider"]'))
        gg_bet_away = get_ods_away(response.xpath('.//tr[@class=" gprov_gv4nx914 provider"]'))
        
        bet365_home = get_ods_home(response.xpath('.//tr[@class=" gprov_3etkx6rj provider"]'))
        bet365_away = get_ods_away(response.xpath('.//tr[@class=" gprov_3etkx6rj provider"]'))
        
        xbet1_home = get_ods_home(response.xpath('.//tr[@class=" gprov_5i4rhap1 provider"]'))
        xbet1_away = get_ods_away(response.xpath('.//tr[@class=" gprov_5i4rhap1 provider"]'))
        
        pinnacle_esport_home = get_ods_home(response.xpath('.//tr[@class="pinnacle-odds gprov_pinnacle provider"]'))
        pinnacle_esport_away = get_ods_away(response.xpath('.//tr[@class="pinnacle-odds gprov_pinnacle provider"]'))
        
        buff8_home = get_ods_home(response.xpath('.//tr[@class="buff8-odds gprov_buff88 provider"]'))
        buff8_away = get_ods_away(response.xpath('.//tr[@class="buff8-odds gprov_buff88 provider"]'))
        
        sts_home = get_ods_home(response.xpath('.//tr[@class="gprov_stsbet provider"]'))
        sts_away = get_ods_away(response.xpath('.//tr[@class="gprov_stsbet provider"]'))
        betsnet_home = get_ods_home(response.xpath('.//tr[@class="betsnet-odds geoprovider_betsnet betting_provider"]'))
        betsnet_away = get_ods_away(response.xpath('.//tr[@class="betsnet-odds geoprovider_betsnet betting_provider"]'))
        
        unikrn_home = get_ods_home(response.xpath('.//tr[@class="unikrn-odds gprov_unikrn provider"]'))
        unikrn_away = get_ods_away(response.xpath('.//tr[@class="unikrn-odds gprov_unikrn provider"]'))
        
        betwinner_home = get_ods_home(response.xpath('.//tr[@class=" gprov_uazy6czn provider"]'))
        betwinner_away = get_ods_away(response.xpath('.//tr[@class=" gprov_uazy6czn provider"]'))
        
        cyberbet_home = get_ods_home(response.xpath('.//tr[@class=" gprov_cyberbet provider"]'))
        cyberbet_away = get_ods_away(response.xpath('.//tr[@class=" gprov_cyberbet provider"]'))
        
        dmgbet_home = get_ods_home(response.xpath('.//tr[@class="  gprov_sFaLXv3p provider"]'))
        dmgbet_away = get_ods_away(response.xpath('.//tr[@class="  gprov_sFaLXv3p provider"]'))

        vulkanbet_home = get_ods_home(response.xpath('.//tr[@class=" gprov_vulkan provider"]'))
        vulkanbet_away = get_ods_away(response.xpath('.//tr[@class=" gprov_vulkan provider"]'))

        luckybox_home = get_ods_home(response.xpath('.//tr[@class=" gprov_luckbox provider"]'))
        luckybox_away = get_ods_away(response.xpath('.//tr[@class=" gprov_luckbox provider"]'))

        csgo500_home = get_ods_home(response.xpath('.//tr[@class=" gprov_csgo500 provider"]'))
        csgo500_away = get_ods_away(response.xpath('.//tr[@class=" gprov_csgo500 provider"]'))

        midnite_home = get_ods_home(response.xpath('.//tr[@class=" gprov_midnite provider"]'))
        midnite_away = get_ods_away(response.xpath('.//tr[@class=" gprov_midnite provider"]'))

        unibet_home = get_ods_home(response.xpath('.//tr[@class=" gprov_vz0pxwkq provider"]'))
        unibet_away = get_ods_away(response.xpath('.//tr[@class=" gprov_vz0pxwkq provider"]'))
        


        loader = ItemLoader(item=Betting_Odds(), response=response)
        loader.add_value('match_id', match_id)
        loader.add_value('match_link', match_link)
        loader.add_value('time_added', int(time.time()))
        loader.add_value('pick_a_winner_home',pick_a_winner_home)
        loader.add_value('pick_a_winner_away',pick_a_winner_away)
        loader.add_value('egb_com_home',egb_com_home)
        loader.add_value('egb_com_away',egb_com_away)
        loader.add_value('betway_com_home',betway_com_home)
        loader.add_value('betway_com_away',betway_com_away)
        loader.add_value('loot_bet_home',loot_bet_home)
        loader.add_value('loot_bet_away',loot_bet_away)
        loader.add_value('gg_bet_home',gg_bet_home)
        loader.add_value('gg_bet_away',gg_bet_away)
        loader.add_value('bet365_home',bet365_home)
        loader.add_value('bet365_away',bet365_away)
        loader.add_value('xbet1_home',xbet1_home)
        loader.add_value('xbet1_away',xbet1_away)
        loader.add_value('pinnacle_esport_home',pinnacle_esport_home)
        loader.add_value('pinnacle_esport_away',pinnacle_esport_away)
        loader.add_value('buff8_home',buff8_home)
        loader.add_value('buff8_away',buff8_away)
        loader.add_value('betsnet_home',betsnet_home)
        loader.add_value('betsnet_away',betsnet_away)
        loader.add_value('unikrn_home',unikrn_home)
        loader.add_value('unikrn_away',unikrn_away)
        loader.add_value('betwinner_home',betwinner_home)
        loader.add_value('betwinner_away',betwinner_away)
        loader.add_value('vulkanbet_home',vulkanbet_home)
        loader.add_value('vulkanbet_away',vulkanbet_away)
        loader.add_value('unibet_home',unibet_home)
        loader.add_value('unibet_away',unibet_away)
        loader.add_value('sts_home',sts_home)
        loader.add_value('sts_away',sts_away)
        loader.add_value('cyberbet_home',cyberbet_home)
        loader.add_value('cyberbet_away',cyberbet_away)
        loader.add_value('dmgbet_home',dmgbet_home)
        loader.add_value('dmgbet_away',dmgbet_away)
        loader.add_value('luckybox_home',luckybox_home)
        loader.add_value('luckybox_away',luckybox_away)
        loader.add_value('csgo500_home',csgo500_home)
        loader.add_value('csgo500_away',csgo500_away)
        loader.add_value('midnite_home',midnite_home)
        loader.add_value('midnite_away',midnite_away)
        yield loader.load_item()


        










