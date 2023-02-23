import time
import pycreds
from calendar import weekday
from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from cryptography.fernet import Fernet

# Decrypt password using pycreds and Fernet
passw = pycreds.find_password("Fernet")
fernet = Fernet(passw.encode('ASCII'))

class Boka_Grupprum:
    """
    A class that represents the Boka Grupprum application.

    This class contains functions that automate the booking process of study rooms in the Boka Grupprum application.
    It uses Selenium webdriver to interact with the website.
    """

    def __init__(self, preferences: list(), schedule: dict(), users: list):
        """
        Initialize the Boka_Grupprum class.

        :param preferences: A list of preferences for the booking process.
        :param schedule: A dictionary that represents the weekly schedule.
        :param users: A list of users who can make bookings.
        """
        self.preferences = preferences
        self.schedule = schedule
        self.users = users
        self.booked_dict = {
            1:              # Week 1
                {0:[],      # Monday
                1:[],       # Tuesday
                2:[],       # Wednesday
                3:[],       # Thursday
                4:[]},      # Friday
            2:              # Week 2
                {0:[],      # Monday
                1:[],       # Tuesday
                2:[],       # Wednesday
                3:[],       # Thursday
                4:[]}}      # Friday
        self.week = 1
        self.weekday = date.weekday(date.today())  # Get current day, returns a number between 0 and 6
        self.main()
        
    def main(self):
        """Main function that runs the booking process"""
        self.booked_list_function() # When this is finished, self.booked_dict is updated with all current bookings
        
        while True:                 # Main loop
            self.day_change()       # Change day
            self.book_room()        # Book room
    
    def booked_list_function(self):
        """Generates a list with all booked rooms from all users"""

        for user in self.users:
            self.login(user)
            time.sleep(1)
            self.booked_list = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='myreservationslist']/table/tbody/tr")))
            del self.booked_list[:2]

            for booked in self.booked_list:
                day, clock, week = self.date_to_weekday(booked.text.strip())
                self.booked_dict.get(week).get(day).append(clock)
            self.logout()
            time.sleep(0.5)

        self.login(self.users.pop())

    def login(self, user):
        """Login to user"""
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH)
        #self.driver.set_window_position(-10000, 0)                  # Comment this line to show chrome window
        self.driver.get("https://cloud.timeedit.net/chalmers/web/")    
        self.driver.find_element(By.CSS_SELECTOR, ".items:nth-child(4)").click()
        self.driver.find_element(By.LINK_TEXT, "Klicka här för att logga in / Please click here to log in").click()
        self.driver.find_element(By.ID, "userNameInput").send_keys(user[0])
        self.driver.find_element(By.ID, "passwordInput").send_keys(fernet.decrypt(user[1]).decode())
        self.driver.find_element(By.ID, "submitButton").click()
        self.driver.find_element(By.CSS_SELECTOR, "#contents > div:nth-child(2) > div:nth-child(7) > div.linklist > div:nth-child(3) > a:nth-child(2) > div > h2").click()
        self.driver.find_element(By.CSS_SELECTOR, "#ffsetx186 .objectinputsearchbutton").click()
        self.actions = ActionChains(self.driver)
        self.name = user[0]
        self.week = 1

    def day_change(self):
        """Changes the day on time edit, if weekend, change to monday"""

        match self.weekday:
            case 4:
                time.sleep(3)
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#leftresdateinc"))).click()
                time.sleep(1)
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#leftresdateinc"))).click()
                time.sleep(1)
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#leftresdateinc"))).click()
                self.weekday = 0
                if self.week == 2:           # TODO This needs a fix
                    self.driver.close()
                    self.driver.quit()  
                    exit()
                self.week = 2
            case 5:
                time.sleep(3)
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#leftresdateinc"))).click()
                time.sleep(1)
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#leftresdateinc"))).click()
                self.weekday = 0
                self.week = 2
            case 6:
                time.sleep(3)
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#leftresdateinc"))).click()
                self.weekday = 0
                self.week = 2
            case _:
                time.sleep(3)
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#leftresdateinc"))).click()
                self.weekday = self.weekday + 1
            
    def book_room(self):
        """Books prefered rooms from self.preferences at time intervals given by self.schedule"""

        time.sleep(1)
        slots_to_book = self.schedule.get(self.weekday)

        for slot in slots_to_book:
            time.sleep(1)
            if self.user_fully_booked(): # If user fully booked, switch user and NEW: break
                break
            if self.already_booked(slot):
                continue
            
            for preference in self.preferences:
                self.driver.find_element(By.ID, "SFC_D_0_0").clear()
                self.driver.find_element(By.ID, "SFC_D_0_0").send_keys(preference)
                self.driver.find_element(By.CSS_SELECTOR, "#ffsetx186 .objectinputsearchbutton").click()
                time.sleep(1)
                self.actions.send_keys(Keys.TAB * (9))
                self.actions.perform()
                time.sleep(0.5)
                self.book_specific_room(slot)

                if self.check_if_room_booked(): # If room booked, continue with next preference, else break
                    self.driver.find_element(By.CSS_SELECTOR, "#newResTimeDiv > div.leftreserve > a").click()
                else:
                    self.driver.find_element(By.CSS_SELECTOR, "#newResTimeDiv > div.leftreserve > a").click()
                    time.sleep(0.5)
                    self.update_booked_dict()
                    break

    def check_if_room_booked(self):
        """Check if specific room is booked by someone else"""

        if "Bokningen kunde ej genomföras." in self.driver.page_source:
            return True
        else:
            return False

    def book_specific_room(self, slot):
        """Try to book specific room at given time slot"""
        time.sleep(0.5)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"#reserveformedit > div.restimedropwrap > table > tbody > tr:nth-child(2) > td:nth-child(1) > select.timedrop.timeHourStart > option:nth-child({int(slot[0].split(':')[0])+1})"))).click()

        match int(slot[0].split(':')[1]):       # Minutes from
            case 00:
                child = 1
            case 15:
                child = 2
            case 30:
                child = 3
            case 45:
                child = 4
        self.driver.find_element(By.CSS_SELECTOR, f"#reserveformedit > div.restimedropwrap > table > tbody > tr:nth-child(2) > td:nth-child(1) > select.timedrop.timeMinuteStart > option:nth-child({child})").click()
        self.driver.find_element(By.CSS_SELECTOR, f"#reserveformedit > div.restimedropwrap > table > tbody > tr:nth-child(2) > td:nth-child(2) > select.timedrop.timeHourEnd > option:nth-child({int(slot[1].split(':')[0])+1})").click()
        match int(slot[1].split(':')[1]):       # Minutes to
            case 00:
                child = 1
            case 15:
                child = 2
            case 30:
                child = 3
            case 45:
                child = 4
        self.driver.find_element(By.CSS_SELECTOR, f"#reserveformedit > div.restimedropwrap > table > tbody > tr:nth-child(2) > td:nth-child(2) > select.timedrop.timeMinuteEnd > option:nth-child({child})").click() 
        time.sleep(0.5)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#leftreswrap > div > table > tbody > tr:nth-child(2) > td > div"))).click()
        time.sleep(0.5)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#info0 > div.infoboxtitle"))).click()
        self.driver.find_element(By.CSS_SELECTOR, "#continueRes2").click()
        time.sleep(0.5) 

    def already_booked(self, slot):
        """Check if slot already booked by user"""
    
        for day, clock in self.booked_dict.get(self.week).items():
            for booked_slot in clock:
                if day == self.weekday and booked_slot == slot:
                    return True
        return False

    def update_booked_dict(self):
        """Updates dicitonary containing all of the slots that are currently booked by all users"""

        self.booked_list = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='myreservationslist']/table/tbody/tr")))
        del self.booked_list[:2]

        for booked in self.booked_list: 
                day, clock, week = self.date_to_weekday(booked.text.strip())
                if clock not in self.booked_dict.get(week).get(day):
                    self.booked_dict.get(week).get(day).append(clock)

    def user_fully_booked(self):
        """Check if user has max amounts of rooms booked and either switches user or quits"""
        self.booked_list = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='myreservationslist']/table/tbody/tr")))
        del self.booked_list[:2]

        if len(self.booked_list) == 4:
            if self.users == []: 
                self.driver.close()
                self.driver.quit()
                exit()
            else:
                self.logout()
                self.login(self.users.pop())
                self.weekday = date.weekday(date.today())
                self.user_fully_booked() # Run again until user with slots left fount
                return True

    def logout(self):
        """Logout from account"""
        self.driver.close()

    @staticmethod
    def date_to_weekday(date_string):
        """Returns weekday, time and week from date_string"""
        booking_day = date_string[0:10]
        datum = datetime.strptime(booking_day, '%Y-%m-%d').date()
        day = datum.weekday()

        time = []
        booking_time = date_string[10:27].strip() # "08:00 - 12:00"
        time.append(booking_time[0:5]) # Appends 08:00
        time.append(booking_time[8:13]) # Appends 12:00

        week_today = datetime.now().isocalendar()[1]
        week_date = datum.isocalendar()[1]
        if week_today == week_date:
            week = 1
        else:
            week = 2

        return day, time, week
    

    # Send mail if not bookable, Not implemented
    def send_mail():
        pass
