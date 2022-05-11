import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import logging
from Utils import download_pdf, download_wait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm
import sys

log = logging.getLogger()
log.setLevel('INFO')

LINK = "https://www.strongmotioncenter.org/stationmap_worldwide/all_stations.php"
STATION_CODE = sys.argv[1]
PDF_FOLDER = './pdfs'  # No colocar ultimo slash, es decir, no hacer ./pdfs/ xd
ZIP_FOLDER = './zips'  # No colocar ultimo slash, es decir, no hacer ./pdfs/ xd
ZIP_FOLDER = os.path.abspath(ZIP_FOLDER)

UNZIP_FOLDER = os.path.join(ZIP_FOLDER, STATION_CODE)
CARPETAS_VERIFICAR = [PDF_FOLDER, ZIP_FOLDER, UNZIP_FOLDER]

EMAIL = open('secrets.txt').read()


options = Options()
options = webdriver.ChromeOptions()

prefs = {"download.default_directory": f"{UNZIP_FOLDER}"}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), chrome_options=options)

driver.get(LINK)
inputElement = driver.find_element(by=By.ID, value="filterText")


for carpeta in CARPETAS_VERIFICAR:

    if not os.path.exists(carpeta):
        try:
            os.makedirs(carpeta)
            logging.info(f"Working folder {carpeta} created.")
        except OSError:
            logging.info(
                f"Working folder {carpeta} already created.")


while True:
    try:
        seleccionable = driver.find_element(
            by=By.XPATH, value=f"//*[text()='{STATION_CODE}']")
        break
    except Exception as e:
        logging.info(f'{STATION_CODE} Volvio a iterar porque no ha cargado')
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

textos = []
driver.switch_to.window(driver.window_handles[1])

rutactual = driver.current_url
checkboxes = driver.find_elements(
    by=By.XPATH, value="//input[@type='checkbox']")

p_parent = checkboxes[0].find_element(by=By.XPATH, value="./..")
td = p_parent.find_element(by=By.XPATH, value="./..")
tr = td.find_element(by=By.XPATH, value="./..")

td_texto = tr.find_elements(by=By.XPATH, value=".//td")[7]
texto_m = td_texto.find_element(by=By.XPATH, value=".//font").text

td_texto = tr.find_elements(by=By.XPATH, value=".//td")[10]
texto_m2 = td_texto.find_element(by=By.XPATH, value=".//font").text

textos.append(f'{texto_m}_{texto_m2}')
boton_descargar = driver.find_element(
    by=By.XPATH, value="//input[@type='SUBMIT']")
driver.execute_script("arguments[0].click();", checkboxes[0])

driver.execute_script("arguments[0].click();", boton_descargar)

driver.switch_to.window(driver.window_handles[2])
ruta_res = driver.current_url + "&Processed=on"
driver.get(ruta_res)
boton = driver.find_element(
    by=By.XPATH, value="//input[@type='SUBMIT']")
driver.execute_script("arguments[0].click();", boton)
texbox_email = driver.find_element(by=By.NAME, value='email')
texbox_email.send_keys(f'{EMAIL}')
texbox_email.send_keys(Keys.ENTER)

boton = driver.find_element(
    by=By.XPATH, value="//input[@type='button']")
driver.execute_script("arguments[0].click();", boton)

driver.switch_to.window(driver.window_handles[2])

downlink = driver.find_element(
    by=By.XPATH, value="//a[text()='Download selected Processed data']")
driver.execute_script("arguments[0].click();", downlink)
driver.close()


logging.info('Empezamos a descargar como animales')

for i in tqdm(range(1, len(checkboxes)), unit=' Registro'):
    driver.switch_to.window(driver.window_handles[1])
    driver.execute_script("arguments[0].click();", checkboxes[i-1])
    driver.execute_script("arguments[0].click();", checkboxes[i])

    p_parent = checkboxes[i].find_element(by=By.XPATH, value="./..")
    td = p_parent.find_element(by=By.XPATH, value="./..")
    tr = td.find_element(by=By.XPATH, value="./..")
    td_texto = tr.find_elements(by=By.XPATH, value=".//td")[7]
    texto_m = td_texto.find_element(by=By.XPATH, value=".//font").text

    td_texto = tr.find_elements(by=By.XPATH, value=".//td")[10]
    texto_m2 = td_texto.find_element(by=By.XPATH, value=".//font").text
    textos.append(f'{texto_m}_{texto_m2}')

    driver.execute_script("arguments[0].click();", boton_descargar)
    driver.switch_to.window(driver.window_handles[2])
    ruta_res = driver.current_url + "&Processed=on"
    driver.get(ruta_res)
    boton = driver.find_element(
        by=By.XPATH, value="//input[@type='SUBMIT']")
    driver.execute_script("arguments[0].click();", boton)
    downlink = driver.find_element(
        by=By.XPATH, value="//a[text()='Download selected Processed data']")
    driver.execute_script("arguments[0].click();", downlink)
    driver.close()

download_wait(UNZIP_FOLDER, 30)  # teamo stranger
zips = os.listdir(UNZIP_FOLDER)

for f in zips:
    if '.zip' in f.lower():
        ruta_archivo_zip = os.path.join(UNZIP_FOLDER, f)
        with zipfile.ZipFile(ruta_archivo_zip, 'r') as zip_ref:
            zip_ref.extractall(UNZIP_FOLDER)

        try:
            os.remove(ruta_archivo_zip)
        except Exception as e:
            logging.info(f'{f} not found')

_zips = os.listdir(UNZIP_FOLDER)
zips = []
for z in _zips:
    if '.zip' in z.lower():
        zips.append(z)
for i, f in enumerate(zips):
    ruta_archivo_zip = os.path.join(UNZIP_FOLDER, f)
    with zipfile.ZipFile(ruta_archivo_zip, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(UNZIP_FOLDER, textos[i]))
    try:
        os.remove(ruta_archivo_zip)
    except Exception as e:
        logging.info(f'{ruta_archivo_zip} not found')
