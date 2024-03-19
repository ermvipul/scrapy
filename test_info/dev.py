import time
import datetime
import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4
import pandas as pd # pip install pandas

def main(query_url):
    try:
        headers= {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        base_url = query_url

        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        total_results = int(soup.find('span', 'totalcount').text)
        total_pages = (total_results // 120) + 1

        search_results = []

        for i in range(0, total_pages):
            params = {
                's': i*120        
            }
            print('Processing Page {0}'.format(i+1))

            response = requests.get(base_url, headers=headers, params=params)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = soup.find('ul', {'id': 'search-results'})
            result_rows = results.find_all('li', 'result-row')

            for result_row in result_rows:
                post_datetime = result_row.time['datetime']
                post_id = result_row.h3.a['data-id']
                post_url = result_row.h3.a['href']
                price = result_row.find('span', 'result-price').text
                location = result_row.find('span', 'result-hood').text if result_row.find('span', 'result-hood') else ''
                post_title = result_row.h3.a.text
                search_results.append([
                    post_datetime, post_id, post_url, price, location, post_title
                ])
            time.sleep(1)

        columns = ('Post Date', 'Post Id', 'Post Url', 'Price', 'Location', 'Post title')
        df = pd.DataFrame(search_results, columns=columns)
        timestamp = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')
        df.to_csv(f'Craigslist Results ({timestamp}).csv', index=False)
        print('File Exported')
    except Exception as e:
        print(e)

main('https://sfbay.craigslist.org/d/for-sale/search/sfc/sss?query=playstation%205')