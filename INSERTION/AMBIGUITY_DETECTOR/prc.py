from nltk.tokenize import word_tokenize
from nltk import stem
stemmer = stem.PorterStemmer()
from textblob import TextBlob
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import spacy


def ambiguity_checker(text):

  nlp = spacy.load('en_core_web_sm')

  with open("media\^dictionary_of_words\^dictionary_of_words_v2\^optionality.data".replace("^",""),"r") as f:
    all_optionality_words = f.read().split(";")
  with open("media\^dictionary_of_words\^dictionary_of_words_v2\^weakness.data".replace("^",""),"r") as f:
    all_weakness_words = f.read().split(";")
  with open("media\^dictionary_of_words\^dictionary_of_words_v2\^vagueness.data".replace("^",""),"r") as f:
    all_vagueness_words = f.read().split(";")

  doc = nlp(text)

  cpt_optionality = 0
  cpt_weakness = 0
  cpt_vagueness = 0
  
  verbs = [token for token in doc if token.pos_ == 'VERB']
  subjects = [token for token in doc if token.dep_ == 'nsubj']
  implicity = [token for token in doc if token.dep_ == 'nsubj' and (token.pos_ == 'PRON' or token.pos_ == "DET")]
  
  objects = [token for token in doc if token.dep_ == 'pobj']
  cpt_multi_vrb = len(verbs)
  cpt_multi_subj = len(subjects)
  cpt_implicity = len(implicity)

  words_optionality = []
  words_weakness = []
  words_vagueness = []
  
  for word in word_tokenize(text):
    if stemmer.stem(word.lower()) in all_optionality_words: 
      cpt_optionality +=1    
      words_optionality.append(word)

    if stemmer.stem(word.lower()) in all_weakness_words: 
      cpt_weakness +=1    
      words_weakness.append(word)

    if stemmer.stem(word.lower()) in all_vagueness_words: 
      cpt_vagueness +=1
      words_vagueness.append(word)

  p_optionality = cpt_optionality > 0
  p_weakness = cpt_weakness > 0
  p_vagueness = cpt_vagueness > 0
  p_subjectivity = TextBlob(text).sentiment[1] > 0.5 
  p_multi_vrb =  cpt_multi_vrb > 1
  p_multi_subj = cpt_multi_subj > 1
  p_implicity = cpt_implicity > 1

  amb_list = [instance for instance in [p_optionality,p_weakness,p_vagueness,p_subjectivity,p_multi_vrb,p_multi_subj,p_implicity] if instance==True]
  score = len(amb_list) / 7.0

  if score> 0.4 :
      decision = 'ambiguous'
  else:
    decision = "unambiguous"
    
    
  return  {
      "score" : score,  
      "decision" : decision,
      "prameters" : {
          "p_optionality" : p_optionality,
          "p_weakness" :p_weakness,
          "p_vagueness" : p_vagueness,
          "p_subjectivity": p_subjectivity,
          "p_multi_vrb" : p_multi_vrb,
          "p_multi_subj" : p_multi_subj,
          "p_implicity" : p_implicity
      },
      "content" : {
          "words_optionality" : words_optionality,
          "words_weakness" :words_weakness,
          "words_vagueness" : words_vagueness,
          "verbs" : verbs ,
          "subjects" : subjects,
          "objects" : objects,
          "implicity" : implicity
      }
  }