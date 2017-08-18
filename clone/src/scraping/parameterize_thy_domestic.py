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
    parser.add_argument("--depAirport",help="Departure Airport")
    parser.add_argument("--arrAirport",help="Arrival Airport")
    parser.add_argument("--depDate",help="Departure Date")
    parser.add_argument("--OWRT",help="One Way/Round Trip info", \
                        choices=["OW","RT"])
    parser.add_argument("--ss",help="Enter any value to take screenshot while scraping")
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
driver.get("http://www.turkishairlines.com/tr-tr?returnoldversion")

flight = Params()
wait = WebDriverWait(driver, 30 )
element = wait.until(EC.presence_of_element_located(('id','godate')))
if flight.OWRT == 'OW':
    driver.find_element_by_class_name('one_way').click()
    selectedDate = driver.find_element_by_xpath('//*[@id="godate"]').get_attribute('value')
    print(selectedDate)
    driver.find_element_by_id('godate').click()
    print(flight.cnvDepMonth)
    flightFound = 0
    for i in range(1,13):
        if selectedDate[3]+selectedDate[4] != flight.cnvDepMonth:
            driver.find_element_by_xpath('//*[@id="calendar-100000001"]/div[2]/a[2]').click() 
            print('clicked next month')                       
        for j in range(1,7):
            if selectedDate != flight.cnvDepDate:
                for i in range(1,8):
                    if selectedDate != flight.cnvDepDate:
                        selectedDate = driver.find_element_by_xpath('//*[@id="godate"]').get_attribute('value')
                        if  selectedDate == flight.cnvDepDate and flightFound == 0:
                            driver.find_element_by_id('from').click()
                            driver.find_element_by_id('from').send_keys(flight.depAirport)
                            driver.find_element_by_id('from').send_keys(Keys.ENTER)
                            driver.find_element_by_id('to').send_keys(flight.arrAirport)
                            driver.find_element_by_id('to').send_keys(Keys.ENTER)
                            driver.find_element_by_id('to').send_keys(Keys.ENTER)
                            flightFound = 1
                        try:
                            if flight.cnvDepDay == driver.find_element_by_xpath('//*[@id="calendar-100000000"]/div[3]/table/tbody/tr[{}]/td[{}]'.format(j,i)).text:
                                driver.find_element_by_xpath('//*[@id="calendar-100000000"]/div[3]/table/tbody/tr[{}]/td[{}]'.format(j,i)).click()
                                if selectedDate == flight.cnvDepDate and flightFound == 0:
                                    driver.find_element_by_id('from').click()
                                    driver.find_element_by_id('from').send_keys(flight.depAirport)
                                    driver.find_element_by_id('from').send_keys(Keys.ENTER)
                                    driver.find_element_by_id('to').send_keys(flight.arrAirport)
                                    driver.find_element_by_id('to').send_keys(Keys.ENTER)
                                    driver.find_element_by_id('to').send_keys(Keys.ENTER)
                                    flightFound = 1
                                else:
                                    driver.find_element_by_id('godate').click()
                        except WebDriverException:
                            print('oh can\'t click ' ,i ,j)
        if selectedDate == flight.cnvDepDate and flightFound == 0:
            driver.find_element_by_id('from').click()
            driver.find_element_by_id('from').send_keys(flight.depAirport)
            driver.find_element_by_id('from').send_keys(Keys.ENTER)
            driver.find_element_by_id('to').send_keys(flight.arrAirport)
            driver.find_element_by_id('to').send_keys(Keys.ENTER)
            driver.find_element_by_id('to').send_keys(Keys.ENTER)
            flightFound = 1

print('Querying the flight')

if flight.ssInfo != None:
    driver.save_screenshot('THY_1.png')
    print('ss1 saved')

try: ## new flight picker
    for i in range(0,41):
        try:    
            if driver.find_element_by_xpath('//*[@id="b0Flight{}Segment0TrEl"]/th[1]/span[1]/time'.format(i)).text == flight.cnvDepTime:
                if i<10:
                    gonnaclick = '0' + str(i)
                    driver.find_element_by_id('b0F{}_TREUPROTdEl'.format(gonnaclick)).click()
                else:
                    driver.find_element_by_id('b0F{}_TREUPROTdEl'.format(i)).click()
                break
        except:
            break
except: ## old flight picker
    for i in range(1,41):
        if driver.find_element_by_xpath('//*[@id="table-fly_list1"]/tbody[{}]/tr/td[1]'.format(i)).text == flight.cnvDepTime:
            driver.find_element_by_xpath('//*[@id="table-fly_list1"]/tbody[{}]/tr/td[8]'.format(i)).click()
            break
    driver.find_element_by_xpath('//*[@id="flightSelectionForm"]/div[6]/button[2]').click()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//*[@id="form1"]/div[4]/button[2]').click()
    
driver.find_element_by_id('sideSubmitButton').click()

if flight.ssInfo != None:
    driver.save_screenshot('THY_2.png')
    print('ss2 saved')

element = wait.until(EC.presence_of_element_located(('id','firstName')))

driver.find_element_by_id('firstName').send_keys('Foo')
driver.find_element_by_id('lastName').send_keys('Bar')
driver.find_element_by_id('title').click()
driver.find_element_by_id('title').send_keys('b')
driver.find_element_by_id('title').send_keys(Keys.ENTER)
driver.find_element_by_id('tcKimlik').send_keys('63482365210')
driver.find_element_by_id('dobDay').click()
driver.find_element_by_id('dobDay').send_keys('1')
driver.find_element_by_id('dobDay').send_keys(Keys.ENTER)
driver.find_element_by_id('dobMonth').click()
driver.find_element_by_id('dobMonth').send_keys('ocak')
driver.find_element_by_id('dobMonth').send_keys(Keys.ENTER)
driver.find_element_by_id('dobYear').click()
driver.find_element_by_id('dobYear').send_keys('1965')
driver.find_element_by_id('dobYear').send_keys(Keys.ENTER)
driver.find_element_by_id('eMail').send_keys('foobar@gmail.com')
driver.find_element_by_id('ceMail').send_keys('foobar@gmail.com')
driver.find_element_by_id('oprCode').send_keys('532')
driver.find_element_by_id('mobilePhone').send_keys('1111111')

element = wait.until(EC.presence_of_element_located(('xpath','//*[@id="form1"]/div[7]/button[1]')))
driver.find_element_by_xpath('//*[@id="form1"]/div[7]/button[1]').click()

element = wait.until(EC.presence_of_element_located(('id','Box_CC')))

if flight.ssInfo != None:
    driver.save_screenshot('THY_3.png')
    print('ss3 saved')

element =  driver.find_element_by_id('grandTotal')
print('Ticket price: ' + element.text)

driver.find_element_by_id('Box_CC').click()

wait = WebDriverWait(driver, 60)
element = wait.until(EC.element_to_be_clickable(('id','number1')))

driver.find_element_by_id('number1').click()
driver.find_element_by_id('number1').send_keys('4916989656739611')
driver.find_element_by_id('CVC').send_keys('127')
driver.find_element_by_id('chCity').send_keys('Mersin')
driver.find_element_by_id('chAdres1').send_keys('Mersin mersin mersin')
driver.find_element_by_id('expmonth').click()
driver.find_element_by_id('expmonth').send_keys('01')
driver.find_element_by_id('expmonth').send_keys(Keys.ENTER)
driver.find_element_by_id('expyear').click()
driver.find_element_by_id('expyear').send_keys('2022')
driver.find_element_by_id('expyear').send_keys(Keys.ENTER)
driver.find_element_by_id('chCountry').click()
driver.find_element_by_id('chCountry').send_keys('T')
driver.find_element_by_id('chCountry').send_keys(Keys.ENTER)

driver.find_element_by_xpath('//*[@id="onay1" and @rel="onay1"]').click()
driver.find_element_by_id('kk_button').click()

print('Scraping has completed successfully')

driver.quit()
