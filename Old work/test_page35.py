# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestPage35():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_page35(self):
    # Test name: Page 35+
    # Step # | name | target | value
    # 1 | executeScript | return 35 | page_count
    self.vars["page_count"] = self.driver.execute_script("return 35")
    # 2 | while | ${page_count} < 50 | 
    while self.driver.execute_script("return (arguments[0] < 50)", self.vars["page_count"]):
      # 3 | open | /en-ca/category/plush?sort=launch_date%2Bdesc&page=${page_count} | 
      self.driver.get("https://www.pokemoncenter.com//en-ca/category/plush?sort=launch_date%2Bdesc&page=self.vars["page_count"]")
      # 4 | storeAttribute | xpath=//main[@id='main']/div[2]/div[2]/div[2]/div[4]/div/div/a@href | link
      attribute = self.driver.find_element(By.XPATH, "//main[@id=\'main\']/div[2]/div[2]/div[2]/div[4]/div/div/a").get_attribute("href")
      self.vars["link"] = attribute
      # 5 | storeText | xpath=//main[@id='main']/div[2]/div[2]/div[2]/div[4]/div/div/a/div[2]/h3 | name
      self.vars["name"] = self.driver.find_element(By.XPATH, "//main[@id=\'main\']/div[2]/div[2]/div[2]/div[4]/div/div/a/div[2]/h3").text
      # 6 | storeText | xpath=//main[@id='main']/div[2]/div[2]/div[2]/div[4]/div/div/a/div[2]/div/span | price
      self.vars["price"] = self.driver.find_element(By.XPATH, "//main[@id=\'main\']/div[2]/div[2]/div[2]/div[4]/div/div/a/div[2]/div/span").text
      # 7 | storeText | xpath=//main[@id='main']/div[2]/div[2]/div[2]/div[4]/div/div/a/div/div | stock
      self.vars["stock"] = self.driver.find_element(By.XPATH, "//main[@id=\'main\']/div[2]/div[2]/div[2]/div[4]/div/div/a/div/div").text
      # 8 | echo | Output - ${page_count}-1 Link: https://www.pokemoncenter.com${link} | 
      print("Output - {}-1 Link: https://www.pokemoncenter.com${link}".format(self.vars["page_count"]))
      # 9 | echo | Output - ${page_count}-1 Name:  ${name} | 
      print("Output - {}-1 Name:  ${name}".format(self.vars["page_count"]))
      # 10 | echo | Output - ${page_count}-1 Price: ${price} | 
      print("Output - {}-1 Price: ${price}".format(self.vars["page_count"]))
      # 11 | echo | Output - ${page_count}-1 OoStock?: ${stock} | 
      print("Output - {}-1 OoStock?: ${stock}".format(self.vars["page_count"]))
      # 12 | executeScript | return 2 | loop_count
      self.vars["loop_count"] = self.driver.execute_script("return 2")
      # 13 | while | ${loop_count} < 31 | 
      while self.driver.execute_script("return (arguments[0] < 31)", self.vars["loop_count"]):
        # 14 | storeAttribute | xpath=//main[@id='main']/div[2]/div[2]/div[2]/div[4]/div[${loop_count}]/div/a@href | link
        attribute = self.driver.find_element(By.XPATH, "//main[@id=\'main\']/div[2]/div[2]/div[2]/div[4]/div[self.vars["loop_count"]]/div/a").get_attribute("href")
        self.vars["link"] = attribute
        # 15 | storeText | xpath=//main[@id='main']/div[2]/div[2]/div[2]/div[4]/div[${loop_count}]/div/a/div[2]/h3 | name
        self.vars["name"] = self.driver.find_element(By.XPATH, "//main[@id=\'main\']/div[2]/div[2]/div[2]/div[4]/div[self.vars["loop_count"]]/div/a/div[2]/h3").text
        # 16 | storeText | xpath=//main[@id='main']/div[2]/div[2]/div[2]/div[4]/div[${loop_count}]/div/a/div[2]/div/span | price
        self.vars["price"] = self.driver.find_element(By.XPATH, "//main[@id=\'main\']/div[2]/div[2]/div[2]/div[4]/div[self.vars["loop_count"]]/div/a/div[2]/div/span").text
        # 17 | storeText | xpath=//main[@id='main']/div[2]/div[2]/div[2]/div[4]/div[${loop_count}]/div/a/div/div | stock
        self.vars["stock"] = self.driver.find_element(By.XPATH, "//main[@id=\'main\']/div[2]/div[2]/div[2]/div[4]/div[self.vars["loop_count"]]/div/a/div/div").text
        # 18 | echo | Output - ${page_count}-${loop_count} Link: https://www.pokemoncenter.com${link} | 
        print("Output - {}-${loop_count} Link: https://www.pokemoncenter.com${link}".format(self.vars["page_count"]))
        # 19 | echo | Output - ${page_count}-${loop_count} Name:  ${name} | 
        print("Output - {}-${loop_count} Name:  ${name}".format(self.vars["page_count"]))
        # 20 | echo | Output - ${page_count}-${loop_count} Price: ${price} | 
        print("Output - {}-${loop_count} Price: ${price}".format(self.vars["page_count"]))
        # 21 | echo | Output - ${page_count}-${loop_count} OoStock?: ${stock} | 
        print("Output - {}-${loop_count} OoStock?: ${stock}".format(self.vars["page_count"]))
        # 22 | executeScript | return ${loop_count} + 1 | loop_count
        self.vars["loop_count"] = self.driver.execute_script("return arguments[0] + 1", self.vars["loop_count"])
        # 23 | end |  | 
      # 24 | executeScript | return ${page_count} + 1 | page_count
      self.vars["page_count"] = self.driver.execute_script("return arguments[0] + 1", self.vars["page_count"])
      # 25 | end |  | 
  
