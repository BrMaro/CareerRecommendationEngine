from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import mysql.connector

# Set up Google Chrome option and open browser
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
url = "https://students.kuccps.net/login/"
driver.get(url)
driver.implicitly_wait(10)

index_no = '20400003321'
examination_year = '2022'
password = '36613105012'

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Kereskwe1",
    "database": "CampusCourses"
}


def login(kcse_index, year, password):
    driver.find_element(By.ID, "id_kcse_index_number").send_keys(kcse_index)
    driver.find_element(By.ID, "id_kcse_year").send_keys(year)
    driver.find_element(By.ID, "id_password").send_keys(password)
    driver.find_element(By.TAG_NAME, "button").click()


def update_institution_values(id, alias, name, category, institution_type, parent_ministry):
    update_institution_table_query = f"""
    INSERT INTO Institution(id,alias,Name,Category,Institution_type,Parent_ministry)
    VALUES(%s,%s,%s,%s,%s,%s)
    """
    data = (id, alias, name, category, institution_type, parent_ministry)
    cursor.execute(update_institution_table_query, data)
    conn.commit()


def get_institution_data():
    driver.find_element(By.XPATH, "(//ul[@class='nav in']//a)[2]").click()  # Institution tab
    select_element = driver.find_element(By.TAG_NAME, "select")
    select = Select(select_element)
    select.select_by_index(3)
    option_text = select.options[3].text

    try:
        while driver.find_element(By.LINK_TEXT, "Next").is_enabled():
            td_elements = driver.find_elements(By.CSS_SELECTOR, "td")
            for i in range(0, (int(option_text) * 6), 6):
                id = td_elements[i].text
                alias = td_elements[i + 1].text
                name = td_elements[i + 2].text
                category = td_elements[i + 3].text
                institution_type = td_elements[i + 4].text
                parent_ministry = td_elements[i + 5].text
                update_institution_values(id, alias, name, category, institution_type, parent_ministry)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element(By.LINK_TEXT, "Next").click()
    except IndexError:
        pass


login(index_no, examination_year, password)

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
show_tables = "SHOW tables"
cursor.execute(show_tables)
for row in cursor.fetchall():
    print(row)

create_institution_table_query = """
CREATE TABLE IF NOT EXISTS Institution (
id INT PRIMARY KEY,
alias VARCHAR(255),
Name VARCHAR(255),
Category VARCHAR(255),
institution_type VARCHAR(255),
Parent_Ministry VARCHAR(255)
);
"""
cursor.execute(create_institution_table_query)
for row in cursor.fetchall():
    print(row)

get_institution_data()
