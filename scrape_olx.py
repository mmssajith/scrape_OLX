# coding=utf8
import datetime
import json
import locale
import re
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from bs4 import BeautifulSoup
import config
# def enable_download_headless(browser, download_dir):
#     browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
#     params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
#     browser.execute("send_command", params)

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2,
    "download.default_directory": r"C:\Users\mcpppp\Downloads\Sample",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
prefs = {'profile.managed_default_content_settings.images': 2,
         'disk-cache-size': 4096}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(
    executable_path='C:\chromedriver.exe', chrome_options=chrome_options)
# download_dir = r"C:\Users\mcpppp\Downloads\Sample"
# enable_download_headless(driver, download_dir)


url = 'https://www.olx.ua'
final_output = []

user_password = [
    {
        "mail": config.username,
        "password": config.password
    }
]


def date_conversion(in_date):
    month_conversion = {
        "янв.": "Jan",
        "фев.": "Feb",
        "мар.": "Mar",
        "апр.": "Apr",
        "май.": "May",
        "июн.": "Jun",
        "июл.": "Jul",
        "авг.": "Aug",
        "сен.": "Sep",
        "окт.": "Oct",
        "ноя.": "Nov",
        "дек.": "Dec"
    }

    month = in_date.split(' ')[-1]
    converted_month = month_conversion[month]
    in_date = in_date.replace(month, converted_month)
    if converted_month == "Dec":
        in_date = f"2020 {in_date}"
    else:
        in_date = f"2021 {in_date}"

    result = datetime.datetime.strptime(in_date, '%Y %d %b').date()
    return result


def enable_cookies():
    try:
        cookies_wait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[11]/button"))
        )
        cookies = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[11]/button')
        cookies.click()
    except:
        pass


def login():
    login_button = driver.find_element(By.XPATH, '//*[@id="topLoginLink"]')
    login_button.click()

    find_mail_area = driver.find_element(By.ID, "userEmail")
    find_password_area = driver.find_element(By.ID, "userPass")

    find_mail_area.send_keys("bacako1750@rezunz.com")
    find_password_area.send_keys("Bacako1750")

    login_button = driver.find_element(By.ID, "se_userLogin")
    login_button.click()
    login_page_wait = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, f'/html/body/div[1]/section/div/div[2]/div/div/div/div/a/span'))
    )


def scraper(table):
    tx = 0
    if table == 1:
        # tx = 7
        tx = 3
    elif table == 2:
        # tx = 41
        tx = 5
    try:
        for tr in range(2, tx):
            try:
                single_page_wait = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'/html/body/div[1]/div[6]/section/div[3]/div/div[1]/table[{table}]/tbody/tr[{tr}]/td/div/table/tbody/tr[1]/td[2]/div/h3/a/strong'))
                )
                product_link = driver.find_element(
                    By.XPATH, f'/html/body/div[1]/div[6]/section/div[3]/div/div[1]/table[{table}]/tbody/tr[{tr}]/td/div/table/tbody/tr[1]/td[2]/div/h3/a').get_attribute('href')
                image_link = driver.find_element(
                    By.XPATH, f'/html/body/div[1]/div[6]/section/div[3]/div/div[1]/table[{table}]/tbody/tr[{tr}]/td/div/table/tbody/tr[1]/td[1]/a/img').get_attribute('src')
                try:
                    time_posted = driver.find_element(
                        By.XPATH, f'/html/body/div[1]/div[6]/section/div[3]/div/div[1]/table[{table}]/tbody/tr[{tr}]/td/div/table/tbody/tr[2]/td[1]/div/p/small[2]/span').text

                    current_date = datetime.datetime.now()
                    week_ago = (current_date -
                                datetime.timedelta(days=7)).date()

                    if week_ago == date_conversion(time_posted):
                        return False

                except Exception as e:
                    print('Date Error', e)
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(f'{product_link}')

                phone_number_wait = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[4]/div/div/div/button'))
                )
                phone_number_button = driver.find_element(By.XPATH,
                                                          '/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[4]/div/div/div/button')
                phone_number_button.click()

                soup = BeautifulSoup(driver.page_source, 'lxml')
                additional_details = name = location_1 = location_2 = title = price = description = contact_no = ''
                try:
                    # location_1_wait = WebDriverWait(driver, 10).until(
                    #     EC.presence_of_element_located(
                    #         (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[3]/div/section/div[1]/div/p[1]'))
                    # )
                    # # location_1 = driver.find_element(By.XPATH,
                    # #                                  "/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[3]/div/section/div[1]/div/p[1]").text
                    # location_1 = driver.find_element(By.XPATH,
                    #                                  "/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[3]/div/section").text
                    location_1 = soup.find(
                        'p', class_="css-7xdcwc-Text eu5v0x0")
                except Exception as e:
                    location_1 = ''
                    print("Location_1 error", e)

                try:
                    location_2 = driver.find_element(By.XPATH,
                                                     '/html/body/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/section/div[1]/div/p[2]').text
                except Exception as e:
                    location_2 = ''
                    print("Location_2 error", e)

                try:
                    title = driver.find_element(By.XPATH,
                                                "/html/body/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/h1").text
                except Exception as e:
                    title = ''
                    print("title error", e)

                try:
                    name = driver.find_element(By.XPATH,
                                               "/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[4]/div/div/section/div/div[2]/h2").text
                except Exception as e:
                    name = ''
                    print("name error", e)

                try:
                    price = driver.find_element(
                        By.XPATH, "/html/body/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[3]/h3").text
                except Exception as e:
                    price = ''
                    print("price error", e)

                try:
                    description = driver.find_element(By.XPATH,
                                                      "/html/body/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[8]/div").text
                except Exception as e:
                    description = ''
                    print("description error", e)

                try:
                    contact_no = driver.find_element(By.XPATH,
                                                     "/html/body/div/div[1]/div[3]/div[2]/div[1]/div[4]/div/div/div/ul/li").text
                except Exception as e:
                    contact_no = ''
                    print("contact_no error", e)

                # catagory_list = []
                # try:
                #
                #     for cat in range(1, 15):
                #         catagory = driver.find_element(By.XPATH,
                #                                        f'/html/body/div[1]/div[1]/div[3]/div[1]/div[1]/ol/li[{cat}]/a').text
                #         if catagory == None:
                #             break
                #         catagory_list.append(catagory)
                # except Exception as e:
                #     print("catagory_list error", e)

                try:
                    catagory = driver.find_element(By.XPATH,
                                                   f'/html/body/div[1]/div[1]/div[3]/div[1]/div[1]/ol').text
                except Exception as e:
                    print("catagory_list error", e)

                try:
                    additional_details = driver.find_element(By.XPATH,
                                                             "/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul").text
                except Exception as e:
                    additional_details = ''
                    print("additional_details error", e)

                output = {
                    'Name of the seller': name,
                    'Product': title,
                    'Location': f'{location_1} {location_2}',
                    'Price': price,
                    'Contact Number': contact_no,
                    'Category': catagory,
                    'Description': description,
                    'page_url': driver.current_url,
                    'image_url': image_link,
                    'additional details': additional_details.replace('\n', ',')
                }
                print(output)
                final_output.append(output)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                single_page_wait_2 = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         f'/html/body/div[1]/div[6]/section/div[3]/div/div[1]/table[{table}]/tbody/tr[{tr}]/td/div/table/tbody/tr[1]/td[2]/div/h3/a/strong'))
                )

            except:
                driver.switch_to.window(driver.window_handles[0])
                print('Skip')
    except:
        print(f'no tr, table:{table}')


print(len(final_output))
if __name__ == "__main__":
    driver.get(url)
    enable_cookies()
    login()
    f = 5
    # while True:
    driver.get(f'{url}/list/?page={f}')
    scraper(1)
    scraper(2)
    # if scraper(2) == False:
    #     break

    headers = ['Name of the seller',
               'Product',
               'Location',
               'Price',
               'Contact Number',
               'Category',
               'Description',
               'page_url',
               'image_url',
               'additional details']
    # with open(f'data_{datetime.datetime.now().date()}.csv', 'w') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=headers)
    #     writer.writeheader()
    #     writer.writerows(final_output)
