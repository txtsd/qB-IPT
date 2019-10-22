# VERSION: 1.01
# AUTHORS: txtsd (thexerothermicsclerodermoid@gmail.com)

# iptorrents.py - A plugin for qBittorrent to search on iptorrents.com
# Copyright (C) 2019  txtsd <thexerothermicsclerodermoid@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from helpers import htmlentitydecode
from novaprinter import prettyPrinter
import re
import tempfile
import io
import gzip
# Some other imports if necessary
import urllib.request as request
from urllib.parse import urlencode, quote
from http.cookiejar import CookieJar
# Logging
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class iptorrents(object):
    # Login information ######################################################
    #
    # SET THESE VALUES!!
    #
    username = ""
    password = ""
    ###########################################################################
    url = 'https://iptorrents.com'
    name = 'IPTorrents'
    supported_categories = {
        'all': '',
        'movies': '72',
        'tv': '73',
        'music': '75',
        'games': '74',
        'anime': '60',
        'software': '1',
        'pictures': '36',
        'books': '35'
    }

    def __init__(self):
        """
        Class initialization
        Requires personal login information
        """
        self.ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
        self.session = None

        self._login()

    def _login(self):
        """Initiate a session and log into IPTorrents"""
        # Build opener
        cj = CookieJar()
        params = {
            'username': self.username,
            'password': self.password
        }
        session = request.build_opener(request.HTTPCookieProcessor(cj))

        # change user-agent
        session.addheaders.pop()
        session.addheaders.append(('User-Agent', self.ua))
        session.addheaders.append(('Referrer', self.url + '/login.php'))

        # send request
        try:
            logging.debug("Trying to connect using given credentials.")
            logging.debug(self.url + '/take_login.php')
            logging.debug(urlencode(params).encode('utf-8'))
            session.open(
                self.url + '/take_login.php',
                urlencode(params).encode('utf-8')
            )
            logging.debug("Connected using given credentials.")
            self.session = session
        except request.URLError as errno:
            print("Connection Error: {}".format(errno.reason))

    def _get_link(self, link):
        """Return the HTML content of url page as a string """
        try:
            logging.debug("Trying to open " + link)
            res = self.session.open(link)
        except request.URLError as errno:
            print("Connection Error: {}".format(errno.reason))
            return ""

        charset = 'utf-8'
        info = res.info()
        try:
            _, charset = info['Content-Type'].split('charset=')
        except:
            pass
        data = res.read()
        data = data.decode(charset, 'replace')

        data = htmlentitydecode(data)
        return data

    def search_parse(self, link, page=1):
        """ Parses IPTorrents for search results and prints them"""
        logging.debug("Parsing " + link)
        data = self._get_link(link + '&p=' + str(page))
        _tor_table = re.search('<form>(<table id=torrents.+?)</form>', data)
        tor_table = _tor_table.groups()[0] if _tor_table else None

        results = re.finditer(
            '<a class=" hv" href="(?P<desc_link>/details.+?)">(?P<name>.+?)</a>.+?href="(?P<link>/download.+?)".+?(?P<size>\d+?\.*?\d*? (|K|M|G)B)<.+?t_seeders">(?P<seeds>\d+).+?t_leechers">(?P<leech>\d+?)</t',
            tor_table
        )

        for result in results:
            entry = dict()
            entry['link'] = self.url + quote(result.group('link'))
            entry['name'] = result.group('name')
            entry['size'] = result.group('size')
            entry['seeds'] = result.group('seeds')
            entry['leech'] = result.group('leech')
            entry['engine_url'] = self.url
            entry['desc_link'] = self.url + result.group('desc_link')
            prettyPrinter(entry)

        _num_pages = re.search('<a>Page <b>(\d+)</b> of <b>(\d+)</b>', data)
        page = _num_pages.groups()[0] if _num_pages else None
        num_pages = _num_pages.groups()[1] if _num_pages else None

        if (page and num_pages) and (int(page) < int(num_pages)):
            next_page = str(int(page) + 1)
            self.search_parse(link, next_page)

    def download_torrent(self, info):
        """
        Downloads torrent to a temp file and loads it in qBittorrent
        """
        file, path = tempfile.mkstemp('.torrent')
        url = info
        # self._login()
        try:
            logging.debug("Trying to download " + url)
            res = self.session.open(url)
        except request.URLError as errno:
            print("Connection Error: {}".format(errno.reason))
            return ""
        data = res.read()
        if data[:2] == b'\x1f\x8b':
            # Data is gzip encoded, decode it
            logging.debug("Data is gzip encoded, decode it")
            compressedstream = io.BytesIO(data)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            extracted_data = gzipper.read()
            data = extracted_data
        with open(file, 'wb') as f:
            f.write(data)
        print(path + " " + url)

    def search(self, what, cat='all'):
        """
        Formats url according to category and calls search_parse()
        """
        if cat == 'all':
            url = "{0}/t?q={1}&o=seeders".format(
                self.url,
                what
            )
        else:
            url = "{0}/t?{1}=&q={2}&o=seeders".format(
                self.url,
                self.supported_categories[cat],
                what
            )
        self.search_parse(url)


# For testing purposes.
# Run with python -m engines.iptorrents
if __name__ == "__main__":
    engine = iptorrents()
    engine.search('one+piece')
    # engine.download_torrent('')
