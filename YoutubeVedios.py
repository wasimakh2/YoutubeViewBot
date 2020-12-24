import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YoutubeVedios:

    def __init__(self,username,password,clink):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--incognito")
        self.youtube_bot = webdriver.Chrome(ChromeDriverManager().install(),options = self.chrome_options)
        self.channel_link = clink
        self.username = username
        self.password = password

    def login_to_gmail(self):
        youtube_bot = self.youtube_bot
        try:
            #Using a third party sign in as google sign-in is protected heavily :(
            youtube_bot.get('https://stackoverflow.com/users/signup')
            #Make the bot mimic human behaviour :P
            youtube_bot.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
            youtube_bot.find_element_by_xpath('//*[@id="identifierId"]').send_keys(self.username)
            time.sleep(2)
            youtube_bot.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]').click()
            time.sleep(2)
            youtube_bot.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(self.password)
            youtube_bot.find_element_by_xpath('//*[@id="passwordNext"]/div/button/div[2]').click()
            # time.sleep(10)
            wait = WebDriverWait(youtube_bot, 60)
            # wait.until(EC.title_is("title"))
            wait.until(EC.title_contains("stackoverflow.com"))


        except Exception as identifier:
            print(identifier)
        
        # We are now logged into Youtube :)
        youtube_bot.get(self.channel_link)
        print("\n Logged Into Youtube")

    def CloseChrome(self):
        """
        docstring
        """
        youtube_bot.quit()
        
    def load_all_videos(self):
        youtube_bot = self.youtube_bot
        #Initial scroll
        page_len = youtube_bot.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);"
            "var page_len=document.documentElement.scrollHeight;"
            "return page_len;")
        scroll_complete = False
        while (scroll_complete == False):
            page_count = page_len
            time.sleep(2)
            #Scroll after every two seconds until page end
            page_len = youtube_bot.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);"
                "var page_len=document.documentElement.scrollHeight;"
                "return page_len;")
            if page_count == page_len:
                scroll_complete = True
                print("\n Scrolling Complete !!")

    def get_all_links(self):
        #Get all links in a list
        global all_links
        youtube_bot = self.youtube_bot
        all_titles = youtube_bot.find_elements_by_id("video-title")
        all_links = [title.get_attribute('href') for title in all_titles]
        print(len(all_links))
        return all_links

    def like_all_videos(self):
        youtube_bot = self.youtube_bot
        #Iterate over each link gathered and like the video if not liked
        for link in all_links:
            youtube_bot.get(link)
            time.sleep(3)
            #For dislike - Change xpath to //*[@id="top-level-buttons"]/ytd-toggle-button-renderer[2]
            like_button = youtube_bot.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]')
            #The class of the like button changes once we click it
            if like_button.get_attribute("class") == "style-scope ytd-menu-renderer force-icon-button style-text":
                like_button.click()
                print("Liked ", link)
                time.sleep(1)
            elif like_button.get_attribute("class") == "style-scope ytd-menu-renderer force-icon-button style-default-active":
                print("Already Liked !!", link)
        print("All videos Liked !!")


channel_videos_link = 'https://www.youtube.com/channel/UCS9nmu42YqXQSUloS94ewdQ/videos'

username=""
password=""

auto_user = YoutubeVedios(username, password, channel_videos_link)
auto_user.login_to_gmail()
auto_user.load_all_videos()
youtubeLinks=auto_user.get_all_links()

for video in youtubeLinks:
    print(str(video))
    os.system("python3 main.py --visits 1 --url "+str(video)+" --verbose ")

