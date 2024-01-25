from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def get_jobs(keyword, num_jobs, path):
    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')
    print(path)
    service = Service(executable_path=path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)

    base_url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="
    driver.get(base_url)
    jobs = []

    # Scroll down to load more job listings
    for i in range(3):  # You can adjust the number of times to scroll based on your needs
        driver.find_element(By.XPATH, '//body').send_keys(Keys.END)
        time.sleep(2)  # Adjust the sleep time based on your internet speed

    # Extract job listings
    job_buttons = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__JBBUV")
    for job_button in job_buttons:
        # Extracted data to be added to the dataframe
        job_data = {
            "Job Title": job_button.find_element(By.CLASS_NAME, "jobLink").text,
            "Company Name": job_button.find_element(By.CLASS_NAME, "jobEmpolyerName").text,
            "Location": job_button.find_element(By.CLASS_NAME, "loc").text,
            "Salary Estimate": job_button.find_element(By.CLASS_NAME, "salaryEstimate").text,
            "Job Description": job_button.find_element(By.CLASS_NAME, "jobDescriptionContent").text
        }

        # Add the job data to the list
        jobs.append(job_data)

    # Create a dataframe from the list of jobs
    df = pd.DataFrame(jobs)

    # Optional: You can print the number of jobs found
    print("Number of jobs found:", len(job_buttons))

    # Optional: Print the dataframe
    print("DataFrame Shape:", df.shape)
    print(df)

    # Close the webdriver
    driver.quit()