# -*- coding: utf-8 -*-
import json
import logging
from typing import ClassVar, Tuple

import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from enginee.login.exceptions import *
from enginee.login.login import check_login, login_request
from enginee.user_config.exceptions import *
from enginee.user_config.parse import user_config_parse

Rules = Tuple[Rule]


class AuthSpider(CrawlSpider):
    name = 'auth'
    start_urls = []
    rules: ClassVar[Rules] = ()

    def __init__(self, *args, **kwargs):
        path_to_user_config = kwargs.get('config')
        self._init_user_config(path_to_user_config)
        # TODO: Assert that the config has the required credentials
        self._populate_rules()
        super().__init__(*args, **kwargs)

    def start_requests(self):
        login_url = self.config_dict['login_url']
        credentials = self.config_dict['credentials']
        check_login_selector = self.config_dict['check_login_css']
        after_login_url = self.config_dict['after_login_url']

        login_info = {
            'credentials': credentials,
            'check_selector': check_login_selector,
            'after_login_url': after_login_url,
        }

        yield Request(
            url=login_url,
            callback=self.login,
            cb_kwargs=login_info,
        )

    def login(self, response: Response, *args, **kwargs):
        """Logs into the desired and calls the `parse` method.

        Arguments:
            response {scrapy.http.Response} --
        """
        credentials = kwargs.get('credentials')
        user_is_logged_in_selector = kwargs.get('check_selector')
        after_login_url = kwargs.get('after_login_url')

        try:
            form_request = login_request(response, credentials=credentials)
            form_request.callback = check_login
            form_request.cb_kwargs.update({
                'selector': user_is_logged_in_selector,
                'after_login_url': after_login_url,
            })
            yield form_request
        except LoginBaseError:
            pass

    def parse(self, response):
        item = {}

        self.log(
            'If you have come this far. Congratulations. You are on 0.1.0.',
            level=logging.CRITICAL,
        )
        return item

    def _populate_rules(self):
        'Create scrapy Rule objects from the user-config.'
        raise NotImplementedError()

    def _init_user_config(self, path: str):
        'Obtain JSON file from `path` and stores it as a dict in the instance.'
        try:
            self.config_dict = user_config_parse(path)
        except UserConfigBaseException as e:
            raise CloseSpider('Could not load user configuration.')
