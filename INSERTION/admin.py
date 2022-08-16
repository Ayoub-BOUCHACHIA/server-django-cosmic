from django.contrib import admin
from .models import *


class COSMICMeasurementAdmin(admin.ModelAdmin):
    list_display = ('PATH_FILE_UR_IN_SERVER','PATH_FILE_UR', 'level_of_granularity', 'level_of_granularity','scope','measurement_purpose')
    list_filter = ('PATH_FILE_UR_IN_SERVER','PATH_FILE_UR','scope','measurement_purpose','level_of_granularity','level_of_granularity')
    
admin.site.register(COSMIC_measurement, COSMICMeasurementAdmin)


class functionalUserAdmin(admin.ModelAdmin):
    list_display = ('cosmic_measurement', 'name', 'type')
    list_filter = ('name','type')
    
admin.site.register(functional_user, functionalUserAdmin)


class nonFunctionalRequirementAdmin(admin.ModelAdmin):
    list_display = ('cosmic_measurement', 'description', 'source')
    list_filter = ('description','source')
admin.site.register(non_functional_requirement, nonFunctionalRequirementAdmin)

    
class ambiguousRequirementAdmin(admin.ModelAdmin):
    list_display = ('cosmic_measurement', 'description', 'source')
    list_filter = ('description','source')
admin.site.register(ambiguous_requirement, ambiguousRequirementAdmin)


    
class functionalUserRequirementAdmin(admin.ModelAdmin):
    list_display = ('cosmic_measurement', 'description', 'source')
    list_filter = ('description','source')
admin.site.register(functional_user_requirement, functionalUserRequirementAdmin)

    
    
class functionalProcessAdmin(admin.ModelAdmin):
    list_display = ('functional_user_requirement', 'triggering_event', 'description')
    list_filter = ('triggering_event', 'description')
admin.site.register(functional_process, functionalProcessAdmin)

    
    
class dataMovementAdmin(admin.ModelAdmin):
    list_display = ('data_group', 'functional_process',
                    'type',
                    'sub_process_description',
                    'number'
    )
    list_filter = ('type',
                    'sub_process_description',
                    'number')
admin.site.register(data_movement, dataMovementAdmin)


class dataGroupAdmin(admin.ModelAdmin):
    object_of_interest
    list_display = ('object_of_interest', 'name', 'attributes')
    list_filter = ('name', 'attributes')
admin.site.register(data_group, dataGroupAdmin)


class objectInterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
admin.site.register(object_of_interest, objectInterestAdmin)