import requests
from bs4 import BeautifulSoup

def get_soup(year,month,_EVENTTARGET=None,_VIEWSTATE=None,_VIEWSTATEGENERATOR=None,_EVENTVALIDATION=None,next_row_starts_from=11):

    cookies = {
    '_gid': 'GA1.2.1242371381.1700516880',
    'WSS_FullScreenMode': 'false',
    '_gat_GSA_ENOR0': '1',
    '_ga': 'GA1.1.859561497.1700516880',
    '_ga_CSLL4ZEK4L': 'GS1.1.1700576561.2.1.1700576900.0.0.0',
    'AWSALB': 'CHHTbWzHWZw3/aRlqw8RJ3Tx+O8ZIhTjBNsfpPsuWWgYDyrIHBznHogfLob+QEVfU6quhSPjfQZQWAkAVyQvdpBEJsTJL7ftf1J70SR+cCQgxC2hhE/MzgK2O90R',
    'AWSALBCORS': 'CHHTbWzHWZw3/aRlqw8RJ3Tx+O8ZIhTjBNsfpPsuWWgYDyrIHBznHogfLob+QEVfU6quhSPjfQZQWAkAVyQvdpBEJsTJL7ftf1J70SR+cCQgxC2hhE/MzgK2O90R',
    }

    headers = {
        'authority': 'www.ginniemae.gov',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.ginniemae.gov',
        'referer': 'https://www.ginniemae.gov/investors/disclosures_and_reports/Pages/remic_prospectuses.aspx?YearDropDown=2023&MonthDropDown=October',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    params = {
        'YearDropDown': year,
        'MonthDropDown': month,
    }

    data = {
        'YearDropDown': year,
        'MonthDropDown': month,
    }
    if _VIEWSTATE:
        data.update({    '__EVENTTARGET': _EVENTTARGET,
        '__EVENTARGUMENT': f'dvt_firstrow={{{next_row_starts_from}}};dvt_startposition={{}}',
        '__VIEWSTATE': _VIEWSTATE,
        '__VIEWSTATEGENERATOR': _VIEWSTATEGENERATOR,
        '__EVENTVALIDATION': _EVENTVALIDATION})
    response = requests.post(
        'https://www.ginniemae.gov/investors/disclosures_and_reports/Pages/remic_prospectuses.aspx',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        return False



def get_pdfs(year,month):
    btn_next = True
    next_row_starts_from = 1
    total_pdf_links = []
    soup = get_soup(year, month)
    while btn_next:

        table = soup.find("table", id="filterTable_s2")
        pagination_content = soup.find("td",class_="ms-paging")
        btn_next = pagination_content.find("img",alt="Next")
        pdf_links = table.find_all("a")
        total_pdf_links += [link.get("href") for link in pdf_links]
        next_row_starts_from += len(pdf_links)
        if btn_next:
            parent_a_tag = btn_next.find_parent('a')
            href_val = parent_a_tag.get("href")
            formatted_str = href_val.split("__doPostBack(")[1].split(",")
            _EVENTTARGET = formatted_str[0].replace("'","")
            _VIEWSTATE = soup.find("input",id="__VIEWSTATE")['value']
            _VIEWSTATEGENERATOR = soup.find("input",id="__VIEWSTATEGENERATOR")['value']
            _EVENTVALIDATION = soup.find("input",id="__EVENTVALIDATION")['value']
            soup = get_soup(year,month,_EVENTTARGET,_VIEWSTATE,_VIEWSTATEGENERATOR,_EVENTVALIDATION,next_row_starts_from)
    return total_pdf_links


