from email import message
from .models import * 
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

import docx2txt
from nltk.tokenize import sent_tokenize

import re

print("laod FU_classifier ...")
from .NFR_FUR.FU_classifier import classify
print("laod AMBIGUITY_DETECTOR ...")
from .AMBIGUITY_DETECTOR.prc import ambiguity_checker
print("laod DATA_MOUVEMENTS_EXTRACTOR ...")
from .DATA_MOUVEMENTS_EXTRACTOR.prc import data_mouvements_extract                                  


 


def check_authentication(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
       return user
    else:
        return None
    
def insert_COSMIC_DATABASE(uploaded_platform_file_url,srs_file):
    
    print("load file (data_measurement) csv ...")

    df_platform = pd.read_excel(uploaded_platform_file_url, sheet_name="Sheet1")

    #df_api = pd.read_excel(uploaded_api_file_url, sheet_name="Feuil1")
    
    print("INSERT INTO COSMIC_measurement(PATH_FILE_UR) ...")
    
    cosmic_measurement = COSMIC_measurement(PATH_FILE_UR_IN_SERVER=srs_file,PATH_FILE_UR=str(df_platform['Tracabilité'].loc[0]).split("-")[0])
    cosmic_measurement.save()
    
    try:
        o_i = object_of_interest.objects.get(name="null")
    except ObjectDoesNotExist:
        
        print("INSERT INTO object_of_interest(name) ...")
        o_i = object_of_interest(name="null")
        o_i.save()
        pass
        
        
    try :
    
        d_g = data_group.objects.get(name="null")
        
    except ObjectDoesNotExist:
        print("INSERT INTO data_group(ID_object_of_interest,name,attributes) ...")
        d_g = data_group(
            object_of_interest = object_of_interest.objects.get(name="null"),
            name = "null",
            attributes="null"
        )
        d_g.save()
    
    for row in range(len(df_platform)):
        try:
            print("INSERT INTO functional_user_requirement(id_measurement, description, source) ...")
            f_u_r = functional_user_requirement(
                cosmic_measurement=cosmic_measurement,
                description=str(df_platform['Description'].loc[row]).replace("'","’"),
                source=df_platform['Tracabilité'].loc[row]
            )

            f_u_r.save()

            print("INSERT INTO functional_process(ID, name) ...")        
            
            f_p = functional_process(
                functional_user_requirement= f_u_r,
                description=str(df_platform['Description'].loc[row]).replace("'","’")
            )
            
            f_p.save()
            
            print("INSERT INTO data_movement(ID_data_group, ID_functional_process, type, number) ...")
            data_movement(
                data_group = d_g,
                functional_process = f_p,
                type = "Entry",
                number = str(df_platform['Entrée'].loc[row])
            ).save()
            
            data_movement(
                data_group = d_g,
                functional_process = f_p,
                type = "Exit",
                number = str(df_platform['Sortie'].loc[row])
            ).save()
            
            data_movement(
                data_group = d_g,
                functional_process = f_p,
                type = "Read",
                number = str(df_platform['Lecture'].loc[row])
            ).save()
            
            data_movement(
                data_group = d_g,
                functional_process = f_p,
                type = "Write",
                number = str(df_platform['Ecriture'].loc[row])
            ).save()
            
            message =  "The data was recorded correctly"
        
        except KeyError:
            return "File format error"
        
    return message
            
            
        
        
    
    

def download_data_COSMIC_measurement():
    c_m = COSMIC_measurement.objects.all()

    data_COSMIC_measurement = {
        "PATH_FILE_UR" : [],
        "level_of_granularity" : [],
        "level_of_decomposition" : [],
        "scope" : [],
        "measurement_purpose" : []
    }
    
    for instance in c_m:
        data_COSMIC_measurement["PATH_FILE_UR"].append(instance.PATH_FILE_UR)
        data_COSMIC_measurement["level_of_granularity"].append(instance.level_of_granularity)
        data_COSMIC_measurement["level_of_decomposition"].append(instance.level_of_decomposition)
        data_COSMIC_measurement["scope"].append(instance.scope)
        data_COSMIC_measurement["measurement_purpose"].append(instance.measurement_purpose)
        
    pd.DataFrame(data_COSMIC_measurement).to_csv('data_COSMIC_measurement.csv')    
    return  'data_COSMIC_measurement.csv'
def download_data_functional_user():
    
    f_u = functional_user.objects.all()
    
    
    
    data_functional_user = {
        "functional_user_name" : [],
        "functional_user_type" : [],   
    }
    
    for instance in f_u:
        data_functional_user["functional_user_name"].append(instance.name)
        data_functional_user["functional_user_type"].append(instance.type)

    pd.DataFrame(data_functional_user).to_csv('data_functional_user.csv')

    return "data_functional_user.csv"

def download_data_non_functional_requirement():
    
    n_f_r = non_functional_requirement.objects.all()

    
    
    data_non_functional_requirement = {
        "non_functional_requirement_description" : [],
        "non_functional_requirement_source" : [],
        
    }


    
    for instance in n_f_r:      
        data_non_functional_requirement["ambiguous_requirement_description"].append(instance.description)
        data_non_functional_requirement["ambiguous_requirement_source"].append(instance.source)
        
    pd.DataFrame(data_non_functional_requirement).to_csv('data_non_functional_requirement.csv')
    return "data_non_functional_requirement.csv"
    
def download_data_ambiguous_requirement():
    a_r = ambiguous_requirement.objects.all()
    data_ambiguous_requirement = {
        "ambiguous_requirement_description" : [],
        "ambiguous_requirement_source" : [],
    }
        
    for instance in a_r:
        data_ambiguous_requirement["ambiguous_requirement_description"].append(instance.description)
        data_ambiguous_requirement["ambiguous_requirement_source"].append(instance.source)

    pd.DataFrame(data_ambiguous_requirement).to_csv('data_ambiguous_requirement.csv')

    return "data_ambiguous_requirement.csv"

    
def download_data_movements():
    d_m = data_movement.objects.all()    
    data_movements = {
        "functional_user_requirement" : [],
        "functional_user_requirement_source" : [],
        "triggering_event" : [],
        "functional_process" : [],
        "object_of_interest" : [],
        "data_group_name" : [],
        "data_group_attributes" : [],
        "data_movement_type" : [],
        "sub_process_description": [],
        "data_movement_number" : []
    }
    
    for instance in d_m:
        data_movements["functional_user_requirement"].append(instance.functional_process.functional_user_requirement.description)
        data_movements["functional_user_requirement_source"].append(instance.functional_process.functional_user_requirement.source)
        data_movements["triggering_event"].append(instance.functional_process.triggering_event)
        data_movements["functional_process"].append(instance.functional_process.description)
        data_movements["object_of_interest"].append(instance.data_group.object_of_interest.name)
        data_movements["data_group_name"].append(instance.data_group.name)
        data_movements["data_group_attributes"].append(instance.data_group.attributes)
        data_movements["data_movement_type"].append(instance.type)
        data_movements["sub_process_description"].append(instance.sub_process_description)
        data_movements["data_movement_number"].append(instance.number)
    
    pd.DataFrame(data_movements).to_csv('data_movements.csv')
    
    return 'data_movements.csv'


import os
def delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)
       
       
def pipline_COSMIC_measurement(path_file):
    
    print("path : ", path_file)
    print("load file ...")
    # read in word file
    document = docx2txt.process(path_file)
    
    paragraphs = document.split("\n\n\n")
    print("paragraphs : ", paragraphs)
    data = {
        "len_ambiguous" : 0,
        "len_unambiguous" : 0,
        "len_nfr" : 0, 
        "len_fur" : 0,
        "len_data_mouvements" : 0,
        "fps" : []
    }
         
    i=0
    for paragraph in paragraphs:
        i+=1
        temp = {
            "content" : paragraph
        }
        
        list_of_sents = sent_tokenize(paragraph)
    
        #capt aumbiguity
        print("capt aumbiguity ...")
        ambiguous = []
        unambiguous = []
        for sent in list_of_sents:
            result = ambiguity_checker(sent)
            if result["decision"] == 'ambiguous':
                ambiguous.append((sent,result))
                data["len_ambiguous"] +=1
            else:
                unambiguous.append((sent,result))
                data["len_unambiguous"] +=1

        
        temp["ambiguous"] = ambiguous
        temp["unambiguous"] = unambiguous


        # capt non functional requirements
        print("capt non functional requirements ...")
        fur = []
        nfr = []
        
        
        # for sent,_ in unambiguous:
        #     result = classify(sent)
        #     if result == 'nf':
        #         nfr.append(sent)
        #         data["len_nfr"] += 1
        #     else:
        #         fur.append(sent)
        #         data["len_fur"] += 1
                
        # temp["nfr"] = nfr
        # temp["fur"] = fur

            
        # capt data mouvements
        print("capt data mouvements...")
        data_mouvements = []
        for sent,_ in unambiguous:
            result = data_mouvements_extract(sent)
            data_mouvements.append(result)    
            data["len_data_mouvements"] += 1 

        temp["data_mouvements"] = data_mouvements
        
        
        data["fps"].append(temp)
        
    return data
