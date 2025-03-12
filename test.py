import pytest
import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def driver():
    # Nonaktifkan pesan DevTools dkk.
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    options.add_argument("--disable-gpu")

    # Inisialisasi WebDriver
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_login_valid(driver):
    driver.get("http://localhost/DamnCRUD-main/login.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("nimda666!" + Keys.RETURN)
    time.sleep(2)
    assert "index.php" in driver.current_url, "Gagal login dengan kredensial valid"

def test_login_invalid(driver):
    driver.get("http://localhost/DamnCRUD-main/login.php")
    driver.find_element(By.NAME, "username").send_keys("wronguser")
    driver.find_element(By.NAME, "password").send_keys("wrongpass" + Keys.RETURN)
    time.sleep(2)
    error_message = driver.find_element(By.TAG_NAME, "body").text
    assert "Damn, wrong credentials!!" in error_message, "Pesan error tidak muncul saat login gagal"

def test_create_contact(driver):
    test_login_valid(driver)  # Pastikan sudah login
    driver.get("http://localhost/DamnCRUD-main/create.php")
    time.sleep(2)
    driver.find_element(By.NAME, "name").send_keys("John Doe")
    driver.find_element(By.NAME, "email").send_keys("johndoe@example.com")
    driver.find_element(By.NAME, "phone").send_keys("08123456789")
    driver.find_element(By.NAME, "title").send_keys("Software Engineer")
    driver.find_element(By.NAME, "title").send_keys(Keys.RETURN)
    time.sleep(2)

    driver.get("http://localhost/DamnCRUD-main/index.php")
    page_content = driver.page_source
    assert "John Doe" in page_content, "Kontak baru tidak muncul di daftar"

def test_edit_contact(driver):
    test_login_valid(driver)
    driver.get("http://localhost/DamnCRUD-main/index.php")
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "edit").click()
    time.sleep(2)

    name_input = driver.find_element(By.NAME, "name")
    name_input.clear()
    name_input.send_keys("Jane Doe")

    email_input = driver.find_element(By.NAME, "email")
    email_input.clear()
    email_input.send_keys("janedoe@example.com")
    driver.find_element(By.NAME, "title").send_keys(Keys.RETURN)
    time.sleep(2)

    driver.get("http://localhost/DamnCRUD-main/index.php")
    page_content = driver.page_source
    assert "Jane Doe" in page_content, "Data kontak tidak berhasil diperbarui"

def test_logout(driver):
    test_login_valid(driver)
    driver.get("http://localhost/DamnCRUD-main/logout.php")
    time.sleep(2)
    assert "login.php" in driver.current_url, "Logout gagal, tidak dialihkan ke login.php"