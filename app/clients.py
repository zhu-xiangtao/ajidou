# -*- coding:utf-8 -*-

import re
import time
import traceback
import requests
from requests import Response,Request
from requests.exceptions import (InvalidSchema, InvalidURL, MissingSchema,
                                 RequestException)


absolute_http_url_regexp = re.compile(r"^https?://", re.I)

class ApiResponse(Response):

    def raise_for_status(self):
        if hasattr(self, "error") and self.error:
            raise self.error
        Response.raise_for_status(self)


class HttpSession(requests.Session):

    def __init__(self):
        super(HttpSession, self).__init__()
        self.request_meta = dict()

    def _build_url(self,path):
        if absolute_http_url_regexp.match(path):
            return path
        else:
            return "%s%s" % (self.base_url, path)

    def request(self, url, method, **kwargs):
        """
        Constructs and sends a :py:class:`requests.Request`.
        Returns :py:class:`requests.Response` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional) Dictionary or bytes to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long in seconds to wait for the server to send data before giving up, as a float,
            or a (`connect timeout, read timeout <user/advanced.html#timeouts>`_) tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response content. Defaults to ``False``.
        :param verify: (optional) if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        """

        # set up pre_request hook for attaching meta data to the request object
        self.request_meta["method"] = method
        self.request_meta["start_time"] = time.time()

        response = self._send_request_safe_mode(method, url, **kwargs)

        # record the consumed time
        self.request_meta["end_time"] = time.time()

        # get the length of the content, but if the argument stream is set to True, we take
        # the size from the content-length header, in order to not trigger fetching of the body
        if kwargs.get("stream", False):
            self.request_meta["content_size"] = int(response.headers.get("content-length") or 0)
        else:
            self.request_meta["content_size"] = len(response.content or b"")

        self.request_meta["content_type"] = response.headers.get("Content-Type")
        self.request_meta["status_code"] = response.status_code
        try:
            response.raise_for_status()
            self.request_meta["status"] = "success"
        except RequestException as e:
            self.request_meta["status"] = "error"
            self.request_meta["message"] = traceback.format_exc()

        return response

    def _send_request_safe_mode(self, method, url, **kwargs):
        """
        Send an HTTP request, and catch any exception that might occur due to connection problems.

        Safe mode has been removed from requests 1.x.
        """
        try:
            return requests.Session.request(self, method, url, **kwargs)
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except RequestException as e:
            r = ApiResponse()
            r.status_code = 0
            r.error = e
            r.request = Request(method, url).prepare()
            return r


