import os
import time
import requests
from dotenv import load_dotenv
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def connect_to_network():
    os.system('cmd /c "netsh wlan show networks"')

    ssid = 'DU_Campus_WiFi'

    os.system(f'''cmd /c "netsh wlan connect name={ssid}"''')
    time.sleep(2) 

def get_redirected_url():
    session = requests.Session()
    try:
        response = session.get("http://neverssl.com")  # A URL that doesn’t use SSL to force redirect
        if response.status_code == 200:
            return response.url 
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None

def login(url, username, password):
    session = requests.Session()
    response = session.get(url) 
       
    def get_redirected_url_with_script(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script')
        
        if script_tag and "window.location" in script_tag.string:
            redirect_url = script_tag.string.split('"')[1]
            return redirect_url
        return None

    response = requests.get("http://neverssl.com")
    redirect_url = get_redirected_url_with_script(response.text)

    if redirect_url:
        print(f"Redirecting to:", redirect_url)
        redirect_response = requests.get(redirect_url)
        
        # Parse the HTML content of the redirected page
        soup = BeautifulSoup(redirect_response.text, 'html.parser')
        
        # Find the login form
        login_form = soup.find('form')
        if login_form is None:
            print("No form found on the page.")
            return None
        else:
            print("There is form:", login_form)
            login_url = urljoin(redirect_url, login_form['action'])
     
    payload = {}
    for input_tag in login_form.find_all('input'):
        input_name = input_tag.get('name')
        if input_name: 
            if 'username' in input_name.lower():
                payload[input_name] = username
            elif 'password' in input_name.lower():
                payload[input_name] = password
            else:
                payload[input_name] = input_tag.get('value', '')
            print(payload)
        else: 
            print("No input_name")
            continue
        
    # Send POST request
    login_response = session.post(login_url, data=payload)
    return login_response

# Your login credentials
load_dotenv()

username =  os.getenv("USERNAME")
password = os.getenv("PASSWORD")



def mainFunction(): 
    # Connect to Wi-Fi
    connect_to_network()
    

    redirected_url = get_redirected_url()
    if redirected_url:
        print(f"Redirected URL: {redirected_url}")
        
        # Perform login
        response = login(redirected_url, username, password)
        if response.status_code == 200:
            print("Logged in successfully!")
        else:
            print(f"Login failed with status code: {response.status_code}")
    else:
        print("Could not get redirected URL.")



mainFunction()