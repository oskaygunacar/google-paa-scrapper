from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# button xpath: //div[@jsname="yEVEwb"]//div[@role="button"] -> doğru olan
# title direkt xpath: //div[@jsname="yEVEwb"]//span[@class="CSkcDe"]


scrapping_dict = dict()

def scrapper():
    try:
        results = driver.find_elements(By.XPATH, '//div[@jsname="yEVEwb"]//div[@role="button"]')
        # bu döngü ile results içerisinde gezip boş string olarak gelen başlıkları siliyoruz.
        for r in results:
            if r.text == '':
                results.remove(r)
        print(len(results))
        if len(results) <= 10:
            results[-1].click()
            time.sleep(5)
            scrapper()
        else:
            for k in results:
                scrapping_dict[keyword].append(k.text)
    except:
        print("Error")

with open('keywords.txt', mode='r', encoding='utf-8', errors='ignore') as file:
    driver = webdriver.Safari()
    driver.set_window_size(1920, 5000)
    driver.get("https://www.google.com")

    for keyword in file:
        keyword = keyword.strip()
        scrapping_dict[keyword] = list()

        # Google'da arama kutusunu bul - Arama kutusu
        search_box = driver.find_element(By.NAME, 'q')
        search_box.clear()

        # arama kutusuna query at
        search_box.send_keys(f'{keyword}')
        search_box.submit()

        # arama sonucunu bekle
        time.sleep(3)

        scrapper()

    print(scrapping_dict)
    # bütün keyword'ler işlendikten sonra tarayıcıyı kapat
    driver.close()

with pd.ExcelWriter('output.xlsx') as writer:
    for keyword, questions in scrapping_dict.items():
        df = pd.DataFrame(questions, columns=['People Also Asked Questions'])
        df.to_excel(writer, sheet_name=keyword, index=False)