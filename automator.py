from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os

# Chrome WebDriver options
options = Options()
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--disable-extensions")  # Disable extensions for faster load
options.add_argument("--no-sandbox")  # Not necessary, but may help in some cases
options.add_argument("--disable-dev-shm-usage")  # Helps in environments with limited memory
options.add_argument("--disable-features=NetworkService,NetworkServiceInProcess")  # Disables network service
options.add_argument("--enable-fast-unload")  # Unload pages faster
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=C:/temp/chrome_user_data")# New user data directory
# options.add_argument("--headless")
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

os.system("")
os.environ["WDM_LOG_LEVEL"] = "0"

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# Intro messages
print(style.BLUE)
print("**********************************************************")
print("**********************************************************")
print("*****                                               ******")
print("*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******")
print("*****      This tool was built by Nouralddin        ******")
print("*****                                               ******")
print("*****                                               ******")
print("**********************************************************")
print("**********************************************************")
print(style.RESET)

# Read message from file and include placeholder for name
with open("message.txt", "r", encoding="utf8") as f:
    message_template = f.read()

print(style.YELLOW + '\nThis is your message template-')
print(style.GREEN + message_template)
print("\n" + style.RESET)

# Read names and numbers from the file
contacts = []
with open("numbers.txt", "r", encoding="utf8") as f:
    for line in f.read().splitlines():
        if line.strip():
            name, number = line.split(',')
            contacts.append((name.strip(), number.strip()))

total_number = len(contacts)
print(style.RED + 'We found ' + str(total_number) + ' contacts in the file' + style.RESET)
delay = 30

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
print('Once your browser opens up, sign in to WhatsApp Web')
driver.get('https://web.whatsapp.com')
input(style.MAGENTA + "AFTER logging into WhatsApp Web and your chats are visible, press ENTER..." + style.RESET)

def find_send_button(driver, delay):
    """Tries different strategies to locate the send button."""
    try:
        return WebDriverWait(driver, delay).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@aria-label='Send' and @data-tab='11']")))
    except:
        return None

# Loop through contacts and send messages
for idx, (name, number) in enumerate(contacts):
    number = number.strip()
    if not number:
        continue

    # Check if the number starts with '20' and adjust if necessary
    if not number.startswith("20"):
        number = "20" + number

    # Check if the message contains [name] and replace it
    if "[name]" in message_template:
        personalized_message = message_template.replace("[name]", name)
    else:
        personalized_message = message_template  # Use the original message if no [name]

    encoded_message = quote(personalized_message)

    print(style.YELLOW + '{}/{} => Sending message to {} ({})'.format((idx + 1), total_number, name, number) + style.RESET)

    try:
        url = f'https://web.whatsapp.com/send?phone={number}&text={encoded_message}'
        sent = False
        
        for attempt in range(3):  # Retry up to 3 times
            if not sent:
                driver.get(url)
                try:
                    send_button = find_send_button(driver, delay)
                    if send_button:
                        sleep(1)  # Wait a second for button stability
                        send_button.click()
                        sent = True
                        sleep(3)  # Wait after sending for message processing
                        print(style.GREEN + 'Message sent to: ' + name + ' (' + number + ')' + style.RESET)
                    else:
                        raise Exception("Send button not found.")
                except Exception as e:
                    print(style.RED + f"Failed to send message to {name} ({number}), retry ({attempt + 1}/3). Error: {e}")
                    print("Make sure your phone and computer are connected to the internet.")
                    print("If there is an alert, please dismiss it." + style.RESET)

        # Handle unexpected alerts or popups
        try:
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            pass  # No alert found
    
    except Exception as e:
        print(style.RED + f'Failed to send message to {name} ({number}). Error: {e}' + style.RESET)

driver.close()

