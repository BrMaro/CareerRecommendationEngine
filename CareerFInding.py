from bs4 import BeautifulSoup
import requests

class Job:
    def __init__(self,name,link):
        self.name = name
        self.link = link


domain = "https://www.myjobmag.co.ke/"

course = "software enineering"
def modify_variable(input_variable):
    if len(input_variable.split())>1:
        return '+'.join(input_variable.split())
    else:
        return str(input_variable)


url = f"https://www.myjobmag.co.ke/search/jobs?q={modify_variable(course)}"
print(url)

response = requests.get(url)

soup = BeautifulSoup(response.text,"html.parser")

job_items = soup.find_all('li',class_="job-list-li")

job_obj_li = []
for job in job_items:
    job_name = job.find('li',class_="mag-b")
    href_val = job.find('a')
    job_name_text = job_name.text if job_name else None

    # Extract the href value of href_val
    href_value = (domain + href_val.get('href')) if href_val else None
    #print(job_name_text, href_value)
    instance = Job(job_name_text,href_value)
    job_obj_li.append(instance)

print(job_obj_li[5].name)