from flask import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from src.exception import CustomException
from bs4 import BeautifulSoup as bs
import pandas as pd
import os, sys
import time
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote


class ScrapeReviews:
    def __init__(self,
                 product_name:str,
                 no_of_products:int):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--headless')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Start a new Chrome browser session
        self.driver = webdriver.Chrome(options=options)

        self.product_name = product_name
        self.no_of_products = no_of_products

    def scrape_product_urls(self, product_name):
        try:
            search_string = product_name.replace(" ","-")
            # no_of_products = int(self.request.form['prod_no'])

            encoded_query = quote(search_string)
            # Navigate to the URL
            url = f"https://www.myntra.com/{search_string}?rawQuery={encoded_query}"
            self.driver.get(url)
            time.sleep(5)
            
            print(f"DEBUG: Navigated to {url}")
            print(f"DEBUG: Page Title is '{self.driver.title}'")
            
            myntra_text = self.driver.page_source
            print(f"DEBUG: Page source length: {len(myntra_text)}")
            
            myntra_html = bs(myntra_text, "html.parser")
            pclass = myntra_html.findAll("ul", {"class": "results-base"})

            product_urls = []
            for i in pclass:
                href = i.find_all("a", href=True)

                for product_no in range(len(href)):
                    t = href[product_no]["href"]
                    product_urls.append(t)

            return product_urls

        except Exception as e:
            raise CustomException(e, sys)

    def extract_reviews(self, product_link):
        try:
            productLink = "https://www.myntra.com/" + product_link
            self.driver.get(productLink)
            time.sleep(2)
            prodRes = self.driver.page_source
            prodRes_html = bs(prodRes, "html.parser")
            title_h = prodRes_html.findAll("title")

            if title_h:
                self.product_title = title_h[0].text
            else:
                self.product_title = "Unknown Product"

            self.product_rating_value = "N/A"
            overallRating = prodRes_html.findAll(
                "div", {"class": "index-overallRating"}
            )
            for i in overallRating:
                div_elem = i.find("div")
                if div_elem:
                    self.product_rating_value = div_elem.text
            
            self.product_price = "N/A"
            price = prodRes_html.findAll("span", {"class": "pdp-price"})
            for i in price:
                self.product_price = i.text
            product_reviews = prodRes_html.find(
                "a", {"class": "detailed-reviews-allReviews"}
            )

            if not product_reviews:
                return None
            return product_reviews
        except Exception as e:
            raise CustomException(e, sys)
        
    def scroll_to_load_reviews(self):
        # Change the window size to load more data
        self.driver.set_window_size(1920, 1080)

        # Get the initial height of the page
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        scroll_count = 0
        max_scrolls = 5  # Limit scrolls to prevent hanging on products with thousands of reviews
        
        while scroll_count < max_scrolls:
            # Scroll down by a small amount
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1.5)  # Slightly faster sleep
            
            # Calculate the new height after scrolling
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Break the loop if no new content is loaded
            if new_height == last_height:
                break
            
            last_height = new_height
            scroll_count += 1



    def extract_products(self, product_reviews: list):
        try:
            t2 = product_reviews["href"]
            Review_link = "https://www.myntra.com" + t2
            self.driver.get(Review_link)
            
            self.scroll_to_load_reviews()
            
            review_page = self.driver.page_source

            review_html = bs(review_page, "html.parser")
            review = review_html.findAll(
                "div", {"class": "detailed-reviews-userReviewsContainer"}
            )

            for i in review:
                user_rating = i.findAll(
                    "div", {"class": "user-review-main user-review-showRating"}
                )
                user_comment = i.findAll(
                    "div", {"class": "user-review-reviewTextWrapper"}
                )
                user_name = i.findAll("div", {"class": "user-review-left"})

            reviews = []
            for i in range(len(user_rating)):
                try:
                    rating = (
                        user_rating[i]
                        .find("span", class_="user-review-starRating")
                        .get_text()
                        .strip()
                    )
                except:
                    rating = "No rating Given"
                try:
                    comment = user_comment[i].text
                except:
                    comment = "No comment Given"
                try:
                    name = user_name[i].find("span").text
                except:
                    name = "No Name given"
                try:
                    date = user_name[i].find_all("span")[1].text
                except:
                    date = "No Date given"

                mydict = {
                    "Product Name": self.product_title,
                    "Over_All_Rating": self.product_rating_value,
                    "Price": self.product_price,
                    "Date": date,
                    "Rating": rating,
                    "Name": name,
                    "Comment": comment,
                }
                reviews.append(mydict)  #  a list of all dictionary elements

            review_data = pd.DataFrame(
                reviews,
                columns=[
                    "Product Name",
                    "Over_All_Rating",
                    "Price",
                    "Date",
                    "Rating",
                    "Name",
                    "Comment",
                ],
            )

            return review_data

        except Exception as e:
            raise CustomException(e, sys)
        
    
    def skip_products(self, search_string, no_of_products, skip_index):
        product_urls: list = self.scrape_product_urls(search_string, no_of_products + 1)

        product_urls.pop(skip_index)

    def get_review_data(self) -> pd.DataFrame:
        try:
            # search_string = self.request.form["content"].replace(" ", "-")
            # no_of_products = int(self.request.form["prod_no"])

            product_urls = self.scrape_product_urls(product_name=self.product_name)

            product_details = []

            review_len = 0


            while review_len < self.no_of_products and review_len < len(product_urls):
                product_url = product_urls[review_len]
                print(f"--> [Product {review_len + 1}/{self.no_of_products}] Navigating to product details page...")
                review = self.extract_reviews(product_url)

                if review:
                    print(f"    [Product {review_len + 1}/{self.no_of_products}] Extracting reviews and scrolling...")
                    product_detail = self.extract_products(review)
                    if product_detail is not None and not product_detail.empty:
                        product_details.append(product_detail)
                        review_len += 1
                        print(f"    [Product {review_len + 1}/{self.no_of_products}] Successfully scraped {len(product_detail)} reviews.")
                    else:
                        print(f"    [Product {review_len + 1}/{self.no_of_products}] No reviews found or extraction failed, skipping...")
                        product_urls.pop(review_len)
                else:
                    print(f"    [Product {review_len + 1}/{self.no_of_products}] No review link found, skipping...")
                    product_urls.pop(review_len)

            self.driver.quit()

            if not product_details:
                raise Exception("No reviews could be scraped. This can happen if Myntra blocked the request or no reviews exist for the search query.")

            data = pd.concat(product_details, axis=0)
            
            data.to_csv("data.csv", index=False)
            
            return data   # For running Streamlit app, you can return the data as dataframe directly
                
            # For running Flask app, you can return the columns and values separately. Uncomment the following lines:

            # columns = data.columns

            # values = [[data.loc[i, col] for col in data.columns ] for i in range(len(data)) ]
            
            # return columns, values
        
    

        except Exception as e:
            raise CustomException(e, sys)
