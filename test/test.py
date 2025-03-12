import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class DamnCRUDTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Gunakan Selenium Grid (di GitHub Actions)
        self.browser = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def login(self, username, password):
        """Fungsi login agar bisa digunakan ulang di berbagai test case."""
        self.browser.get("http://localhost/DamnCRUD-main/login.php")
        self.browser.find_element(By.NAME, "username").send_keys(username)
        self.browser.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
        self.assertIn("index.php", self.browser.current_url, "Gagal login dengan kredensial valid")

    def test_login_valid(self):
        self.login("admin", "nimda666!")

    def test_login_invalid(self):
        self.browser.get("http://localhost/DamnCRUD-main/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("wronguser")
        self.browser.find_element(By.NAME, "password").send_keys("wrongpass" + Keys.RETURN)

        error_message = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Damn, wrong credentials!!", error_message, "Pesan error tidak muncul saat login gagal")

    def test_create_contact(self):
        self.login("admin", "nimda666!")
        self.browser.get("http://localhost/DamnCRUD-main/create.php")

        self.browser.find_element(By.NAME, "name").send_keys("John Doe")
        self.browser.find_element(By.NAME, "email").send_keys("johndoe@example.com")
        self.browser.find_element(By.NAME, "phone").send_keys("08123456789")
        self.browser.find_element(By.NAME, "title").send_keys("Software Engineer" + Keys.RETURN)

        self.browser.get("http://localhost/DamnCRUD-main/index.php")
        page_content = self.browser.page_source
        self.assertIn("John Doe", page_content, "Kontak baru tidak muncul di daftar")

    def test_logout(self):
        self.login("admin", "nimda666!")
        self.browser.get("http://localhost/DamnCRUD-main/logout.php")
        self.assertIn("login.php", self.browser.current_url, "Logout gagal, tidak dialihkan ke login.php")

if __name__ == '__main__':
    unittest.main(verbosity=2)
