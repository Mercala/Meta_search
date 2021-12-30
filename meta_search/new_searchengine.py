#!/usr/bin/env python3

import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import requests
import datetime
import re
from keywords import fraud, pep, terror
import tag

img_compliance = 'https://media-exp1.licdn.com/dms/image/C4E0BAQHkZvu6YUpqhA/company-logo_200_200/0/1553651588715?e=2159024400&v=beta&t=V8jZHXQqBBy5mnhfXG-IqkHyFbdXRZj_OOOmiJn1fps'
img_sparta = 'https://www.creativefabrica.com/wp-content/uploads/2019/03/Spartan-helmet-logo-vector-by-DEEMKA-STUDIO-4-580x406.jpg'
img_digital_forensics = 'https://www.sec64.com/img/cyber-security/it-digital-forensics.jpg'

hide_streamlit_style = """
            <style>
            @media print {
              body {
                -webkit-print-color-adjust: exact;
              }
              .customClass{
                 //customCss + !important;
              }
              //more of your custom css
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Current date
today = datetime.datetime.today()


HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }


@st.cache
def get_serp_google(search_term):

    global HEADERS
    url = 'https://www.google.com/search?q='

    for i in range(0, 10*4, 10):

        search = url + urllib.parse.quote_plus(search_term) + f'&start={i}'

        response = requests.get(search, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Catch no hits page
        p = soup.find('p', {'aria-level':"3"})
        if not p:

            divs = soup.findAll('div', class_="tF2Cxc")

    return [('Google', div.a['href']) for div in divs]


@st.cache
def get_serp_bing(search_term):

    global HEADERS
    search = urllib.parse.quote(search_term)

    for i in range(0, 40, 10):

        response = requests.get(f'https://www.bing.com/search?q={search}&first={i}', headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')

        lis = soup.findAll('li', class_="b_algo")

    return [('Bing', li.a['href']) for li in lis if li.p.span]


def get_serp_duckduckgo(search_term):

    search = urllib.parse.quote_plus(search_term)
    url = 'https://lite.duckduckgo.com/lite/&q=' + search

    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    tds = soup.findAll('td', valign='top')

    return [('Duckduckgo', td.find_next_sibling().a['href']) for td in tds]


def get_serp_yahoo(search_term):

    search = urllib.parse.quote(search_term)

    lst = []
    for i in range(0, 7*4, 7):

        response = requests.get(f'https://search.yahoo.com/search?q={search}&b={i}', headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')

        h3s = soup.findAll('h3')

        for h3 in h3s:
            if h3.a and 'RU' in h3.a['href']:

                result = re.search(r'RU=(.*)RK=', h3.a['href']).group(1)
                lst.append(urllib.parse.unquote(result))

    return lst


def search_cn(search_term):

    params = {
            's': f'{search_term}'
        }

    # url, request and soupify
    url = 'https://caribischnetwerk.ntr.nl/'
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        lst = []
        pagination = soup.find('ul', class_='pagination')
        if pagination:
            last_li = pagination.findAll('li')[-1]
            # catch last page for results less than 5 pages long
            if last_li.get_text(strip=True) == 'laatste':
                result = re.search(r'/page/(\d+)/', last_li.a['href'])
                if result:
                    last_page = int(result.group(1))

            else:
                last_li = pagination.findAll('li')[-2]
                result = re.search(r'/page/(\d+)/', last_li.a['href'])
                if result:
                    last_page = int(result.group(1))

            hrefs = [f"https://caribischnetwerk.ntr.nl/page/{page}/?s={params['s']}" for page in range(1, last_page + 1)]
            for href in hrefs:
                response = requests.get(href, headers=HEADERS)
                soup = BeautifulSoup(response.content, 'lxml')
                for article in soup.find('main').findAll('article'):
                    if article.find('h2').find('a'):
                        lst.append(('CN', f"{article.find('h2').a['href']}"))

            return lst

        else:
            for article in soup.find('main').findAll('article'):
                # Catch No Results
                if article.get_text(strip=True) != 'Geen zoekresultaten.':
                    lst.append(('CN', f"{article.find('h2').a['href']}"))

            return lst


def search_ad(search_term):

    params = {
        'searchword': f'{search_term}',
        'ordering': 'newest',
        'searchphrase': 'all',
        'limit': '100'
    }

    url = 'https://antilliaansdagblad.com/component/search/'
    response = requests.get(url, headers=HEADERS, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    if soup.find('div', class_="searchintro").get_text(strip=True) != 'Totaal:0resultaten gevonden.':
        dts = soup.find('dl').findAll('dt')

        return [('AD', f"https://antilliaansdagblad.com{dt.a['href']}") for dt in dts]

    else:
        return []


def search_dclp(search_term):

    global HEADERS

    params = {
        'searchword': f'{urllib.parse.quote(search_term)}',
        'searchphrase': 'all'
    }

    url = 'http://www.dutchcaribbeanlegalportal.com/search'
    base_url = 'http://www.dutchcaribbeanlegalportal.com/'

    response = requests.get(url, params=params, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    dts = soup.findAll('dt', class_="result-title")

    return [('DCLP', f"{base_url}{dt.a['href']}") for dt in dts if dt.a]



@st.cache
def get_paragraphs(url):

    global user_input
    lst_paragraphs = set()

    if not url.endswith('.pdf'):

        try:
            response = requests.get(url, headers=HEADERS, allow_redirects=False, timeout=3)
            response.raise_for_status()

            if re.search(f'{user_input}', response.text, flags=re.I):

                soup = BeautifulSoup(response.text, 'html.parser')

                if not url.startswith('http://www.dutchcaribbeanlegalportal.com'):
                    paragraphs = soup.findAll('p')
                    for p in paragraphs:
                        if user_input.lower() in p.get_text().lower():
                            lst_paragraphs.add(p.get_text())

                else:
                    paragraphs = soup.findAll(text=True)
                    for p in paragraphs:
                        if user_input.lower() in p.lower():
                            lst_paragraphs.add(p)

        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)


    return list(lst_paragraphs)



if __name__ == '__main__':
    dct = {
        'fraud_count': 0,
        'pep_count': 0,
        'terror_count': 0,
    }

    col1, col2, col3 = st.columns([1, 1, 10])
    col1.markdown(f"<div><img style='width:150px' src={img_digital_forensics}></div>", unsafe_allow_html=True)
    col3.subheader('SOLID COMPLIANCE ARUBA')
    col3.write('Forensic Meta Search')
    # col1, col2, col3, col4 = st.columns([6, 1, 1, 1])
    with st.sidebar.form('Enter name'):
        user_input = st.text_input('Enter name')

        st.form_submit_button('Search!')

    if user_input:
        st.write(' ')
        st.write(' ')
        st.write(f"**Meta Search** results for '***{user_input}***' on {today.strftime('%B %-d')}, {today.strftime('%Y')}")
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        my_bar = st.progress(0)
        google = get_serp_google(user_input)
        bing = get_serp_bing(user_input)
        duck = get_serp_duckduckgo(user_input)
        yahoo = get_serp_yahoo(user_input)
        cn = search_cn(user_input)
        ad = search_ad(user_input)
        dclp = search_dclp(user_input)

        all_search = list(set(google + bing + duck + yahoo + cn + ad + dclp))
        # all_search = list(set(dclp))
        for index, url in enumerate(all_search):
            paragraph = get_paragraphs(url[1])
            if paragraph:
                for p in paragraph:
                    result, dct = tag.tag(p, user_input, dct)
                    st.markdown(result, unsafe_allow_html=True)
                    col_1, col_2 = st.columns([1, 7])
                    col_1.write(f"**{url[0]}**"); col_2.write(url[1])

            my_bar.progress((index + 1)/ len(all_search))


        col1.write('Number of keywords related to:')
        if dct:
            col2.metric('FRAUD', f"#{dct['fraud_count']}")
            # if pep_count:
            col3.metric('PEP', f"#{dct['pep_count']}")
            # if terror_count:
            col4.metric('TERROR', f"#{dct['terror_count']}")
