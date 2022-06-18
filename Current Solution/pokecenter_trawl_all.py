# Generated by Selenium IDE
import pytest
import time
import json
import sys
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IEOptions


class EnTrawler():
    def pre_setup_vars(self):
        # self.service = FirefoxService(executable_path=GeckoDriverManager().install())
        # self.driver = webdriver.Firefox(service=self.service)
        self.service = EdgeService(
            executable_path=EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=self.service)
        self.driver.implicitly_wait(120)
        self.driver.set_window_size(776.642, 701.800)

    def setup_method(self, the_region, the_category):
        self.region = the_region
        self.category = the_category
        self.sort = "?sort=launch_date%2Bdesc"

        self.url = "https://www.pokemoncenter.com" + self.region + \
            "/category" + self.category + self.sort + \
            "&ps=90&page="
        self.num_items_displayed = 90  # 30 # 60
        # self.single_category_file = open(
        #     'pokecenter_output_' + self.region[1:] + '_'+self.category[1:] + '_new.txt', 'w', encoding="utf-8")
        self.all_category_file = open(
            'pokecenter_output_' + self.region[1:] + '_new.txt', 'a', encoding="utf-8")

    def teardown_single(self):
        # self.single_category_file.close()
        self.all_category_file.close()

    def teardown_method(self):
        self.driver.quit()
        # self.single_category_file.close()
        self.all_category_file.close()

    def print_line(self):
        if self.stock == "SOLD OUT" or "soldout" in self.stock:
            in_stock = "NO"
        else:
            in_stock = "YES"
        product_number = self.link.replace("https://www.pokemoncenter.com"
                                           + self.region
                                           + "/product/", "")
        product_number = product_number.replace(
            "https://www.pokemoncenter.com/product/", "")
        product_number = product_number.replace(
            "https://www.pokemoncenter-online.com/?p_cd=", "")
        product_number = product_number.split("/")[0]

        real_number = self.page_count - 1
        real_number *= self.num_items_displayed
        real_number += self.loop_count
        stringToPrint = "{},{},{},{},{},{},{}-{},{}\n".format(
            real_number,
            self.link,
            product_number,
            self.name,
            self.price,
            in_stock,
            self.page_count, self.loop_count,
            self.category.replace("/", "")
        )
        print(stringToPrint)
        # self.single_category_file.write(stringToPrint)
        self.all_category_file.write(stringToPrint)

    def get_page_vars(self, isFirst):
        self.base_xpath = "//main[@id='main']/div[2]/div[2]/div[2]/div[4]/"
        if isFirst:
            extra_div = "div"
        else:
            extra_div = "div[" + str(self.loop_count) + "]"
        self.link = WebDriverWait(self.driver, 120).until(
            lambda d: d.find_element(By.XPATH,
                                     self.base_xpath + extra_div + "/div/a").get_attribute("href"))
        self.name = WebDriverWait(self.driver, 120).until(
            lambda d: d.find_element(By.XPATH,
                                     self.base_xpath + extra_div + "/div/a/div[2]/h3").text)
        self.price = WebDriverWait(self.driver, 120).until(
            lambda d: d.find_element(By.XPATH,
                                     self.base_xpath + extra_div + "/div/a/div[2]/div/span").text)
        self.stock = WebDriverWait(self.driver, 120).until(
            lambda d: d.find_element(By.XPATH,
                                     self.base_xpath + extra_div + "/div/a/div/div").text)

    def scrape_page_not_last_page(self):
        self.page_count = 1
        self.loop_count = 1
        self.driver.get(self.url + str(self.page_count))
        WebDriverWait(self.driver, 120).until(
            lambda driver: '|' in driver.title)

        self.total_count_string = WebDriverWait(self.driver, 120).until(
            lambda d: d.find_element(By.XPATH,
                                     "//main[@id='main']/div[2]/div[2]/div[2]/div[3]/div/div/h3/span").text)
        self.total_count = self.total_count_string.split("of ")[
            1].replace(" )", "")
        self.total_full_page_count = int(
            self.total_count) // int(self.num_items_displayed)
        self.total_page_count = self.total_full_page_count + 1

        while self.page_count < self.total_page_count:
            self.loop_count = 1
            self.driver.get(self.url + str(self.page_count))
            self.get_page_vars(isFirst=True)
            self.print_line()

            self.loop_count = 2
            while self.loop_count < (self.num_items_displayed + 1):
                self.get_page_vars(isFirst=False)
                self.print_line()
                self.loop_count += 1

            self.page_count += 1

    def scrape_page_last(self):
        # for last page only runs
        # self.total_count = 1079 # set manually!
        # self.total_full_page_count = int(self.total_count) // int(self.num_items_displayed)
        # self.total_page_count = self.total_full_page_count + 1

        self.page_count = self.total_page_count
        self.loop_count = 1
        # problem: we need to skip if the page remainder is 0!
        if int(self.total_count) % int(self.num_items_displayed) != 0:
            self.driver.get(self.url + str(self.page_count))
            self.get_page_vars(isFirst=True)
            self.print_line()

            self.loop_count = 2
            self.past_items = int(self.total_full_page_count) * \
                int(self.num_items_displayed)
            self.new_num_items = int(self.total_count) - int(self.past_items)
            while self.loop_count < (self.new_num_items + 1):
                self.get_page_vars(isFirst=False)
                self.print_line()
                self.loop_count += 1


class JpTrawler(EnTrawler):
    def pre_setup_vars(self):
        self.service = FirefoxService(
            executable_path=GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=self.service)
        # self.service = EdgeService(
        #     executable_path=EdgeChromiumDriverManager().install())
        # self.driver = webdriver.Edge(service=self.service)
        self.driver.implicitly_wait(120)
        self.driver.set_window_size(776.642, 701.800)

    def setup_method(self, the_category):
        self.region = "jp-jp"
        self.sort = "&sort=new"
        self.category = the_category  # plush
        self.url = "https://www.pokemoncenter-online.com/?main_page=product_list" + \
            self.sort + "&cat1=" + self.category + "&page="
        self.translate_url_additions = ""  # chrome autotranslate adds "/font/font"
        self.num_items_displayed = 40  # default=40

        # self.single_category_file = open(
        #     'pokecenter_output_' + self.region + '_'+self.category + '_new.txt', 'w', encoding="utf-8")
        self.all_category_file = open(
            'pokecenter_output_' + self.region + '_new.txt', 'a', encoding="utf-8")

    def get_page_vars(self, isFirst):
        self.base_xpath = "//div[@id='product_list']/ul/"
        if isFirst:
            extra_div = "li"
        else:
            extra_div = "li[" + str(self.loop_count) + "]"
        # xpath=//div[@id='product_list']/ul/li/a
        self.link = WebDriverWait(self.driver, 120).until(
            lambda d: d.find_element(By.XPATH,
                                     self.base_xpath + extra_div + "/a").get_attribute("href"))
        #  xpath=//div[@id='product_list']/ul/li[2]/a/div/p/font/font
        self.name = WebDriverWait(self.driver, 120).until(
            lambda d: d.find_element(By.XPATH,
                                     self.base_xpath + extra_div + "/a/div/p" + self.translate_url_additions).text)
        # xpath=//div[@id='product_list']/ul/li[2]/a/div/p[2]/font/font
        self.price = WebDriverWait(self.driver, 120).until(
            lambda d: d.find_element(By.XPATH,
                                     self.base_xpath + extra_div + "/a/div/p[2]" + self.translate_url_additions).text)
        # xpath=//div[@id='product_list']/ul/li[4]
        self.stock = WebDriverWait(self.driver, 120).until(
            lambda d: d.find_element(By.XPATH,
                                     self.base_xpath + extra_div).get_attribute("class"))

    def scrape_page_not_last_page(self):
        self.page_count = 1
        self.loop_count = 1
        self.driver.get(self.url + str(self.page_count))
        WebDriverWait(self.driver, 120).until(
            lambda driver: '商品検索結果 : ポケモンセンターオンライン' in driver.title)

        self.total_count_string = WebDriverWait(self.driver, 120).until(
            lambda d: d.find_element(By.XPATH,
                                     "//div[@id='contents']/div/h1" + self.translate_url_additions).text)
        self.total_count = self.total_count_string.split("全 ")[
            1].replace("件）", "").replace(",", "")
        self.total_full_page_count = int(
            self.total_count) // int(self.num_items_displayed)
        self.total_page_count = self.total_full_page_count + 1

        while self.page_count < self.total_page_count:
            self.loop_count = 1
            self.driver.get(self.url + str(self.page_count))
            self.get_page_vars(isFirst=True)
            self.print_line()

            self.loop_count = 2
            while self.loop_count < (self.num_items_displayed + 1):
                self.get_page_vars(isFirst=False)
                self.print_line()
                self.loop_count += 1

            self.page_count += 1


categories = ["/plush", "/figures-and-pins",
              "/trading-card-game", "/clothing", "/home", "/video-game"]
regions = ["/en-ca", "/en-gb", "/en-us"]
en = EnTrawler()
en.pre_setup_vars()

try:
    for the_region in regions:
        for the_category in categories:
            en.setup_method(the_region, the_category)
            en.scrape_page_not_last_page()
            en.scrape_page_last()
            en.teardown_single()
finally:
    en.teardown_method()

jp_categories = ["toy", "game", "card",
                 "stationery", "goods",
                 "kitchen", "phone", "fashion",
                 "apparel", "book", "cddvd", "food"]  # "ticket"
jp = JpTrawler()
jp.pre_setup_vars()

try:
    for the_jp_category in jp_categories:
        jp.setup_method(the_jp_category)
        jp.scrape_page_not_last_page()
        jp.scrape_page_last()
        jp.teardown_single()
finally:
    jp.teardown_method()
