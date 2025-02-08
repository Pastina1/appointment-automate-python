#import necessary libraries
import selenium
import smtplib
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from termcolor import colored


#Name the program
print(colored("Melbourne Italian Consulate Automated Appointment Availability Script - v1.1", 'cyan'))

while True:
    try:


        #assign driver to the chrome webdriver. Put driver in headless mode, disable WebGL and GPU, go incognito, and modify user-agent string.
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--incognito")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--headless=new")
        options.add_argument("window-size=1920x1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
        options.add_argument('--log-level=1')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(options=options)

        #go to italian consulate link
        driver.get('https://prenotami.esteri.it/')
        time.sleep(10)
        x = 0
        y = 10

        #Loop the process until the login has been completed.
        while True:

            #Attempt to login by finding the email and password ID.
            element = driver.find_element(By.ID, 'login-email')
            element.send_keys('[EMAIL HERE]')                          #PUT YOUR EMAIL HERE
            element = driver.find_element(By.ID, 'login-password')
            element.send_keys('[PASSWORD HERE]')                          #PUT YOUR PASSWORD HERE
            element.submit()

            
            #wait for the page to load
            time.sleep(10)

            #Check if login was successful by verifying the current URL
            if driver.current_url == 'https://prenotami.esteri.it/UserArea':
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                print(colored("Login successful as of ", 'green'), colored(dt_string, 'white'))
                break #Exit the loop if login is successful

            else:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                x += 1
                print(colored("Login unsuccessful as of ", 'red') , colored(dt_string, 'white'), colored("Retrying in ", 'yellow'), colored(x, 'blue'), colored(" seconds.", 'yellow'))
                driver.get('https://prenotami.esteri.it')
                time.sleep(x)

                if x >= y:
                        print(colored("Maximum retries reached. Quitting driver and restarting in 10 minutes.", 'red'))
                        driver.quit()  # Quit the driver
                        time.sleep(10 * 60)  # Wait 10 minutes before restarting the script
                        # Break out of both loops by using a flag or a direct break
                        raise Exception("Max retries reached, restarting script.")

        #once logged in, go to the correct appointments link
        driver.get('https://prenotami.esteri.it/Services/Booking/494')
        time.sleep(10)

        #Check if link was successful and email me if so
        get_url = driver.current_url
        if get_url == 'https://prenotami.esteri.it/Services/Booking/494':
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('[GMAIL HERE]', '[APP SPECIFIC PASSWORD]')     #PUT YOUR EMAIL AND PASSWORD HERE
            server.sendmail('[YOUR GMAIL HERE]', '[YOUR GMAIL HERE]', 'There are available bookings at the Italian consulate!')
            server.quit()
            print(colored("Appointments are available, email sent.", 'green'))
            
        else:
            print(colored("No appointments available.", 'red'))
            pass

        #return to home page
        driver.get('https://prenotami.esteri.it/')

        #logout of webpage
        button = driver.find_element(By.ID, 'logoutForm')
        button.click()
        
        #quit driver to avoid memory leak, wait 30 minutes and then restart
        print(colored("Quitting driver.", 'white'))
        driver.quit()
        time.sleep(10*60)

    except Exception as e:
        print("An error occurred: ", e)
        driver.quit()



