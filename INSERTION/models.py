from django.db import models

# Create your models here.
from django.db import models
import pandas as pd
from pkg_resources import require

class COSMIC_measurement(models.Model):
    PATH_FILE_UR_IN_SERVER = models.FileField(upload_to='media',blank=True, null=True, default=None)
    PATH_FILE_UR = models.CharField(max_length=400)
    level_of_granularity = models.IntegerField(default=3)
    level_of_decomposition = models.IntegerField(default=3)
    scope =  models.TextField(blank=True, null=True)
    measurement_purpose = models.TextField(blank=True, null=True)

    def get_content(self):
        return (
            self.PATH_FILE_UR,
            self.level_of_granularity,
            self.level_of_decomposition,
            self.scope,
            self.measurement_purpose
        )
        
        
    def to_dataframe(self):
        data = self.objects.all()
        attributs = self._meta.fields
        data_content = []
        for instance in data:
            data_content.append(instance.get_content())
            
        return pd.DataFrame(data=data_content, columns=attributs)
            
            
            

class functional_user(models.Model):
    cosmic_measurement = models.ForeignKey(COSMIC_measurement, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    type = models.TextField(blank=True, null=True)
    
    def get_content(self):
        return (
            self.name,
            self.type
        )
        
        
    def to_dataframe(self):
        data = self.objects.all()
        attributs = self._meta.fields
        data_content = []
        for instance in data:
            data_content.append(instance.get_content())
            
        return pd.DataFrame(data=data_content, columns=attributs)
            
    
class non_functional_requirement(models.Model):
    cosmic_measurement = models.ForeignKey(COSMIC_measurement, on_delete=models.CASCADE)
    description =  models.TextField()
    source = models.CharField(max_length=150)
    
    
    def get_content(self):
        return (
            self.description,
            self.source
        )
        
        
    def to_dataframe(self):
        data = self.objects.all()
        attributs = self._meta.fields
        data_content = []
        for instance in data:
            data_content.append(instance.get_content())
            
        return pd.DataFrame(data=data_content, columns=attributs)
            

class ambiguous_requirement(models.Model):
    cosmic_measurement = models.ForeignKey(COSMIC_measurement, on_delete=models.CASCADE)
    description =  models.TextField()
    source = models.CharField(max_length=150)


    def get_content(self):
        return (
            self.description,
            self.source
        )
        
        
    def to_dataframe(self):
        data = self.objects.all()
        attributs = self._meta.fields
        data_content = []
        for instance in data:
            data_content.append(instance.get_content())
            
        return pd.DataFrame(data=data_content, columns=attributs)
            
class functional_user_requirement(models.Model):
    cosmic_measurement = models.ForeignKey(COSMIC_measurement, on_delete=models.CASCADE)
    description =  models.TextField()
    source = models.CharField(max_length=150)
    
    
    def get_content(self):
        return (
            self.description,
            self.source
        )
        
        
    def to_dataframe(self):
        data = self.objects.all()
        attributs = self._meta.fields
        data_content = []
        for instance in data:
            data_content.append(instance.get_content())
            
        return pd.DataFrame(data=data_content, columns=attributs)
            
    
class functional_process(models.Model):
    functional_user_requirement = models.ForeignKey(functional_user_requirement, on_delete=models.CASCADE)
    triggering_event =  models.TextField(blank=True, null=True)
    description = models.TextField()
    
    
    def get_content(self):
        return (
            self.triggering_event,
            self.description
        )
        
        
    def to_dataframe(self):
        data = self.objects.all()
        attributs = self._meta.fields
        data_content = []
        for instance in data:
            data_content.append(instance.get_content())
            
        return pd.DataFrame(data=data_content, columns=attributs)
            
            
class object_of_interest(models.Model):
    name =  models.CharField(max_length=150)

    def get_content(self):
        return (
            self.name,
        )
        
        
    def to_dataframe(self):
        data = self.objects.all()
        attributs = self._meta.fields
        data_content = []
        for instance in data:
            data_content.append(instance.get_content())
            
        return pd.DataFrame(data=data_content, columns=attributs)
            

class data_group(models.Model):
    object_of_interest = models.ForeignKey(object_of_interest, on_delete=models.CASCADE)
    name =  models.CharField(max_length=150)
    attributes = models.TextField()
    
    
    def get_content(self):
        return (
            self.name,
            self.attributes
        )
        
        
    def to_dataframe(self):
        data = self.objects.all()
        attributs = self._meta.fields
        data_content = []
        for instance in data:
            data_content.append(instance.get_content())
            
        return pd.DataFrame(data=data_content, columns=attributs)
            
    
class data_movement(models.Model):
    data_group = models.ForeignKey(data_group, on_delete=models.CASCADE)
    functional_process = models.ForeignKey(functional_process, on_delete=models.CASCADE)
    type =  models.TextField()
    sub_process_description = models.TextField(blank=True, null=True)
    number = models.IntegerField()
    
    
    
    def get_content(self):
        return (
            self.type,
            self.sub_process_description,
            self.number,
        )
        
      
        
    def to_dataframe(self):
        data = self.objects.all()
        attributs = self._meta.fields
        data_content = []
        for instance in data:
            data_content.append(instance.get_content())
            
        return pd.DataFrame(data=data_content, columns=attributs)
            