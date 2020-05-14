import pytesseract
import os
import requests
import urllib
import random
import string
import numpy
import imagehash
import sys
import binascii
import config as cfg

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tbselenium.tbdriver import TorBrowserDriver
from os.path import dirname, join, realpath, getsize
from PIL import Image, ImageDraw
currentdir = os.path.join(os.getcwd(), '')

class DevNull:
    def write(self, msg):
        pass

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

files = {'file': open('random.jpg', 'rb')}
values = {'nickname': 'anon', 'email': ''}

sys.stderr = DevNull()
global driver
imagestring = randomString() + ".jpg"
RANDOMSTRING=binascii.b2a_hex(os.urandom(32))
JPG="ffd8ffdb"
with open(imagestring, "wb") as f:
	f.write(binascii.unhexlify(JPG + RANDOMSTRING))
try:
	with TorBrowserDriver(cfg.c["tor_directory"]) as driver:
		driver.load_url("http://REMOVED.onion/", wait_for_page_body=True)
		captcha = driver.find_element_by_xpath('//img[@src="Generate_Captcha.php"]')
		inputcaptcha = driver.find_element_by_xpath('//input[@name="captcha_code"]')
		inputfile = driver.find_element_by_xpath('//input[@name="file"]')
		sendurl = driver.find_element_by_xpath('/html/body/div/div[4]/div/form/div/input[5]')
		location = captcha.location
		size = captcha.size
		driver.save_screenshot("temp.jpg")
		x = location['x']
		y = location['y']
		width = location['x']+size['width']
		height = location['y']+size['height']
		im = Image.open('temp.jpg')
		im = im.convert("L")
		im = im.crop((int(x), int(y), int(width), int(height)))
		im.save('temp2.jpg')
		os.remove('temp.jpg')
		captcha_text = pytesseract.image_to_string(Image.open('temp2.jpg'), config='letters', lang="eng")
		sys.stdout.write("Detected text: " + "\033[1;36m" + captcha_text + "\033[0;0m")
		os.rename("temp2.jpg", captcha_text + ".jpg")
		inputcaptcha.send_keys(captcha_text)
		inputfile.send_keys(currentdir+imagestring)
		sendurl.click()
	
		wait = WebDriverWait(driver, 10)
		wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/a/div[2]/div[1]')))
		sys.stdout.write("\n")
		os.remove(currentdir+imagestring)
		filename = driver.find_element_by_css_selector("a[href*='_anon_']").text.split("\n")[0]
		cururl = "http://REMOVED.onion/"+driver.current_url.split("/")[-2]+"/"
		print(cururl+filename)
		###### DOWNLOAD CODE ######
		os.system('torsocks curl -s -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" -H "Accept-Language: en-US,en;q=0.5" --compressed -H "Connection: keep-alive" -H "Cookie: PHPSESSID=REMOVED" -H "Upgrade-Insecure-Requests: 1" -o PATH TO CURRENT FOLDER/images/'+filename+" "+cururl+filename)
		file_path = "PATH TO CURRENT FOLDER/images/"+filename
		if file_size(file_path) == "36.0 bytes":
			print("File downloaded is from us. Removing...")
			os.remove(file_path)
		else:
			print("File isn't fake!")

		###### DOWNLOAD CODE ######
		print('--------------------')
		driver.close()

except:
	sys.stdout.write(" -- " + "\033[1;31m" + "Failed to grab info" + "\033[0;0m" + "\n")
	os.remove(currentdir+imagestring)
