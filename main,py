import requests
import statistics
import os
from terminaltables import AsciiTable, DoubleTable, SingleTable


def main():

  title = 'HeadHunter Moscow'

  TABLE_DATA = (
    ('Development languages', 'Amount vacancies', 'Average salary'),
    ('python', get_amount_vacancies_for_hh('Программист python') ,predict_rub_salary_for_hh('Программист python')),
    ('Java', get_amount_vacancies_for_hh('Программист Java') ,predict_rub_salary_for_hh('Программист Java')),
    ('PHP', get_amount_vacancies_for_hh('Программист PHP') ,predict_rub_salary_for_hh('Программист PHP')),
    ('C#', get_amount_vacancies_for_hh('Программист C#') ,predict_rub_salary_for_hh('Программист C#')),
    ('Java script', get_amount_vacancies_for_hh('Программист Java script') ,predict_rub_salary_for_hh('Программист Java script')),
  )

  display_table(TABLE_DATA,title)

  title = 'SuperJob Moscow'

  TABLE_DATA = (
    ('Development languages', 'Amount vacancies', 'Average salary'),
    ('python', get_amount_vacancies_for_sj('Программист python') ,predict_rub_salary_for_sj('Программист python')),
    ('Java', get_amount_vacancies_for_sj('Программист Java') ,predict_rub_salary_for_sj('Программист Java')),
    ('PHP', get_amount_vacancies_for_sj('Программист PHP') ,predict_rub_salary_for_sj('Программист PHP')),
    ('C#', get_amount_vacancies_for_sj('Программист C#') ,predict_rub_salary_for_sj('Программист C#')),
    ('Java script', get_amount_vacancies_for_sj('Программист Java script') ,predict_rub_salary_for_sj('Программист Java script')),
  )

  display_table(TABLE_DATA,title)
  


def display_table(TABLE_DATA,title):
  table_instance = DoubleTable(TABLE_DATA, title)
  table_instance.justify_columns[2] = 'right'
  print(table_instance.table)
  print()


def get_predict_salary(salary_from, salary_to):
  return statistics.mean([salary_from,salary_to])

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
  return(response.json()['total'])

def predict_rub_salary_for_sj(vacancy):
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

  salaryList = []
  for vacancy in response.json()['objects']:
    if vacancy['payment_from'] == 0: 
      averageSalary = vacancy['payment_to'] * 0.8
      salaryList.append(averageSalary)
      continue
    if vacancy['payment_to'] == 0:
      averageSalary = vacancy['payment_from'] * 1.2
      salaryList.append(averageSalary)
      continue
    averageSalary = get_predict_salary(vacancy['payment_from'],vacancy['payment_to']) 

  if len(salaryList) == 0:
    return 0
  sortedSalary = sorted(salaryList)
  minSalary = salaryList[0]
  maxSalary = salaryList[-1]
  totalAverageSalary = get_predict_salary(minSalary,maxSalary)
  return totalAverageSalary

def predict_rub_salary_for_hh(vacancy):
  headers = {
      'User-Agent': 'SearchingJob/1.0 (m.vadimpopov@gmail.com)'
  }
  params = {
    'text' : vacancy,
    'area' : '1',
    'period' : '30',
    'page' : '1',
    'only_with_salary' : 'true',
    'per_page': '100'
  }
  base_url = 'https://api.hh.ru/vacancies'
  response = requests.get(base_url, headers=headers, params=params)
  salaryList = []
  for vacancy in response.json()['items']:
    salary = vacancy['salary']
    if salary['from'] is None: 
      averageSalary = salary['to'] * 0.8
      salaryList.append(averageSalary)
      continue
    if salary['to'] is None:
      averageSalary = salary['from'] * 1.2
      salaryList.append(averageSalary)
      continue
    averageSalary = statistics.mean([salary['from'],salary['to']])
    salaryList.append(averageSalary)

  if len(salaryList) == 0:
    return 0
    
  sortedSalary = sorted(salaryList)
  minSalary = salaryList[0]
  maxSalary = salaryList[-1]
  totalAverageSalary = get_predict_salary(minSalary,maxSalary)
  return totalAverageSalary
    

def get_amount_vacancies_for_hh(vacancy):
  headers = {
    'User-Agent': 'SearchingJob/1.0 (m.vadimpopov@gmail.com)'
  }
  params = {
    'text' : vacancy,
    'area' : '1',
    'period' : '30',
    'only_with_salary' : 'true',
    'per_page': '1'
  }
  base_url = 'https://api.hh.ru/vacancies'
  response = requests.get(base_url, headers=headers, params=params)
  amountVacancies = response.json()['found']
  return amountVacancies


if __name__ == '__main__':
 main()
