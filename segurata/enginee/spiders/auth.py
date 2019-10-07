# -*- coding: utf-8 -*-
import json
import logging
from typing import ClassVar, Tuple

import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider

from ..login.exceptions import *
from ..login.login import check_login, login_request
from ..user_config.exceptions import *
from ..user_config.parse import user_config_parse


class AuthSpider(Spider):
    '''Spider that logs in a website and scrapes its content.

    Arguments:

        config {str} -- path to the configuration file.

    The configuration files has all the necessary configurations
    like the credentials and DOM selectors to scrape the items.

    '''
    name = 'auth'
    start_urls = []

    def __init__(self, *args, config, **kwargs):
        user_config = user_config_parse(config)
        self.config = user_config
        super().__init__(*args, **kwargs)

    def start_requests(self):
        config = self.config

        login_url = config.get('login_url')
        assert login_url is not None, 'Please input login URL.'

        start_urls = config.get('start_urls')
        assert start_urls is not None, 'Please input URLs to scrape.'
        self.start_urls = start_urls

        login_info = {
            'credentials': config['credentials'],
            'check_selector': config['check_login_css_selector'],
        }

        yield Request(
            url=login_url,
            callback=self.login,
            cb_kwargs=login_info,
        )


    def login(self, response: Response, *args, **kwargs):
        """Log into the desired and calls the `parse` method.

        Arguments:
            response {scrapy.http.Response} --
        """
        credentials = kwargs.get('credentials')
        user_is_logged_in_selector = kwargs.get('check_selector')
        after_login_url = kwargs.get('after_login_url')

        try:
            form_request = login_request(response, credentials=credentials)
            form_request.callback = self.check_login
            form_request.cb_kwargs.update({
                'selector': user_is_logged_in_selector,
                'after_login_url': after_login_url,
            })
            yield form_request
        except LoginBaseError:
            pass

    def check_login(self, response: Response, *args, **kwargs):
        'Check if the user is logged in and start the requests in start_urls.'
        check_login(response, selector=kwargs.get('selector'))
        for url in self.start_urls:
            yield Request(
                url=url,
                dont_filter=True,
                meta={'cookiejar': 0}
            )


    def parse(self, response):
        item = {}
        schemas = self.config.get('schemas', [])

        for schema in schemas:
            _schema_name = schema['schema_name']
            properties = schema['properties']
            for prop_name, prop_selector in properties.items():
                item[prop_name] = response.css(prop_selector).extract()
            yield item

    def rules_from_info(self):
        'Create scrapy Rule objects from the user-config.'
        pass

