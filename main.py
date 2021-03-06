import requests
import statistics
import os
from terminaltables import AsciiTable, DoubleTable, SingleTable


def main():

  title = 'HeadHunter Moscow'

  table_data = (
    ('Development languages', 'Amount vacancies', 'Average salary'),
    ('python', get_amount_vacancies_for_hh('Программист python') ,predict_rub_salary_for_hh('Программист python')),
    ('Java', get_amount_vacancies_for_hh('Программист Java') ,predict_rub_salary_for_hh('Программист Java')),
    ('PHP', get_amount_vacancies_for_hh('Программист PHP') ,predict_rub_salary_for_hh('Программист PHP')),
    ('C#', get_amount_vacancies_for_hh('Программист C#') ,predict_rub_salary_for_hh('Программист C#')),
    ('Java script', get_amount_vacancies_for_hh('Программист Java script') ,predict_rub_salary_for_hh('Программист Java script')),
  )

  display_table(table_data,title)

  title = 'SuperJob Moscow'

  table_data = (
    ('Development languages', 'Amount vacancies', 'Average salary'),
    ('python', get_amount_vacancies_for_sj('Программист python') ,predict_rub_salary_for_sj('Программист python')),
    ('Java', get_amount_vacancies_for_sj('Программист Java') ,predict_rub_salary_for_sj('Программист Java')),
    ('PHP', get_amount_vacancies_for_sj('Программист PHP') ,predict_rub_salary_for_sj('Программист PHP')),
    ('C#', get_amount_vacancies_for_sj('Программист C#') ,predict_rub_salary_for_sj('Программист C#')),
    ('Java script', get_amount_vacancies_for_sj('Программист Java script') ,predict_rub_salary_for_sj('Программист Java script')),
  )

  display_table(table_data,title)


def display_table(table_data,title):
  table_instance = DoubleTable(table_data, title)
  table_instance.justify_columns[2] = 'right'
  print(table_instance.table)
  print()


def predict_salary(salary_from, salary_to):
  if not salary_from: 
    return salary_to * 0.8
  if not salary_to:
    return salary_from * 1.2
  average_salary = statistics.mean([salary_from,salary_to])
  return average_salary

def get_amount_vacancies_for_sj(vacancy):
  token = os.getenv("SecretKey")
  headers = {
    'X-Api-App-Id': token
  }
  params = {
    'not_archive' : '1',
    't': '4',
    'catalogues': '48',
    'no_agreement': '1',
    'keyword': vacancy
  }
  base_url = 'https://api.superjob.ru/2.0/vacancies/'
  response = requests.get(base_url, headers=headers, params=params)
  return response.json()['total']

def predict_rub_salary_for_sj(vacancy_name):
  page = 0
  pages = 1
  salary_list = []
  total_salary = 0
  while page < pages:
    token = os.getenv("SecretKey")
    headers = {
      'X-Api-App-Id': token
    }
    params = {
      'not_archive' : '1',
      't': SJ_MOSCOW,
      'catalogues': SJ_IT_CATALOG,
      'no_agreement': '1',
      'keyword': vacancy_name
    }
    base_url = 'https://api.superjob.ru/2.0/vacancies/'
    response = requests.get(base_url, headers=headers, params=params)

    for vacancy in response.json()['objects']: 
      average_salary = predict_salary(vacancy['payment_from'],vacancy['payment_to']) 
      salary_list.append(average_salary)
      total_salary += average_salary
      
  return total_salary/len(salary_list)

def predict_rub_salary_for_hh(vacancy_name):
  page = 0
  pages = 1
  salary_list = []
  total_salary = 0
  while page < pages:
    headers = {
        'User-Agent': 'SearchingJob/1.0 (m.vadimpopov@gmail.com)'
    }   
    params = {
      'text' : vacancy_name,
      'area' : HH_MOSCOW,
      'period' : '30',
      'page' : page,
      'only_with_salary' : 'true',
      'per_page': '100',
      'no_magic': True,
      'premium' : False
    }
    base_url = 'https://api.hh.ru/vacancies'
    response = requests.get(base_url, headers=headers, params=params).json()
    pages = response['pages']

    for vacancy in response['items']: 
      salary = vacancy['salary']
      average_salary = predict_salary(salary['from'],salary['to']) 
      salary_list.append(average_salary)
      total_salary += average_salary
    
  return total_salary/len(salary_list)
    

def get_amount_vacancies_for_hh(vacancy):
  headers = {
    'User-Agent': 'SearchingJob/1.0 (m.vadimpopov@gmail.com)'
  }
  params = {
    'text' : vacancy,
    'area' : HH_MOSCOW,
    'period' : '30',
    'only_with_salary' : 'true',
    'per_page': '1'
  }
  base_url = 'https://api.hh.ru/vacancies'
  response = requests.get(base_url, headers=headers, params=params)
  amount_vacancies = response.json()['found']
  return amount_vacancies


if __name__ == '__main__':
 HH_MOSCOW = '1'
 SJ_IT_CATALOG = '48'
 SJ_MOSCOW = '4'
 main()
