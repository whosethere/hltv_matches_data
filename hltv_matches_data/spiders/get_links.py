import scrapy
from matches_data.items import Upcoming_matches_links
from scrapy.loader import ItemLoader
from matches_data.mongo_connection import get_connection, match_in_database, link_in_database, update_match_timestamp
from matches_data.processing_methods import get_matchid_from_link

#odpalać co 5 minut

class GetUpcomingMatchesSpider(scrapy.Spider):
    name = 'get_links'
    allowed_domains = ['hltv.org']
    start_urls = ['https://www.hltv.org/matches']

    def parse(self, response):

        upcoming_matches = response.xpath('//div[@class="match"]')
        base_url = 'http://hltv.org'

        for match in upcoming_matches:
            # if not match.xpath('.//td[@class="team-cell"]'):
            #     continue
            if len(match.xpath('.//div[@class="line-align"]/img')) < 2:
                continue
            
            match_timestamp = match.xpath('.//div[@class="time"]/@data-unix')[0].extract()
            match_timestamp = int(match_timestamp) / 1000

            match_link = match.xpath('.//a[@class="a-reset"]/@href').extract()
            match_link = base_url + str(match_link[0])

            match_id = get_matchid_from_link(match_link)

            
            if link_in_database(match_id):
                update_match_timestamp(match_id, match_timestamp)
                continue

            loader = ItemLoader(item=Upcoming_matches_links(), response=response)
            loader.add_value('match_link', match_link)
            loader.add_value('match_id', match_id)
            loader.add_value('match_timestamp', match_timestamp)
            yield loader.load_item()