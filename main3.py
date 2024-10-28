from cgitb import html
from pandas import Grouper
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#dimiourgia vasikou dataframe poy tha graftei sto excel
main_dataframe = pd.DataFrame()

def capture_game_name(game_row):
    GAME_TITLE_RE = r'<h2 class="search-results-row-game-title">(.*?)<\/h2>' #regex gia to capture tou titlou tou paixnidiou
    game_title_match = re.search(GAME_TITLE_RE, game_row).groups() #pairnoume to monadiko apotelesma kai apo ekei ta group tou
    print (game_title_match[0])
    return game_title_match[0]

def capture_rating(game_row):
    GAME_RATING_RE = r'data-product-id="\d+">\s*(\d+(\.\d)?)\s*<div class="metacritic-spinner-wrapper">'
    game_rating_match = re.findall(GAME_RATING_RE, game_row)
    if len(game_rating_match)>0:
        print (game_rating_match[0][0])
        return game_rating_match[0][0]
    else:
        print (" - ")
        return " - "

def capture_price(game_row):
    GAME_PRICE_RE = r'search-results-row-price">\s*(\d+(.\d+)?€)\s*?<\/div>'
    game_price_match = re.findall(GAME_PRICE_RE, game_row)
    if len(game_price_match)>0:
        print (game_price_match[0][0])
        return game_price_match[0][0]
    else:
        return ""

def capture_release_genre(game_row):
    GAME_YEAR_GENRE_RE = r'search-results-row-game-infos">(\d+) - ([\w ]+)<\/div>'
    game_year_genre_match = re.findall(GAME_YEAR_GENRE_RE, game_row)
    if len(game_year_genre_match)>0:
        print (game_year_genre_match[0][0])
        if len(game_year_genre_match[0])>0:
            print (game_year_genre_match[0][1])
            return game_year_genre_match[0][0], game_year_genre_match[0][1]
        else:
            return game_year_genre_match[0][0], ""
    else:
        return "", ""

def capture_info_link (game_row):
    GAME_LINK_RE = r'<a href="(https:\/\/www.allkeyshop.com/\w+\/[\w\d-]+\/)" class="search-results-row-link">'
    game_link_match = re.findall(GAME_LINK_RE, game_row)
    if len (game_link_match) > 0 : 
        print (game_link_match[0])
        return game_link_match[0]

def getDriversource(main_link):
    chrome_options = Options()
    chrome_options.add_argument("--headless") #o browser tha einai headless dld tha ekteleitai sto backgroudn

    driver = webdriver.Chrome(options= chrome_options, service=Service((ChromeDriverManager().install()))) # katevazoume ton driver gia to chrome

    driver.get(main_link) #dilwnoume tin selida ston driver gia na tin fortwsei
    
    return driver


def capture_likes(html_source):
    GET_LIKES_REGEX = r'<span class="aks-follow-counter-count" data-counter-count="">\s*(\d+)\s*</span>'
    likes = re.findall(GET_LIKES_REGEX, html_source)
    if len(likes) > 0:
        likes = likes[0]
    else:
        likes = ""
    return likes

def capture_comments(html_source):
    GET_COMMENTS_REGEX = r'<div class="aks-rating-btn-text">(\d+)</div>'
    comments = re.findall(GET_COMMENTS_REGEX, html_source)
    if len(comments) > 0:
        comments = comments[0]
    else:
        comments = ""
    return comments

def capture_score(html_source):
    GET_SCORE_REGEX = r'<span class="metacritic-count-comment-text">\s*(\d+)\s*</span>'
    score = re.findall(GET_SCORE_REGEX, html_source)
    if len(score) > 0:
        score = score[0]
    else:
        score = ""
    return score

def crawl_main_source_page(driver):

    #get_all_rows from the page
    game_list = driver.find_elements(By.CLASS_NAME, "search-results-row")

    for game in game_list:
        
        game_name = game.find_element(By.CLASS_NAME, "search-results-row-game-title").text
        
        print (game_name)


        #anaktisi tu rating ean ayto uparxei
        try:
            rating = game.find_element(By.CSS_SELECTOR, "div.metacritic-button.metacritic-button-basic.metacritic-button-green").get_attribute("textContent")
            print (rating.strip())
        except NoSuchElementException:
            print("-")

        #anaktisi tis timis
        price = game.find_element(By.CLASS_NAME, "search-results-row-price").text
        print (price)

        #anaktisi tis imerominias kukloforias
        release_genre = game.find_element(By.CLASS_NAME, "search-results-row-game-infos").text
        print (release_genre)

        #anaktisi tou link tou paixnidiu
        game_link = game.find_element(By.CLASS_NAME, "search-results-row-link").get_attribute("href")
        print (game_link)
        


def main():
    main_link = 'https://www.allkeyshop.com/blog/catalogue/category-pc-games-all/'
    driver =  getDriversource(main_link)
    crawl_main_source_page(driver)

if __name__ == "__main__":
    main()