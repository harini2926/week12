
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.getenv("APP_URL", "http://127.0.0.1:5000")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use a remote Selenium browser if SELENIUM_REMOTE_URL is configured.
    remote_url = os.getenv("SELENIUM_REMOTE_URL")

    if remote_url:
        browser = webdriver.Remote(
            command_executor=remote_url,
            options=options
        )
    else:
        browser = webdriver.Chrome(options=options)

    yield browser
    browser.quit()


def test_registration_page_opens(driver):
    driver.get(BASE_URL + "/register")

    assert "Course Registration form of student" in driver.page_source


def test_successful_registration(driver):
    driver.get(BASE_URL + "/register")

    driver.find_element(By.NAME, "name").send_keys("Harini")
    driver.find_element(By.NAME, "email").send_keys("harini@example.com")
    driver.find_element(By.NAME, "course").send_keys("Information Technology")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    wait = WebDriverWait(driver, 10)
    heading = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    )

    assert heading.text == "Registration Successful!"
    assert "Harini" in driver.page_source
    assert "harini@example.com" in driver.page_source
    assert "Information Technology" in driver.page_source


def test_empty_fields_show_error(driver):
    driver.get(BASE_URL + "/register")

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    wait = WebDriverWait(driver, 10)
    error = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Please fill in all fields.')]")
        )
    )

    assert error.is_displayed()


def test_register_another_student_link(driver):
    driver.get(BASE_URL + "/register")

    driver.find_element(By.NAME, "name").send_keys("Harini")
    driver.find_element(By.NAME, "email").send_keys("harini@example.com")
    driver.find_element(By.NAME, "course").send_keys("IT")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    wait = WebDriverWait(driver, 10)
    link = wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Register another student")
        )
    )
    link.click()

    assert "/register" in driver.current_url
    assert "Course Registration form of student" in driver.page_source


def test_home_redirects_to_registration(driver):
    driver.get(BASE_URL + "/")

    assert driver.current_url.rstrip("/").endswith("/register")
    assert "Course Registration form of student" in driver.page_source
