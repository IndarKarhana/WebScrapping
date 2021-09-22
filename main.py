# Libraries
import requests
from bs4 import BeautifulSoup
import json
import csv
import re
import time


class GoogleScraper:
    # Crawler entry point
    base_url = 'https://www.google.com/search'
    
    # Query string parameters to crawl through results pages
    pagination_params = {
        'sa': 'N',
        'rlz': '1C1NHXL_enIN802IN802',
        'tbs': 'lf:1,lf_ui:3',
        'tbm': 'lcl',
        'sxsrf': 'AOaemvKiKXNKleFGrBBM_osTBGvNrQqjSg:1632246266766',
        'q': 'pharmaceutical stores in india',
        'rflfq': '1',
        'num': '10',
        'ved': '2ahUKEwjL_qmXz5DzAhULH7cAHbNiAysQjGp6BAgHEEU',
        'biw': '656',
        'bih': '645',
        'dpr': '1'
    }
    
    # Query string parameters for initial results page
    initial_params = {
        'q': '',
        'rlz': '1C1NHXL_enIN802IN802',
        'sxsrf': 'AOaemvIHt-qMn9hq0RO6TI7H5aL1Ch_Wwg:1632236606159',
        'ei': 'PvRJYbejCYb0rQH5n6bwDw',
        'start': '',
        'sa': 'N',
        'ved': '2ahUKEwi3uuWYq5DzAhUGeisKHfmPCf44MhDy0wN6BAgBEDY',
        'biw': '1358',    
        'bih': '645',
        'dpr': '1'
    }
    
    # Request headers
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'cookie': 'SID=BAjXRR2X2jgd5Cn08rNUMFpdyNuLGRLeTD73fFWfXY8OWmad3wuWQ4-pmgBN4UrDHd0wgw.; __Secure-1PSID=BAjXRR2X2jgd5Cn08rNUMFpdyNuLGRLeTD73fFWfXY8OWmadiiJIo847evtrX_xxsTpceA.; __Secure-3PSID=BAjXRR2X2jgd5Cn08rNUMFpdyNuLGRLeTD73fFWfXY8OWmadzLImUADNXrV83Mh8_zt_-A.; HSID=AaUJI9NK2pZUF69qo; SSID=At5VevoBVq_LsghaR; APISID=-v1o-EgE_6hA0Nkt/AmQpw751cxpsOOLVQ; SAPISID=CXht6UkiQ-qljC22/AWuW1FvRWcRpid72I; __Secure-1PAPISID=CXht6UkiQ-qljC22/AWuW1FvRWcRpid72I; __Secure-3PAPISID=CXht6UkiQ-qljC22/AWuW1FvRWcRpid72I; SEARCH_SAMESITE=CgQIsJMB; NID=511=V9sANw0mcYuK60SohVrUubuw3KnS8IdYOKgWa76mDSPVG2RKB04IsUFiSOTwQHtGNMVJq0Ihm9F6WMuSO-BU15Dn7OeNN_-ghO4GnBh1L8TyQw3bG2HERk_IRV9OjzCftujE25v5LJSxuS2xZjlFnqr1V_FXR1fZLmGlsdn5xDQ_1q3cwHHSKvfdem2W--uDGQhQz8sT47ewVmFd1Gfkr7PFS2eSvs9YmOcDaS69HEl-ZIWVaDLPw9eMuVuXXhtR6A; 1P_JAR=2021-09-21-16; SIDCC=AJi4QfFox4hpEe3KYKngrYn45Relk80vfOnQ9YFwS_9uIEh1aHdn4dmHiyWoeYaDbfBrT78nR0VH; __Secure-3PSIDCC=AJi4QfFlR8s9DCiWWGG_czcjpnIoX-LsvEqRPv8H8TnXdFrh5hGeOkhFHkPhWwqq5mV_CH4PuR4; DV=ExlMVmiTFYxDUOUcLYCoi45bdzmUwJdvU3dyzytndAIAAGCqGssnH9E8vQAAAPCSFA-qpoSSOgAAAA',
        'dnt': '1',
        'referer': 'https://www.google.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    
    # Scraped results
    results = []
    
    def fetch(self, query, page):
        '''Makes HTTP GET request to fetch search results from google'''
        
        # Init initial_params search query (e.g. "linux mint")
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
        
        # Make HTTP GET request
        response = requests.get(self.base_url, params=params, headers=self.headers)
        print('HTTP GET request to URL: %s | Status code: %s' % (response.url, response.status_code))
        
        # Return HTTP response
        return response
        
    def parse(self, html):
        '''Parses response's text and extract data from it'''
        
        # Parse content
        content = BeautifulSoup(html, 'html.parser')
        
        # Extract data
        title_elements = content.findAll('div', {'class': 'dbg0pd'})
        title = [title.text for title in title_elements]
        contact_details_elements = content.findAll('div', {'class': 'rllt__deails'})
        contact_details = [contact_details.text for contact_details in contact_details_elements]
        content.find_all()
        
        # Loop over the number of entries
        for index in range(0, len(title)):
            # Append extracted data to results list
            self.results.append({
                'title': title[index],
                'contact_details': contact_details[index]
            })
    
    def write_csv(self):
        '''Writes scpared results to CSV file'''
        
        # Check results list in not empty
        if len(self.results):
            print('Writing results to "res.csv"... ', end='')
            
            # Open file stream to write CSV
            with open('res.csv', 'w') as csv_file:
                # Init CSV dictionary writer
                writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
                
                # Write column names to file
                writer.writeheader()
                
                # Write results list to CSV file
                for row in self.results:
                    writer.writerow(row)
            
            print('Done')
       
    def store_response(self, response):
        '''Stores HTML response to file for debugging parser'''
        
        # If response is OK
        if response.status_code == 200:
            print('Saving response to "res.html"... ', end='')
            
            # Write response to HTML file
            with open('res.html', 'w') as html_file:
                html_file.write(response.text)
            
            print('Done')
        else:
            print('Bad response!')
    
    def load_response(self):
        '''Loads HTML response for debugging parser'''
        html = ''
        
        # Open HTML file
        with open('res.html', 'r') as html_file:
            for line in html_file.read():
                html += line
        
        # Return HTML as string
        return html
        
    def run(self):
        '''Starts crawler'''
        
        # Loop over the range of pages to scrape
        for page in range(0, 5):
            # Make HTTP GET request
            response = self.fetch('linux mint', page)
            
            # Parse content
            self.parse(response.text)
            
            # Wait for 5 sec            
            time.sleep(5)
        
        # Write scraped results to CSV file
        self.write_csv()


# Main driver
if __name__ == '__main__':
    scraper = GoogleScraper()
    scraper.run()

