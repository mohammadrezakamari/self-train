from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

path='chromedriver.exe'
driver=webdriver.Chrome(executable_path=path)

driver.get('https://digikala.com')

serch_digi=WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By
.XPATH,'//*[@id="base_layout_desktop_fixed_header"]/header/div/div/div/div[1]/div/div/div[1]/div/span/div')))
serch_digi.click()

in_serch_digi=WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By
.XPATH,'//*[@id="base_layout_desktop_fixed_header"]/header/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/span/label/div/div/input')))
in_serch_digi.send_keys('دریل')
in_serch_digi.send_keys(Keys().ENTER)

time.sleep(5)

info_box=driver.find_element(By().CSS_SELECTOR,'.product-list_ProductList__pagesContainer__zAhrX.product-list_ProductList__pagesContainer--withSidebar__17nz1')
print(info_box)
elment_box=info_box.find_elements(By().CLASS_NAME,'product-list_ProductList__item__LiiNI')

#time.sleep(5)
link_txt=''
price_txt=''
topic_txt=''
driver.execute_script("window.scrollTo(0, 5000)") 
for index,el_at in enumerate(elment_box):
    a_tag=el_at.find_element(By.TAG_NAME,'a')
    href=a_tag.get_attribute('href')
    
    pic_tag=el_at.find_element(By().TAG_NAME,'picture')
    img_tag=pic_tag.find_element(By().TAG_NAME,'img')
    img_src=img_tag.get_attribute('src')
    time.sleep(1)
    print(img_src)
    try:
     img_data=requests.get(img_src).content
     with open(f'pics\pic{index}.jpg','wb') as x:
        x.write(img_data)
    except:
        pass 
    price_tag=el_at.find_element(By.CSS_SELECTOR,'.d-flex.ai-center.jc-end.gap-1.color-700.color-400.text-h5.grow-1')
    span_price=price_tag.find_element(By().TAG_NAME,'span')
    price_value=span_price.get_attribute('innerHTML')
    price_txt+=str(price_value)+'\n'
    link_txt+=str(href)+'\n'

    topic=el_at.find_element(By().CSS_SELECTOR,'.ellipsis-2.text-body2-strong.color-700.styles_VerticalProductCard__productTitle__6zjjN')
    topic_str=topic.get_attribute('innerHTML')
    topic_txt+=str(topic_str)+'\n'
with open('link.txt','w') as p:
    p.write(link_txt) 

with open('price.txt','w',encoding='utf-8') as z:
    z.write(price_txt)
with open('topic.txt','w',encoding='utf-8') as c:
    c.write(topic_txt)


