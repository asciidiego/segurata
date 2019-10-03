import scrapy
from loginform import fill_login_form
from scrapy import Request, FormRequest
from .exceptions import *

def do_login(response: scrapy.http.Response):
    """Tries to login using a form created with the credentials provided in the response.

    Arguments:
        response {scrapy.http.Response} -- 
    Return:
        FormRequest
    """
    credentials = response.meta['credentials']
    
    formdata, login_url, _reqType = fill_login_form(
        url=response.url,
        body=response.body_as_unicode(),
        username=credentials['username'],
        password=credentials['password'],
    )

    return FormRequest(
        url=login_url,
        formdata=formdata,
        callback=check_login,
        meta={'cookiejar': 0}
    )

def check_login(response: scrapy.http.Response):
    raise NotImplementedError()