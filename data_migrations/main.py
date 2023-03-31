import pandas as pd
import numpy as np
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service

# form_url = 'http://ee.kobo.local/x/2eyzRNLp'
# form_prefix = '/aCgbxk7xTdP4RgAwqHmSdo/'
# form_prefix_without = 'aCgbxk7xTdP4RgAwqHmSdo'
form_url = 'http://enketo.qbitsx.com/x/H1Oi37pI'
form_prefix = '/aK4sNs43KmuDvvQT25aJn7/'
form_prefix_without = 'aK4sNs43KmuDvvQT25aJn7'

df = pd.read_csv('घर_धर_ववरण_समबनध_परशनवल_-_all_versions_-_English_en_-_2023-03-27-04-29-43.csv')
form_sheet_url = 'palata_form.xlsx'
form_df = pd.read_excel(form_sheet_url, sheet_name=[0,1,2])


s = Service("drivers/chromedriver_linux64/chromedriver") # add the path of the driver
driver = webdriver.Chrome(service=s)



# click on show more btn
def join_with(data):
    final_join = []
    for c in data:
        name = c.split()
        final_join.append("_".join(name))
    return final_join
        
def get_url(url):
    driver.get(url)
    time.sleep(5)

def show_more_btn():
    show_more = driver.find_element(By.CLASS_NAME, 'Buttons__Button-sc-19xdot-1')
    show_more.click()

def to_bs4_object(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    return soup

# Return the current url html code
def get_page_source():
    result = driver.page_source
    soup = to_bs4_object(result)
    return soup

def submit_form():
    save_draft = driver.find_element(By.ID, 'save-draft')
    save_draft.click()
    time.sleep(2)
    save_draft_close = driver.find_element(By.XPATH, '/html/body/div[5]/div/form/div[4]/button[1]')
    save_draft_close.click()
    # submit = driver.find_element(By.ID, 'submit-form')
    # submit.click()

def fill_form(form_name, data, prefix=form_prefix):
    # fill the form
    try:
        text_input = driver.find_element(By.NAME, prefix + form_name)
        text_input.clear()
        text_input.send_keys(data)
    except:
        pass

def click_radio_btn(form_name):
    radio_btn = driver.find_element(By.XPATH, form_name)
    radio_btn.click()

def select_option_value(form_name, data):
    select = Select(driver.find_element(By.NAME, form_name))
    select.select_by_value(data)

def select_dropdown(form_name, data):
    # select the dropdown
    select = Select(driver.find_element(By.NAME, form_name))
    select.select_by_visible_text(data)
    

def click_btn(value):
    btn = driver.find_element(By.CLASS_NAME, value)
    btn.click()
    
def click_btns_xpath(xpath, radio_xpath):
    time.sleep(1)
    btn = driver.find_element(By.XPATH, xpath)
    btn.click()
    time.sleep(1)
    radio_btn = driver.find_element(By.XPATH, radio_xpath)
    radio_btn.click()
    time.sleep(1)
    
def click_btn_by_xpath(xpath):
    btn = driver.find_element(By.XPATH, xpath)
    btn.click()

# filter by user
def filter_data_by_user(user, data=df):
    data_user_mask = data['_submitted_by'] == user
    final_data = data[data_user_mask]
    return final_data

def conver_to_int(num):
    try:
        number = int(num)
    except:
        number = 0
    return number

def click_radio_btn(xpath):
    radio_btn = driver.find_element(By.XPATH, xpath)
    radio_btn.click()

def write_in_file(num):
    f = open('counter.txt', 'w')
    f.write(str(num))
    f.close()

form_input_df = form_df[0].copy()
form_input_choices_df = form_df[1].copy()

def fill_form_by_xpath(xpath, value):
    try:
        text_input = driver.find_element(By.XPATH, xpath)
        text_input.clear()
        text_input.send_keys(value)
    except:
        pass

def get_text_start_with(dataframe, column, text):
    mask = []
    for i in range(len(dataframe)):
        d = dataframe[column][i]
        start_bol = d.startswith(text)
        mask.append(start_bol)
    return dataframe[mask]

def filter_by_value(dataframe, value, col_name='list_name'):
    new_df = dataframe[dataframe[col_name]==value]
    return new_df

def get_name_value(choice_code, input_value, select_type='select_one'):
    inputs = filter_by_value(form_input_df, select_type + ' ' + choice_code, col_name='type')
    choices = filter_by_value(form_input_choices_df, choice_code)
    selected = filter_by_value(choices, input_value, col_name='label::Nepali (ne)')
    name = ''
    value = ''
    if len(inputs) == 1:
        name = inputs['name'][inputs.index[0]]
    if len(selected) ==1:
        value = selected['name'][selected.index[0]]
    return name, value

def press_radio_btn(choice_code, input_value, select_type='select_one', group=''):
    name, value = get_name_value(choice_code, input_value, select_type)
    try:
        if group != '':
            click_radio_btn("//input[@value='" + value +"'][@name='"+ form_prefix + group + name + "']")
        else:
            click_radio_btn("//input[@value='" + value +"'][@name='"+ form_prefix + name + "']")
    except:
        pass

def get_name_columns(choice_code, select_type='select_multiple'):
    inputs = filter_by_value(form_input_df, select_type + ' ' + choice_code, col_name='type')
    choices = filter_by_value(form_input_choices_df, choice_code)
    name = ''
    question = ''
    if len(inputs) == 1:
        name = inputs['name'][inputs.index[0]]
        question = inputs['label::Nepali (ne)'][inputs.index[0]]
    return name, question, choices

def press_multiple_select_btn(choice_code, ind, select_type='select_multiple'):
    name, question, choices = get_name_columns(choice_code, select_type)
    for i in choices.index:
        col_name = question + "/" + choices['label::Nepali (ne)'][i]
        val = df[col_name][ind]
        print()
        if val == 1:
            value = choices['name'][i]
            try:
                click_btn_by_xpath("//input[@value='" + value +"'][@name='"+ form_prefix + name + "']")
            except:
                pass

def format_url(url):
    try:
        img_url = url.split('=')
        not_formated_url = img_url[1].split('%2F')
        formated_url = '/'.join(not_formated_url)
        return 'media/' + formated_url
    except:
        ''

def file_input_form(xpath, file_path):
    try:
        file_input = driver.find_element(By.XPATH, xpath)
        file_input.send_keys(os.getcwd()+"/"+file_path)
    except:
        pass

try:
    counter = int(open('counter.txt', 'r'))
except:
    counter = 0

for i in range(len(df)):
    if i > counter:
        get_url(form_url)
        fill_form('Full_Name', df['Full Name'][i])
        fill_form('Full_Name_in_Block_Letter', df['Full Name in Block Letter'][i])
        file_input_form("//input[@type='file'][@name='" + form_prefix + "Photo']", format_url(df['Photo_URL'][i]))
        fill_form('__006', df['बावुको नाम'][i])
        fill_form('_006_003', df['आमाको नाम'][i])
        fill_form('__007', df["Grandfather's Name"][i])
        fill_form('__008', df["Grandmother's Name"][i])
        click_btns_xpath('//label[10]/div/button', "//label[10]/div/ul/li/a/label/input[@value='6']")
        click_btns_xpath('//label[11]/div/button', "//label[11]/div/ul/li/a/label/input[@value='64']")
        click_btns_xpath('//label[12]/div/button', "//label[12]/div/ul/li/a/label/input[@value='754']")
        fill_form('__114', conver_to_int(df['वार्ड न'][i]))
        press_radio_btn('vt1zz96', df["घर नम्बर छ कि छैन?"][i])
        fill_form('lat', df['_GPS Location_latitude'][i], prefix='')
        fill_form('long', df['_GPS Location_longitude'][i], prefix='')
        fill_form('alt', df['_GPS Location_altitude'][i], prefix='')
        fill_form('acc', df['_GPS Location_precision'][i], prefix='')
        press_radio_btn('cz2jk72', df["टोल विकास संस्थामा आवद्ध हो कि हैन?"][i])
        press_radio_btn('wm62p77',df["ल्याण्डलाईन फोन छ कि छैन?"][i])
        press_radio_btn('yp0hq40', df["५. तपाईको परिवारमा १ बर्ष भित्र परिवारको सदस्यको मृत्यु भएको छ कि छैन?"][i])
        press_multiple_select_btn('lg3eo60', i)
        press_radio_btn('tx2yg79', df["८. गत १२ महिनामा तपाईँको परिवारमा गर्भवती महिलाले नियमित रूपमा तालिम प्राप्त स्वास्थ्य कर्मीहरुबाट स्वास्थ्य जाँच गराउनु भयो ?"][i])
        press_radio_btn('wp07t02', df["९. यदि गर्भवती महिलाले नियमित रूपमा तालिम प्राप्त स्वास्थ्यकर्मीबाट स्वास्थ्य जाँच नगराएको भए, कारण के हो ?"][i])
        press_radio_btn('hc5rq16', df["१०. गत १२ महिनामा तपाईँको परिवारबाट कसैले जिवित शिशुलाई जन्म दिनु भएको भए कहाँ जन्म दिनु भयो ?"][i])
        press_radio_btn('km6qn48', df["११. गत १२ महिनामा तपाईँको परिवारबाट कसैले जिवित शिशुलाई जन्म दिनु भएको भए बच्चा जन्माउँदा कसले सहयोग गरेको थियो ?"][i])
        press_radio_btn('qy6qi96', df["१२. यदि तालिम प्राप्त स्वास्थ्य कर्मीबाट सहयोग नलिनु भएको भए किन नलिनु भएको हो ?"][i])
        press_radio_btn('bs0wz87', df["१३. गत १२ महिनामा तपाईँको परिवारको कुनै महिला सदस्यको गर्भवती अवस्थामा वा सुत्केरी हुँदा वा सुत्केरी भएको ६ हप्ता भित्र मृत्यु भएको थियो ?"][i])
        press_radio_btn('hc3gl33', df["१४. गत १२ महिनामा तपाईँको परिवारमा कुनै जन्मिएको शिशुको सुत्केरी हुँदा वा सुत्केरी भएको ६ हप्ता भित्र मृत्यु भएको थियो ?"][i])
        press_radio_btn('xi6tl55', df["१५. तपाईँको परिवारमा ५ वर्ष मुनिका केटाकेटीलाई सबै खोपको मात्रा (वि.सि.जी., डि.पि.टी. र दादुरा) दिनु भएको छ ?"][i])
        press_radio_btn('kj4rw88', df["१६. परिवारले कृषि तथा पशुपालन कार्यका लागी जग्गा प्रयोग गरेको छ ?"][i])
        press_radio_btn('su9vw15', df["१८. तपाईँले अन्नबाली उत्पादनको लागि जग्गाको व्यवस्थापन कसरी गर्नु भएको छ ?"][i])
        press_radio_btn('fo0ch54', df["२०. तपाईँले खेती गरिरहनु भएको जमिनमा सिँचाई सुविधा पुगेको छ ?"][i])
        press_radio_btn('ib9ta50', df["२२. तपाई बसेको घरको स्वामित्व कस्तो प्रकारको हो?"][i])
        press_radio_btn('ya8uz87', df["२५. तपाईको घर भाडामा दिनु भएको छ कि छैन?"][i], group='group_tz3jl07/')
        fill_form('group_tz3jl07/group_go5vq67/_1235454332113', df['बहालमा लिनेको नाम'][i], prefix='')
        fill_form('group_tz3jl07/group_go5vq67/_1235', df['बहालमा लिनेको नाम'][i], prefix='')
        press_radio_btn('wi4rc65', df["२६. तपाईको परिवारको खानेपानीको मुख्य स्रोत के हो ?"][i])
        press_radio_btn('se4qu81', df["२७. पिउने पानी पिउनु अघि शुद्धिकरण गर्ने गर्नुहुन्छ ?"][i])
        press_radio_btn('sj12s54', df["२८. यदि शुद्धिकरण गर्नुहुन्छ भने कुन विधिको प्रयोग गर्नुभएको छ ?"][i])
        press_radio_btn('eq3vw73', df["२९. तपाईको परिवारले खाना पकाउन प्रयोग गर्ने मुख्य इन्धन कुन हो?"][i])
        press_radio_btn('pf2hi63', df["३०. तपाईँको घरमा कस्तो प्रकारको चुल्हो प्रयोग गर्नु हुन्छ?"][i])
        press_radio_btn('nh0uj70', df["३१. तपाईँको भान्सामा वायु संचार प्रणाली छ कि छैन ?"][i])
        press_radio_btn('eu2sk39', df["३३. तपाईको परिवारले प्रयोग गर्ने बत्तीको मुख्य स्रोत के हो ?"][i])
        press_radio_btn('rh4da62', df["३४. वत्ति वाल्न विजुलीको प्रयोग गर्नुभएको छ भने, आफ्नै घरमा विजुलीको मिटर जडान भएको छ ?"][i])
        press_radio_btn('ye7yn19', df["३५. यदि वत्ति वाल्न विजुलीको प्रयोग गर्नुभएको छैन भने किन प्रयोग नगर्नु भएको हो ?"][i])
        press_radio_btn('su4tg61', df["३६. तपाईको परिवारले प्रयोग गर्ने शौचालय कस्तो प्रकारको छ ?"][i])
        press_radio_btn('qo9jj22', df["घर, आँगन, शौचालयवाट निष्कृति फोहोरमैलालाई व्यवस्थित गर्ने घरधुरी"][i])
        press_multiple_select_btn('ch6xi14', i)
        press_radio_btn('oa9wy64', df["इण्टरनेट सेवा उपलव्ध हुन नसके घर"][i])
        press_radio_btn('ap7hd86', df["४४. परिवारले कुनै चौपाया तथा पशुपंक्षी पालेको छ ?"][i])
        press_radio_btn('jy7vb01', df["गाइगोरु /बाच्छाबाच्छी"][i])
        press_radio_btn('pk1fu07', df["राँगाभैसी/पाडापाडी"][i])
        press_radio_btn('go1uh46', df["बाख्रा/भेडा, खसी/बोका, सुँगुर/वंगुर"][i])
        press_radio_btn('te1dg11', df["कुखुरा/हाँस"][i])
        press_radio_btn('bd5aq17', df["अस्ट्रिच"][i])
        press_radio_btn('mb5ld93', df["कालिज (फ्रेन्च/घर पालुवा)"][i])
        press_radio_btn('lk0ie33', df["तपाइको परिवारमा माछापालन गरिएको छ ?"][i])
        press_radio_btn('zy9xd83', df["तपाइको परिवारमा मौरीपालन गरिएको छ ?"][i])
        press_radio_btn('ej65a51', df["तपाइको परिवारमा रेशमपालन गरिएको छ ?"][i])
        press_radio_btn('le5db96', df["स्वास्थ्य चौकी (हेल्थ पोष्ट) पुग्ने माध्यम"][i])
        press_radio_btn('bz5eb29', df["अस्पताल पुग्ने माध्यम"][i])
        press_multiple_select_btn('rg87t90', i)
        press_radio_btn('vp4sj17', df["५०. तपाईँको घर सम्म कस्तो सतह ढलको व्यवस्था छ ?"][i])
        press_radio_btn('wr4qv34', df["५२. तपाईँको टोलमा सार्वजनिक विकास निर्माण सम्वन्धी कार्यको लागतमा समुदायको सहभागीता कति सम्म हुनसक्छ ?"][i])
        press_radio_btn('nt3hn18', df["५३. तपाईको परिवारमा महिला सदस्य कुनै सङ्घ/संस्थामा संलग्न भएका छन् ?"][i])
        press_multiple_select_btn('wv2fa62', i)
        press_radio_btn('zn4xo43', df["५६. वितेको एक वर्षभित्र कुनै प्रकोपबाट तपाइँको परिवार पिडीत भयो ?"][i])
        press_radio_btn('zl0ye17', df["घरव्यवहारसम्बन्धी विषयमा निर्णय"][i])
        press_radio_btn('sc2la54', df["घरायसी काममा संलग्न"][i])
        press_radio_btn('ig15u66', df["बैँकमा खाता सञ्चालन"][i])
        press_radio_btn('ht9sq98', df["विद्यालय व्यवस्थापन समितिमा सहभागिता"][i])
        press_radio_btn('al9cj52', df["उद्योग व्यापारमा सहभागिता"][i])
        press_radio_btn('fl65i91', df["५९. तपाई पालिकामा करदाताको रुपमा दर्ता हुनुभएको छ कि छैन ?"][i])
        fill_form('__003', conver_to_int(df['तपाईको जम्मा परिवार संख्या कति छ ?'][i]))
        fill_form('group_mz42f71/_014512', conver_to_int(df['कृषि आय'][i]))
        fill_form('group_mz42f71/_12454545', conver_to_int(df['ब्यापार आय'][i]))
        fill_form('group_mz42f71/_52012', conver_to_int(df['उद्योग आय'][i]))
        fill_form('group_mz42f71/_12054', conver_to_int(df['जागीर आय'][i]))
        fill_form('group_mz42f71/_2155878', conver_to_int(df['बैदेशिक रोजगारी (विप्रेषण) आय'][i]))
        fill_form('group_mz42f71/_212544', conver_to_int(df['भाडा (बहाल) आय'][i]))
        fill_form('group_mz42f71/_545121', conver_to_int(df['उद्यम आय'][i]))
        fill_form('group_mz42f71/_45456876754', conver_to_int(df['अन्य आय'][i]))
        fill_form('_020_001', conver_to_int(df['खाना वार्षिक खर्च'][i]))
        fill_form('_021_001', conver_to_int(df['शिक्षा खर्च'][i]))
        fill_form('_022_002', conver_to_int(df['स्वास्थ्य खर्च'][i]))
        fill_form('_023_001', conver_to_int(df['कर तथा सेवा शुल्क भुक्तानी खर्च'][i]))
        fill_form('_024_001', conver_to_int(df['मनोरञ्जन तथा भ्रमण खर्च'][i]))
        fill_form('_025_001', conver_to_int(df['सामाजिक कार्य खर्च'][i]))
        fill_form('_026_001', conver_to_int(df['दान खर्च'][i]))
        fill_form('_027_001', conver_to_int(df['अन्य खर्च'][i]))
        fill_form('__057', conver_to_int(df['मोवाइल फोन प्रयोगकता संख्या'][i]))
        fill_form('__089', df['स्वास्थ्य चौकी (हेल्थ पोष्ट) रहेको स्थान'][i])
        fill_form('__090', conver_to_int(df['स्वास्थ्य चौकी (हेल्थ पोष्ट) पुग्न लाग्ने समय'][i]))
        fill_form('__092', df['अस्पताल रहेको स्थान'][i])
        fill_form('__093', conver_to_int(df['अस्पताल पुग्न लाग्ने समय'][i]))
        file_input_form("//input[@type='file'][@name='" + form_prefix + "__112']", format_url(df['औंठा छाप (बायाँ)_URL'][i]))
        file_input_form("//input[@type='file'][@name='" + form_prefix + "__113']", format_url(df['औंठा छाप (दायाँ)_URL'][i]))
        fill_form('__009', df['House Number'][i])
        fill_form('__011', df['आबद्ध टोल विकास संस्था'][i])
        fill_form('__012', df['फोन नं.'][i])
        press_radio_btn('pf1rb96', df["परिवार बाहेक अरुको स्वामित्वमा जग्गा छ ?"][i])
        press_radio_btn('lo3uc18', df["२१. सिँचाई के मार्फत गरिएको छ?"][i], group='group_hk4mk33/')
        fill_form_by_xpath("//*[@id='"+ form_prefix_without +"']/section[8]/section/label[1]/input", df['बहालमा लिनेको नाम'][i])
        fill_form_by_xpath("//*[@id='"+ form_prefix_without +"']/section[8]/section/label[2]/input", df['बहालको प्रयोग'][i])
        fill_form_by_xpath("//*[@id='"+ form_prefix_without +"']/section[8]/section/label[3]/input", conver_to_int(df['बहालको कोठा संख्या'][i]))
        fill_form_by_xpath("//*[@id='"+ form_prefix_without +"']/section[8]/section/label[4]/input", conver_to_int(df['बहालको सम्झौता अवधी'][i]))
        fill_form_by_xpath("//*[@id='"+ form_prefix_without +"']/section[8]/section/label[5]/input", df['बहालको मिति'][i])
        fill_form_by_xpath("//*[@id='"+ form_prefix_without +"']/section[8]/section/label[6]/input", conver_to_int(df['बहाल अवधी'][i]))
        fill_form_by_xpath("//*[@id='"+ form_prefix_without +"']/section[8]/section/label[7]/input", conver_to_int(df['बहाल रकम'][i]))
        press_radio_btn('ai8dr92', df["३२. यदि छ भने कुन प्रकारको रहेको छ ?"][i])
        time.sleep(2)
        submit_form()
        time.sleep(2)
        write_in_file(i)
        print(i)