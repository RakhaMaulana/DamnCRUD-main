import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )
    driver.implicitly_wait(5)

    yield driver
    driver.quit()

def login(browser, username, password):
    """Fungsi login dengan WebDriverWait agar lebih stabil."""
    browser.get("http://localhost/DamnCRUD-main/login.php")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    ).send_keys(username)

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys(password + Keys.RETURN)

    WebDriverWait(browser, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

def test_login_valid(browser):
    login(browser, "admin", "nimda666!")
    WebDriverWait(browser, 10).until(EC.url_contains("index.php"))
    assert "index.php" in browser.current_url, "Gagal login dengan kredensial valid"

def test_login_invalid(browser):
    browser.get("http://localhost/DamnCRUD-main/login.php")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    ).send_keys("wronguser")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys("wrongpass" + Keys.RETURN)

    error_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    ).text

    assert "Damn, wrong credentials!!" in error_message, "Pesan error tidak muncul saat login gagal"

def test_create_contact(browser):
    login(browser, "admin", "nimda666!")
    browser.get("http://localhost/DamnCRUD-main/create.php")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "name"))
    ).send_keys("John Doe")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    ).send_keys("johndoe@example.com")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "phone"))
    ).send_keys("08123456789")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    ).send_keys("Software Engineer" + Keys.RETURN)

    browser.get("http://localhost/DamnCRUD-main/index.php")
    page_content = browser.page_source
    assert "John Doe" in page_content, "Kontak baru tidak muncul di daftar"

def test_logout(browser):
    login(browser, "admin", "nimda666!")
    browser.get("http://localhost/DamnCRUD-main/logout.php")

    WebDriverWait(browser, 10).until(EC.url_contains("login.php"))
    assert "login.php" in browser.current_url, "Logout gagal, tidak dialihkan ke login.php"
