from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import *
driver = webdriver.Chrome()
wait = WebDriverWait(driver,60)

def test_pageload():
    driver.delete_all_cookies()
    driver.get("https://www.flypgs.com/")
    driver.maximize_window()

def test_flight_query():
    driver.find_element_by_xpath('//*[@id="fligth-searh"]/div[1]/label[2]').click()
    driver.find_element_by_xpath('//*[@id="dp1"]').click()
    driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[2]/div/a/span').click()
    driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[2]/div/a/span').click()
    driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[2]/table/tbody/tr[4]/td[4]/a').click()
    driver.find_element_by_xpath('//*[@id="fligth-searh"]/div[2]/span[1]/span[1]/span[1]/span/span[2]/b').click()
    driver.save_screenshot('ss_saved.png')
    driver.find_element_by_xpath('//*[contains(@id,"SAW") and contains(text(), "Istanbul-S.Gökçen")]').click()
    driver.implicitly_wait(2)
    driver.find_element_by_xpath('//*[contains(@id,"ADA")]').click()
    driver.find_element_by_xpath('//*[@id="fligth-searh"]/button').click()
    driver.implicitly_wait(5)

def test_flight_date():
    assert driver.find_element_by_xpath('/html/body/form/div/div[2]/div[3]/div[2]/span[5]').text  == '23.11.2017'

def test_ticket_price():
    driver.find_element_by_xpath('//*[starts-with(@id, "DEP_23.11.2017_18:05")]').click()
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[@id="btnText"]').click()
    driver.find_element_by_xpath('//*[@id="bundle-upgrade-modal"]/div[1]/div/div[2]/a[2]').click()

def test_personal_info():
    driver.find_element_by_id('btnSubmit').click()
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[@id="modal-insurance"]/span[1]/span').click()
    driver.find_element_by_xpath('//*[@id="AdultGender0"]').click()
    driver.find_element_by_xpath('//*[@id="AdultGender0"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)
    driver.find_element_by_xpath('//*[@id="AdultName0"]').send_keys('Foo')
    driver.find_element_by_xpath('//*[@id="AdultSurname0"]').send_keys('Bar')
    driver.find_element_by_xpath('//*[@id="AdultBDayDay0"]').click()
    driver.find_element_by_xpath('//*[@id="AdultBDayDay0"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)
    driver.find_element_by_xpath('//*[@id="AdultBDayMonth0"]').click()
    driver.find_element_by_xpath('//*[@id="AdultBDayMonth0"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)
    driver.find_element_by_xpath('//*[@id="AdultBDayYear0"]').click()
    driver.find_element_by_xpath('//*[@id="AdultBDayYear0"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)
    driver.find_element_by_xpath('//*[@id="Citizenship_Adult0"]').click()
    element = wait.until(EC.presence_of_element_located(('xpath','//*[@id="AdultSocSecNo0"]')))
    driver.find_element_by_xpath('//*[@id="AdultSocSecNo0"]').send_keys('37749558288')
    driver.find_element_by_xpath('//*[@id="PhoneCountryCode"]').send_keys('90')
    driver.find_element_by_xpath('//*[@id="PhoneAreaCode"]').send_keys('532')
    driver.find_element_by_xpath('//*[@id="PhoneNumber"]').send_keys('3698520')
    driver.find_element_by_xpath('//*[@id="Email"]').send_keys('foobar@gmail.com')
    driver.find_element_by_xpath('//*[@id="COUNTRY_OF_RESIDENCE"]').click()
    driver.find_element_by_xpath('//*[@id="COUNTRY_OF_RESIDENCE"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)
    driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/div[2]/div[8]/div[2]/div/div/div[2]/input').click()
    driver.find_element_by_xpath('//*[@id="CBSMS"]').click()
    element = wait.until(EC.presence_of_element_located(('xpath','/html/body/form/div[2]/div[2]/div[2]/a/span')))
    driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/div[2]/div[8]/div[2]/div/div/div[2]').click()
    
def test_final_price():
    driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/div[2]/a/span').click()
    element = wait.until(EC.visibility_of_element_located(('xpath','//*[@id="confirm-modal"]/span[2]/span')))
    driver.find_element_by_xpath('//*[@id="confirm-modal"]/span[2]/span').click()

def test_card_info():
    driver.find_element_by_xpath('//*[@id="CB_CC"]').click()
    driver.find_element_by_xpath('//*[@id="TBCC1234Clone"]').send_keys('4916989656739611')
    driver.find_element_by_xpath('//*[@id="TBCCHolder"]').send_keys('Foo Bar')
    driver.find_element_by_xpath('//*[@id="TBCVC"]').send_keys('127')
    driver.find_element_by_xpath('//*[@id="TBExpMonth"]').click()
    driver.find_element_by_xpath('//*[@id="TBExpMonth"]').send_keys('01',Keys.ENTER)
    driver.find_element_by_xpath('//*[@id="TBExpYear"]').click()
    driver.find_element_by_xpath('//*[@id="TBExpYear"]').send_keys('2022',Keys.ENTER)
    driver.find_element_by_xpath('//*[@id="RULES_CB"]').click()