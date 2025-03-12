from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import os

# Menonaktifkan pesan log DevTools dan error
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Hilangkan DevTools message
options.add_argument("--log-level=3")  # Log hanya error penting
options.add_argument("--disable-gpu")  # Matikan GPU rendering (opsional)

# Menonaktifkan pesan error terminal dari TensorFlow Lite dan perangkat USB
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)

# Inisialisasi WebDriver dengan opsi tambahan
driver = webdriver.Chrome(options=options)

driver.get("http://localhost/DamnCRUD-main/login.php")

def test_login_valid():
    driver.get("http://localhost/DamnCRUD-main/login.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("nimda666!" + Keys.RETURN)
    time.sleep(2)
    assert "index.php" in driver.current_url, "Gagal login dengan kredensial valid"

def test_login_invalid():
    driver.get("http://localhost/DamnCRUD-main/login.php")
    driver.find_element(By.NAME, "username").send_keys("wronguser")
    driver.find_element(By.NAME, "password").send_keys("wrongpass" + Keys.RETURN)
    time.sleep(2)
    error_message = driver.find_element(By.TAG_NAME, "body").text
    assert "Damn, wrong credentials!!" in error_message, "Pesan error tidak muncul saat login gagal"

def test_create_contact():
    test_login_valid()
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

def test_edit_contact():
    test_login_valid()
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

def test_logout():
    test_login_valid()
    driver.get("http://localhost/DamnCRUD-main/logout.php")
    time.sleep(2)
    assert "login.php" in driver.current_url, "Logout gagal, tidak dialihkan ke login.php"

try:
    test_login_valid()
    print("✅ Test 1: Login dengan kredensial valid - PASS")
except AssertionError as e:
    print(f"❌ Test 1: {e}")

try:
    test_login_invalid()
    print("✅ Test 2: Login dengan kredensial salah - PASS")
except AssertionError as e:
    print(f"❌ Test 2: {e}")

try:
    test_create_contact()
    print("✅ Test 3: Tambah Data Kontak Baru - PASS")
except AssertionError as e:
    print(f"❌ Test 3: {e}")

try:
    test_edit_contact()
    print("✅ Test 4: Edit Data Kontak - PASS")
except AssertionError as e:
    print(f"❌ Test 4: {e}")

try:
    test_logout()
    print("✅ Test 5: Logout - PASS")
except AssertionError as e:
    print(f"❌ Test 5: {e}")

driver.quit()
