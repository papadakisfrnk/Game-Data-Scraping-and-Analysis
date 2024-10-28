from cgitb import html
from pandas import Grouper
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd

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

def getHTMLsource(main_link):
    chrome_options = Options()
    chrome_options.add_argument("--headless") #o browser tha einai headless dld tha ekteleitai sto backgroudn

    driver = webdriver.Chrome(options= chrome_options, service=Service((ChromeDriverManager().install()))) # katevazoume ton driver gia to chrome

    driver.get(main_link) #dilwnoume tin selida ston driver gia na tin fortwsei
    hmtl_source = driver.page_source #katevasma toy kwdika tis selidas
    return hmtl_source


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

def crawl_main_source_page(html_source):
    #print (hmtl_source)

    #get_all_rows from the page
    GET_ALL_ROWS_RE = r'<li class="search-results-row">((.|\n)*?)<\/li>'
    game_list = re.findall(GET_ALL_ROWS_RE, html_source)

    for row in game_list:
        
        game_row = row[0]
        
        game_name = capture_game_name(game_row)
        rating = capture_rating(game_row)
        price = capture_price(game_row)
        release_date, game_genre = capture_release_genre(game_row)
        info_link = capture_info_link(game_row)
        game_detail_source = getHTMLsource(info_link)
        
        likes = capture_likes(game_detail_source)
        comments = capture_comments(game_detail_source)
        score = capture_score(game_detail_source)

        temp_dictionary = {}
        temp_dictionary['game_name'] = game_name
        temp_dictionary['rating'] = rating
        temp_dictionary['price'] = price[:-1]
        temp_dictionary['release_date'] = release_date
        temp_dictionary['game_genre'] = game_genre
        temp_dictionary['info_link'] = info_link
        temp_dictionary['likes'] = likes
        temp_dictionary['comments'] = comments
        temp_dictionary['score'] = score

        global main_dataframe
        #dimiourgia dataframe apo to sugkekrimeno lexiko
        df = pd.DataFrame([temp_dictionary])

        #prosthiki tou neou dataframe sto vasiko dataframe
        main_dataframe = pd.concat([main_dataframe, df], ignore_index=True, sort=False)

    print(main_dataframe)
    #meta to telos tis anaktisis grafoume to dataframe sto excel
    with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:
        main_dataframe.to_excel(writer, sheet_name='sheet1')


def main():
    main_link = 'https://www.allkeyshop.com/blog/catalogue/category-pc-games-all/'
    source_code =  getHTMLsource(main_link)
    crawl_main_source_page(source_code)

if __name__ == "__main__":
    main()