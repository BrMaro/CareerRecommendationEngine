import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class Job:
    name: str
    link: str

def get_related_jobs(course_name):
    domain = "https://www.myjobmag.co.ke/"
    
    def modify_variable(input_variable):
        if len(input_variable.split()) > 1:
            return '+'.join(input_variable.split())
        return str(input_variable)

    try:
        url = f"https://www.myjobmag.co.ke/search/jobs?q={modify_variable(course_name)}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        job_items = soup.find_all('li', class_="job-list-li")

        jobs = []
        for job in job_items:
            job_name = job.find('li', class_="mag-b")
            href_val = job.find('a')
            
            if job_name and href_val:
                job_name_text = job_name.text.strip()
                href_value = domain + href_val.get('href') if href_val.get('href') else None
                if job_name_text and href_value:
                    jobs.append(Job(job_name_text, href_value))

        return jobs[:5]  # Return only first 5 jobs
    
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return [] 