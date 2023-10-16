from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def check_certification_duplicate_records(prog_code):
    check_duplicate_query = "SELECT * FROM my_table WHERE Programme_Code = %s"
    data = prog_code
    cursor.execute(check_duplicate_query,data)
    if cursor.fetchone() is not None:
        return True
    else:
        return False

def update_course_values():



def get_course_and_certfication_data():
    driver.find_element(By.XPATH, "(//span[@class='hide-menu'])[3]").click()  # Institution tab
    dropdown_ul = driver.find_elements(By.XPATH, "(//ul[@class='dropdown-menu inner'])")
    li_elements = dropdown_ul[1].find_elements(By.TAG_NAME,"li")
    li_elements = li_elements[1:]
    for i in range(len(li_elements)):
        driver.find_element(By.XPATH, "(//span[@class='filter-option pull-left'])[2]").click()  # Group tab
        dropdown_ul = driver.find_elements(By.XPATH, "(//ul[@class='dropdown-menu inner'])")
        li_elements = dropdown_ul[1].find_elements(By.TAG_NAME, "li")
        li_elements = li_elements[1:]
        li_elements[i].click()
        print(f"Cluster {i+1} collected")
        driver.find_element(By.XPATH,"//button[contains(@class,'btn bg-inverse')]").click() # search button




login(index_no, examination_year, password)

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
show_tables = "SHOW tables"
cursor.execute(show_tables)
for row in cursor.fetchall():
    print(row)


get_course_and_certfication_data()


create_course_table_query = """
CREATE TABLE IF NOT EXISTS Course (
id INT PRIMARY KEY,
alias VARCHAR(255),
course_name VARCHAR(255),
Cluster/Group VARCHAR(255),
Cluter_subject_1 VARCHAR(255),
Cluter_subject_2 VARCHAR(255),
Cluter_subject_3 VARCHAR(255),
Cluter_subject_4 VARCHAR(255),
Minimum_subject_1 VARCHAR(255),
Minimum_subject_1_grade VARCHAR(255),
Minimum_subject_2 VARCHAR(255),
Minimum_subject_2_grade VARCHAR(255),
Minimum_subject_3 VARCHAR(255),
Minimum_subject_3_grade VARCHAR(255),
Overall_grade VARCHAR(255),
);
"""

create_certification_table_query = """
CREATE TABLE IF NOT EXISTS Certfication (
Programme_Code INT PRIMARY KEY,
FOREIGN KEY(Name) REFERENCES Name(Intitution),
FOREGIN KEY(course_name)
Programme_Name VARCHAR(255),
Year_1_Programme_cost VARCHAR(255),
2022_cut_off VARCHAR(255),
2021_cut_off VARCHAR(255),
2020_cut_off VARCHAR(255)
);
"""
