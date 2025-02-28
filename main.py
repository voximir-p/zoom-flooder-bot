# -*- coding: utf-8 -*-

print('Loading...')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import random
import os
import keyboard
import time
import concurrent.futures
import sys
import subprocess

# Create a custom stdout to filter out unwanted errors
class FilteredStdout:
    def __init__(self, original_stdout):
        self.original_stdout = original_stdout
        self.filtered_strings = [
            "ERROR:gles2_cmd_decoder_passthrough",
            "Automatic fallback to software WebGL",
            "ERROR:sdp_o qffer_answer",
            "ERROR:dtls_transport",
            "ERROR:dtls_srtp_transport",
            "No DTLS-SRTP selected crypto suite"
        ]
    
    def write(self, text):
        if not any(error_msg in text for error_msg in self.filtered_strings):
            self.original_stdout.write(text)
    
    def flush(self):
        self.original_stdout.flush()

# Redirect stdout through our filter
sys.stdout = FilteredStdout(sys.stdout)

os.system('cls' if os.name == 'nt' else 'clear')
print('Loaded Zoom Flooder Bot V1 Fix By Pasit')

# Setup
try:
    with open('defualt.txt', 'r') as f:
        default_data = f.read().split('\n')
except FileNotFoundError:
    print("Error: 'defualt.txt' file not found!")
    exit()
threadCnt = int(input('Thread Count (Blank for Default): ').strip()) or default_data[0]
meetingID = input('Meeting ID (Blank for Default): ').strip() or default_data[1]
meetingPasscode = input('Meeting Passcode (Blank for Default): ').strip() or default_data[2]
numberOfBots = int(input('Number of Bots: '))
customName = input('Bot Name (Blank for Random): ').strip()
os.system('cls' if os.name == 'nt' else 'clear')

# Load random names
try:
    with open('names.txt', 'r') as f:
        names_list = [name.strip() for name in f.read().split('\n') if name.strip()]
    if not names_list:
        print("Warning: 'names.txt' is empty, using default names.")
        names_list = ["User", "Participant", "Student", "Guest", "Attendee"]
except FileNotFoundError:
    print("Warning: 'names.txt' file not found! Using default names.")
    names_list = ["User", "Participant", "Student", "Guest", "Attendee"]

# Chrome options setup
def get_chrome_options():
    options = Options()
    options.add_argument('--log-level=3')  # Suppress most Chrome logging
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--mute-audio")
    options.add_argument("--headless")
    
    # Add options to disable WebGL errors
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
    options.add_argument("--enable-unsafe-swiftshader")
    
    # Disable logging
    options.add_argument("--silent")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Disable Webcams and Microphone
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 2,
        "profile.default_content_setting_values.media_stream_camera": 2,
        "profile.default_content_setting_values.notifications": 2
    })
    
    return options

# Function to verify input fields are properly filled
def verify_input_fields(driver, bot_name, passcode):
    try:
        # Check if name field contains expected value
        name_input = driver.find_element(By.ID, 'input-for-name')
        current_name = name_input.get_attribute('value')
        if not current_name:
            # Clear and try again if empty
            name_input.clear()
            name_input.send_keys(bot_name)
            time.sleep(0.5)
        
        # Check if passcode field contains expected value
        passcode_input = driver.find_element(By.ID, 'input-for-pwd')
        current_passcode = passcode_input.get_attribute('value')
        if not current_passcode:
            # Clear and try again if empty
            passcode_input.clear()
            passcode_input.send_keys(passcode)
            time.sleep(0.5)
        
        # Double-check both fields again
        if not name_input.get_attribute('value') or not passcode_input.get_attribute('value'):
            return False
        
        return True
    except:
        return False

# Function to launch a single bot
def launch_bot(bot_id):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            options = get_chrome_options()
            service = Service('chromedriver.exe')
            # Redirect WebDriver's stdout to devnull to suppress console messages
            service.creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            
            driver = webdriver.Chrome(service=service, options=options)
            
            # Set a generous timeout for page loading
            driver.set_page_load_timeout(30)
            driver.get(f'https://zoom.us/wc/join/{meetingID}')
            
            # Use a longer wait time to ensure elements load properly
            wait = WebDriverWait(driver, 2)
            
            # Generate bot name
            if not customName:
                bot_name = f"{random.choice(names_list)}"
            
            # Handle the "Continue without audio or video" dialog if it appears
            try:
                continue_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'continue')))
                continue_btn.click()
                time.sleep(1)
            except:
                pass
            
            # Make sure the join form is visible
            try:
                wait.until(EC.visibility_of_element_located((By.ID, 'input-for-name')))
                wait.until(EC.visibility_of_element_located((By.ID, 'input-for-pwd')))
            except TimeoutException:
                print(f"Bot {bot_id+1}: Form fields not visible, retrying...")
                driver.quit()
                time.sleep(2)
                continue
            
            # Enter name with explicit waits
            name_input = wait.until(EC.presence_of_element_located((By.ID, 'input-for-name')))
            name_input.clear()
            name_input.send_keys(bot_name)
            time.sleep(0.5)  # Wait for input to register
            
            # Enter passcode with explicit waits
            passcode_input = wait.until(EC.presence_of_element_located((By.ID, 'input-for-pwd')))
            passcode_input.clear()
            passcode_input.send_keys(meetingPasscode)
            time.sleep(0.5)  # Wait for input to register
            
            # Verify inputs before clicking join
            if not verify_input_fields(driver, bot_name, meetingPasscode):
                print(f"Bot {bot_id+1}: Input verification failed, retrying...")
                driver.quit()
                time.sleep(1)
                continue
            
            # Find and click the join button
            join_btn = None
            try:
                join_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'preview-join-button')]")))
                # Use JavaScript click which is more reliable
                driver.execute_script("arguments[0].click();", join_btn)
            except ElementClickInterceptedException:
                print(f"Bot {bot_id+1}: Join button click intercepted. Checking inputs...")
                # Check if inputs are still valid
                if not verify_input_fields(driver, bot_name, meetingPasscode):
                    raise Exception("Input fields validation failed")
                
                # Try to find and click the join button again
                join_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'preview-join-button')]")
                if join_buttons:
                    driver.execute_script("arguments[0].click();", join_buttons[0])
                else:
                    raise Exception("Could not find join button")
            
            # Wait briefly to confirm joining
            time.sleep(2)
            
            print(f'Bot {bot_id+1} successfully joined!')
            return driver
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"Bot {bot_id+1}: Error on attempt {attempt+1}/{max_attempts}: {str(e)}")
                try:
                    driver.quit()
                except:
                    pass
                time.sleep(2 * (attempt + 1))  # Increasing backoff
            else:
                print(f"Bot {bot_id+1}: Failed after {max_attempts} attempts: {str(e)}")
                try:
                    driver.quit()
                except:
                    pass
                return None

# Launch bots in batches to avoid overwhelming the system
print(f'Launching {numberOfBots} bots...')
active_drivers = []

# Define batch size based on number of bots
batch_size = min(threadCnt, numberOfBots)
total_batches = (numberOfBots + batch_size - 1) // batch_size

for batch in range(total_batches):
    start_idx = batch * batch_size
    end_idx = min((batch + 1) * batch_size, numberOfBots)
    
    print(f'Launching batch {batch+1}/{total_batches} (Bots {start_idx+1}-{end_idx})...')
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
        # Submit the tasks for this batch
        future_to_bot = {executor.submit(launch_bot, i): i for i in range(start_idx, end_idx)}
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_bot):
            bot_id = future_to_bot[future]
            driver = future.result()
            if driver:
                active_drivers.append((bot_id+1, driver))
    
    # Add a delay between batches to reduce detection risk
    if batch < total_batches - 1:
        delay = random.uniform(1, 2)
        print(f'Batch {batch+1} complete. Waiting {delay:.1f} seconds before next batch...')
        time.sleep(delay)

print(f'{len(active_drivers)} of {numberOfBots} bots successfully joined!')
print('Press Alt+Ctrl+Shift+E to exit all bots.')

# Waiting for user to quit bots
try:
    while True:
        if keyboard.is_pressed('alt') and keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift') and keyboard.is_pressed('e'):
            break
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
active_drivers.sort(key=lambda x: x[0])
# Cleanup
os.system('cls' if os.name == 'nt' else 'clear')
for i, (bot_id, driver) in enumerate(active_drivers):
    try:
        print(f'Exiting Bot {bot_id}...')
        driver.quit()
    except:
        pass

print(f'All {len(active_drivers)} bots exited successfully, you may now use ctrl+c to close the program.')
