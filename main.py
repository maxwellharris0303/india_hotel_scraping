from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import pyautogui
import allcitylist
import get_latitude_and_longitude
import re

# all_city_list = allcitylist.get_all_cities()
# print(all_city_list)
# print(len(all_city_list))

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.makemytrip.com/hotels/")

try:
    accept_cookie_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class=\"cookiesModal__acceptCookiesBtn buttonCls btn__primary uppercase \"]")))
    accept_cookie_button.click()
except:
    pass

WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-cy=\"city\"]"))).click()

search_input = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder=\"Where do you want to stay?\"]")))
search_input.send_keys("Delhi")

suggest_list = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul[class=\"react-autosuggest__suggestions-list\"]")))
suggest_list.find_element(By.TAG_NAME, 'li').click()
sleep(2)
pyautogui.click(10, 500)

sleep(2)

search_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-cy=\"submit\"]")))
search_button.click()

sleep(3)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"listingRowOuter hotelTileDt makeRelative \"]")))

try:
    lowest_price_tab = driver.find_elements(By.CSS_SELECTOR, "span[class=\"srtByFltr__list--itemSubTitle\"]")[2]
    lowest_price_tab.click()
except:
    pass

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"listingRowOuter hotelTileDt makeRelative \"]")))

hotel_list = driver.find_elements(By.CSS_SELECTOR, "div[class=\"listingRowOuter hotelTileDt makeRelative \"]")
print(len(hotel_list))

city_name = driver.find_element(By.CSS_SELECTOR, "input[id=\"city\"]").get_attribute('value')

for hotel in hotel_list:
    try:
        location = hotel.find_element(By.CSS_SELECTOR, "span[class=\"blueText\"]").text
    except:
        location = ""
    try:
        star_category = hotel.find_element(By.CSS_SELECTOR, "span[class=\"ratingText latoBlack appendLeft3 darkBlueText font16\"]").text
    except:
        star_category = ""
    try:
        price = hotel.find_element(By.CSS_SELECTOR, "p[id=\"hlistpg_hotel_shown_price\"]").text
    except:
        price = ""
    try:
        couple_friendly_text = hotel.find_element(By.CSS_SELECTOR, "div[class=\"persuasion__item pc__hotelCategoryPerNew\"]").text
        if couple_friendly_text == "Couple Friendly":
            couple_friendly = "Allowed"
    except:
        couple_friendly = "Not Allowed"
    
    hotel.click()
    sleep(3)
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    sleep(3)

    try:
        driver.find_element(By.CSS_SELECTOR, "div[class=\"accoDtlHdr__left--info\"]").click()
    except:
        driver.find_element(By.CSS_SELECTOR, "span[class=\"appendLeft10\"]").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"sprite icGridDefault\"]"))).click()
    sleep(5)

    image_listing = driver.find_element(By.CSS_SELECTOR, "ul[class=\"imageListing\"]")
    image_items = image_listing.find_elements(By.TAG_NAME, "li")
    number_of_photos = len(image_items)
    print(len(image_items))

    try:
        hotel_name = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h1[class=\"font26 blackText latoBlack appendBottom10\"]"))).text
    except:
        hotel_name = ""
    print(f"Hotel name: {hotel_name}")
    print(f"City name: {city_name}")
    print(f"Location: {location}")

    try:
        latitude, longitude = get_latitude_and_longitude.get_coordinates(location)
    except:
        latitude = ""
        longitude = ""
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print(f"Star Category: {star_category}")
    print(f"Price: {price}")

    try:
        number_of_room_text = driver.find_element(By.CSS_SELECTOR, "h4[class=\"rmTypeDropDown__heading\"]").text
        number_of_rooms = re.findall(r'\d+', number_of_room_text)[0]
    except:
        number_of_rooms = 1
    print(f"Number of Rooms in property: {number_of_rooms}")

    try:
        description = driver.find_element(By.CSS_SELECTOR, "section[class=\"page__section appendBottom35\"]").text
    except:
        description = ""
    print(f"Description: {description}")
    print(f"Couple friendly: {couple_friendly}")

    try:
        property_rules = driver.find_element(By.CSS_SELECTOR, "div[class=\"htlRules\"]")
    except:
        property_rules = None

    pet_friendly = ""
    if property_rules != None:
        if "Pets" in property_rules.text:
            pet_friendly = "Not Allowed"
        else:
            pet_friendly = "Allowed"
        if "Food" in property_rules.text:
            outside_food_allowed = "Not Allowed"
        else:
            outside_food_allowed = "Allowed"
        if "Smoking" in property_rules.text:
            smoking_allowed = "Not Allowed"
        else:
            smoking_allowed = "Allowed"
    print(f"Pet friendly: {pet_friendly}")
    try:
        check_in_time = driver.find_element(By.CSS_SELECTOR, "span[class=\"latoBlack appendRight5\"]").text
    except:
        check_in_time = ""
    try:
        check_out_time = driver.find_element(By.CSS_SELECTOR, "span[class=\"latoBlack appendLeft5\"]").text
    except:
        check_out_time = ""

    cctv = False
    security_guard = False
    fire_extinguishers = False
    first_aid_services = False
    wake_up_call = False
    luggage_assistance = False
    reception = False
    banquet = False
    conference_room = False
    spa = False
    restaurant = False
    indoor_games = False
    _25_hour_roo_service = False
    wheelchair = False
    lounge = False
    bar = False
    cafe = False
    steam_and_sauna = False
    salon = False
    yoga = False
    kids_play_area = False
    library = False
    dry_cleaning_service = False
    laundry_service = False
    housekeeping = False
    power_backup = False
    elevator_lift = False
    intercom = False
    wi_fi = False
    newspaper = False
    parking = False
    airport_transfer_available = False
    vehicle_rentals = False
    medical_services = False
    atm = False
    currency_excahnge = False
    bonfire = False

    facilities_section = driver.find_elements(By.CSS_SELECTOR, "section[class=\"page__section appendBottom35\"]")[2]
    # print(facilities_section.text)
    # driver.execute_script("arguments[0].scrollIntoView();", facilities_section)
    # sleep(5)
    try:
        all_facilities_button = facilities_section.find_element(By.CSS_SELECTOR, "a[class=\"font14 latoBlack blueText\"]")
        driver.execute_script("arguments[0].scrollIntoView();", facilities_section)
        all_facilities_button.click()
        sleep(1)
        try:
            more_buttons = facilities_section.find_elements(By.CSS_SELECTOR, "li[class=\"lineHight20 makeFlex pointer\"]")
            for more in more_buttons:
                more.click()
            if "CCTV" in facilities_section.text:
                cctv = True
            if "Security Guard" in facilities_section.text:
                security_guard = True
            if "Fire Extinguishers" in facilities_section.text:
                fire_extinguishers = True
            if "First Aid Services" in facilities_section.text:
                first_aid_services = True
            if "Wake-up Call" in facilities_section.text:
                wake_up_call = True
            if "Luggage Assistance" in facilities_section.text:
                luggage_assistance = True
            if "Reception" in facilities_section.text:
                reception = True
            if "Banquet" in facilities_section.text:
                banquet = True
            if "Conference Room" in facilities_section.text:
                conference_room = True
            if "Spa" in facilities_section.text:
                spa = True
            if "Restaurant" in facilities_section.text:
                restaurant = True
            if "Indoor Games" in facilities_section.text:
                indoor_games = True
            if "24-hour Room Service" in facilities_section.text:
                _25_hour_roo_service = True
            if "Wheelchair" in facilities_section.text:
                wheelchair = True
            if "Lounge" in facilities_section.text:
                lounge = True
            if "Bar" in facilities_section.text:
                bar = True
            if "Cafe" in facilities_section.text:
                cafe = True
            if "Steam and Sauna" in facilities_section.text:
                steam_and_sauna = True
            if "Salon" in facilities_section.text:
                salon = True
            if "Yoga" in facilities_section.text:
                yoga = True
            if "Kids Play Area" in facilities_section.text:
                kids_play_area = True 
            if "Library" in facilities_section.text:
                library = True
            if "Dry Cleaning Service" in facilities_section.text:
                dry_cleaning_service = True 
            if "Laundry Service" in facilities_section.text:
                laundry_service = True
            if "Housekeeping" in facilities_section.text:
                housekeeping = True
            if "Power Backup" in facilities_section.text:
                power_backup = True
            if "Elevator/Lift" in facilities_section.text:
                elevator_lift = True
            if "Intercom" in facilities_section.text:
                intercom = True
            if "Wi-Fi" in facilities_section.text:
                wi_fi = True
            if "Newspaper" in facilities_section.text:
                newspaper = True
            if "Parking" in facilities_section.text:
                parking = True
            if "Airport Transfers" in facilities_section.text:
                airport_transfer_available = True
            if "Vehicle Rentals" in facilities_section.text:
                vehicle_rentals = True
            if "Medical Services" in facilities_section.text:
                medical_services = True
            if "ATM" in facilities_section.text:
                atm = True 
            if "Currency Exchange" in facilities_section.text:
                currency_excahnge = True
            if "Bonfire" in facilities_section.text:
                bonfire = True
    
        except:
            pass
    except:
        pass
    print(f"CCTV: {cctv}")
    print(f"Security Guard: {security_guard}")
    print(f"Fire Extinguishers: {fire_extinguishers}")
    print(f"First Aid Services: {first_aid_services}")
    print(f"Wake-up Call: {wake_up_call}")
    print(f"Luggage Assistance: {luggage_assistance}")
    print(f"Reception: {reception}")
    print(f"Banquet: {banquet}")
    print(f"Conference Room: {conference_room}")
    print(f"Spa: {spa}")
    print(f"Restaurant: {restaurant}")
    print(f"Indoor Games: {indoor_games}")
    print(f"24-hour Room Service: {_25_hour_roo_service}")
    print(f"Wheelchair: {wheelchair}")
    print(f"Lounge: {lounge}")
    print(f"Bar: {bar}")
    print(f"Cafe: {cafe}")
    print(f"Steam and Sauna: {steam_and_sauna}")
    print(f"Salon: {salon}")
    print(f"Yoga: {yoga}")
    print(f"Kids Play Area: {kids_play_area}")
    print(f"Library: {library}")
    print(f"Dry Cleaning Service: {dry_cleaning_service}")
    print(f"Laundry Service: {laundry_service}")
    print(f"Housekeeping: {housekeeping}")
    print(f"Power Backup: {power_backup}")
    print(f"Elevator/Lift: {elevator_lift}")
    print(f"Intercom: {intercom}")
    print(f"Wi-Fi: {wi_fi}")
    print(f"Newspaper: {newspaper}")
    print(f"Parking: {parking}")
    print(f"Airport Transfers: {airport_transfer_available}")
    print(f"Vehicle Rentals: {vehicle_rentals}")
    print(f"Medical Services: {medical_services}")
    print(f"ATM: {atm}")
    print(f"Currency Exchange: {currency_excahnge}")
    print(f"Bonfire: {bonfire}")

    try:
        driver.find_element(By.CSS_SELECTOR, "span[class=\"cm__modalClose \"]").click()
    except:
        pass

    print(f"Check In Time: {check_in_time}")
    print(f"Check Out Time: {check_out_time}")

    print(f"Outside Food Allowed: {outside_food_allowed}")
    print(f"Smoking Allowed: {smoking_allowed}")


    # sleep(100)
    driver.close()
    driver.switch_to.window(window_handles[0])
    sleep(3)
 
