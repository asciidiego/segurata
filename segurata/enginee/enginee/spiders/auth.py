# -*- coding: utf-8 -*-
import json
import scrapy
import logging
from typing import Tuple, ClassVar
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from enginee.user_config.parse import user_config_parse
from enginee.user_config.exceptions import *
from enginee.login.login import *

Rules = Tuple[Rule]


class AuthSpider(CrawlSpider):
    name = 'auth'
    start_urls = []
    rules: ClassVar[Rules] = ()

    def __init__(self, *args, **kwargs):
        path_to_user_config = kwargs.get('config')
        self._init_user_config(path_to_user_config)
        self._populate_rules()
        super().__init__(*args, **kwargs)

    def start_requests(self):
        login_url = self.config_dict['login_url']
        credentials = self.config_dict['credentials']
        yield Request(
                url=login_url, 
                callback=self.login,
                meta={'credentials': credentials}
        )

    def login(self, response):
        yield do_login(response)

    def parse_item(self, response):
        item = {}
        return item

    def _populate_rules(self):
        'Create scrapy Rule objects from the user-config.'
        raise NotImplementedError()

    def _init_user_config(self, path: str):
        'Obtain JSON file from `path` and stores it as a dict in the instance.'
        try:
            self.config = user_config_parse(path)
        except UserConfigBaseException as e:
            raise CloseSpider('Could not load user configuration.')
