from unittest import TestCase

from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class MyCase(TestCase):
    def test_signin(self):
        # driver = webdriver.Firefox(executable_path="C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")
        driver = webdriver.Chrome(executable_path="D:\\chromedriver.exe")
        driver.get('http://127.0.0.1:8000' + reverse('add'))

        wait = WebDriverWait(driver, 3)
        wait.until(lambda driver: 'edit' in driver.current_url)
        driver.close()
