#!/usr/bin/env python3
import argparse
import json
import os
import re
import traceback
import time
import pandas as pd
import threading

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from crawler_producers.figshare.python.pycrawler.crawler_lib.article import Article

FIGSHARE_SEARCH_TERM_URL = "https://figshare.com/search?q=xtc%E2%80%8B%2C%20%E2%80%8Bdcd%2C%E2%80%8B%20%E2%80%8Bntraj%2C%20netcdf%2C%20trr%2C%20lammpstrj%2C%20xyz%2C%20binpos%2C%20hdf5%2C%20dtr%2C%20arc%2C%20tng%2C%20mdcrd%2C%20crd%2C%20dms%2C%20trj%2C%20ent%2C%20ncdf"

FIGSHARE_ARTICLE_JS_QUERY = "return document.querySelectorAll('div[role=article]')"

FIGSHARE_ALL_XPATH = ".//*"

FIGSHARE_ANCHOR_XPATH = ".//a"

DEFAULT_IMPLICIT_WAIT_TIME = 30

DEFAULT_SCROLL_DOWN_KEY_PRESSES = 150

PRIMARY_EXEC_LIMIT = 5

#SECONDARY_LINK_LIMIT =  30

def agree_to_cookies(driver):
    driver.find_element_by_tag_name('button').send_keys(Keys.RETURN)

def get_primary_page_article_content(element):
    text_list = element.find_element_by_xpath(".//*").text
    href_list = element.find_element_by_xpath(".//a").get_attribute("href")
    return text_list, href_list

def fetch_all_current_articles(driver):
    return driver.execute_script(FIGSHARE_ARTICLE_JS_QUERY)

def execute_manual_scroll_down(driver):
    for _ in range(0, DEFAULT_SCROLL_DOWN_KEY_PRESSES):
        driver.find_element_by_tag_name('button').send_keys(Keys.RETURN)

def parse_text_list(text_list:str):
    text = text_list.split('\n')
    assert(len(text) == 4)
    article_type = text[0]
    title = text[1]
    ##TODO: parse posted on text, extract date and destination
    posted_on_text = text[2]
    author = text[3]
    article = Article(title=title)
    article.add_author(author)
    return article

def build_article_from_element(element):
    text_list, href_list = get_primary_page_article_content(element)
    article = parse_text_list(text_list)
    assert(len(href_list) == 1)
    article.source_url = href_list[0]
    return article

def create_webdriver():
    #if args.webdriver == "firefox":
   print("starting firefox driver")
   firefox_options = webdriver.FirefoxOptions()
   firefox_options.add_argument('--headless')
   driver = webdriver.Firefox(firefox_options=firefox_options)
   # elif args.webdriver == "chrome":
   #     print("starting chrome driver")
   #     if args.webdriver_location is None:
   #         print("webdriver file location required, please add...")
   #     chrome_options = webdriver.ChromeOptions()
   #     chrome_options.add_argument('--headless')
   #     chrome_options.add_argument('--no-sandbox')
   #     chrome_options.add_argument('--disable-dev-shm-usage')
   #     #driver = webdriver.Chrome()
   #     driver = webdriver.Chrome(chrome_options=chrome_options)
   # if driver is None:
   #     print("could not build webdriver on localhost")
   return driver

def fetch_articles_and_scroll(driver):
    article_list = list()
    current_articles = fetch_all_current_articles(driver)
    for element in current_articles:
        article_list.append(build_article_from_element(element))
    execute_manual_scroll_down(driver)
    return article_list



##TODO refactor below:
#def run(url: str) -> dict:
#    messages = []
#
#    initial_response = url_response(messages, url)
#
#    if initial_response is None:
#        messages.append("got response of None, exiting")
#        return {"messages": messages}
#
#    append_bs_parsing(messages, initial_response)
#    if args.use_selenium:
#        append_selenium_parsing(messages, url, args)
#    if args.parse_secondary:
#        parse_secondary_links(messages, args)
#    output_pandas_csv(messages, args)
#    return {"messages": messages}
#
#
#def url_response(messages: list, url: str) -> requests.Response:
#    try:
#        response = requests.get(url, )
#        messages.append("request to: url produced: {}".format(url, str(response.status_code)))
#        return response
#    except Exception as e:
#        messages.append("initial request failed, error: {}".format(e))
#
#
#def append_bs_parsing(messages, initial_response):
#    try:
#        soup = BeautifulSoup(initial_response.content, "html.parser")
#        links = soup.body.findAll("a")
#        hrefs = []
#        for link in links:
#            hrefs.append(link.attrs["href"])
#
#        hrefs_reg = []
#        for item in hrefs:
#            search_obj = re.search(r"http.*", item, re.I)
#            if search_obj:
#                hrefs_reg.append(search_obj.group())
#
#        messages.append({"soup": "parsed",
#                         "links": hrefs,
#                         "urls": hrefs_reg})
#    except Exception:
#        soup = {"status": "failed to parse"}
#        messages.append({"soup": soup, "exception": traceback.format_exc()})
#
#
#def append_selenium_parsing(messages: list, url: str, args: argparse.Namespace):
#    try:
#        prepare_selenium_response(url, args)
#        messages.append({"selenium": "parsed",
#                         "links": FIGSHARE_SELENIUM_LINKS,
#                         "total": str(len(FIGSHARE_SELENIUM_LINKS))})
#    except:
#        selenium = {"status": "failed to parse"}
#        messages.append({"selenium": selenium, "exception": traceback.format_exc()})
#
#
#def prepare_selenium_response(url: str, args: argparse.Namespace) -> None:
#    driver = build_webdriver(args)
#    driver.get(url)
#    driver.implicitly_wait(DEFAULT_IMPLICIT_WAIT_TIME)
#    accept_cookies(driver)
#
#    scroll_to_bottom_and_get_links(driver)
#    driver.close()
#
#
#def accept_cookies(driver) -> None:
#    cookie_string = FIGSHARE_COOKIE_XPATH
#    element = driver.find_element_by_xpath(cookie_string)
#    if element:
#        element.click()
#
#
#def scroll_to_bottom_and_get_links(driver) -> None:
#    seed_height = driver.execute_script("return document.body.scrollHeight")
#    scroll_down_finding_links(driver, seed_height, 0)
#
#
#def scroll_down_finding_links(driver, height, run) -> None:
#    if run > PRIMARY_EXEC_LIMIT:
#        return
#    driver.execute_script("scroll(0, 250);")
#    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#    get_links_in_browser(driver, 0)
#    print("current links ", len(FIGSHARE_SELENIUM_LINKS))
#    executed_height = driver.execute_script("return document.body.scrollHeight")
#    if executed_height == height:
#        return
#    print("scrolling to bottom, current height: {}, previous height: {}".format(executed_height, height))
#    time.sleep(DEFAULT_INFINI_SCROLL_TIMEOUT)
#    run += 1
#    scroll_down_finding_links(driver, executed_height, run)
#
#
#def get_links_in_browser(driver, current_attempt: int) -> None:
#    try:
#        if current_attempt > 10:
#            print("giving up!")
#            return
#        # TODO:try to abstract the find element for anchor
#        links = driver.find_elements_by_xpath(FIGSHARE_ANCHOR_XPATH)
#        if links:
#            update_figshare_links(links)
#    except Exception as e:
#        current_attempt += 1
#        error_msg = "could not parse element it on attempt: " \
#                    + str(current_attempt) \
#                    + ", retrying. error:"
#        print(error_msg, str(e))
#        get_links_in_browser(driver, current_attempt)
#
#
#def update_figshare_links(links_found):
#    for link in links_found:
#        link_string = link.get_attribute('href')
#        if link_string not in FIGSHARE_SELENIUM_LINKS:
#            FIGSHARE_SELENIUM_LINKS.append(link_string)
#
#
#def parse_secondary_links(messages: list, args: argparse.Namespace) -> None:
#    try:
#        links = FIGSHARE_SELENIUM_LINKS
#        thread_list = []
#        for link in links[:SECONDARY_LINK_LIMIT]:
#            t = threading.Thread(target=parse_secondary_figshare_url, args=(link, args, 0))
#            thread_list.append(t)
#
#        study_params = [str(x) for x in PARSED_STUDY_PARAMS]
#        print(study_params)
#        messages.append({"secondary": "parsed",
#                         "study_params": study_params,
#                         "total": str(len(study_params))})
#    except Exception as e:
#        secondary = {"status": "failed to parse"}
#        messages.append({"secondary": secondary, "exception": traceback.format_exc()})
#
#def parse_secondary_figshare_url(link, args, attempts):
#    browser = build_webdriver(args)
#    print("parsing secondary links")
#    normal_link_string = "//ul//a[@class = 'normal-link']"
#    title_xpath = "//h2[@class = 'title']"
#    author_xpath = "//a[@class = 'normal-link author']"
#    tag_section_xpath = "//div[@class = 'tags section']//a[@class = 'tag-wrap']"
#    description_xpath = "//Div[@class = 'description section']"
#    try:
#        if attempts > 5:
#            print("giving up secondary parse")
#            return
#        if link:
#            study = StudyParameters(source_url=link)
#            browser.get(link)
#            title = browser.find_element_by_xpath(title_xpath).text  # Extracting tittle of trayectory
#            author = browser.find_element_by_xpath(author_xpath).text  # EXtracting the author
#            print("author:", author)
#            study.add_authors(author)
#            print("title:", title)
#            study.add_title(title)
#            categories = [x.text for x in browser.find_elements_by_xpath(normal_link_string)]
#            print("categories:", categories)
#            for category in categories:
#                study.add_category(category)
#
#            keywords = [x.get_attribute("title") for x in browser.find_elements_by_xpath(tag_section_xpath)]
#            print("keywords:", keywords)
#            for keyword in keywords:
#                study.add_keyword(keyword)
#            description = study.add_description(browser.find_element_by_xpath(description_xpath).text)
#            print(description)
#            PARSED_STUDY_PARAMS.append(study)
#    except Exception as e:
#        attempts += 1
#        print("couldn't parse study on attempt", attempts, " retrying...")
#        parse_secondary_figshare_url(link, args, attempts)
#    browser.close()




#def output_pandas_csv(messages, args) -> None:
#    if 'output_location' in args and args.output_location == 'console':
#        data = build_panda_data_dict()
#        for study in PARSED_STUDY_PARAMS:
#            update_data_with_study(study, data)
#        dataframe = pd.DataFrame(data)
#        messages.append({"pandas_csv": str(dataframe.to_csv())})


#def build_panda_data_dict() -> dict:
#    data = dict()
#    data['Title'] = []
#    data['Author'] = []
#    data['Categories'] = []
#    data['Keywords'] = []
#    data['Description'] = []
#    data['Source_Url'] = []
#    data['Upload_Date'] =[]
#    return data
#
#
#def update_data_with_study(study: StudyParameters, data: dict):
#    data['Title'].append(study.title)
#    data['Authors'].append(study.author_list)
#    data['Categories'].append(study.categories)
#    data['Keywords'].append(study.keywords)
#    data['Description'].append(study.description)
#    data['Source_Url'].append(study.source_url)
#    data['Upload_Date'].append(study.upload_date)
#    return data


def main(args: argparse.Namespace) -> None:
    url = args.url
    try:
        json_response = json.dumps(run(url), indent=4)
        print(json_response)
    except Exception as exc:
        print("failed to run crawler", exc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="command line tool to parse web links for bioinfo links")

    parser.add_argument('--url', type=str, default=os.environ.get('URL'))
    parser.add_argument('--webdriver', type=str, choices=["chrome", "firefox"], default=os.environ.get('WEBDRIVER'))
    parser.add_argument('--webdriver_location', type=str, default=os.environ.get('WD_LOCATION'))
    parser.add_argument('--output_location', type=str, default="console")
    parser.add_argument('--use_selenium', action="store_true", default=False)
    parser.add_argument('--parse_secondary', action="store_true", default=False)
    args = parser.parse_args()
    print("python args:{}".format(args))
    main(args)
