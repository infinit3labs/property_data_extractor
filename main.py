import datetime
from streets import extractor


""" 
These modules are developed for adhoc property research.  It explores historical sales data for properties
in a given suburb.  The data is saved in a format ready for analysis.  There is no provision for finding
new data over a time period, but it would be a useful feature.

Data is only retained for properties that have historical sales.  It does not extract data on all listings.

Unfortunately there is no API on Allhomes so these scripts are fragile to any CSS changes.  Thankfully they
have used some unique class codes which helps to target specific data on the page.

This does generate a reasonable amount of site traffic but there is no parallel processing which should make
the crawler more palatable to the IT team.  Nevertheless, best to run late at night in off-peak times.

This is a private project.  I have no association with Allhomes and it is not intended for commercial use.
"""


# Add/remove as required - data must be manually obtained from the Allhomes website. See instructions in the
# streets module.
locations = {
    # 'phillip': '121467610',
    # 'holt': '121472810',
    # 'cook': '121463510',
    # 'kingston': '121488910',
    # 'queanbeyan-east': '121465610',
    # 'queanbeyan': '121451510',
    # 'crestwood': '121428910',
    # 'karabar': '121470510',
    # 'melba': '121466010',
    # 'macquarie': '121458810',
    # 'belconnen': '121477710',
    # 'lyneham': '121479010',
    # 'turner': '121468510',
    # 'o-connor': '121479210',
    'braddon': '121483810',
    'griffith': '121475410',
    'garran': '121492310',
    'lyons': '121482910',
    'hughes': '121493910',
    'curtin': '121496110',
    'kambar': '121477510'
}

keys = locations.keys()

for key in keys:
    print('Start:', datetime.datetime.now())
    extractor(suburb=key, code=locations[key])
