#import necessary libraries
import selenium
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

while True:
    try:
        #assign driver to the chrome webdriver
        driver = webdriver.Chrome()

        #go to italian consulate link
        driver.get('https://prenotami.esteri.it/')
        time.sleep(10)
        x = 0

        #Loop the process until the login has been completed.
        while True:
            #Attempt to login by finding the email and password ID.
            element = driver.find_element(By.ID, 'login-email')
            element.send_keys('[YOUR EMAIL HERE]')
            element = driver.find_element(By.ID, 'login-password')
            element.send_keys('[YOUR PASSWORD HERE]')
            element.submit()
            
            #wait for the page to load
            time.sleep(10)

            #Check if login was successful by verifying the current URL
            if driver.current_url == 'https://prenotami.esteri.it/UserArea':
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                print("Login successful as of ", dt_string)
                break #Exit the loop if login is successful
            else:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                x += 1
                print("Login unsuccessful as of", dt_string, ". Retrying in ", x, " seconds." )
                driver.get('https://prenotami.esteri.it')
                time.sleep(x)

        #once logged in, go to the correct appointments link
        driver.get('https://prenotami.esteri.it/Services/Booking/494')
        time.sleep(10)

        #Check if link was successful and email me if so
        get_url = driver.current_url
        if get_url == 'https://prenotami.esteri.it/Services/Booking/494':
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('[YOUR GMAIL HERE]', '[APP SPECIFIC PASSWORD')
            server.sendmail('[YOUR GMAIL HERE]', 'There are available bookings at the Italian consulate!')
            server.quit()
            print("Appointments are available, email sent.")
        else:
            print("No appointments available.")
            pass

        #return to home page
        driver.get('https://prenotami.esteri.it/')

        #logout of webpage
        button = driver.find_element(By.ID, 'logoutForm')
        button.click()
        
        #quit driver to avoid memory leak, wait 30 minutes and then restart
        print("Quitting driver.")
        driver.quit()
        time.sleep(30*60)

    #Catch any exceptions that may be raised and rerun code
    except Exception as e:
        print("An error occurred: ", e)
        driver.quit()



