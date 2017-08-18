import argparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

caps = DesiredCapabilities.PHANTOMJS
caps["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0"
driver = webdriver.PhantomJS(desired_capabilities=caps)

class Params:
    #read parameters from csv convert 'em to needed format to query the flight
    parser = argparse.ArgumentParser()
    parser.add_argument("--depAirport",help="Departure Airport code")
    parser.add_argument("--arrAirport",help="Arrival Airport code")
    parser.add_argument("--depDate",help="Departure Date in MMDDYYY format")
    parser.add_argument("--OWRT",help="One Way/Round Trip info", \
                        choices=["OW","RT"])
    parser.add_argument("--ss",help="Enter any value to take screenshot while scraping")#EKRAN GORUNTUSU AL/ALMA OPSIYONU EKLE!parser.add_argument()  !!HEPSI ICIN!!!! default false olacak
    parser.add_argument("--retDate",help="Return Date(only if it's Round Trip)")

    args = parser.parse_args()
    ssInfo= args.ss
    OWRT = args.OWRT
    depAirport = args.depAirport
    arrAirport = args.arrAirport
    cnvDepDate = args.depDate[2] + args.depDate[3] + '.' + args.depDate[0] + args.depDate[1] + '.' + args.depDate[4] + args.depDate[5] + args.depDate[6] + args.depDate[7]
    cnvDepDay = args.depDate[2] + args.depDate[3]
    cnvDepTime = args.depDate[9] + args.depDate[10] + ':' + args.depDate[11] + args.depDate[12]
    if args.depDate[2] == '0':
        cnvDepDay = args.depDate[3]
    cnvDepMonth = args.depDate[0] + args.depDate[1]
    if args.retDate != None:
        cnvRetDate = args.retDate[2] + args.retDate[3] + '.' + args.retDate[0] + args.retDate[1] + '.' + args.retDate[4] + args.retDate[5] + args.retDate[6] + args.retDate[7]
        cnvRetDay =  args.retDate[2] + args.retDate[3]
    if args.retDate != None:
        cnvRetTime = args.retDate[9] + args.retDate[10] + ':' + args.retDate[11] + args.retDate[12]
    if args.retDate != None and args.retDate[2] == '0':
        cnvRetDay = args.retDate[3]

driver.delete_all_cookies()
print('Cookies deleted')

driver.get("https://www.flypgs.com/")
driver.maximize_window()

flight = Params()
wait = WebDriverWait(driver, 30 )
element = wait.until(EC.presence_of_element_located(('xpath','//*[@id="fligth-searh"]/div[2]/span[1]/span[1]/span[1]/span')))
actions = ActionChains(driver)
if flight.OWRT == 'OW':
    flightFound = 0
    driver.find_element_by_xpath('//*[@id="fligth-searh"]/div[1]/label[2]').click()
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[@id="fligth-searh"]/div[2]/span[1]/span[1]/span[1]/span').click()
    driver.find_element_by_xpath('//*[contains(@id,"%s")]' % flight.depAirport).click()
    driver.implicitly_wait(2)
    driver.find_element_by_xpath('//*[contains(@id,"%s")]' % flight.arrAirport).click()
    selectedDate = driver.find_element_by_xpath('//*[@id="dp1"]').get_attribute('value')
    if selectedDate == flight.cnvDepDate:
        driver.find_element_by_xpath('//*[@id="fligth-searh"]/button').click()
        flightFound = 1
    for i in range(1,13):
        if selectedDate[3]+selectedDate[4] != flight.cnvDepMonth:
            element = wait.until(EC.visibility_of_element_located(('xpath','//*[@id="pgs-departure-datepicker"]/div/div[2]/div/a/span')))
            driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[2]/div/a/span').click()
            print('clicked next month')                       
        for j in range(1,7):
            if selectedDate != flight.cnvDepDate:
                for i in range(1,8):
                    if selectedDate != flight.cnvDepDate:
                        selectedDate = driver.find_element_by_xpath('//*[@id="dp1"]').get_attribute('value')
                        if  selectedDate == flight.cnvDepDate and flightFound == 0:
                            driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[1]/table/tbody/tr[{}]/td[{}]/a'.format(j,i-1)).send_keys(Keys.ENTER)
                            driver.find_element_by_xpath('//*[@id="fligth-searh"]/button').click()
                            flightFound = 1
                        try:
                            if flight.cnvDepDay == driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[1]/table/tbody/tr[{}]/td[{}]/a'.format(j,i)).text:
                                driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[1]/table/tbody/tr[{}]/td[{}]/a'.format(j,i)).click()
                                if selectedDate == flight.cnvDepDate and flightFound == 0:
                                    driver.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[1]/table/tbody/tr[{}]/td[{}]/a'.format(j,i)).send_keys(Keys.ENTER)
                                    flightFound = 1
                                else:
                                    driver.find_element_by_xpath('//*[@id="dp1"]').click()
                        except WebDriverException:
                            print('oh can\'t click ' ,i ,j)
        if selectedDate == flight.cnvDepDate and flightFound == 0:
            driver.find_element_by_xpath('//*[@id="fligth-searh"]/button').click()
            flightFound = 1

if flight.ssInfo != None:    
    driver.save_screenshot('PGS_1.png')
    print('ss1 saved.')

element = wait.until(EC.presence_of_element_located(('xpath','//*[starts-with(@id, "DEP_' + flight.cnvDepDate + '_' + flight.cnvDepTime +'")]')))
print(driver.find_element_by_xpath('//*[@id="threeDaysViewDEP"]/div[1]/div/div[2]').text)
driver.find_element_by_xpath('//*[starts-with(@id, "DEP_' + flight.cnvDepDate + '_' + flight.cnvDepTime +'")]').click()
driver.implicitly_wait(3)
element = driver.find_element_by_xpath('//*[@id="actualDayFlightsDEP"]/div[1]/div')
print(element.text)
driver.implicitly_wait(3)

element = wait.until(EC.element_to_be_clickable(('id','btnText')))

driver.find_element_by_id('btnText').click()

try:
    element = wait.until(EC.presence_of_element_located(('xpath','//*[@id="bundle-upgrade-modal"]/div[1]/div/div[2]/a[2]')))
    driver.find_element_by_xpath('//*[@id="bundle-upgrade-modal"]/div[1]/div/div[2]/a[2]').click()
except:
    pass

if flight.ssInfo != None:
    driver.save_screenshot('PGS_2.png')
    print('ss2 saved.')

element = driver.find_element_by_id('totalFare')
print('Ticket price: '+element.text)

driver.find_element_by_id('btnSubmit').click()
driver.implicitly_wait(3)
driver.find_element_by_xpath('//*[@id="modal-insurance"]/span[1]/span').click()

if flight.ssInfo != None:
    driver.save_screenshot('PGS_3.png')
    print('ss3 saved.')

driver.find_element_by_xpath('//*[@id="AdultGender0"]').click()
driver.find_element_by_xpath('//*[@id="AdultGender0"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)
driver.find_element_by_xpath('//*[@id="AdultName0"]').send_keys('Foo')
driver.find_element_by_xpath('//*[@id="AdultSurname0"]').send_keys('Bar')
driver.find_element_by_xpath('//*[@id="AdultBDayDay0"]').click()
driver.find_element_by_xpath('//*[@id="AdultBDayDay0"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)
driver.find_element_by_xpath('//*[@id="AdultBDayMonth0"]').click()
driver.find_element_by_xpath('//*[@id="AdultBDayMonth0"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)
driver.find_element_by_xpath('//*[@id="AdultBDayYear0"]').click()
driver.find_element_by_xpath('//*[@id="AdultBDayYear0"]').send_keys(1965)
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
print(driver.title)

if flight.ssInfo != None:
    driver.save_screenshot('PGS_4.png')
    print('ss4 saved.')

driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/div[2]/a/span').click()

element = wait.until(EC.visibility_of_element_located(('xpath','//*[@id="confirm-modal"]/span[2]/span')))
driver.find_element_by_xpath('//*[@id="confirm-modal"]/span[2]/span').click()

driver.implicitly_wait(30)

if flight.ssInfo != None:
    driver.save_screenshot('PGS_5.png')
    print('ss5 saved.')

driver.find_element_by_xpath('//*[@id="CB_CC"]').click()
driver.find_element_by_xpath('//*[@id="TBCC1234Clone"]').send_keys('4916989656739611')
driver.find_element_by_xpath('//*[@id="TBCCHolder"]').send_keys('Foo Bar')
driver.find_element_by_xpath('//*[@id="TBCVC"]').send_keys('127')
driver.find_element_by_xpath('//*[@id="TBExpMonth"]').click()
driver.find_element_by_xpath('//*[@id="TBExpMonth"]').send_keys('01',Keys.ENTER)
driver.find_element_by_xpath('//*[@id="TBExpYear"]').click()
driver.find_element_by_xpath('//*[@id="TBExpYear"]').send_keys('2022',Keys.ENTER)
driver.find_element_by_xpath('//*[@id="RULES_CB"]').click()

if flight.ssInfo != None:
    driver.save_screenshot('PGS_6.png')
    print('ss6 saved.')

print('Scraping has completed successfully.')

driver.quit()
