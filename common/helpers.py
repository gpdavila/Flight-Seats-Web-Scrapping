import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.structures import *


def validate_args(first, second):
    '''
    Checks if both seats contains letters AND numbers
    '''
    if((not first.isalpha() and not first.isdigit())
        and (not second.isalpha() and not second.isdigit())):
        return True

def find_element(driver, identifier):
    '''
    Returns the HTML element otherwise, it returns None
    '''
    try:
        return driver.find_element_by_id(identifier)
    except:
        return None

def select_seat_position(seat_number,seat_letter):
    '''
    Selects the correct seat position considering the 
    special seat line cases (seat_numbers 22 and 60)
    '''
    seat_position = column_seat.get(seat_letter, '-1')
    if(seat_position == '-1'):
        raise MyError(ErrorMessage.INVALID)

    if(seat_number == "60"):
        if(seat_letter == "B" or seat_letter == "J"):
            raise MyError(ErrorMessage.INVALID)
        elif(seat_letter == "C" or seat_letter == "K"):
            seat_position = 1

    if(seat_number == "22"):
        if(seat_letter == "C" or seat_letter == "K"):
            seat_position = 0
        else:
            raise MyError(ErrorMessage.INVALID)

    return seat_position

def select_seat(driver, seat):
    '''
    Selects the seat
    '''
    seat_number = re.findall(r'\d+', seat)
    seat_letter = re.findall(r'[a-zA-Z]+', seat)

    available_halls = driver.find_elements_by_xpath(
        "//*[@class='row-group gr-flex gr-justify-center gr-items-center gr-py-3px sm:gr-p-2'and ./ancestor::div[@class='row-"
        + seat_number[0]
        + " gr-flex gr-justify-between gr-items-center gr-px-4 sm:gr-border-l-8 sm:gr-border-r-8 gr-border-gray-300']]"
        )
    
    #seat number is not valid
    if(len(available_halls)==0):
        raise MyError(ErrorMessage.INVALID)

    #seat letter is not valid
    column = column_group.get(seat_letter[0].upper(), '-1')
    if (column == '-1'):
        raise MyError(ErrorMessage.INVALID)

    correct_hall = available_halls[column]
    available_seat_columns = correct_hall.find_elements_by_xpath("./button")

    #full coffe/bathroom seat_column in the hall
    if(len(available_seat_columns) == 0): 
        raise MyError(ErrorMessage.INVALID)

    seat_position = select_seat_position(seat_number[0], seat_letter[0].upper())

    #seat is taken
    if(available_seat_columns[seat_position].get_attribute("style") == 'margin: 0rem;'):
        raise MyError(ErrorMessage.OCCUPIED) 

    available_seat_columns[seat_position].click()
    
    #seat is near by an emergency exit
    accept_exit_regulations_button = find_element(driver, "accept_exit_regulations")
    if (accept_exit_regulations_button != None):
        accept_exit_regulations_button.click()

    seat_select_list = driver.find_elements_by_id("select-seat")
    seat_select_button = seat_select_list[0]
    seat_select_button.click()

    next_button = driver.find_element_by_id("next-button")
    next_button.click()

def take_seats_screenshot(driver):
    '''
    Goes to the bottom of the main page and takes a
    screenshot of the "Seat Selection" only
    '''
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "next-button"))
    )
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #select the web element "Seat Selection"
    image = driver.find_element_by_xpath("//*[@class='sc-eCssSg hmocIu gr-block sm:gr-flex']")

    image.screenshot('screenshot.png')