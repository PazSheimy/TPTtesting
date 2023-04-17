from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


# checks if error is thrown when entering valid object name and invalid radius
def test_error1():
    driver = webdriver.Firefox("C:\\Users\\pmac3\\PycharmProjects\\Software Testing\\TPTtesting\\driver")
    driver.get("http://127.0.0.1:5000/")
    driver.maximize_window()

    element = driver.find_element(By.ID, "search_input")
    element.send_keys("sirius")
    element = driver.find_element(By.ID, "radius")
    element.send_keys("def")
    element = driver.find_element(By.ID, "search_btn")
    sleep(2)
    element.click()
    sleep(2)
    element_error = driver.find_elements(By.ID, "error_message")
    assert len(element_error) > 0
    driver.close()


# checks if error is thrown when entering valid numbers in search letters in radius
def test_error2():
    driver = webdriver.Firefox("C:\\Users\\pmac3\\PycharmProjects\\Software Testing\\TPTtesting\\driver")
    driver.get("http://127.0.0.1:5000/")
    driver.maximize_window()

    element = driver.find_element(By.ID, "search_input")
    element.send_keys("101.2872 -16.7161")
    element = driver.find_element(By.ID, "radius")
    element.send_keys("abc")
    element = driver.find_element(By.ID, "search_btn")
    sleep(2)
    element.click()
    sleep(2)
    element_error = driver.find_elements(By.ID, "error_message")
    assert len(element_error) > 0
    driver.close()


# checks if error is thrown when entering negative number for radius
def test_error3():
    driver = webdriver.Firefox("C:\\Users\\pmac3\\PycharmProjects\\Software Testing\\TPTtesting\\driver")
    driver.get("http://127.0.0.1:5000/")
    driver.maximize_window()

    element = driver.find_element(By.ID, "search_input")
    element.send_keys("101.2872 -16.7161")
    element = driver.find_element(By.ID, "radius")
    element.send_keys("-1")
    element = driver.find_element(By.ID, "search_btn")
    sleep(2)
    element.click()
    sleep(2)
    element_error = driver.find_elements(By.ID, "error_message")
    assert len(element_error) > 0
    driver.close()
