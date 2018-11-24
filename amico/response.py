#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-17
'''

import amico
import json
import w3lib.url as urltool
from amico.exceptions import NotValidJsonContent

class mdict(dict):

   def __getattr__(self, item):
       try:
           a = self[item]
       except:
           return None
       return a

class Response(object):
    def __init__(self,url,
                 status=200,
                 headers=None,
                 request=None,
                 priority=0,
                 encoding='utf-8',
                 body=None,
                 exc = None,
                 filter=False,
                 cookies=None
                 ):

        assert isinstance(request,amico.Request),\
            'not a valid Request for Response,got "%s".'%type(request).__name__

        if exc is not None:
            if not isinstance(exc, Exception):
                raise TypeError('Not an valid Exception for Response,got "%s".'
                                % type(exc).__name__)

        self.headers = headers
        self.cookies = cookies
        self.status = status
        self.request = request
        self.spider = request.spider
        self.callback = request.callback
        self.errback = request.errback
        self.excback = request.excback
        self.encoding = encoding
        self.priority = priority
        self.filter  = filter
        self._body = body
        self.exception = exc
        self.meta =mdict(request.kwargs_cb)
        self._set_url(url)

    def _set_url(self,url):
        self.url = urltool.canonicalize_url(
            urltool.safe_download_url(url),encoding=self.encoding)

    def text(self,encoding=None):
        encoding = encoding if encoding else self.encoding
        if isinstance(self._body,bytes):
            return str(self._body,encoding=encoding)
        return self._body

    def json(self):
        try:
            res  = json.loads(self._body)
            return res
        except json.decoder.JSONDecodeError as e:
            raise NotValidJsonContent(e)

    def read(self,encoding=None):
        encoding = encoding if encoding else self.encoding
        if isinstance(self._body,str):
            return bytes(self._body,encoding=encoding)
        return self._body

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self,url):
        #only starts with schema:file,http,https allowed to be a valid url
        if not urltool.is_url(url):
            raise ValueError('Not a valid url for Request.')
        else:
            self.__url = urltool.safe_download_url(url)


    def __str__(self):
        return '<Response obj at %s [status=%d url=%s] >'\
               %(hex(id(self)),self.status,self.url)

