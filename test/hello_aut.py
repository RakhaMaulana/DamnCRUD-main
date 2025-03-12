import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import os
import tempfile

# Menonaktifkan pesan log DevTools dan error
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Hilangkan DevTools message
options.add_argument("--log-level=3")  # Log hanya error penting
options.add_argument("--disable-gpu")  # Matikan GPU rendering (opsional)

# Menonaktifkan pesan error terminal dari TensorFlow Lite dan perangkat USB
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)

# Inisialisasi WebDriver dengan opsi tambahan
with tempfile.TemporaryDirectory() as user_data_dir:
    options.add_argument(f"--user-data-dir={user_data_dir}")
    driver = webdriver.Chrome(options=options)

driver.get("http://localhost/DamnCRUD-main/login.php")

@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    options.add_argument("--disable-gpu")
    with tempfile.TemporaryDirectory() as user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()

def test_login_valid(browser):
    browser.get("http://localhost/DamnCRUD-main/login.php")
    browser.find_element(By.NAME, "username").send_keys("admin")
    browser.find_element(By.NAME, "password").send_keys("nimda666!" + Keys.RETURN)
    time.sleep(2)
    assert "index.php" in browser.current_url, "Gagal login dengan kredensial valid"

def test_login_invalid(browser):
    browser.get("http://localhost/DamnCRUD-main/login.php")
    browser.find_element(By.NAME, "username").send_keys("wronguser")
    browser.find_element(By.NAME, "password").send_keys("wrongpass" + Keys.RETURN)
    time.sleep(2)
    error_message = browser.find_element(By.TAG_NAME, "body").text
    assert "Damn, wrong credentials!!" in error_message, "Pesan error tidak muncul saat login gagal"

def test_create_contact(browser):
    test_login_valid(browser)
    browser.get("http://localhost/DamnCRUD-main/create.php")
    time.sleep(2)

    browser.find_element(By.NAME, "name").send_keys("John Doe")
    browser.find_element(By.NAME, "email").send_keys("johndoe@example.com")
    browser.find_element(By.NAME, "phone").send_keys("08123456789")
    browser.find_element(By.NAME, "title").send_keys("Software Engineer")
    browser.find_element(By.NAME, "title").send_keys(Keys.RETURN)
    time.sleep(2)

    browser.get("http://localhost/DamnCRUD-main/index.php")
    page_content = browser.page_source
    assert "John Doe" in page_content, "Kontak baru tidak muncul di daftar"

def test_edit_contact(browser):
    test_login_valid(browser)
    browser.get("http://localhost/DamnCRUD-main/index.php")
    time.sleep(2)

    browser.find_element(By.LINK_TEXT, "edit").click()
    time.sleep(2)

    name_input = browser.find_element(By.NAME, "name")
    name_input.clear()
    name_input.send_keys("Jane Doe")

    email_input = browser.find_element(By.NAME, "email")
    email_input.clear()
    email_input.send_keys("janedoe@example.com")

    browser.find_element(By.NAME, "title").send_keys(Keys.RETURN)
    time.sleep(2)

    browser.get("http://localhost/DamnCRUD-main/index.php")
    page_content = browser.page_source
    assert "Jane Doe" in page_content, "Data kontak tidak berhasil diperbarui"

def test_logout(browser):
    test_login_valid(browser)
    browser.get("http://localhost/DamnCRUD-main/logout.php")
    time.sleep(2)
    assert "login.php" in browser.current_url, "Logout gagal, tidak dialihkan ke login.php"