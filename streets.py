import csv
import urllib.request
from urllib.error import HTTPError
import time
import datetime
import logging
from bs4 import BeautifulSoup
from properties import props
from listing import listing


def extractor(suburb, code):
    """
    This function extracts a list of streets in a suburb, and then each property on a street.
    It collects a range of statistics from the listing and only retains properties that contain
    past sales history.
    There is no automated way to ensure the URL remains correct.  If a page breaks, go to Allhomes:
        1) search for desired suburb
        2) select any listing
        3) scroll down to suburb profile and click through to suburb profile main page
        4) copy link
        5) save suburb text and numeric code to dictionary in the main module
    :param suburb: obtained from the locations dictionary in the main module.
    :param code: this is added to all Allhomes suburb pages (and is likely to change over time).
    :return: None.  Function saves extracted data to csv with suburb name.
    """
    base_url = 'https://www.allhomes.com.au/ah/research/'
    _suburb = suburb
    _code = code
    url = base_url + '{}/'.format(_suburb) + '{}'.format(_code)
    logging.info(f'Url: {url}')
    try:
        f = urllib.request.urlopen(url)
        page_data = f.read()
        html_doc = page_data
        soup = BeautifulSoup(html_doc, 'html.parser')

        # get all the page headers
        spans = soup.find_all('span', 'min-format-tab-header')

        matches = []

        # loop through headers and find node with links to streets and save to matches list
        for match in spans:
            # print(match.string)
            if match.string == 'Streets in':
                matches.append(match)

        # get all the 'dd' elements under the parent node of the streets header
        match_parent = matches[0].parent.parent.find_all('dd')

        streets = []

        # loop through list of elements and extract the url for the street and save to streets list
        for i in match_parent:
            streets.append(i.contents[1].attrs['href'])

        # DEBUG
        # print(streets)

        properties = []

        # for each street, call the props function and get the property urls and save to properties list
        for street in streets:
            # DEBUG
            # print(street)
            # get all property urls
            _data = props(street)
            if _data:
                for i in _data:
                    properties.append(i)
            else:
                pass

        listings = []

        # for each property url, call the listing function to extract data and append to the listings list
        for prop in properties:
            # DEBUG
            logging.info(prop)
            _data = listing(prop)
            listings.append(_data)
            # best to run late at night but can add in crawler delay (in secs)
            # time.sleep(1)

        # filter out properties with no data (i.e. no prior sales data) from listings
        data1 = list(filter(None, listings))
        data = []
        # loop through returned list and flatten to a single list
        for item in data1:
            for i in item:
                data.append(i)

        # save list of dictionaries to csv
        file = open('{}.csv'.format(_suburb), 'w+', newline='')
        keys = data[0].keys()

        logging.info(f'Rows: {len(data)}')
        logging.info(f'Keys: {keys}')
        with file:
            write = csv.DictWriter(file, keys)
            write.writeheader()
            try:
                write.writerows(data)
            except ValueError as e:
                logging.warning(f'Could not write to file: {e}')
                pass
        logging.info(f'End: {datetime.datetime.now()}')
    except HTTPError:
        logging.warning(f'Failed with HTTP Error: {url}')
        pass
