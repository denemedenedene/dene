from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
caps = DesiredCapabilities.PHANTOMJS
caps["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0"
driver = webdriver.PhantomJS(desired_capabilities=caps)

driver.delete_all_cookies()
print('Cookies deleted')
driver.get("http://www.turkishairlines.com/tr-tr/")

wait = WebDriverWait(driver, 60 )
element = wait.until(EC.presence_of_element_located(('id','godate')))
driver.find_element_by_class_name('one_way').click()
driver.find_element_by_id('godate').click()
driver.find_element_by_xpath('//*[@id="calendar-100000001"]/div[3]/table/tbody/tr[4]/td[4]').click()
driver.find_element_by_id('from').send_keys('ist')
driver.find_element_by_id('from').send_keys(Keys.ENTER)
driver.find_element_by_id('to').send_keys('ada')
driver.find_element_by_id('to').send_keys(Keys.ENTER)
driver.find_element_by_id('to').send_keys(Keys.ENTER)
print('Querying the flight')

driver.implicitly_wait(60)
driver.save_screenshot('THY_1.png')
print('ss1 saved')

try:
    element = wait.until(EC.presence_of_element_located(('id','sideSubmitButton')))
except:
    driver.refresh()

driver.find_element_by_id('sideSubmitButton').click()
driver.save_screenshot('THY_2.png')
print('ss2 saved')

element = wait.until(EC.presence_of_element_located(('id','firstName')))

print('Filling personal informations')
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
