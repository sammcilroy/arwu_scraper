'''
Academic World Ranking of Universities (ARWU) 
Global Ranking of Academic Subjects

Scrape ranking data by subject and year from
AWRU pages to csv

Sam McIlroy
'''

# setup
import pandas as pd
from pandas import Series, DataFrame
import re
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import os

# variables
# subject names by code
subjects_map = {'RS0101': 'Mathematics',
                'RS0102': 'Physics',
                'RS0103': 'Chemistry',
                'RS0104': 'Earth Sciences',
                'RS0105': 'Geography',
                'RS0106': 'Ecology',
                'RS0107': 'Oceanography',
                'RS0108': 'Atmospheric Science',
                'RS0201': 'Mechanical Engineering',
                'RS0202': 'Electrical and Electronic Engineering',
                'RS0205': 'Automation and Control',
                'RS0206': 'Telecommunication Engineering',
                'RS0207': 'Instruements Science and Technology',
                'RS0208': 'Biomedical Engineering',
                'RS0210': 'Computer Science and Engineering',
                'RS0211': 'Civil Engineering',
                'RS0212': 'Chemical Enginering',
                'RS0213': 'Materials Science and Engineering',
                'RS0214': 'Nanoscience and Nanotechnology',
                'RS0215': 'Energy Science and Engineering',
                'RS0216': 'Environmental Science and Engineering',
                'RS0217': 'Water Resources',
                'RS0219': 'Food Science and Technology',
                'RS0220': 'Biotechnology',
                'RS0221': 'Aerospace Engineering',
                'RS0222': 'Marine/Ocean Engineering',
                'RS0223': 'Transportation Science and Technology',
                'RS0224': 'Remote Sensing',
                'RS0226': 'Mining and Mineral Engineering',
                'RS0227': 'Metallurgical Engineering',
                'RS0301': 'Biological Sciences',
                'RS0302': 'Human Biological Sciences',
                'RS0303': 'Agricultural Sciences',
                'RS0304': 'Veterinary Sciences',
                'RS0401': 'Clinical Medicine',
                'RS0402': 'Public Health',
                'RS0403': 'Denal and Oral Sciences',
                'RS0404': 'Nursing',
                'RS0405': 'Medical Technology',
                'RS0406': 'Pharmacy and Pharmaceutical Sciences',
                'RS0501': 'Economics',
                'RS0502': 'Statistics',
                'RS0503': 'Law',
                'RS0504': 'Political Sciences',
                'RS0505': 'Sociology',
                'RS0506': 'Education',
                'RS0507': 'Communication',
                'RS0508': 'Psychology',
                'RS0509': 'Business Administration',
                'RS0510': 'Finance',
                'RS0511': 'Management',
                'RS0512': 'Public Administration',
                'RS0513': 'Hospitality and Tourism Management',
                'RS0515': 'Libary and Information Science'}
# AWRU county codes
countries_dic = {'af':'Afghanistan',
                'xq':'Africa, not otherwise specified',
                'ax':'Aland Islands {Ahvenamaa}',
                'al':'Albania',
                'dz':'Algeria',
                'as':'American Samoa',
                'ad':'Andorra',
                'ao':'Angola',
                'ai':'Anguilla',
                'xx':'Antarctica and Oceania, not otherwise specified',
                'ag':'Antigua and Barbuda',
                'ar':'Argentina',
                'am':'Armenia',
                'aw':'Aruba',
                'xs':'Asia (Except Middle East), not otherwise specified',
                'au':'Australia',
                'at':'Austria',
                'az':'Azerbaijan',
                'bs':'Bahamas, The',
                'bh':'Bahrain',
                'bd':'Bangladesh',
                'bb':'Barbados',
                'by':'Belarus',
                'be':'Belgium',
                'bz':'Belize',
                'bj':'Benin',
                'bm':'Bermuda',
                'bt':'Bhutan',
                'bo':'Bolivia',
                'ba':'Bosnia and Herzegovina',
                'bw':'Botswana',
                'br':'Brazil',
                'vg':'British Virgin Islands [Virgin Islands, British]',
                'bn':'Brunei [Brunei Darussalam]',
                'bg':'Bulgaria',
                'bf':'Burkina [Burkina Faso]',
                'mm':'Burma [Myanmar]',
                'bi':'Burundi',
                'kh':'Cambodia',
                'cm':'Cameroon',
                'ca':'Canada',
                'ic':'Canary Islands',
                'cv':'Cape Verde',
                'xw':'Caribbean, not otherwise specified',
                'ky':'Cayman Islands',
                'cf':'Central African Republic',
                'xu':'Central America, not otherwise specified',
                'td':'Chad',
                'xl':'Channel Islands, not otherwise specified',
                'cl':'Chile',
                'cn':'China',
                'tw':'China (Taiwan) [Taiwan, Province Of China]',
                'cx':'Christmas Island',
                'cc':'Cocos (Keeling) Islands',
                'co':'Colombia',
                'km':'Comoros',
                'cg':'Congo',
                'cd':'Congo (Democratic Republic) [Congo (The Democratic Republic of the)] {Formerly Zaire}',
                'ck':'Cook Islands',
                'cr':'Costa Rica',
                'hr':'Croatia',
                'cu':'Cuba',
                'xa':'Cyprus (European Union)',
                'xb':'Cyprus (Non-European Union)',
                'xc':'Cyprus, not otherwise specified',
                'cz':'Czech Republic',
                'xm':'Czechoslovakia not otherwise specified',
                'dk':'Denmark',
                'dj':'Djibouti',
                'dm':'Dominica',
                'do':'Dominican Republic',
                'tl':'East Timor [Timor Leste]',
                'ec':'Ecuador',
                'eg':'Egypt',
                'sv':'El Salvador',
                'xf':'England',
                'gq':'Equatorial Guinea',
                'er':'Eritrea',
                'ee':'Estonia',
                'et':'Ethiopia',
                'xp':'Europe, not otherwise specified',
                'eu':'European Union, not otherwise specified',
                'fk':'Falkland Islands [Falkland Islands (Malvinas)]',
                'fo':'Faroe Islands',
                'fj':'Fiji',
                'fi':'Finland',
                'fr':'France',
                'gf':'French Guiana',
                'pf':'French Polynesia',
                'ga':'Gabon',
                'gm':'Gambia, The',
                'ge':'Georgia',
                'de':'Germany',
                'gh':'Ghana',
                'gi':'Gibraltar',
                'gr':'Greece',
                'gl':'Greenland',
                'gd':'Grenada',
                'gp':'Guadeloupe {includes St Martin (North)}',
                'gu':'Guam',
                'gt':'Guatemala',
                'gg':'Guernsey',
                'gn':'Guinea',
                'gw':'Guinea-Bissau',
                'gy':'Guyana',
                'ht':'Haiti',
                'hn':'Honduras',
                'hk':'Hong Kong (Special Administrative Region of China) [Hong Kong]',
                'hu':'Hungary',
                'is':'Iceland',
                'in':'India',
                'id':'Indonesia',
                'ir':'Iran [Iran, Islamic Republic of]',
                'iq':'Iraq',
                'ie':'Ireland',
                'im':'Isle of Man',
                'il':'Israel',
                'it':'Italy',
                'ci':'Ivory Coast',
                'jm':'Jamaica',
                'jp':'Japan',
                'je':'Jersey',
                'jo':'Jordan',
                'kz':'Kazakhstan',
                'ke':'Kenya',
                'ki':'Kiribati',
                'kp':'Korea (North) [Korea, Democratic People’s Republic of]',
                'kr':'Korea (South) [Korea, Republic of]',
                'qo':'Kosovo',
                'kw':'Kuwait',
                'kg':'Kyrgyzstan',
                'la':'Laos [Lao People’s Democratic Republic]',
                'lv':'Latvia',
                'lb':'Lebanon',
                'ls':'Lesotho',
                'lr':'Liberia',
                'ly':'Libya [Libyan Arab Jamahiriya]',
                'li':'Liechtenstein',
                'lt':'Lithuania',
                'lu':'Luxembourg',
                'mo':'Macao (Special Administrative Region of China) [Macao]',
                'mk':'Macedonia [Macedonia, The Former Yugoslav Republic of]',
                'mg':'Madagascar',
                'mw':'Malawi',
                'my':'Malaysia',
                'mv':'Maldives',
                'ml':'Mali',
                'mt':'Malta',
                'mh':'Marshall Islands',
                'mq':'Martinique',
                'mr':'Mauritania',
                'mu':'Mauritius',
                'yt':'Mayotte',
                'mx':'Mexico',
                'fm':'Micronesia [Micronesia, Federated States of]',
                'xr':'Middle East, not otherwise specified',
                'md':'Moldova [Moldova, Republic of]',
                'mc':'Monaco',
                'mn':'Mongolia',
                'ms':'Montserrat',
                'ma':'Morocco',
                'mz':'Mozambique',
                'na':'Namibia',
                'nr':'Nauru',
                'np':'Nepal',
                'nl':'Netherlands',
                'an':'Netherlands Antilles {Comprises Curacao, Bonaire, Saba, St Eustatius, St Martin (South)}',
                'nc':'New Caledonia',
                'nz':'New Zealand',
                'ni':'Nicaragua',
                'ne':'Niger',
                'ng':'Nigeria',
                'nu':'Niue',
                'nf':'Norfolk Island',
                'xt':'North America, not otherwise specified',
                'xg':'Northern Ireland',
                'mp':'Northern Mariana Islands',
                'no':'Norway',
                'zz':'Not Known',
                'om':'Oman',
                'pk':'Pakistan',
                'pw':'Palau',
                'pa':'Panama',
                'pg':'Papua New Guinea',
                'py':'Paraguay',
                'pe':'Peru',
                'ph':'Philippines',
                'pn':'Pitcairn, Henderson, Ducie And Oeno Islands [Pitcairn]',
                'pl':'Poland',
                'pt':'Portugal {Includes Madeira, Azores}',
                'pr':'Puerto Rico',
                'qa':'Qatar',
                're':'Réunion',
                'ro':'Romania',
                'ru':'Russia [Russian Federation]',
                'rw':'Rwanda',
                'ws':'Samoa',
                'sm':'San Marino',
                'st':'Sao Tome And Principe',
                'sa':'Saudi Arabia',
                'xh':'Scotland',
                'sn':'Senegal',
                'qn':'Serbia And Montenegro',
                'sc':'Seychelles',
                'sl':'Sierra Leone',
                'sg':'Singapore',
                'sk':'Slovakia',
                'si':'Slovenia',
                'sb':'Solomon Islands',
                'so':'Somalia',
                'za':'South Africa',
                'xv':'South America, not otherwise specified',
                'gs':'South Georgia And The South Sandwich Islands',
                'es':'Spain {includes CEUTA, MELILLA}',
                'xd':'Spain (Except Canary Islands)',
                'xe':'Spain, not otherwise specified',
                'lk':'Sri Lanka',
                'sh':'St Helena',
                'kn':'St Kitts And Nevis',
                'lc':'St Lucia',
                'pm':'St Pierre And Miquelon',
                'vc':'St Vincent And The Grenadines',
                'aa':'Stateless',
                'sd':'Sudan',
                'sr':'Surinam [Suriname]',
                'sj':'Svalbard And Jan Mayen',
                'sz':'Swaziland',
                'se':'Sweden',
                'ch':'Switzerland',
                'sy':'Syria [Syrian Arab Republic]',
                'tj':'Tajikistan',
                'tz':'Tanzania [Tanzania, United Republic of]',
                'th':'Thailand',
                'tg':'Togo',
                'tk':'Tokelau',
                'to':'Tonga',
                'tt':'Trinidad and Tobago',
                'tn':'Tunisia',
                'tr':'Turkey',
                'tm':'Turkmenistan',
                'tc':'Turks and Caicos Islands',
                'tv':'Tuvalu',
                'ug':'Uganda',
                'ua':'Ukraine',
                'xn':'Union of Soviet Socialist Republics not otherwise specified',
                'ae':'United Arab Emirates',
                'gb':'United Kingdom',
                'xk':'United Kingdom, not otherwise specified',
                'us':'United States',
                'vi':'United States Virgin Islands [Virgin Islands, U. S.]',
                'uy':'Uruguay',
                'uz':'Uzbekistan',
                'vu':'Vanuatu',
                'va':'Vatican City [Holy See (Vatican City State)]',
                've':'Venezuela',
                'vn':'Vietnam',
                'xi':'Wales',
                'wf':'Wallis and Futuna',
                'ps':'West Bank (including East Jerusalem) and Gaza Strip [Palestinian Territory, Occupied]',
                'eh':'Western Sahara',
                'ye':'Yemen',
                'xo':'Yugoslavia not otherwise specified',
                'zm':'Zambia',
                'zw':'Zimbabwe'}

def get_driver(headless=False):
    # setup Selenium Firefox driver
    # option to run headless or to monitor the collection
    if not headless:
        # SET DRIVER PATH TO PATH TO REPO /driver/geckodriver ON LOCAL MACHINE
        driver = webdriver.Firefox(executable_path= r"/Users/sam/code/arwu_scraper/driver/geckodriver")
    else:
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(executable_path= r"/Users/sam/code/arwu_scraper/driver/geckodriver", options=options)
    return driver

def get_num_pages(driver):
    # get the number of pages to be processed by the number of
    # page navigation options available
    pages = driver.find_elements_by_class_name('ant-pagination-item')
    num_pages = int((pages[-1].text))
    return num_pages

def get_table(driver):
    # Using Pandas read_html function, isolate and retrieve the current
    # rankings table as a Pandas DataFrame
    html_src = driver.page_source
    table = pd.read_html(html_src)
    data = DataFrame(table[0])
    data = data[['World Rank','Institution', 'Total Score', 'Unnamed: 4']]
    return data

def get_countries(html_src):
    # county values are represented by png images
    # find all country-flags pngs used in order
    # lookup country codes (e.g. us.png = United States)
    # this list forms the country column
    pattern = "(?<=country-flags/png100/).*?(?=.png)"
    countries = re.findall(pattern,html_src)
    return countries

def select_from_dropdown(span, link):
    # select additional column dropdown
    li = span.parent.find_elements_by_tag_name('li')
    for i in range(0,len(li)):
        if li[i].text == link:
            # select specified column to show data
            element = li[i]
            element.click()

def reset_page_options(driver, span):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    span.click()
    select_from_dropdown(span, 'Q1')

def get_category(subject):
    i = subject[3]
    if i == '1':
        return 'Natural Sciences'
    elif i == '2':
        return 'Engineering'
    elif i == '3':
        return 'Life Sciences'
    elif i == '4':
        return 'Medical Sciences'
    elif i == '5':
        return 'Social Sciences'
    else:
        return ''

def main():
    # if csv already exists, delete and refresh
    if os.path.exists("awru_complete_dataset.csv"):
        os.remove("awru_complete_dataset.csv")
    
    # set subjects and years to collect
    subjects = ['RS0101', 'RS0102', 'RS0103', 'RS0104', 'RS0105', 'RS0106','RS0201', 
    'RS0202', 'RS0205', 'RS0206', 'RS0207', 'RS0208', 'RS0210', 'RS0211', 'RS0212',
    'RS0213', 'RS0214', 'RS0215', 'RS0216', 'RS0217', 'RS0219', 'RS0220', 'RS0221', 
    'RS0222', 'RS0223', 'RS0224', 'RS0226', 'RS0227', 'RS0301', 'RS0302', 'RS0303', 
    'RS0304','RS0401', 'RS0402', 'RS0403', 'RS0404', 'RS0405', 'RS0406', 'RS0501',
    'RS0502', 'RS0503', 'RS0504', 'RS0505', 'RS0506', 'RS0507', 'RS0508', 'RS0509', 
    'RS0510', 'RS0511', 'RS0512', 'RS0513', 'RS0515']
    # years = ['2021', '2020', '2019', '2018', '2017']
    years = ['2021'] # data is abvailable between 2017 and 2021 if needed

    # get url for each subject and year to be collected
    for year in years:
        url_year = 'https://www.shanghairanking.com/rankings/gras/' + year
        for subject in subjects:
            url = url_year + '/' + subject
            # setup Selenium driver to run Firefox
            driver = get_driver(headless=True)
            # use driver to run new window fullscreen and retrieve the current URL and HTML source code
            driver.implicitly_wait(0.4)
            driver.maximize_window()
            driver.get(url)
            html_src = driver.page_source
            # get how many pages to process (how many pages the rankings are split by, 30 per page)
            num_pages = get_num_pages(driver)
            # store the current rankings table on the current page as Pandas DataFrame
            data = get_table(driver)
            # First 'additional/unkonw column is default, Q1'
            data.rename(columns={'Unnamed: 4': 'Q1'}, inplace=True)
            # add Subject column as current subject being processed
            data['Subject'] = subject
            # rename to full title using subjects_map lookup
            data['Subject'] = data['Subject'].map(subjects_map)
            # get country flags used on page in order, forms the country column
            countries = get_countries(html_src)
            # add Country column
            data['Country'] = countries
            data['Country'] = data['Country'].map(countries_dic)
            # re-sort data
            data = data[['World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'Subject']]
            # add additional columns
            # identify and click column selection dropdown
            span = driver.find_element_by_xpath('//*[@id="content-box"]/div[2]/table/thead/tr/th[5]/div/div[1]/div[1]/input')
            span.click()
            # add CNCI column
            # select CNCI option
            select_from_dropdown(span, 'CNCI')
            # get new table
            cnci = get_table(driver)
            cnci = cnci[['Institution', 'Unnamed: 4']]
            # rename CNCI column
            cnci.rename(columns={'Unnamed: 4': 'CNCI'}, inplace=True)
            # add CNCI column to dataset
            data = pd.merge(data, cnci, on='Institution', how='left')
            # re-sort data
            data = data[['World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'CNCI', 'Subject']]
            # add IC column
            # select IC option
            span.click()
            select_from_dropdown(span, 'IC')
            # get new table
            ic =  get_table(driver)
            ic = ic[['Institution', 'Unnamed: 4']]
            # rename IC column
            ic.rename(columns={'Unnamed: 4': 'IC'}, inplace=True)
            # add IC column to dataset
            data = pd.merge(data, ic, on='Institution', how='left')
            # re-sort data
            data = data[['World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'CNCI', 'IC', 'Subject']]
            # add TOP column
            # select TOP option
            span.click()
            select_from_dropdown(span, 'TOP')
            # get new table
            top =  get_table(driver)
            top = top[['Institution', 'Unnamed: 4']]
            # rename TOP column
            top.rename(columns={'Unnamed: 4': 'TOP'}, inplace=True)
            # add TOP column to dataset
            data = pd.merge(data, top, on='Institution', how='left')
            # re-sort data
            data = data[['World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'CNCI', 'IC', 'TOP', 'Subject']]
            # add AWARD column
            # select AWARD option
            span.click()
            select_from_dropdown(span, 'AWARD')
            # get new table
            award =  get_table(driver)
            award = award[['Institution', 'Unnamed: 4']]
            # rename AWARD column
            award.rename(columns={'Unnamed: 4': 'AWARD'}, inplace=True)
            # add AWARD column to dataset
            data = pd.merge(data, award, on='Institution', how='left')
            # re-sort data
            data = data[['World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'CNCI', 'IC', 'TOP', 'AWARD', 'Subject']]
            # reset page options to default options (Q1)
            reset_page_options(driver, span)
            # FIRST PAGE COMPLETE
            # COLLECT REMAINING PAGES IN SAME FORMAT
            try:
                # for page 2 to last page identified
                for i in range(2,num_pages+1):
                    # find the page navigation buttons by tag <li>
                    li = span.parent.find_elements_by_tag_name('li')
                    # for the page navigation buttons
                    for l in li:
                        try:
                            # find and click the next page in the sequence
                            if l.text == str(i):
                                element = l
                                element.click()
                                # move page to top
                                driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
                                # get current page HTML source code
                                html_src = driver.page_source
                                # retrieve next page main table, Q1
                                data_next = get_table(driver)
                                # additional column is default Q1
                                data_next.rename(columns={'Unnamed: 4': 'Q1'}, inplace=True)
                                # add subject code
                                data_next['Subject'] = subject
                                # map to subject name
                                data_next['Subject'] = data_next['Subject'].map(subjects_map)
                                # get country column
                                countries = get_countries(html_src)
                                # add Country to dataset
                                data_next['Country'] = countries
                                data_next['Country'] = data_next['Country'].map(countries_dic)
                                # re-sort data
                                data_next = data_next[['World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'Subject']]
                                # CNCI
                                # select CNCI from dropdown
                                span.click()
                                select_from_dropdown(span, 'CNCI')
                                # get HTML
                                html_src = driver.page_source 
                                # get table 
                                cnci = get_table(driver)
                                cnci = cnci[['Institution', 'Unnamed: 4']]
                                # additional column is CNCI
                                cnci.rename(columns={'Unnamed: 4': 'CNCI'}, inplace=True)
                                # add CNCI column to dataset
                                data_next = pd.merge(data_next, cnci, on='Institution', how='left')
                                # re-sort data
                                data_next = data_next[['World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'CNCI', 'Subject']]
                                # IC
                                # select IC from dropdown
                                span.click()
                                select_from_dropdown(span, 'IC')
                                # get HTML
                                html_src = driver.page_source 
                                # get table 
                                ic = get_table(driver)
                                ic = ic[['Institution', 'Unnamed: 4']]
                                # additional column is CNCI
                                ic.rename(columns={'Unnamed: 4': 'IC'}, inplace=True)
                                # add CNCI column to dataset
                                data_next = pd.merge(data_next, ic, on='Institution', how='left')
                                # re-sort data
                                data_next = data_next[['World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'CNCI', 'IC', 'Subject']]
                                # TOP
                                # select TOP from dropdown
                                span.click()
                                select_from_dropdown(span, 'TOP')
                                # get HTML
                                html_src = driver.page_source 
                                # get table 
                                top = get_table(driver)
                                top = top[['Institution', 'Unnamed: 4']]
                                # additional column is CNCI
                                top.rename(columns={'Unnamed: 4': 'TOP'}, inplace=True)
                                # add CNCI column to dataset
                                data_next = pd.merge(data_next, top, on='Institution', how='left')
                                # re-sort data
                                data_next = data_next[['World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'CNCI', 'IC', 'TOP', 'Subject']]
                                # AWARD
                                # select AWARD from dropdown
                                span.click()
                                select_from_dropdown(span, 'AWARD')
                                # get HTML
                                html_src = driver.page_source 
                                # get table 
                                award = get_table(driver)
                                award = award[['Institution', 'Unnamed: 4']]
                                # additional column is CNCI
                                award.rename(columns={'Unnamed: 4': 'AWARD'}, inplace=True)
                                # add CNCI column to dataset
                                data_next = pd.merge(data_next, award, on='Institution', how='left')
                                # re-sort data
                                data_next = data_next[['World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'CNCI', 'IC', 'TOP', 'AWARD', 'Subject']]
                                # ADD THIS COLLECTED PAGE TO MAIN DATASET AND RESET
                                data = pd.concat([data, data_next], ignore_index=True)
                                reset_page_options(driver, span)
                        except Exception as ex:
                            # Continue if current subject has less than 500 rankings
                            pass
                # ONCE ALL PAGES COMPLETE, WRITE/APPEND SUBJECT DATASET TO CSV
                # add Year to dataset
                data['Year'] = year
                # add Category to dataset by subject
                data['Category'] = subject
                # subject lookup Category (e.g. Mathematics to Natural Sciences)
                data['Category'] = data['Category'].apply(get_category)
                # re-sort data
                data = data[['Year', 'Category', 'Subject', 'World Rank', 'Institution', 'Country', 'Total Score', 'Q1', 'CNCI', 'IC', 'TOP', 'AWARD']]
                # WRITE DATA TO CSV
                # if the csv does not exist include a header row and create new file
                if not os.path.exists("awru_complete_dataset.csv"):
                    data.to_csv("awru_complete_dataset.csv", index=False, header=True)
                else:
                    # if csv does exist (process has already started)
                    # append to the current csv, ommiting the header
                    with open('awru_complete_dataset.csv', 'a') as f:
                        data.to_csv(f, index=False, header=False)
            except:
                pass
            # CLOSE DRIVER BEFORE MOVING ON TO NEXT SUBJECT
            driver.close()




if __name__ == '__main__':
    main()

