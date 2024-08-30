import selenium.common.exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from collections import Counter
import mysql.connector
import os

options = Options()
options.add_experimental_option("detach", True)
driver_path = 'C:\\Users\\Techron\\PycharmProjects\\chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(options=options,service=service)
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


def save_progress(cluster_index, page_number, course_index):
    with open("progress.txt", "w") as file:
        file.write(f"{cluster_index},{page_number},{course_index}")


def load_progress():
    if os.path.exists("progress.txt"):
        with open("progress.txt", "r") as file:
            progress = file.read().split(",")
            return int(progress[0]), int(progress[1]), int(progress[2])
    return 0, 1, 0


#logs into kuccps
def login(kcse_index, year, password):
    driver.find_element(By.ID, "id_kcse_index_number").send_keys(kcse_index)
    driver.find_element(By.ID, "id_kcse_year").send_keys(year)
    driver.find_element(By.ID, "id_password").send_keys(password)
    driver.find_element(By.TAG_NAME, "button").click()


#return True if the record is already recorded
def check_certification_duplicate_records(prog_code):
    check_duplicate_query = "SELECT * FROM Certification WHERE Programme_Code = %s"
    data = (prog_code,)
    cursor.execute(check_duplicate_query, data)
    if cursor.fetchone() is not None:
        return True
    else:
        return False


def check_course_duplicate_records(course_name):
    check_duplicate_course = "SELECT * FROM course WHERE programme_name = %s"
    cursor.execute(check_duplicate_course, (course_name,))
    print(f"- Checking for Duplicates")
    if cursor.fetchone() is not None:
        return True
    else:
        return False


def update_course_values(programme_name, Cluster, Cluster_s_1, Cluster_s_2, Cluster_s_3, Cluster_s_4, Min_s_1,Min_s_1_grade, Min_s_2, Min_s_2_grade, Min_s_3, Min_s_3_grade, Min_s_4, Min_s_4_grade,Min_grade):
    update_course_table_query = f"""
    INSERT INTO Course(programme_name,Cluster,Cluster_subject_1 ,Cluster_subject_2,Cluster_subject_3 ,Cluster_subject_4 ,Minimum_subject_1,Minimum_subject_1_grade ,Minimum_subject_2 ,Minimum_subject_2_grade,Minimum_subject_3 ,Minimum_subject_3_grade,Minimum_subject_4 ,Minimum_subject_4_grade,Minimum_Mean_Grade)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    data = (programme_name, Cluster, Cluster_s_1, Cluster_s_2, Cluster_s_3, Cluster_s_4, Min_s_1, Min_s_1_grade,
            Min_s_2, Min_s_2_grade, Min_s_3, Min_s_3_grade, Min_s_4, Min_s_4_grade, Min_grade)
    cursor.execute(update_course_table_query, data)
    conn.commit()


def update_certification_values(Programme_Code, Iname, Programme_Name, Year_1_Programme_cost,_2022_cut_off, _2021_cut_off, _2020_cut_off):
    update_certification_table_query = f"""
        INSERT INTO certification(Programme_Code,Iname,Programme_Name,Year_1_Programme_cost,_2022_cut_off,_2021_cut_off,_2020_cut_off)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
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


def get_course_and_certification_data():
    cluster_index, page_number, course_index = load_progress()

    while True:
        try:
            # Institution tab click
            institution_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='hide-menu'])[3]")))
            institution_tab.click()

            dropdown_ul = driver.find_elements(By.XPATH, "(//ul[@class='dropdown-menu inner'])")
            li_elements = dropdown_ul[1].find_elements(By.TAG_NAME, "li")[1:]

            # Scrape Cluster list
            for cl in range(cluster_index, len(li_elements)):
                li_element = li_elements[cl]

                try:
                    # Scroll to the cluster element
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", li_element)

                except selenium.common.exceptions.StaleElementReferenceException:
                    dropdown_ul = driver.find_elements(By.XPATH, "(//ul[@class='dropdown-menu inner'])")
                    li_elements = dropdown_ul[1].find_elements(By.TAG_NAME, "li")[1:]
                    li_element = li_elements[cl]
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", li_element)



                # Ensure the element is clickable
                group_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='filter-option pull-left'])[2]")))
                group_tab.click()

                # Refresh the dropdown elements
                dropdown_ul = driver.find_elements(By.XPATH, "(//ul[@class='dropdown-menu inner'])")
                li_elements = dropdown_ul[1].find_elements(By.TAG_NAME, "li")[1:]

                li_elements[cl].click()
                print(f"Collecting Cluster {cl + 1}")

                search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn bg-inverse')]")))
                search_button.click()

                try:
                    pg1 = driver.find_element(By.LINK_TEXT, "1")
                    all_pg = driver.find_elements(By.XPATH, "(//li[@class='paginate_button ']//a)")
                    all_pg.insert(0, pg1)

                except selenium.common.NoSuchElementException:
                    print(f"No courses in Cluster {cl + 1}")
                    continue

                # scrape courses per page
                for pg in range(page_number, len(all_pg)):

                    prog_table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "col-sm-12")))
                    prog_tbody = prog_table.find_element(By.TAG_NAME, "tbody")
                    prog_tr = prog_tbody.find_elements(By.CSS_SELECTOR, "tr")

                    for i in range(course_index, len(prog_tr)):
                        course_row = prog_tr[i]
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", course_row)

                        prog_table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "col-sm-12")))
                        prog_tbody = prog_table.find_element(By.TAG_NAME, "tbody")
                        prog_tr = prog_tbody.find_elements(By.CSS_SELECTOR, "tr")

                        prog_tr[i].click()

                        # Scrape course details
                        programme_name = driver.find_element(By.XPATH, "//h3[@class='text-center']").text
                        cluster = driver.find_element(By.XPATH, "//button[contains(@class,'btn btn-outline')]").text
                        print(f"{programme_name}")

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
                        elif len(entry_td3_elements) == 2 and table_elements[0].find_element(By.TAG_NAME,
                                                                                             "th").text == "Minimum Mean Grade":
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

                        # update values to the database if not already in database
                        if not check_course_duplicate_records(programme_name):
                            update_course_values(programme_name, cluster, Cluster_s_1, Cluster_s_2, Cluster_s_3,Cluster_s_4, Min_s_1, Min_s_1_grade, Min_s_2, Min_s_2_grade, Min_s_3,Min_s_3_grade, Min_s_4, Min_s_4_grade, Min_grade)

                        itable = driver.find_element(By.XPATH, "//table[@class = 'table table-bordered small']")
                        itable_tbody = itable.find_element(By.TAG_NAME, 'tbody')
                        itable_tr_elements = itable_tbody.find_elements(By.TAG_NAME, "td")

                        course_index = i + 1  # Update course index
                        save_progress(cl, pg, course_index)  # Save progress


                        # scrape certification list
                        for i in range(0, len(itable_tr_elements), 9):
                            Programme_Code = itable_tr_elements[i + 2].text.replace("TRANSFER","")
                            Iname = itable_tr_elements[i].text
                            #Programme_Name = itable_tr_elements[i+3].text
                            Year_1_Programme_cost = itable_tr_elements[i + 4].text
                            _2022_cut_off = itable_tr_elements[i + 5].text
                            _2021_cut_off = itable_tr_elements[i + 6].text
                            _2020_cut_off = itable_tr_elements[i + 7].text
                            # print(Programme_Code)
                            if not check_certification_duplicate_records(Programme_Code):
                                update_certification_values(Programme_Code, Iname, programme_name,Year_1_Programme_cost, _2022_cut_off, _2021_cut_off,_2020_cut_off)  # the programme name used here is the programme name taken before preceding loop
                                print(f"Program Code: {Programme_Code, Iname}",end=", ")

                        driver.back()

                        #Reload group list
                        prog_table = driver.find_element(By.CLASS_NAME, "col-sm-12")
                        prog_tbody = prog_table.find_element(By.TAG_NAME, "tbody")
                        prog_tr = prog_tbody.find_elements(By.CSS_SELECTOR, "tr")

                    pg1 = driver.find_element(By.LINK_TEXT, "1")
                    all_pg = driver.find_elements(By.XPATH, "(//li[@class='paginate_button ']//a)")
                    all_pg.insert(0, pg1)

                    if len(all_pg) > 1 and pg + 1 < len(all_pg):
                        page_number = pg + 1  # Move to the next page
                        course_index = 0  # Reset course index for the next page
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",all_pg[pg + 1])
                        all_pg[pg + 1].click()


                    save_progress(cl, pg + 1, course_index)

                print(f"Cluster {cl + 1} collected\n")
                cluster_index = cl + 1  # Move to the next cluster
                page_number = 1  # Reset page number for the next cluster
                save_progress(cluster_index, page_number, course_index)  # Save progress

        except selenium.common.NoSuchWindowException or KeyboardInterrupt:
            print("\nWindow Closed")
            return

        except selenium.common.NoSuchDriverException:
            print("\nUpdate Chromedriver")
            return


login(index_no, examination_year, password)

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

create_course_table_query = """
CREATE TABLE IF NOT EXISTS Course (
ccourse_id INT AUTO_INCREMENT PRIMARY KEY,
programme_name VARCHAR(255) UNIQUE,
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
CREATE TABLE IF NOT EXISTS Certification (
Programme_Code INT PRIMARY KEY,
Iname VARCHAR(255),
Programme_name VARCHAR(255),
FOREIGN KEY(Programme_name) REFERENCES Course(programme_name),
Programme_Name_in_campus VARCHAR(255),
Year_1_Programme_cost VARCHAR(255),
_2022_cut_off VARCHAR(255),
_2021_cut_off VARCHAR(255),
_2020_cut_off VARCHAR(255)
);
"""


get_course_and_certification_data()