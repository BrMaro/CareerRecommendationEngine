from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from collections import Counter
import mysql.connector

# Set up Google Chrome option and open browser
options = Options()
options.add_experimental_option("detach", True)
 # Enable headless mode

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


def update_course_values(id, programme_name, Cluster, Cluster_s_1, Cluster_s_2, Cluster_s_3, Cluster_s_4, Min_s_1,
                         Min_s_1_grade, Min_s_2, Min_s_2_grade, Min_s_3, Min_s_3_grade, Min_s_4, Min_s_4_grade,
                         Min_grade):
    update_course_table_query = f"""
    INSERT INTO Institution(id,programme_name,Cluster,Cluster_subject_1 ,Cluster_subject_2,Cluster_subject_3 ,Cluster_subject_4 ,Min_subject_1,Min_subject_1_grade ,Min_subject_2 ,Min_subject_2_grade,Min_subject_3 ,Min_subject_3_grade,Min_subject_4 ,Min_subject_4_grade,Minimum_Mean_Grade)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    data = (id, programme_name, Cluster, Cluster_s_1, Cluster_s_2, Cluster_s_3, Cluster_s_4, Min_s_1, Min_s_1_grade,
            Min_s_2, Min_s_2_grade, Min_s_3, Min_s_3_grade, Min_s_4, Min_s_4_grade, Min_grade)
    cursor.execute(update_course_table_query, data)
    conn.commit()


def update_certification_values(Programme_Code, Iname, Programme_Name, Year_1_Programme_cost,
                                _2022_cut_off, _2021_cut_off, _2020_cut_off):
    update_certification_table_query = f"""
        INSERT INTO Institution(Programme_Code,Iname,Programme_Name,Year_1_Programme_cost,_2022_cut_off,_2021_cut_off,_2020_cut_off)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
    data = (Programme_Code, Iname, Programme_Name, Year_1_Programme_cost, _2022_cut_off, _2021_cut_off,
            _2020_cut_off)
    cursor.execute(update_certification_table_query, data)
    conn.commit()


def most_common_code(numbers):
    if not numbers:
        return None  # Return None if the input list is empty.

    # Use Counter to count the occurrences of each element.
    count = Counter(numbers)

    # Find the element with the highest count.
    most_common = max(count, key=count.get)

    return most_common


def get_course_and_certfication_data():
    driver.find_element(By.XPATH, "(//span[@class='hide-menu'])[3]").click()  # Institution tab
    dropdown_ul = driver.find_elements(By.XPATH, "(//ul[@class='dropdown-menu inner'])")
    li_elements = dropdown_ul[1].find_elements(By.TAG_NAME, "li")
    li_elements = li_elements[1:]

    #scrape Cluster list
    for i in range(len(li_elements)):
        driver.find_element(By.XPATH, "(//span[@class='filter-option pull-left'])[2]").click()  # Group tab
        dropdown_ul = driver.find_elements(By.XPATH, "(//ul[@class='dropdown-menu inner'])")
        li_elements = dropdown_ul[1].find_elements(By.TAG_NAME, "li")
        li_elements = li_elements[1:]
        li_elements[i].click()
        print(f"Cluster {i + 1} collected")
        driver.find_element(By.XPATH, "//button[contains(@class,'btn bg-inverse')]").click()  # search button

        prog_table = driver.find_element(By.CLASS_NAME,"col-sm-12")
        prog_tbody = prog_table.find_element(By.TAG_NAME,"tbody")
        prog_tr = prog_tbody.find_elements(By.CSS_SELECTOR,"tr")

        #scrape course list
        for i in range(len(prog_tr)):
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", prog_tr[i])

            print(prog_tr[i].text)
            prog_tr[i].click()
            programme_name = driver.find_element(By.XPATH, "//h3[@class='text-center']").text
            cluster = driver.find_element(By.XPATH, "//button[contains(@class,'btn btn-outline')]").text
            #print(programme_name, cluster)

            Cluster_s_1 = ""
            Cluster_s_2 = ""
            Cluster_s_3 = ""
            Cluster_s_4 = ""
            Min_s_1 = ""
            Min_s_1_grade = ""
            Min_s_2 = ""
            Min_s_2_grade = ""
            Min_s_3 = ""
            Min_s_3_grade = ""
            Min_s_4 = ""
            Min_s_4_grade = ""
            Min_grade = ""
            table_elements = driver.find_elements(By.XPATH, "//div[@class = 'col-md-6']")
            # scrape from the minimum entry requirements table
            entry_td3_elements = table_elements[0].find_elements(By.TAG_NAME, "td")
            if len(entry_td3_elements) == 5:
                Cluster_s_1 = entry_td3_elements[0].text
                Cluster_s_2 = entry_td3_elements[1].text
                Cluster_s_3 = entry_td3_elements[2].text
                Cluster_s_4 = entry_td3_elements[3].text
            elif len(entry_td3_elements) == 4:
                Cluster_s_1 = entry_td3_elements[0].text
                Cluster_s_2 = entry_td3_elements[1].text
                Cluster_s_3 = entry_td3_elements[2].text
            elif len(entry_td3_elements) == 3:
                Cluster_s_1 = entry_td3_elements[0].text
                Cluster_s_2 = entry_td3_elements[1].text
            elif len(entry_td3_elements) == 2:
                Cluster_s_1 = entry_td3_elements[0].text
            elif len(entry_td3_elements) == 2 and table_elements[0].find_element(By.TAG_NAME,"th").text == "Minimum Mean Grade":
                Min_grade = entry_td3_elements[0].text

            # Scrape from the minimum subject requirements table
            subject_td3_elements = table_elements[1].find_elements(By.TAG_NAME, "td")
            if len(subject_td3_elements) == 8:
                Min_s_1 = subject_td3_elements[0].text
                Min_s_1_grade = subject_td3_elements[1].text
                Min_s_2 = subject_td3_elements[2].text
                Min_s_2_grade = subject_td3_elements[3].text
                Min_s_3 = subject_td3_elements[4].text
                Min_s_3_grade = subject_td3_elements[5].text
                Min_s_4 = subject_td3_elements[6].text
                Min_s_4_grade = subject_td3_elements[7].text
                #print(Min_s_1, Min_s_1_grade)
            elif len(subject_td3_elements) == 6:
                Min_s_1 = subject_td3_elements[0].text
                Min_s_1_grade = subject_td3_elements[1].text
                Min_s_2 = subject_td3_elements[2].text
                Min_s_2_grade = subject_td3_elements[3].text
                Min_s_3 = subject_td3_elements[4].text
                Min_s_3_grade = subject_td3_elements[5].text
                #print(Min_s_1, Min_s_1_grade)
            elif len(subject_td3_elements) == 4:
                Min_s_1 = subject_td3_elements[0].text
                Min_s_1_grade = subject_td3_elements[1].text
                Min_s_2 = subject_td3_elements[2].text
                Min_s_2_grade = subject_td3_elements[3].text
                #print(Min_s_1, Min_s_1_grade)
            elif len(subject_td3_elements) == 2:
                Min_s_1 = subject_td3_elements[0].text
                Min_s_1_grade = subject_td3_elements[1].text
                #print(Min_s_1, Min_s_1_grade)

            # update values to the database
            # update_course_values(id, programme_name, cluster, Cluster_s_1, Cluster_s_2, Cluster_s_3, Cluster_s_4, Min_s_1, Min_s_1_grade,Min_s_2, Min_s_2_grade, Min_s_3, Min_s_3_grade,Min_s_4,Min_s_4_grade,Min_grade)

            itable = driver.find_element(By.XPATH, "//table[@class = 'table table-bordered small']")
            itable_tbody = itable.find_element(By.TAG_NAME, 'tbody')
            itable_tr_elements = itable_tbody.find_elements(By.TAG_NAME, "td")


            # scrape certification list
            for i in range(0, len(itable_tr_elements),9):
                Programme_Code = itable_tr_elements[i+2].text
                Iname = itable_tr_elements[i].text
                Programme_Name = itable_tr_elements[i+3].text
                Year_1_Programme_cost = itable_tr_elements[i+4].text
                _2022_cut_off = itable_tr_elements[i+5].text
                _2021_cut_off = itable_tr_elements[i+6].text
                _2020_cut_off = itable_tr_elements[i+7].text
                # update_certification_values(Programme_Code, Iname, Programme_Name, Year_1_Programme_cost,_2022_cut_off, _2021_cut_off, _2020_cut_off)
            driver.back()

            #Reload group list
            prog_table = driver.find_element(By.CLASS_NAME, "col-sm-12")
            prog_tbody = prog_table.find_element(By.TAG_NAME, "tbody")
            prog_tr = prog_tbody.find_elements(By.CSS_SELECTOR, "tr")


        try:
            if driver.find_element(By.LINK_TEXT, "Next").is_enabled():
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

get_course_and_certfication_data()

create_course_table_query = """
CREATE TABLE IF NOT EXISTS Course (
id INT PRIMARY KEY,
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
Minimum_subject_4 VARCHAR(255),
Minimum_subject_4_grade VARCHAR(255),
Minimum_Mean_Grade VARCHAR(255)
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
