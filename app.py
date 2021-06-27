from selenium import webdriver
import sys
from common.helpers import find_element, select_seat, take_seats_screenshot, validate_args


def main(first_seat, second_seat):
    '''
    This program receives two seat numbers as input,
    selects the seats from a web page and then takes
    a screenshot of the "Seat Selection" element
    '''
    try:

        driver = webdriver.Chrome()
        driver.get("https://static.gordiansoftware.com/")
        driver.maximize_window()
        
        select_seat(driver, first_seat)

        select_seat(driver, second_seat)

        take_seats_screenshot(driver)

    except Exception as e:
        print(e)
        print("Exiting program...")
        exit(1)
    else:
        print("Seats selected!")

    finally:
        driver.close()

if __name__ == "__main__":

    if(len(sys.argv) != 3):
        print("Oops... You must enter 2 seats as parameters. Please try it again. :) ")
        sys.exit()

    ok = validate_args(str(sys.argv[1]), str(sys.argv[2]))
    if not ok:
        print("This is not a valid seat. Please try it again including letters and numbers.")
        sys.exit()

    main(sys.argv[1], sys.argv[2])
