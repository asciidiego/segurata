# -*- coding: utf-8 -*-
import json
import scrapy
import logging
from typing import Tuple, ClassVar
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


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

    def parse_item(self, response):
        item = {}
        return item

    def _populate_rules(self):
        'Create scrapy Rule objects from the user-config.'
        raise NotImplementedError()

    def _init_user_config(self, path: str):
        'Obtain JSON file from `path` and stores it as a dict in the instance.'

        if not path.endswith('.json'):
            raise CloseSpider(
                    reason="The config path specified does not correspond to a json file."
            )
