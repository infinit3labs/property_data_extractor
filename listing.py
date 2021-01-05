import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def listing(url):
    """
    This function uses unique class codes used on a property listing page to extract data.
    It is probable that these codes will change as the site is modified over time.
    :param url: HREF to a single property page.
    :return: List of dictionaries with data about a single property.
    Multiple entries exist if the property has multiple past sales history.
    """
    url = url
    try:
        f = urllib.request.urlopen(url)
        page_data = f.read()
        html_doc = page_data
        soup = BeautifulSoup(html_doc, 'html.parser')

        # DEBUG
        # print(url)

        if soup.find_all('div', 'css-1waaw1k'):

            # this is returned after data extracted
            data = []

            try:
                prop_type = soup.find_all('span', 'css-1m19ztq')[0].string
            except IndexError:
                prop_type = 'N/A'

            listing_details = soup.find_all('span', 'css-8dprsf')

            listing_details_data = {}

            if listing_details:
                for i in listing_details:
                    _val = i.find_all('span')[0].text
                    _type = i.find_all('svg')[0].text
                    listing_details_data[_type] = _val

            try:
                bedrooms = listing_details_data['bedrooms']
            except KeyError:
                bedrooms = 'N/A'
            try:
                bathrooms = listing_details_data['bathrooms']
            except KeyError:
                bathrooms = 'N/A'
            try:
                garages = listing_details_data['garage spaces']
            except KeyError:
                garages = 'N/A'
            try:
                eer = listing_details_data['EER']
            except KeyError:
                eer = 'N/A'

            key_details_data = {}

            key_details = soup.find_all('div', 'css-hboir5')

            if key_details:
                for detail in key_details:
                    try:
                        _key = detail.find_all('span', 'css-nqo9lc')[0].text.split(':')[0]
                    except IndexError:
                        try:
                            _key = detail.find_all('span', 'css-nqo9lc')[0].text
                        except IndexError:
                            _key = 'N/A'
                    try:
                        _val = detail.find_all('span', 'css-5hg4fg')[0].text
                    except IndexError:
                        _val = 'N/A'
                    key_details_data[_key] = _val

            try:
                uv = key_details_data['Unimproved Value'].split(' ')[0]
            except KeyError:
                uv = 'N/A'
            try:
                uv_year = key_details_data['Unimproved Value'].split(' ')[1].split('(')[1].split(')')[0]
            except KeyError:
                uv_year = 'N/A'
            try:
                block_size = key_details_data['Block Size'].split(' ')[0]
            except KeyError:
                block_size = 'N/A'
            try:
                house_size = key_details_data['House Size'].split(' ')[0]
            except KeyError:
                house_size = 'N/A'
            try:
                townhouse_size = key_details_data['Townhouse Size'].split(' ')[0]
            except KeyError:
                townhouse_size = 'N/A'
            try:
                apartment_size = key_details_data['Apartment Size'].split(' ')[0]
            except KeyError:
                apartment_size = 'N/A'

            prev_sale_spans = soup.find_all('div', 'css-1waaw1k')

            if prev_sale_spans:
                for i in prev_sale_spans:
                    prop = soup.title.text.split(' -')[0]
                    sale_type = i.find_all('div', 'css-xscdvh')[0].string
                    price = i.find_all('div', 'css-a2p3z9')[0].string
                    if price is None:
                        price = 'N/A'
                    details = i.find_all('div', 'css-104pj7g')

                    _data = {}
                    prev_sale_details_data = {}

                    if details:
                        for detail in details:
                            _key = detail.text.split(': ')[0]
                            _val = detail.text.split(': ')[1]
                            prev_sale_details_data[_key] = _val

                    try:
                        contract = prev_sale_details_data['Contract']
                    except KeyError:
                        contract = 'N/A'
                    try:
                        tfer_date = prev_sale_details_data['Transfer']
                    except KeyError:
                        tfer_date = 'N/A'
                    try:
                        listed_date = prev_sale_details_data['Listed']
                    except KeyError:
                        listed_date = 'N/A'
                    try:
                        days_mkt = prev_sale_details_data['Days on market']
                    except KeyError:
                        days_mkt = 'N/A'

                    # For a property on the market or recently sold, this is the footer info with stats like:
                    # number of views, date of listing, last update date.
                    try:
                        listing_info = soup.find_all('div', 'css-rklfmn')[0].text
                    except IndexError:
                        listing_info = 'N/A'

                    _data['property'] = prop

                    if prop_type:
                        # TODO: Prop type can also be extracted from key details but is now taken from the main
                        # listing details block.  Many cases the logic fails and returns N/A.
                        _data['prop_type'] = prop_type
                    if sale_type:
                        _data['sale_type'] = sale_type
                    if price:
                        _data['price'] = price
                    if bedrooms:
                        _data['bedrooms'] = bedrooms
                    if bathrooms:
                        _data['bathrooms'] = bathrooms
                    if garages:
                        _data['garages'] = garages
                    if eer:
                        _data['eer'] = eer
                    if contract:
                        _data['contract_date'] = contract
                    if tfer_date:
                        _data['tfer_date'] = tfer_date
                    if listed_date:
                        _data['list_date'] = listed_date
                    if days_mkt:
                        _data['days_on_mkt'] = days_mkt
                    if block_size:
                        _data['block_size'] = block_size
                    if house_size:
                        _data['house_size'] = house_size
                    if townhouse_size:
                        _data['townhouse_size'] = townhouse_size
                    if apartment_size:
                        _data['apartment_size'] = apartment_size
                    if uv:
                        _data['unimp_val'] = uv
                    if uv_year:
                        _data['unimp_val_year'] = uv_year
                    if listing_info:
                        _data['info'] = listing_info

                    data.append(_data)

                return data
    except HTTPError:
        print('Failed with HTTP Error:', url)
        pass
