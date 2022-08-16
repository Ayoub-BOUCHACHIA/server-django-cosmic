import pickle
from unittest import result
from nltk.tokenize import word_tokenize



def classify(document):
            
    def get_features(document,word_features):
        try:
            words = set(word_tokenize(document))
            words = [word_lower.lower() for word_lower in words]
                
            features = {}
            for word in word_features:
                features[word] = word in words
        except Exception:
            print("document : ",document)
            raise Exception
        
        return features
        

    word_features = pickle.load(open("media\^ML_model\^word_features.pickle".replace("^",""), 'rb'))    
    loaded_model = pickle.load(open("media\^ML_model\^NSVC_classifier.pickle".replace("^",""), 'rb'))
    
    result =  loaded_model.classify(get_features(document,word_features))
    print(result)
    return result

