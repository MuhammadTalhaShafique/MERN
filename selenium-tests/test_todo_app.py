import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

BASE_URL = "http://13.48.163.120:3000"  # TODO: Replace with your EC2 public IP/domain

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    yield driver
    driver.quit()

def unique_username():
    return f"testuser_{int(time.time())}"

def test_signup_new_user(driver):
    driver.get(BASE_URL)
    driver.find_element(By.XPATH, "//button[text()='Signup']").click()
    uname = unique_username()
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys(uname)
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("testpass123")
    driver.find_element(By.XPATH, "//button[text()='Signup']").click()
    assert "Your Notes" in driver.page_source

def test_signup_existing_user_error(driver):
    driver.get(BASE_URL)
    driver.find_element(By.XPATH, "//button[text()='Signup']").click()
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("existinguser")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("password")
    driver.find_element(By.XPATH, "//button[text()='Signup']").click()
    assert "User already exists" in driver.page_source or "Signup failed" in driver.page_source

def test_login_valid(driver):
    driver.get(BASE_URL)
    # Use a valid user you know exists (after running signup test)
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("existinguser")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("password")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    assert "Your Notes" in driver.page_source

def test_login_invalid_password(driver):
    driver.get(BASE_URL)
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("existinguser")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("wrongpass")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    assert "Invalid credentials" in driver.page_source or "Login failed" in driver.page_source

def test_add_note(driver):
    driver.get(BASE_URL)
    # Login first
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("existinguser")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("password")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    note = f"Test Note {int(time.time())}"
    driver.find_element(By.XPATH, "//input[@placeholder='Add new note']").send_keys(note)
    driver.find_element(By.XPATH, "//button[text()='Add']").click()
    time.sleep(1)
    assert note in driver.page_source

def test_add_empty_note(driver):
    driver.get(BASE_URL)
    # Login first
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("existinguser")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("password")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    driver.find_element(By.XPATH, "//input[@placeholder='Add new note']").send_keys("")
    driver.find_element(By.XPATH, "//button[text()='Add']").click()
    # Should not add a blank note
    time.sleep(1)
    notes = driver.find_elements(By.XPATH, "//li")
    assert all(note.text.strip() != "" for note in notes)

def test_delete_note(driver):
    driver.get(BASE_URL)
    # Login first
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("existinguser")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("password")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    # Add a note to delete
    note = f"Delete Me {int(time.time())}"
    driver.find_element(By.XPATH, "//input[@placeholder='Add new note']").send_keys(note)
    driver.find_element(By.XPATH, "//button[text()='Add']").click()
    time.sleep(1)
    # Find and delete the note
    elements = driver.find_elements(By.XPATH, f"//li[contains(., '{note}')]")
    assert elements
    elements[0].find_element(By.XPATH, ".//button[text()='Delete']").click()
    time.sleep(1)
    assert note not in driver.page_source

def test_logout(driver):
    driver.get(BASE_URL)
    # Login first
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("existinguser")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("password")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    driver.find_element(By.XPATH, "//button[text()='Logout']").click()
    assert "Login" in driver.page_source

def test_invalid_signup_empty_fields(driver):
    driver.get(BASE_URL)
    driver.find_element(By.XPATH, "//button[text()='Signup']").click()
    driver.find_element(By.XPATH, "//button[text()='Signup']").click()
    assert "Signup failed" in driver.page_source or "required" in driver.page_source

def test_login_empty_fields(driver):
    driver.get(BASE_URL)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    assert "Login failed" in driver.page_source or "required" in driver.page_source