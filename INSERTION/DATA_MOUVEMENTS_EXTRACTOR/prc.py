import spacy
from nltk import stem


def merge_chunk(dict,key):
  new_dict = {}
  keys = list(dict.keys())
  if len(keys)>1:
    for id_1 in range(len(keys)):
      for id_2 in range(id_1,len(keys)):
        if keys[id_1] != keys[id_2]:
          if dict[keys[id_1]][key] == dict[keys[id_2]][key]:
            temp_dict = {}
            for key_k in dict[keys[id_1]]:
              temp_dict[key_k] = dict[keys[id_1]][key_k]
            for key_k in dict[keys[id_2]]:
              temp_dict[key_k] = dict[keys[id_2]][key_k]
            new_dict[keys[id_1]+"_"+keys[id_2]] = temp_dict
    return new_dict
  else: 
    return dict


def data_mouvements_extract(text):
  
  nlp = spacy.load('en_core_web_sm')

  with open("media\^dictionary_of_words\^Entry_Verbs.data".replace("^",""),"r") as f:
    Entry_Verbs = f.read().split(";")
  with open("media\^dictionary_of_words\^Exit_Verbs.data".replace("^",""),"r") as f:
    Exit_Verbs =  f.read().split(";")
  with open("media\^dictionary_of_words\^Read_Verbs.data".replace("^",""),"r") as f:
    Read_Verbs = f.read().split(";")
  with open("media\^dictionary_of_words\^Write_Verbs.data".replace("^",""),"r") as f:
    Write_Verbs =  f.read().split(";")
  with open("media\^dictionary_of_words\^Triggering_Entry_Verbs.data".replace("^",""),"r") as f:
    Triggering_Entry_Verbs = f.read().split(";")
  with open("media\^dictionary_of_words\^System_Message_Exit_Verbs.data".replace("^",""),"r") as f:
    System_Message_Exit_Verbs =  f.read().split(";")
  with open("media\^dictionary_of_words\^Attribute_Names.data".replace("^",""),"r") as f:
    Attribute_Names = f.read().split(";")
  with open("media\^dictionary_of_words\^Data_group_Names.data".replace("^",""),"r") as f:
    Data_group_Names= f.read().split(";")
  with open("media\^dictionary_of_words\^Actor_Names.data".replace("^",""),"r") as f:
    Actor_Names= f.read().split(";")

  doc = nlp(text)
  data_ext = {}
  
  stemmer = stem.PorterStemmer()
  for chunk in doc.noun_chunks:
      print(chunk.text, chunk.root.text, chunk.root.dep_,chunk.root.head.text)
      if chunk.root.dep_ == "nsubj" and chunk.root.head.pos_=="VERB":
        data_ext["subject_"+chunk.root.text] = {
            'subject' : chunk.text,
            'verb' : chunk.root.head.text,
        }
      elif (chunk.root.dep_ == "dobj" or chunk.root.dep_ == "pobj")  and chunk.root.head.pos_=="VERB":
        data_ext["object_"+chunk.root.text] = {
            'object' : chunk.text,
            'verb' : chunk.root.head.text,
        }

  data_ext = merge_chunk(data_ext,"verb")

  for key in data_ext:  
        
      if stemmer.stem(str(data_ext[key]["verb"]).lower()) in Entry_Verbs : 
        data_ext[key]["type_dm"] = "Entry data mouvement"
      if stemmer.stem(str(data_ext[key]["verb"]).lower()) in Exit_Verbs : 
        data_ext[key]["type_dm"] = "Exit data mouvement"
      if stemmer.stem(str(data_ext[key]["verb"]).lower()) in Read_Verbs : 
        data_ext[key]["type_dm"] = "Read data mouvement"
      if stemmer.stem(str(data_ext[key]["verb"]).lower()) in Write_Verbs : 
        data_ext[key]["type_dm"] = "Write data mouvement"


  return data_ext



