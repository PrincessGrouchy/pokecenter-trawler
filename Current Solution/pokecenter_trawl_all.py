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


class TestPage1():
    def setup_method(self):
        # self.service = FirefoxService(executable_path=GeckoDriverManager().install())
        # self.driver = webdriver.Firefox(service=self.service)
        self.service = EdgeService(
            executable_path=EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=self.service)

        self.driver.implicitly_wait(120)
        self.driver.set_window_size(776.642, 701.800)
        self.vars = {}
        self.region = "/en-ca"  # "" # "/en-gb"
        self.category = "/plush"
        self.url = "https://www.pokemoncenter.com" + self.region + \
            "/category" + self.category + "?sort=launch_date%2Bdesc&ps=90&page="
        self.num_items_displayed = 90  # 30 # 60
        self.base_xpath = "//main[@id='main']/div[2]/div[2]/div[2]/div[4]/"
        self.file1 = open('pokecenter_output_' +
                          self.region[1:] + '_new.txt', 'w', encoding="utf-8")

    def teardown_method(self):
        self.driver.quit()
        self.file1.close()

    def print_line(self):
        if self.stock == "SOLD OUT":
            in_stock = "NO"
        else:
            in_stock = "YES"
        product_number = self.link.replace("https://www.pokemoncenter.com"
                                           + self.region
                                           + "/product/", "").split("/")[0]
        real_number = self.page_count - 1
        real_number *= self.num_items_displayed
        real_number += self.loop_count
        stringToPrint = "{},{},{},{},{},{},{}-{}\n".format(
            real_number,
            self.link,
            product_number,
            self.name,
            self.price,
            in_stock,
            self.page_count, self.loop_count
        )
        print(stringToPrint)
        self.file1.write(stringToPrint)

    def get_page_vars(self, isFirst):
        if isFirst:
            extra_div = "div"
        else:
            extra_div = "div[" + str(self.loop_count) + "]"
        self.link = WebDriverWait(self.driver, 120).until(lambda d: d.find_element(By.XPATH,
                                                                                   self.base_xpath + extra_div + "/div/a").get_attribute("href"))
        self.name = WebDriverWait(self.driver, 120).until(lambda d: d.find_element(By.XPATH,
                                                                                   self.base_xpath + extra_div + "/div/a/div[2]/h3").text)
        self.price = WebDriverWait(self.driver, 120).until(lambda d: d.find_element(By.XPATH,
                                                                                    self.base_xpath + extra_div + "/div/a/div[2]/div/span").text)
        self.stock = WebDriverWait(self.driver, 120).until(lambda d: d.find_element(By.XPATH,
                                                                                    self.base_xpath + extra_div + "/div/a/div/div").text)

    def scrape_page_not_last_page(self):
        self.page_count = 1
        self.loop_count = 1
        self.driver.get(self.url + str(self.page_count))
        WebDriverWait(self.driver, 120).until(
            lambda driver: 'Plush |' in driver.title)

        self.total_count_string = WebDriverWait(self.driver, 120).until(lambda d: d.find_element(By.XPATH,
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

            time.sleep(20)
            self.page_count += 1

    def scrape_page_last(self):
        # for last page only runs
        # self.total_count = 1079 # set manually!
        # self.total_full_page_count = int(self.total_count) // int(self.num_items_displayed)
        # self.total_page_count = self.total_full_page_count + 1

        self.page_count = self.total_page_count
        self.loop_count = 1
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


try:
    x = TestPage1()
    x.setup_method()
    x.scrape_page_not_last_page()
    x.scrape_page_last()
    x.teardown_method()
finally:
    x.teardown_method()
