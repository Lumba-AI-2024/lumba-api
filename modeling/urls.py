from django.urls import path
from .record_views import *
from .modeling_views import *
from .predict_views import *

urlpatterns = [
    path('initiate/', initiate_modeling),
    path('save/', save_model),
    path('createrecord/', create_training_record),
    path('updaterecord/', update_training_record),
    path('getrecord/', get_training_record),
    path('listmodel/', list_model),
    path('columns/', get_columns_type_by_modeling_method),
    path('predict/', model_do_predict),
]