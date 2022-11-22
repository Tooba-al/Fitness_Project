import imp
import random
# from sms.models import Operator, Message
from django.utils.translation import gettext as _
import pandas as pd
import numpy as np
import codecs as cs
import json
# from . import auto_functions
import string

def generate_code():
    return str(random.randint(1000, 9999))

def get_verification_text(code):
    return _("به umind خوش آمدید: %s" % code)

# def send_verification_code(to, code):
#     #print("to:", to)
#     message = Message.objects.create(to=to, message=get_verification_text(code))
#     if(Operator.objects.exists()):
#         Operator.objects.first().send_message(message)
#     else:
#         #print('No operator defined')
#         pass

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def make_json(xlsxFilePath, fileJsonPath):
    
    data_read = pd.read_excel(xlsxFilePath)
    data = {
        'Test': []
        }

    
    for i in data_read.index:
        s_data = {
            
            'Num': int(np.int64(data_read['Num'][i])), 
            'Question': data_read['Question'][i], 
            'Type':data_read['Type'][i], 
            'Answers': ''
            
            }
        

        list_of_answers = []
        for column in data_read.columns[3:]:
            data_in_column = data_read[column][i]
            if(not pd.isnull(data_in_column) and represents_int(data_in_column) == True):
                data_in_column = int(np.int64(data_in_column))
                list_of_answers.append(data_in_column)
                
            elif (not pd.isnull(data_in_column)):
                list_of_answers.append(data_in_column)
                

        s_data['Answers'] = list_of_answers
        data['Test'].append(s_data)
        
        with cs.open(fileJsonPath, "w", "utf-8") as outfile:
            outfile.write(json.dumps(data, ensure_ascii=False))

# def do_auto_function(test_name, answers):

#     function = getattr(auto_functions, test_name)
#     return function(answers)

def generate_16char_link():
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return x
