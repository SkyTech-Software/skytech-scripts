from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from backend.api_v1.commands.mailer import send_mail

async def send_request_to_play(imei_number, target_email):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.play.pl/uslugi/sprawdz-wlasciciela-telefonu-imei")

    try:
        accept_cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        accept_cookies_button.click()
    except Exception as e:
        pass

    try:
        cancel_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cancel']")))
        cancel_button.click()
        pass
    except Exception as e:
        pass

    try:
        imei_input = driver.find_element(By.NAME, "imei")
        imei_input.send_keys(imei_number)

        submit_button = driver.find_element(By.CLASS_NAME, "p20-button")
        submit_button.click()
    except Exception as e:
        pass
    response = None
    try:
        response_heading = driver.find_element(By.CSS_SELECTOR, "p.v-heading.v-response__heading.center")
        response = response_heading.text
    except Exception as e:
        pass
    
    driver.quit()
    if not response:
        response = "Could not check Play automatically: https://www.play.pl/uslugi/sprawdz-wlasciciela-telefonu-imei"
    mail_sent = await send_mail(target_email=target_email, subject="Play IMEI", message=response, file=None)
    if mail_sent:
        return True
        