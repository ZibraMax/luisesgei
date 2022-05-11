from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import logging
from Utils import download_pdf
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

log = logging.getLogger()
log.setLevel('INFO')

options = Options()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

LINK = "https://www.strongmotioncenter.org/stationmap_worldwide/all_stations.php"
driver.get(LINK)
inputElement = driver.find_element(by=By.ID, value="filterText")

STATION_CODE = 'CE12267'
PDF_FOLDER = './pdfs'  # No colocar ultimo slash, es decir, no hacer ./pdfs/

if not os.path.exists(PDF_FOLDER):
    try:
        os.makedirs(PDF_FOLDER)
        logging.info(f"Working folder {PDF_FOLDER} created.")
    except OSError:
        logging.info(
            f"Working folder {PDF_FOLDER} already created.")


while True:
    try:
        seleccionable = driver.find_element(
            by=By.XPATH, value=f"//*[text()='{STATION_CODE}']")
        driver.execute_script("arguments[0].click();", seleccionable)
        station_info = driver.find_element(
            by=By.XPATH, value="//u[text()='Station Information ']")
        driver.execute_script("arguments[0].click();", station_info)

        driver.switch_to.window(driver.window_handles[1])  # POPUP
        imagen0 = driver.find_elements(by=By.XPATH, value="//img")[1]
        driver.execute_script("arguments[0].click();", imagen0)
        driver.switch_to.window(driver.window_handles[2])
        download_pdf(driver.current_url, STATION_CODE, PDF_FOLDER)
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        records_info = driver.find_element(
            by=By.XPATH, value="//u[text()='View Records ']")
        driver.execute_script("arguments[0].click();", records_info)

        driver.switch_to.window(driver.window_handles[1])

        break
    except Exception as e:
        logging.info('Volvio a iterar porque no ha cargado')

a = 0
