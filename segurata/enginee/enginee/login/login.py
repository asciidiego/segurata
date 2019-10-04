import scrapy
from loginform import fill_login_form
from scrapy import FormRequest, Request
from scrapy.http import Response

from .exceptions import *


def login_request(
            response: Response,
            *args,
            credentials: dict,
            **kwargs
        ):
    """Create a form request using the HTTP response and the
    credentials provided.

    Arguments:
        response {Response} --
        credentials {dict} -- contain username and password key-value pairs.
    Return:
        FormRequest
    """
    # BUG: What if there is no username AND no password

    formdata, login_url, _reqType = fill_login_form(
        url=response.url,
        body=response.body_as_unicode(),
        username=credentials['username'],
        password=credentials['password'],
    )

    return FormRequest(
        url=login_url,
        formdata=formdata,
        method='POST',
        callback=dumb_callback,
        meta={'cookiejar': 0},
    )


def check_login(response: Response, **kwargs) -> Request:
    'Return a parametric Request if the user is logged in.'
    check_login_selector = kwargs.get('selector')
    matching_elements = response.css(check_login_selector)

    if not matching_elements:
        raise NotLoggedInError()

    after_login_url = kwargs.get('after_login_url')

    return Request(
        url=after_login_url,
        meta={'cookiejar': 0},
    )


def dumb_callback(response: Response) -> None:
    raise NotImplementedError('You must select a valid callback.')
