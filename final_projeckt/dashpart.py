from dash import Dash,dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import Input,Output
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

import plotly.express as px
import plotly.graph_objects as go

from unidecode import unidecode


app=Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

my_tx=html.H1('salam')

my_in=dbc.Input(style={'text-align':'right'})
my_bt=dbc.Button('serch',style={'margin-top':'20px','margin-right':'100px'})
my_tx2=html.H1()
my_div=html.Div()
my_div2=html.Div()
my_graf=dcc.Graph(figure={})

@app.callback(Output(my_graf,component_property='figure'),
              Output(my_div2,component_property='children'),
              Output(my_bt,component_property='n_clicks'),
              Output(my_div,component_property='children'),
              Input(my_bt,component_property='n_clicks'),
              Input(my_in,component_property='value')
              )

def rr(n_clicks,my_in):
    if n_clicks>0:
       path='chromedriver.exe'
       driver=webdriver.Chrome(executable_path=path)

       driver.get('https://digikala.com')

       serch_digi=WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By
       .XPATH,'//*[@id="base_layout_desktop_fixed_header"]/header/div/div/div/div[1]/div/div/div[1]/div/span/div')))
       serch_digi.click()

       in_serch_digi=WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By
       .XPATH,'//*[@id="base_layout_desktop_fixed_header"]/header/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/span/label/div/div/input')))
       in_serch_digi.send_keys(my_in)
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
           with open(f'assets\sss\pic{index}.jpg','wb') as x:
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

       rows=[html.Tr([html.Th('عنوان'),html.Th('قیمت'),html.Th('تصویر'),])] 
       with open('topic.txt',encoding='utf-8') as c:
        t_s=c.read().split('\n')
       with open('link.txt') as c:
        l_s=c.read().split('\n')
       with open('price.txt',encoding='utf-8') as c:
        p_s=c.read().split('\n')
       im_li=os.listdir('assets\sss') 
       for t,p,l,img in zip(t_s,p_s,l_s,im_li):
        img_sh=html.Img(src=app.get_asset_url(f'sss/{img}'),width='100px',height='100px')
        d=html.Tr([html.Td(img_sh),html.Td(p),html.Td(html.A(t,href=l))]) 
        rows.append(d)
       children=[html.Table(rows,style={'width':'100%'})] 
       g_li=[]
       m=[]
       with open('price.txt',) as d:
        g_li=d.read().split('\n')
        print(g_li)
       g_li=[x.replace(',','') for x in g_li]
       g_li=[unidecode(b) for b in g_li]
       for i,x in enumerate(g_li):
        if x=='':
         g_li.pop(i)
       g_li=list(map(int,g_li))
       figure=go.Figure(data=go.Scatter(x=list(range(0,len(g_li))),y=g_li))  
    return figure,children,n_clicks,my_in  


app.layout=dbc.Container([
    dbc.Row([my_tx,my_in,my_bt,my_div,my_div2,my_graf],className='text-center')
])

app.run_server(port='54020')