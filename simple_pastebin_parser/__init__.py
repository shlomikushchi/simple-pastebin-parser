"""Top-level package for simple pastebin parser."""

__author__ = """Shlomi Kushchi"""
__email__ = 'shlomik@example.com'

from time import sleep

from simple_pastebin_parser.paste import Paste
from simple_pastebin_parser.utils import parse_html, Url

KNOWN_HREFS = ['/favicon.ico', '/i/pastebin.min.v9.css?1575389335', '/pro', '/api', '/faq', '/login', '/signup',
               '/archive', '/tools#chrome', '/languages', '/archive', '/faq', '/night_mode', '/dmca', '/contact']

KNOWN_PREFIXES = ['http://', 'https://', '/tools', '/doc_', '/archive/']
PASTEBIN_ARCHIVE_URL = 'https://pastebin.com/archive'


def get_posts(should_stream: bool=False, sampling_frequency=60*2):
    """
    get the current posts on pastebin.com as a snapshot.

    :return:
    """
    hrefs = []
    while 1:
        tree = parse_html(Url(PASTEBIN_ARCHIVE_URL))
        new_hrefs = get_all_hrefs_in_html(tree)

        for href in new_hrefs:
            if href not in hrefs:
                yield Paste(href)
                hrefs.append(href)
        sleep(sampling_frequency)
        if not should_stream:
            break


def get_all_hrefs_in_html(tree):
    unfiltered_hrefs = [ref for ref in tree.xpath("//@href") if ref not in KNOWN_HREFS]
    hrefs = []
    for href in unfiltered_hrefs:
        is_pastebin_href = True
        for prefix in KNOWN_PREFIXES:
            if str(href).startswith(prefix):
                is_pastebin_href = False
                break
        if is_pastebin_href:
            hrefs.append(href)

    hrefs = [href for href in hrefs if len(href) > 5]
    return hrefs

