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
    cursor.execute(check_duplicate_query, data)
    if cursor.fetchone() is not None:
        return True
    else:
        return False


def update_course_values(id, alias, course_name, Cluster, Cluster_s_1, Cluster_s_2, Cluster_s_3, Cluster_s_4, Min_s_1,
                         Min_s_1_grade, Min_s_2, Min_s_2_grade, Min_subject_3, Min_s_3_grade, Overall_grade):
    update_course_table_query = f"""
    INSERT INTO Institution(id,alias,course_name,Cluster,Cluster_subject_1 ,Cluster_subject_2,Cluster_subject_3 ,Cluster_subject_4 ,Min_subject_1,Min_subject_1_grade ,Min_subject_2 ,Min_subject_2_grade,Min_subject_3 ,Min_subject_3_grade,Overall_grade)
    VALUES(%s,%s,%s,%s,%s,%s)
    """
    data = (id, alias, course_name, Cluster, Cluster_s_1, Cluster_s_2, Cluster_s_3, Cluster_s_4, Min_s_1, Min_s_1_grade,
            Min_s_2, Min_s_2_grade, Min_subject_3, Min_s_3_grade, Overall_grade)
    cursor.execute(update_course_table_query, data)
    conn.commit()


def update_certification_values(Programme_Code,Iname,course_name,Programme_Name,Year_1_Programme_cost,_2022_cut_off,_2021_cut_off,_2020_cut_off):
    update_certification_table_query = f"""
        INSERT INTO Institution(Programme_Code,Iname,course_name,Programme_Name,Year_1_Programme_cost,_2022_cut_off,_2021_cut_off,_2020_cut_off)
        VALUES(%s,%s,%s,%s,%s,%s)
        """
    data = (Programme_Code,Iname,course_name,Programme_Name,Year_1_Programme_cost,_2022_cut_off,_2021_cut_off,_2020_cut_off)
    cursor.execute(update_certification_table_query, data)
    conn.commit()


def get_course_and_certfication_data():
    driver.find_element(By.XPATH, "(//span[@class='hide-menu'])[3]").click()  # Institution tab
    dropdown_ul = driver.find_elements(By.XPATH, "(//ul[@class='dropdown-menu inner'])")
    li_elements = dropdown_ul[1].find_elements(By.TAG_NAME, "li")
    li_elements = li_elements[1:]
    for i in range(len(li_elements)):
        driver.find_element(By.XPATH, "(//span[@class='filter-option pull-left'])[2]").click()  # Group tab
        dropdown_ul = driver.find_elements(By.XPATH, "(//ul[@class='dropdown-menu inner'])")
        li_elements = dropdown_ul[1].find_elements(By.TAG_NAME, "li")
        li_elements = li_elements[1:]
        li_elements[i].click()
        print(f"Cluster {i + 1} collected")
        driver.find_element(By.XPATH, "//button[contains(@class,'btn bg-inverse')]").click()  # search button

        select_element = driver.find_element(By.TAG_NAME, "select")
        select = Select(select_element)
        select.select_by_index(3)

        td_elements = driver.find_elements(By.CSS_SELECTOR, "td")

        for i in range(len(td_elements)):
            td_elements[i].click()
            course_name = driver.find_element(By.XPATH, "//h3[@class='text-center']").text
            cluster = driver.find_element(By.XPATH, "//button[contains(@class,'btn btn-outline')]").text
            print(course_name, cluster)

            table = driver.find_element(By.TAG_NAME, "table")
            entry_requirements = driver.find_element(By.XPATH, "//div=[@class = 'col-md-6']")

        print(f"Cluster {i + 1} collected")


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
programme_name VARCHAR(255),
Cluster VARCHAR(255),
Cluster_subject_1 VARCHAR(255),
Cluster_subject_2 VARCHAR(255),
Cluster_subject_3 VARCHAR(255),
Cluster_subject_4 VARCHAR(255),
Minimum_subject_1 VARCHAR(255),
Minimum_subject_1_grade VARCHAR(255),
Minimum_subject_2 VARCHAR(255),
Minimum_subject_2_grade VARCHAR(255),
Minimum_subject_3 VARCHAR(255),
Minimum_subject_3_grade VARCHAR(255),
Overall_grade VARCHAR(255)
);
"""
create_certification_table_query = """
CREATE TABLE IF NOT EXISTS Certfication (
Programme_Code INT PRIMARY KEY,
FOREIGN KEY(IName) REFERENCES IName(Institution),
FOREIGN KEY(programme_name) REFERENCES programme_name(Course),
Programme_Name VARCHAR(255),
Year_1_Programme_cost VARCHAR(255),
2022_cut_off VARCHAR(255),
2021_cut_off VARCHAR(255),
2020_cut_off VARCHAR(255)
);
"""

# cursor.execute(create_course_table_query)
# for row in cursor.fetchall():
#     print(row)

# cursor.execute(create_certification_table_query)
# for row in cursor.fetchall():
#     print(row)
