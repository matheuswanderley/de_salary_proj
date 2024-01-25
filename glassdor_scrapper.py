from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver with service
    service = ChromeService(executable_path=path)
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + \
        keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    driver.get(url)
    jobs = []
    modal_appeared = False  # Flag to track if the modal has appeared

    # If true, should still be looking for new jobs.
    while len(jobs) < num_jobs:

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        # Going through each job on this page
        # jl for Job Listing. These are the buttons we're going to click.
        job_buttons = driver.find_elements(
            By.XPATH, '//li[@data-test="jobListing"]')
        for job_button in job_buttons:
            print("Progress: {}".format(
                "" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            # Click the job button
            ActionChains(driver).move_to_element(job_button).click().perform()

            # Aguarde até que o modal apareça (se ainda não apareceu)
            if not modal_appeared:
                try:
                    modal_overlay = WebDriverWait(driver, 0.5).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, '.ModalOverlay'))
                    )
                    print("Modal appeared")
                    modal_appeared = True
                except TimeoutException:
                    print("Modal did not appear within 0.5 seconds")

            # Aguarde até que o modal desapareça
            try:
                WebDriverWait(driver, 0.5).until_not(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, '.ModalOverlay'))
                )
                print("Modal disappeared")
            except TimeoutException:
                print("Modal did not disappear within 0.5 seconds")

            # Agora que o modal desapareceu, você pode clicar no botão de fechar (X)
            try:
                close_button = WebDriverWait(driver, 0.5).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'button.CloseButton'))
                )
                close_button.click()
                print("Close button clicked successfully")
            except TimeoutException:
                print("Close button not clickable within 0.5 seconds")
            except Exception as e:
                print("Error while clicking close button:", str(e))

            # Aguarde no máximo 1 segundo antes de clicar no próximo botão
            time.sleep(1)

            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element(
                        By.XPATH, './/span[@class="EmployerProfile_employerName__Xemli"]').text
                    location = driver.find_element(
                        By.XPATH, './/div[@data-test="emp-location"]').text
                    job_title = driver.find_element(
                        By.XPATH, './/a[@class="JobCard_seoLink__WdqHZ"]').text
                    job_description = driver.find_element(
                        By.XPATH, './/div[@data-test="descSnippet"]').text
                    collected_successfully = True
                except:
                    time.sleep(100)

            try:
                salary_estimate = driver.find_element(
                    By.XPATH, './/div[@data-test="detailSalary"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                rating = driver.find_element(
                    By.XPATH, './/div[@class="EmployerProfile_ratingContainer__N4hxE"]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))
                print("Modal appeared")

            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element(
                    By.XPATH, './/div[@class="tab" and @data-tab-type="overview"]').click()

                try:
                    # <div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    # </div>
                    headquarters = driver.find_element(
                        By.XPATH, './/div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = driver.find_element(
                        By.XPATH, './/div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(
                        By.XPATH, './/div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element(
                        By.XPATH, './/div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element(
                        By.XPATH, './/div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(
                        By.XPATH, './/div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(
                        By.XPATH, './/div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element(
                        By.XPATH, './/div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            # Rarely, some job postings do not have the "Company" tab.
            except NoSuchElementException:
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Headquarters": headquarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "Competitors": competitors})
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH, './/li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching the target number of jobs. Needed {}, got {}.".format(
                num_jobs, len(jobs)))
            break

    # Fora do loop while e após coletar todas as informações
    df = pd.DataFrame(jobs)

    # Salve o DataFrame como um arquivo CSV
    df.to_csv('glassdoor_jobs.csv', index=False)

    # Feche o driver após concluir a extração
    driver.quit()
