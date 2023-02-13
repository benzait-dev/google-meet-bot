# Import required libraries
import time 
from threading import Thread 
import sys, subprocess 
import pyautogui 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 

# Define variables for the meeting link, minimum recording time, and minimum number of members
meetlink = sys.argv[1] 
min_record_time = 200 
min_members = 40 

# Set up Chrome options and launch the browser
options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=/home/aman/snap/chromium/common/chromium') 
browser = webdriver.Chrome('/snap/bin/chromium.chromedriver', options=options) 
browser.get(meetlink) 
time.sleep(6) 

# Define the "meet_join" function to join the meeting
def meet_join(): 
    # Find the body element and send keyboard shortcuts to join the meeting
    meetpage = browser.find_element_by_tag_name('body') 
    meetpage.send_keys(Keys.CONTROL + 'e') 
    meetpage.send_keys(Keys.CONTROL + 'd') 
    
    # Wait for 3 seconds
    time.sleep(3) 
    
    # Click on the join meeting button using JavaScript
    browser.execute_script('document.getElementsByClassName("snByac")[1].click()') 
    
    # Wait for 5 seconds
    time.sleep(5) 

# Define the "meeting" function to monitor the meeting
def meeting(): 
    # Start a timer
    tic = time.perf_counter() 
    
    # Continuously monitor the meeting
    while True: 
        meetingleft = '' 
        
        # Check if the meeting is still active
        for classname in ['j7nIZb','nS35F']: 
            try: 
                # Find the text indicating if the meeting has ended
                meetingleft = browser.find_element_by_xpath(f'//*[contains(concat( " ", @class, " " ), concat( " ", "{classname}", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "snByac", " " ))]').text.strip() 
                
                # If the meeting has ended, reload the page and join the meeting again
                if meetingleft == 'Return to home screen': 
                    browser.execute_script('location.reload();') 
                    meet_join() 
                    break 
            except: 
                pass 
        
        # Check if the meeting is ready to join
        try: 
            joinpage = browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "Jyj1Td", " " ))]').text.strip() 
        except: 
            joinpage = '' 
        
        # Calculate the elapsed time
        toc = time.perf_counter() 
        
        # If the meeting is not ready to join, not ended, and the minimum recording time has been exceeded, check the number of members
        if joinpage != 'Ready to join' and meetingleft != 'Return to home screen' and (toc-tic > min_record_time): 
            try: 
                # Find the number of members
                members = int(browser.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[4]/div[3]/div[6]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]').text.strip()) 
                
                # Print the number of members
                print('\n\n'+str(members)+'\n\n') 
                
                # If the number of members is less than the minimum required, close the browser, terminate the recording process, and exit the loop
                if members < min_members: 
                    #pyautogui.hotkey('ctrl','w') 
                    browser.close() 
                    recorder.p.terminate() 
                    break 
            except: 
                pass 
        
        # Wait for 6 seconds
        time.sleep(6) 

# Define the "recorder" function to start recording the meeting
def recorder(): 
    # Set the time string for the recording file name
    timestr = time.strftime("%Y%m%d-%H%M%S") 
    
    # Define the command for recording using FFmpeg
    command = f'ffmpeg -f pulse -ac 2 -i alsa_output.pci-0000_00_1f.3.analog-stereo.monitor -f x11grab -r 25 -s 1920x1024 -i :0.0 -vcodec libx264 -pix_fmt yuv420p -preset ultrafast -crf 0 -threads 0 -acodec pcm_s16le -y /home/aman/Documents/output-{timestr}.mkv'.split() 
    
    # Start the recording process using subprocess.Popen
    recorder.p = subprocess.Popen(command, stdout=subprocess.PIPE) 

# Call the "meet_join" function to join the meeting
meet_join() 

# Start the "meeting" and "recorder" functions as separate threads
p1 = Thread(target=meeting) 
p2 = Thread(target=recorder) 
p2.start() 
p1.start() 
