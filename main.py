import time
import requests
import logging
from bs4 import BeautifulSoup
from cachetools.func import lru_cache
from fake_useragent import UserAgent


@lru_cache(maxsize=100)  # Decorate the function with lru_cache

def parse(html):
    """Parses response's text and extracts data from it"""
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all('div', {'class': 'yuRUbf'})
    for item in content:
        try:
            title = item.find('h3', {'class': 'LC20lb MBeuO DKV0Md'}).text.strip()
        except AttributeError:
            title = ""
        try:
            link = item.a['href']
            #print(link)
        except (AttributeError, KeyError):
            link = ""
        except Exception as e:
            logging.error("Error processing search result: %s", str(e))
            continue
        # Yield the link
        yield link

class GoogleScraper:
    """Class for scraping Google search results"""

    def __init__(self, country='us', language='en-us'):
        self.language = language
        self.country = country
        self.extracted_links = []  # Initialize an empty list to store links

    base_url = 'https://www.google.com/search?q='
    # Query string parameters to crawl through results pages
    pagination_params = {
        'q': '',
        'sxsrf': 'ACYBGNRmhZ3C1fo8pX_gW_d8i4gVeu41Bw:1575654668368',
        'ei': 'DJXqXcmDFumxrgSbnYeQBA',
        'start': '',
        'sa': 'N',
        'ved': '2ahUKEwjJua-Gy6HmAhXpmIsKHZvOAUI4FBDy0wN6BAgMEDI',
        'biw': '811',
        'bih': '628'
    }
    # Query string parameters for initial results page
    initial_params = {
        'sxsrf': 'ACYBGNQ16aJKOqQVdyEW9OtCv8zRsBcRig:1575650951873',
        'source': 'hp',
        'ei': 'h4bqXcT0MuPzqwG87524BQ',
        'q': '',
        'oq': '',
        'gs_l': 'psy-ab.1.1.35i362i39l10.0.0..139811...4.0..0.0.0.......0......gws-wiz.....10.KwbM7vkMEDs'
    }


    def fetch(self, query, page):
        """Makes HTTP GET request to fetch search results from Google"""
        # Init initial_params search query (e.g. "data scrape")
        # Request headers
        ua = UserAgent()
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'cache-control': 'no-cache',
            'cookie': 'CGIC=InZ0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIz; HSID=AenmNVZxnoADsXz_x; SSID=AjbLhhwkjh8f3FOM8; APISID=IqkNtUA0V2DXlees/A0tA9iPSadMC2X6dt; SAPISID=8-N4B06I_D5N1mvR/AleccT6Zt0QllrukC; CONSENT=YES+UA.en+; OTZ=5204669_48_48_123900_44_436380; SID=rAd3UAFN_dCIGQ87HqDZZGiNyxdz0dL4dZKy_XquqSr_CHTzqSzfDdNTfLmA2xCMEZOZMA.; ANID=AHWqTUnDWUSHdvWhJiIoPxMAKYXmVtHCQIq7LBMYgiSlZZr3AMGTwY2aVUdjeY7z; NID=193=QImFbOa1vnKpflG8yJytqPXbJYJ9k8fWbIzQMGExsMa4g5oJwdnI56WNjgEVFAyAPJ1SEEOQ-zlW4HAUv-JLj0yAUImTgeT1syDIgFTMWAqxdz10lWRlzFC-3Fmjv6xJcqm2o6RKI50dmb7GetiheNdSAYPkAjng_c0lOHoXZLmtMwFOpkPTrQwVyUW8R2x4o1ux3OW3_kEbR_BREowRV8lVqrsnyo1ffC_Pm40zf81k7aS0cv9esYweGHF6Lxd532z4wA; 1P_JAR=2019-12-06-16; DV=k7BRh0-RaJtZsO9g7sjbrkcKoUjC7RYhxDh5AdfYgQAAAID1UoVsAVkvPgAAAFiry7niUB6qLgAAAGCQehpdCXeKnikKAA; SEARCH_SAMESITE=CgQIvI4B; SIDCC=AN0-TYv-lU3aPGmYLEYXlIiyKMnN1ONMCY6B0h_-owB-csTWTLX4_z2srpvyojjwlrwIi1nLdU4',
            'pragma': 'no-cache',
            'referer': 'https://www.google.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': ua.random
        }
        try:
            self.initial_params['q'] = query
            # If getting the first results page
            if not page:
                # Use initial params
                params = self.initial_params
            # Otherwise we're scraping the following pages
            else:
                # Use pagination params
                params = self.pagination_params
                # Specify page number in format page * 10
                params['start'] = str(page * 10)
                # Init search query
                params['q'] = query
            params['gl'] = self.country
            params['hl'] = self.language
            # Make HTTP GET request
            response = requests.get(self.base_url, params=params, headers=headers)
            response.raise_for_status()  # Raise exception for non-200 status codes

            # Calculate the delay based on response time
            delay = max(1, int(response.elapsed.total_seconds()))  # Minimum delay of 1 second
            logging.info('HTTP GET request to URL: %s | Status code: %s', response.url, response.status_code)
            #print('HTTP GET request to URL: %s | Status code: %s' % (response.url, response.status_code))
            time.sleep(delay)  # Adjusted delay based on response time
            # Return HTTP response
            return response
        except requests.exceptions.RequestException as e:
            logging.info(" Error during HTTP Get request : %s", str(e))
            # Increase delay on error
            time.sleep(5)
            return None

    def run(self, query):
        """
        Runs the scraping process for the given query.
        """
        for page in range(0, 15):
            response = self.fetch(query, page)
            if response:
                html = response.text  # Extract the HTML content
                links = parse(html)
                self.extracted_links.extend(links)  # Store links in the extracted_links list
                return self.extracted_links  # Return the extracted_links


if __name__ == '__main__':
    scraper = GoogleScraper()
