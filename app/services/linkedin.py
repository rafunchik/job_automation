import time
import requests
import re
import urllib.parse

from bs4 import BeautifulSoup
from services.llm import is_remote2, is_contract


def get_jobs(location: str, keywords: str, age=386400):
    converted_location = urllib.parse.quote(location)
    converted_keywords = urllib.parse.quote(keywords)
    jobids = []
    role = {}
    job_list = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    target_url = (
        'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?'
        'f_TPR=r{age}&'
        'f_WT=2&'
        'location={converted_location}&'
        'keywords={converted_keywords}&'
        'refresh=true&start={page_index}')
    total = 1
    i = 1
    while total > 0:
        time.sleep(2)
        res = requests.get(target_url.format(age=age,
                                             converted_location=converted_location,
                                             converted_keywords=converted_keywords,
                                             page_index=i),
                           headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        alljobs_on_this_page = soup.find_all("li")
        total_page_jobs = len(alljobs_on_this_page)
        print(total_page_jobs)
        total = total_page_jobs
        i += 25
        for x in range(0, total_page_jobs):
            try:
                jobid = alljobs_on_this_page[x].find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
                jobids.append(jobid)
            except Exception as e:
                pass
    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    for j in range(0, min(len(jobids), 10)):
        time.sleep(1)
        resp = requests.get(
            url=target_url.format(jobids[j]),
            headers=headers)
        text = resp.text
        soup = BeautifulSoup(text, 'html.parser')

        job_title = ""
        try:
            role["job-title"] = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
            job_title = role["job-title"]
        except:
            role["job-title"] = None

        try:
            company = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
            role["company"] = company
        except Exception as e:
            print(e)
            role["company"] = ""

        # try:
        #     tracker_url = soup.find("section", {"class": "top-card-layout"}).find("a", {'data-tracking-control-name': 'public_jobs_topcard_logo'}).get('href')
        #     pattern = r'\?trk=.*$'
        #
        #     # Use re.sub() to replace the unwanted part with an empty string
        #     company_url = re.sub(pattern, '', tracker_url)
        #
        #     # Append '/about' to the URL
        #     company_url += '/about'
        #
        #     cookie = {
        #         'name': 'li_at',
        #         'value': LINKEDIN_COOKIE,
        #         'domain': '.linkedin.com'
        #     }
        #     session = requests.Session()
        #     session.cookies.update(cookie)
        #     resp_company = session.get(
        #         url=company_url,
        #         headers=headers)
        #     soup_company = BeautifulSoup(resp_company.text, 'html.parser')
        #     import pdb
        #     pdb.set_trace()
        #     company_field = soup_company.find("section",{"class": "org-page-details-module__card-spacing"}).select("dl > dd:nth-child(1)")[0].text.strip()
        #     print(company_field)
        #     break
        #
        #     role["company_field"] = company_field
        # except Exception as e:
        #     print(e)
        #     role["company_field"] = ""


        # Regular expression pattern for matching email addresses
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        # Find all email addresses in the text
        matches = re.findall(pattern, text)

        if matches:
            role["email"] = ','.join(matches)
        else:
            role["email"] = ""

        pattern = r'£(.+?)<'
        match = re.search(pattern, text)

        if match:
            role["salary"] = re.sub(r'[^£0-9- kK]', '', match.group())
        else:
            role["salary"] = ""

        pattern = r'(https://www.linkedin.com/jobs/view.+?)"'
        match = re.search(pattern, text)

        if match:
            role["link"] = match.group().replace('"', '')
        else:
            role["link"] = ""
        try:
            description = soup.find("div", {"class": "description__text description__text--rich"}).find("div").text.strip()
            role["description"] = description
            augmented_description = job_title + ", " + description + ", Salary: " + role["salary"]
            role["remote"] = (is_remote2(augmented_description))
            role["contract"] = (is_contract(augmented_description))
        except Exception as e:
            print(e)
            role["description"] = ""
            role["remote"] = ""
            role["contract"] = ""
        job_list.append(role)
        role = {}
    return job_list
