import requests
from bs4 import BeautifulSoup
import re
import time
import random


def get_page_source(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        response.encoding = "utf-8"
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    
def get_page_source_r(url, max_retries=4, delay=30):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = "utf-8"
            return response.text

        except requests.exceptions.RequestException as e:
            print()
            print(f"Request failed (attempt {attempt}) for {url}: {e}")
            if attempt < max_retries:
                print(f"Waiting {delay}s before retrying...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed to fetch after {max_retries} retries.")

def get_all_injuries_r(base, path):
    html = get_page_source_r(path)
    soup = BeautifulSoup(html, 'html.parser')

    Table = soup.select_one('#yw1')
    table1 = soup.select_one('#yw1 table.items')

    # 没有任何伤病史的处理
    if not table1:
        return [] 
    
    # 在这里开始，如果不存在分页，下面三个列表全部为空，代码正常运行
    all_li = Table.select('li.tm-pagination__list-item')
    last_li = [li for li in all_li if li.get('class') == ['tm-pagination__list-item']]     # 从所有li中筛选出未显示的页面
    
    last_hrefs = [li.find('a')['href'] for li in last_li if li.find('a')]
#     print(all_li, last_li, last_hrefs)

    all_table = [table1]
    for hrefs in last_hrefs:
        html = get_page_source_r(base + hrefs)
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.select_one('#yw1 table.items')
        all_table.append(table)
        time.sleep(random.uniform(8,10))

    injury_infos = []
    for table in all_table:
        rows = table.select(".even, .odd")
        for row in rows:
            injury_data = {}
            tds = row.find_all('td')
            if len(tds) < 6:
                raise IndexError("wrong table")
            injury_data['injury'] = tds[1].get_text(strip=True)
            injury_data['from'] = tds[2].get_text(strip=True)
            injury_data['util'] = tds[3].get_text(strip=True)
            injury_data['days'] = tds[4].get_text(strip=True)
            injury_data['games_missed'] = tds[5].get_text(strip=True)
            injury_infos.append(injury_data)
            
    return injury_infos