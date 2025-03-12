import unittest
import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class DamnCRUDTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        server = 'http://localhost:4444'

        self.browser = webdriver.Remote(command_executor=server, options=options)
        self.addCleanup(self.browser.quit)

    def test_login_valid(self):
        self.browser.get("http://localhost/DamnCRUD-main/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!" + Keys.RETURN)
        time.sleep(2)
        self.assertIn("index.php", self.browser.current_url, "Gagal login dengan kredensial valid")

    def test_login_invalid(self):
        self.browser.get("http://localhost/DamnCRUD-main/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("wronguser")
        self.browser.find_element(By.NAME, "password").send_keys("wrongpass" + Keys.RETURN)
        time.sleep(2)
        error_message = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Damn, wrong credentials!!", error_message, "Pesan error tidak muncul saat login gagal")

    def test_create_contact(self):
        self.test_login_valid()
        self.browser.get("http://localhost/DamnCRUD-main/create.php")
        time.sleep(2)

        self.browser.find_element(By.NAME, "name").send_keys("John Doe")
        self.browser.find_element(By.NAME, "email").send_keys("johndoe@example.com")
        self.browser.find_element(By.NAME, "phone").send_keys("08123456789")
        self.browser.find_element(By.NAME, "title").send_keys("Software Engineer" + Keys.RETURN)
        time.sleep(2)

        self.browser.get("http://localhost/DamnCRUD-main/index.php")
        page_content = self.browser.page_source
        self.assertIn("John Doe", page_content, "Kontak baru tidak muncul di daftar")

    def test_edit_contact(self):
        self.test_login_valid()
        self.browser.get("http://localhost/DamnCRUD-main/index.php")
        time.sleep(2)

        self.browser.find_element(By.LINK_TEXT, "edit").click()
        time.sleep(2)

        name_input = self.browser.find_element(By.NAME, "name")
        name_input.clear()
        name_input.send_keys("Jane Doe")

        email_input = self.browser.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys("janedoe@example.com")

        self.browser.find_element(By.NAME, "title").send_keys(Keys.RETURN)
        time.sleep(2)

        self.browser.get("http://localhost/DamnCRUD-main/index.php")
        page_content = self.browser.page_source
        self.assertIn("Jane Doe", page_content, "Data kontak tidak berhasil diperbarui")

    def test_logout(self):
        self.test_login_valid()
        self.browser.get("http://localhost/DamnCRUD-main/logout.php")
        time.sleep(2)
        self.assertIn("login.php", self.browser.current_url, "Logout gagal, tidak dialihkan ke login.php")

if __name__ == '__main__':
    unittest.main(verbosity=2)