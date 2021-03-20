import urllib.request
import logging
from bs4 import BeautifulSoup


def props(url):
    """
    This function extracts the list of properties within a street.  It is called from the streets module.
    :param url: HREF to a single street page.
    :return: List of urls to each property on a given street.
    """
    _url = url
    f = urllib.request.urlopen(_url)
    page_data = f.read()
    html_doc = page_data
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Check to make sure street page has properties
    headers_data = []
    headers = soup.find_all('span', 'min-format-tab-header')
    for header in headers:
        headers_data.append(header.text)

    if 'Properties in' in headers_data:
        try:
            spans = soup.find_all('div', 'four_column_wrapper')[0].find_all('dd')
            props = []

            for i in spans:
                # DEBUG
                # print(i.text)
                props.append(i.contents[1].attrs['href'])
            return props
        except (IndexError, TypeError) as e:
            pass
    else:
        pass
