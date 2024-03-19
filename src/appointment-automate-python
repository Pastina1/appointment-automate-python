#import necessary libraries
import selenium
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

while True:
#assign driver to the chrome webdriver
    driver = webdriver.Chrome()

#go to italian consulate link
    driver.get('https://prenotami.esteri.it/')
    time.sleep(10)

#find email and password ID, input the correct data and submit
    element = driver.find_element(By.ID, 'login-email')
    element.send_keys('[Your Email Here]')
    element = driver.find_element(By.ID, 'login-password')
    element.send_keys('[Your Password Here]')
    element.submit()
    time.sleep(10)

#once logged in, go to the correct appointments link
    driver.get('https://prenotami.esteri.it/Services/Booking/494')
    time.sleep(20)

#Check if link was successful and email me if so
    get_url = driver.current_url
    if get_url == 'https://prenotami.esteri.it/Services/Booking/494':
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('[Your Gmail Here]', '[Your App Specific Password Here]')
        server.sendmail('[Your Gmail Here]', 'There are available bookings at the Italian consulate!')
        server.quit()
    else:
        pass

#return to home page
    driver.get('https://prenotami.esteri.it/')

#logout of webpage
    button = driver.find_element(By.ID, 'logoutForm')
    button.click()
#quit driver to avoid memory leak, wait 30 minutes and then restart
    driver.quit()
    time.sleep(10)

