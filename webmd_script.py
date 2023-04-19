import os
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup

first_ = 'https://www.webmd.com/a-to-z-guides/health-topics'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

response = requests.get(first_, headers=headers)


if response.status_code == 200:
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    az_index_nav_letters = soup.find(class_='az-index-nav-letters')
    if az_index_nav_letters:
        li_elements = az_index_nav_letters.find_all('li')
        for li in li_elements:
            link = li.find('a')
            if link:
                href = link['href']
                response2 = requests.get(
                    'https://www.webmd.com/a-to-z-guides/health-topics' + str(href), headers=headers)
                content2 = response2.text
                soup2 = BeautifulSoup(content2, 'html.parser')
                az_index_results_group_list = soup2.find(
                    class_='az-index-results-group-list')
                if az_index_results_group_list:
                    list_items = az_index_results_group_list.find_all('li')

                    for li2 in list_items:

                        # title content title
                        link2 = li2.find('a')

                        if link2:
                            print(link2.text, link2['href'])
                            namefile = link2.text.replace('/', '_')
                            topic_url = link2['href']
                            response3 = requests.get(
                                topic_url, headers=headers)
                            content3 = response3.text
                            soup3 = BeautifulSoup(content3, 'html.parser')
                            symptom_start = soup3.find(
                                lambda tag: tag.name == 'h2' and 'Symptoms' in tag.text)
                            diagnosis_start = soup3.find(
                                lambda tag: tag.name == 'h2' and 'Diagnosis' in tag.text)
                            treatment_and_prevention_start = soup3.find(
                                lambda tag: tag.name == 'h2' and 'Treatment' in tag.text)
                            cause_start = soup3.find(
                                lambda tag: tag.name == 'h2' and 'Cause' in tag.text)

                            if symptom_start:
                                symptom_start_index = content3.find(
                                    str(symptom_start))
                                h2_start = content3.find(
                                    '<h2 ', symptom_start_index + len(str(symptom_start)))
                                if h2_start != -1:
                                    html_between_strings = content3[symptom_start_index:h2_start]
                                    soup_between_strings = BeautifulSoup(
                                        html_between_strings, 'html.parser')
                                    symptom_start.extract()
                                    text_between_strings = soup_between_strings.get_text(
                                        separator=' ', strip=True)
                                    with open(os.path.join('H:\Programming\webmd\website/text/symptom', f'{namefile}_symptoms.text'), 'w') as file:
                                        file.write(
                                            unidecode(text_between_strings))

                            if diagnosis_start:
                                diagnosis_start_index = content3.find(
                                    str(diagnosis_start))
                                h2_start = content3.find(
                                    '<h2 ', diagnosis_start_index + len(str(diagnosis_start)))
                                if h2_start != -1:
                                    html_between_strings = content3[diagnosis_start_index:h2_start]
                                    soup_between_strings = BeautifulSoup(
                                        html_between_strings, 'html.parser')
                                    diagnosis_start.extract()
                                    text_between_strings = soup_between_strings.get_text(
                                        separator=' ', strip=True)
                                    with open(os.path.join('H:\Programming\webmd\website/text/diagnosis', f'{namefile}_diagnosis.text'), 'w') as file:
                                        file.write(
                                            unidecode(text_between_strings))

                            if treatment_and_prevention_start:
                                treatment_and_prevention_start_index = content3.find(
                                    str(treatment_and_prevention_start))
                                h2_start = content3.find(
                                    '</section', treatment_and_prevention_start_index + len(str(treatment_and_prevention_start)))
                                if h2_start != -1:
                                    html_between_strings = content3[treatment_and_prevention_start_index:h2_start]
                                    soup_between_strings = BeautifulSoup(
                                        html_between_strings, 'html.parser')
                                    treatment_and_prevention_start.extract()
                                    text_between_strings = soup_between_strings.get_text(
                                        separator=' ', strip=True)
                                    with open(os.path.join('H:\Programming\webmd\website/text/treatment', f'{namefile}_treatment.text'), 'w') as file:
                                        file.write(
                                            unidecode(text_between_strings))

                            if cause_start:
                                cause_start_index = content3.find(
                                    str(cause_start))
                                h2_start = content3.find(
                                    '</section', cause_start_index + len(str(cause_start)))
                                if h2_start != -1:
                                    html_between_strings = content3[cause_start_index:h2_start]
                                    soup_between_strings = BeautifulSoup(
                                        html_between_strings, 'html.parser')
                                    cause_start.extract()
                                    text_between_strings = soup_between_strings.get_text(
                                        separator=' ', strip=True)
                                    with open(os.path.join('H:\Programming\webmd\website/text/cause', f'{namefile}_cause.text'), 'w') as file:
                                        file.write(
                                            unidecode(text_between_strings))
else:
    print(f'Failed to fetch the content. Status code: {response.status_code}')
