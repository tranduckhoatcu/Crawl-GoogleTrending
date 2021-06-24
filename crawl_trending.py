from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import os
import Keywords
import plotChart
keywords = Keywords.keywords
plot_chart = plotChart

from datetime import datetime

start = datetime.strptime("2020-01-01", "%Y-%m-%d").strftime("%Y-%m-%d")
stop = datetime.strptime("2020-12-31", "%Y-%m-%d").strftime("%Y-%m-%d")

############# Please Change the path here ######################### 
webdriver_path = '/Users/khoatran-xps/Documents/Git/crawl_trending/chromedriver'

def enable_headless_download(browser, download_path):
    browser.command_executor._commands["send_command"] = \
        ("POST", '/session/$sessionId/chromium/send_command')
 
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': download_path}}
    browser.execute("send_command", params)

def download():
    for keys, values in keywords.items():
        download_path = 'file_downloaded/' + keys
        chrome_options = Options()
        download_prefs = {'download.default_directory' : download_path,
                            'download.prompt_for_download' : False,
                            'profile.default_content_settings.popups' : 0,
                            'profile.default_content_setting_values.automatic_downloads': 1,
                            "profile.managed_default_content_settings.images": 2,
                            'permissions.default.stylesheet':2,
                            'permissions.default.image':2,
                            'disk-cache-size': 4096,
                            }

        chrome_options.add_experimental_option('prefs', download_prefs)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920x1080')
        if (keys == 'All categories'):
            url = f'https://trends.google.com/trends/explore?date={start}%20{stop}&geo=VN'
        else:
            url = f'https://trends.google.com/trends/explore?cat={values}&date={start}%20{stop}&geo=VN'
        print('Processing with '+keys+' category...')
        if (os.path.exists(download_path+'/relatedEntities.csv') == False & (os.path.exists(download_path+'/relatedQueries.csv') == False)):
            while True:
                try:
                    browser = webdriver.Chrome(executable_path=webdriver_path,options=chrome_options)
                    browser.get(url) 
                    enable_headless_download(browser, download_path)
                    # Load webpage
                    browser.get(url)
                    if(keys == 'All categories'):
                        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div.trends-wrapper > div:nth-child(2) > div > md-content > div > div > div:nth-child(1) > trends-widget > ng-include > widget > div > div > div > widget-actions > div > button.widget-actions-item.export"))).click()
                        time.sleep(1)
                        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div.trends-wrapper > div:nth-child(2) > div > md-content > div > div > div:nth-child(2) > trends-widget > ng-include > widget > div > div > div > widget-actions > div > button.widget-actions-item.export"))).click()
                        time.sleep(1)
                    else:
                        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div.trends-wrapper > div:nth-child(2) > div > md-content > div > div > div:nth-child(2) > trends-widget > ng-include > widget > div > div > div > widget-actions > div > button.widget-actions-item.export"))).click()
                        time.sleep(1)
                        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div.trends-wrapper > div:nth-child(2) > div > md-content > div > div > div:nth-child(3) > trends-widget > ng-include > widget > div > div > div > widget-actions > div > button.widget-actions-item.export"))).click()
                        time.sleep(1)
                    browser.quit()
                except (NoSuchElementException, TimeoutException, WebDriverException) as error:
                    print("Retrying...")
                    browser.quit()
                    continue
                break

if __name__ == '__main__':
    print('Please wait a little bit for downloading since there are rate-limited by Google Trends')
    download()
    plot_chart.save_and_plot()

