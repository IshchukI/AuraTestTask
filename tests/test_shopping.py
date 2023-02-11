from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#Amazon locators
__url: str = "https://www.amazon.com/"
__search_field: str = 'twotabsearchtextbox'
__search_submit_button: str = 'nav-search-submit-button'
__popup_close_btn: str = '//input[@class="a-button-input"][@data-action-type="DISMISS"]'
__product_reviews: str = '//span[@class="a-size-base s-underline-text"]'
__price_whole: str = 'a-price-whole'
__price_fraction: str = 'a-price-fraction'


#Ebay locators
_url = "https://www.ebay.com/"
_search_field = '//input[@aria-label="Search for anything"]'
_product_reviews: str = 's-item__seller-info-text'
_price_whole: str = 's-item__price'
_search_submit_button: str = '//input[@value="Search"]'
_filter: str = '//a[@href="https://www.ebay.com/sch/i.html?_from=R40&_nkw=samsung+galaxy+s22&_sacat=0&rt=nc&Model' \
          '=Samsung%2520Galaxy%2520S22&_dcat=9355"]'

def test_shopping(driver):

    product = 'samsung galaxy s22'
    wait = WebDriverWait(driver, 10, 0.3)

    driver.get(__url)

    popup_close_btn = wait.until(EC.visibility_of_element_located((By.XPATH, __popup_close_btn)))
    popup_close_btn.click()

    search_field = wait.until(EC.visibility_of_element_located((By.ID, __search_field)))
    search_submit_button = wait.until(EC.visibility_of_element_located((By.ID, __search_submit_button)))
    search_field.send_keys(product)
    search_submit_button.click()


#Товары с самыми большими ревью Out of Stock
    # product_reviews_dict = {}
    # product_reviews = wait.until(EC.visibility_of_all_elements_located((By.XPATH, __product_reviews)))
    # for review in product_reviews:
    #     product_reviews_dict[int(review.text.replace(',', ''))] = review
    # max_val_reviews = max(product_reviews_dict.keys())
    # product_reviews_dict[max_val_reviews].click()
    # wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.HOME)

    product_price = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, __price_whole)))
    product_price_fraction = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, __price_fraction)))
    product_price_fool = []
    for price, fraction_price in zip(product_price, product_price_fraction):
        product_price_fool.append(int(price.text + fraction_price.text)/100)
    amazon_price = min(product_price_fool)
    print(amazon_price)

# bestbuy.com Access Denied
    driver.get(_url)
    search_field = wait.until(EC.visibility_of_element_located((By.XPATH, _search_field)))
    search_submit_button = wait.until(EC.visibility_of_element_located((By.XPATH, _search_submit_button)))
    search_field.send_keys(product)
    search_submit_button.click()

    product_filter = wait.until(EC.visibility_of_element_located((By.XPATH, _filter)))
    product_filter.click()

    product_reviews_dict = {}
    product_reviews = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, _product_reviews)))
    product_prices = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, _price_whole)))
    product_prices.pop(0)
    for review, price in zip(product_reviews, product_prices):
        review_text = review.text
        review_text_first_index = review_text.find("(") + 1
        review_text_last_index = review_text.find(")")
        product_reviews_dict_key = int(review_text[review_text_first_index:review_text_last_index].replace(',', ''))
        product_reviews_dict_value = (price.text.replace('$', '').replace(',', ''))
        product_reviews_dict[product_reviews_dict_key] = product_reviews_dict_value
    max_val_reviews = max(product_reviews_dict.keys())
    ebay_price = float(product_reviews_dict[max_val_reviews])
    print(ebay_price)

    assert amazon_price > ebay_price

