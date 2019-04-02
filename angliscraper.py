from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date, timedelta
import time
from selenium.webdriver.support.ui import Select


driver = webdriver.Chrome('input_driver_location_here')
f = open('anglilist.txt', 'w+')

# init start and end dates
# (change to dates within which you want to find the new anglicisms)
start_date = date(2017, 1, 1)
end_date = date(2018, 1, 1)

# funct that gives back date range
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date+timedelta(n)


latestmonth = str(date.today().month)
latestday = str(date.today().day)

# loops through all anglicisms pages for given daterange
for day in daterange(start_date, end_date):
    yr = day.strftime("%Y")
    date = day.strftime("%Y%m%d")
    driver.get('http://clu.uni.no/avis/nye/klass/' + yr + '/' + date + '/anglicisms.html')

    # locates all links
    linkslist = driver.find_elements_by_tag_name('a')

    # saves text from all anglicisms in anglilist file
    for link in linkslist[1:]:  # cuts of first link bc it's to Arkiv
        f.write(link.text + '\n')

# closes anglicism storage file
f.close()

# opens file to read anglicisms
fi = open('anglilist.txt', 'r')

# opens file to store anglicisms and frequencies
wf = open('angli_freqs.txt', 'w')
wf.write("Word,Frequency\n")
currwd = fi.readline().strip()
driver.get('http://clu.uni.no/avis/bokm.html')

# locates the input box for the search word
inputbox = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[2]/td[2]/input')

while currwd != '':
    #input the current word in the search box
    inputbox.send_keys(currwd)

    # selects the year to be searched
    # if wish to change year(s) to be searched,
    # change the "KORPUSXX" value below
    dropdown = Select(driver.find_element_by_xpath('/html/body/form/table[1]/tbody/tr[2]/td[1]/select'))
    dropdown.select_by_value("KORPUS12")

    # click search
    driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[1]/td/input').click()

    # locate necessary number on page
    el = driver.find_element_by_tag_name('body')
    numlist = el.text.split('\n')[4].split()
    num = numlist[5]

    # if frequency number is above threshold, put word and frequency into file
    if int(num) > 4:
        wf.write(currwd + ',' + num + '\n')

    # go back to search page, redefine inputbox and clear it, update word
    driver.back()
    inputbox = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[2]/td[2]/input')
    inputbox.clear()
    currwd = fi.readline().strip()

wf.close()
fi.close()
driver.close()
