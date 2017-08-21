from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import *
driver = webdriver.Chrome()
wait = WebDriverWait(driver,30)

def test_pageload():
    driver.delete_all_cookies()
    driver.get("https://www.flypgs.com/")
    driver.maximize_window()

def test_flight_query():
    global queryTime
    queryTime = '18:05'
    queryDate = '18.11.2017'
    queryDay = queryDate[0] + queryDate[1]
    queryMonth = queryDate[3] + queryDate[4]
    queryYear =  queryDate[6] + queryDate[7] + queryDate[8] + queryDate[9]
    flightFound = 0
    driver.find_element_by_xpath('//*[@id="fligth-searh"]/div[1]/label[2]').click()
    driver.find_element_by_xpath('//*[@id="fligth-searh"]/div[2]/span[1]/span[1]/span[1]/span/span[2]/b').click()
    driver.find_element_by_xpath('//*[contains(@id,"SAW") and contains(text(), "Istanbul-S.Gökçen")]').click()
    driver.implicitly_wait(2)
    driver.find_element_by_xpath('//*[contains(@id,"ADA")]').click()
    selectedDate = driver.find_element_by_xpath('//*[@id="dp1"]').get_attribute('value')
    while selectedDate != queryDate:
        selectedDate = driver.find_element_by_xpath('//*[@id="dp1"]').get_attribute('value')
        if selectedDate == queryDate and flightFound == 0:
            driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[1]/table/tbody/tr[{}]/td[{}]/a'.format(j,i)).send_keys(Keys.ENTER)
            flightFound = 1
            driver.find_element_by_xpath('//*[@id="fligth-searh"]/button').click()
            break
        for i in range(1,4):
            if selectedDate[3]+selectedDate[4] != queryMonth:
                element = wait.until(EC.visibility_of_element_located(('xpath','//*[@id="pgs-departure-datepicker"]/div/div[2]/div/a/span')))
                driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[2]/div/a/span').click()                      
            for j in range(1,7):
                if selectedDate != queryDate:
                    for i in range(1,8):
                        if selectedDate != queryDate:
                            selectedDate = driver.find_element_by_xpath('//*[@id="dp1"]').get_attribute('value')
                            if  selectedDate == queryDate and flightFound == 0:
                                driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[1]/table/tbody/tr[{}]/td[{}]/a'.format(j,i-1)).send_keys(Keys.ENTER)
                                driver.find_element_by_xpath('//*[@id="fligth-searh"]/button').click()
                                flightFound = 1
                                break
                            try:
                                if queryDay == driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[1]/table/tbody/tr[{}]/td[{}]/a'.format(j,i)).text:
                                    driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[1]/table/tbody/tr[{}]/td[{}]/a'.format(j,i)).click()
                                    if selectedDate == queryDate and flightFound == 0:
                                        driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[1]/table/tbody/tr[{}]/td[{}]/a'.format(j,i)).send_keys(Keys.ENTER)
                                        flightFound = 1
                                    else:
                                        driver.find_element_by_xpath('//*[@id="dp1"]').click()
                            except WebDriverException:
                                pass
            if selectedDate == queryDate and flightFound == 0:
                driver.find_element_by_xpath('//*[@id="fligth-searh"]/button').click()
                flightFound = 1
                break
        if selectedDate != queryDate:
            queryMonth = int(queryMonth) + 3
            if int(queryMonth) > 12:
                queryMonth = int(queryMonth)%12
                queryYear = int(queryYear)+1
            queryDate = '18.' + str(queryMonth) + '.' + str(queryYear)
        global finalDate
        finalDate = queryDate
    driver.implicitly_wait(5)

def test_flight_date():
    assert driver.find_element_by_xpath('/html/body/form/div/div[2]/div[3]/div[2]/span[5]').text  == finalDate

def test_ticket_price():
    driver.find_element_by_xpath('//*[starts-with(@id, "DEP_' + finalDate + '_' + queryTime + '")]').click()
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
    driver.quit()