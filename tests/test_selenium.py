from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_login():
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get("http://127.0.0.1:5000")

    # Find fields
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.send_keys("admin")
    password.send_keys("1234")

    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(3)

    assert "Dashboard" in driver.page_source

    driver.quit()