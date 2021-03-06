"""
A crude script that scrapes a currency converter website using Selenium Webdriver.
"""

from selenium import webdriver

# Define years and currencies to loop through
target_years = range(1871, 1972)
target_currencies = [
    'US dollar [1791-2015]',
    'UK pound [1658-2015]', 
    'German mark [1871-1924]', 
    'German reichsmark [1924-1948]',
    'German Deutsche Mark [1948-2015]',
    'French franc [1795-1960]',
    'French franc [1960-2015]'
]
destination_currency = 'US dollar [1791-2015]'
destination_year = '2015'

# Initialize web driver
driver = webdriver.Safari()

# Initialize list to store results
conversions = []

for target_currency in target_currencies: # Loop through each currency

    for target_year in target_years: # Loop through each year

        # Load page and wait
        driver.get('https://www.historicalstatistics.org/Currencyconverter.html')
        driver.implicitly_wait(0.5)

        # Get relevant form elements
        form_curr_amt = driver.find_element_by_name('penningsumma')
        form_target_curr = driver.find_element_by_name('valutaenhet')
        form_target_year = driver.find_element_by_name('start')
        form_dest_curr = driver.find_element_by_name('currencycompared')
        form_dest_year = driver.find_element_by_name('end')
        form_submit_button = driver.find_element_by_xpath("//input[@type='SUBMIT']")

        # Fill out and submit form
        form_curr_amt.send_keys('1')
        form_target_curr.send_keys(target_currency)
        form_target_year.send_keys(str(target_year))
        form_dest_curr.send_keys(destination_currency)
        form_dest_year.send_keys(str(destination_year))
        form_submit_button.submit()
        driver.implicitly_wait(0.5)

        # Get HTML <p> element containing result text
        result = driver.find_element_by_xpath('//body/p[4]').text

        # Locate start and end positions of answer
        result_start = result.find('as ')
        result_end = result.find(' US dollar [1791-2015] could')

        # If start/end positions are valid, store numerical result as float
        if result_start == -1 or result_end == -1: # Invalid result
            result = 'Null'
        else: 
            result = float(result[result_start + 3 : result_end])

        # Append result to output list
        conversions.append([target_currency, target_year, result])
        driver.implicitly_wait(3)

# Close driver
driver.quit()

# Output results to CSV
f = open('knoedler_curr_conversion.csv', 'a')

for conversion in conversions:
    f.write("{0},{1},{2}\n".format(conversion[0],conversion[1],conversion[2]))

f.close()
