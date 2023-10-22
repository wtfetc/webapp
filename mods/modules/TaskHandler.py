from datetime import datetime, timedelta
from time import time, sleep
from random import randint
import json
import base64

# from web_app_4dk.tools import send_bitrix_request
from mods.tools import send_bitrix_request
from fast_bitrix24 import Bitrix
webhook = "https://vc1c.bitrix24.ru/rest/479/mjmdi5w3wvl9jo5g/"
b = Bitrix(webhook)
def fill_task_title(req, event):
    task_id = req['data[FIELDS_AFTER][ID]']
    print(task_id)
    #BitrixQ = 'Imh0dHBzOi8vdmMxYy5iaXRyaXgyNC5ydS9yZXN0LzQ3OS9tam1kaTV3M3d2bDlqbzVnLyIK'
    print("q1")
    #webhook = base64.b64decode(BitrixQ).decode('utf-8')
    #webhook = "https://vc1c.bitrix24.ru/rest/479/mjmdi5w3wvl9jo5g/"
    print("q2")
    #b = Bitrix(webhook)
    print("q3")
    task_info = b.get_all(
        'tasks.task.get', {
        'taskId': task_id,
        'select': ['*', 'UF_*']
    })
    print("ok")
    '''
    task_info = send_bitrix_request('tasks.task.get', {
        'taskId': task_id,
        'select': ['*', 'UF_*']
    })
    print("ok")
    '''
    if not task_info or 'task' not in task_info or not task_info['task']: # если задача удалена или в иных ситуациях
        print("0")
        return
    task_info = task_info['task']
   # task_registry(task_info, event)
    '''
    if task_info['closedDate'] and task_info['ufAuto934103382947'] != '1':
        send_notification(task_info, 'Завершение')
    '''

    if 'ufCrmTask' not in task_info or not task_info['ufCrmTask']: # ufCrmTask - связь с сущностью (список)
        print("00")
        return

    company_crm = list(filter(lambda x: 'CO' in x, task_info['ufCrmTask']))
    print(company_crm)
    print ("4")
    uf_crm_task = []
    if not company_crm:
       
     
        print("1")
        contact_crm = list(filter(lambda x: 'C_' in x, task_info['ufCrmTask']))
        if not contact_crm:
            return
        contact_crm = contact_crm[0][2:]
        print(contact_crm)
        contact_companies = list(map(lambda x: x['COMPANY_ID'], b.get_all('crm.contact.company.items.get', {'id': contact_crm})))
        if not contact_companies:
            print ("13")
            return
        
        '''
        contact_companies_info = send_bitrix_request('crm.company.list', {
           'select': ['UF_CRM_1660818061808'],     # Вес сделок
            'filter': {
                'ID': contact_companies,
            }
            
        })
        '''
        if contact_companies:
            print(contact_companies)
           # for i in range(len(contact_companies_info)):
           #     if not contact_companies_info[i]['UF_CRM_1660818061808']:
           #         contact_companies_info[i]['UF_CRM_1660818061808'] = 0
           # best_value_company = list(sorted(contact_companies_info, key=lambda x: float(x['UF_CRM_1660818061808'])))[-1]['ID'] #последний элемент в общем списке - с макс value
            best_value_company = contact_companies
            uf_crm_task = ['CO_' + best_value_company, 'C_' + contact_crm] # нельзя дописать, можно толлько перезаписать обоими значениями заново
            company_id = best_value_company #Это для тайтла
            print (uf_crm_task)
            print (company_id)
            
    else:
        print ("5")
        company_id = company_crm[0][3:]
        print (company_id)
 #   if event == 'ONTASKADD':
  #      check_similar_tasks_this_hour(task_info, company_id)


    print ("6")
    #company_info = send_bitrix_request('crm.company.get', {
    #    'ID': company_id,
    #})
    company_info = b.get_all(
        'crm.company.get',{
        'ID': company_id,
    })
    if company_info and company_info['TITLE'].strip() in task_info['title']: # strip() - очищает от пробелов по краям, если есть название компании в тайтле, то возрват
        print ("7")
        return

    if not uf_crm_task: #если не заполнено CRM - если в задаче уже есть company_id и нам не нужно ее заполнять
        print ("8")
        #send_bitrix_request('tasks.task.update', {
        #    'taskId': task_id,
        #    'fields': {
        #        'TITLE': f"{task_info['title']} {company_info['TITLE']}",
        #    }})
        b.call('tasks.task.update', {
            'taskId': task_id,
            'fields': {
                'TITLE': f"{task_info['title']} {company_info['TITLE']}",
            }})
    else:
        print ("9")
        b.call('tasks.task.update', {
            'taskId': task_id,
            'fields': {
                'TITLE': f"{task_info['title']} {company_info['TITLE']}",
                'UF_CRM_TASK': uf_crm_task,
            }})
        '''
        print ("9")
        send_bitrix_request('tasks.task.update', {
            'taskId': task_id,
            'fields': {
                'TITLE': f"{task_info['title']} {company_info['TITLE']}",
                'UF_CRM_TASK': uf_crm_task,
            }})
        '''
    return task_info


def task_handler(req, event=None):
    try:
        task_info = fill_task_title(req, event)
        print ("10")
    except:
        return
    '''
    send_notification(task_info, 'Создание')
    '''
