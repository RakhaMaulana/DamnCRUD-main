import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

# Konfigurasi WebDriver
options = Options()
options.add_argument("--headless")  # Jalankan dalam mode headless (opsional)
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")  # Hanya log penting

@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def print_result(test_name, result):
    status = "✅" if result else "❌"
    print(f"{status} {test_name} - {'PASS' if result else 'FAIL'}")

def test_login_valid(browser):
    browser.get("http://localhost/DamnCRUD-main/login.php")
    browser.find_element(By.NAME, "username").send_keys("admin")
    browser.find_element(By.NAME, "password").send_keys("nimda666!" + Keys.RETURN)
    time.sleep(2)
    result = "index.php" in browser.current_url
    print_result("Test 1: Login dengan kredensial valid", result)
    assert result

def test_login_invalid(browser):
    browser.get("http://localhost/DamnCRUD-main/login.php")
    browser.find_element(By.NAME, "username").send_keys("wronguser")
    browser.find_element(By.NAME, "password").send_keys("wrongpass" + Keys.RETURN)
    time.sleep(2)
    error_message = browser.find_element(By.TAG_NAME, "body").text
    result = "Damn, wrong credentials!!" in error_message
    print_result("Test 2: Login dengan kredensial salah", result)
    assert result

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
    result = "John Doe" in page_content
    print_result("Test 3: Membuat kontak baru", result)
    assert result

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
    result = "Jane Doe" in page_content
    print_result("Test 4: Mengedit kontak", result)
    assert result

def test_logout(browser):
    test_login_valid(browser)
    browser.get("http://localhost/DamnCRUD-main/logout.php")
    time.sleep(2)
    result = "login.php" in browser.current_url
    print_result("Test 5: Logout dari aplikasi", result)
    assert result
