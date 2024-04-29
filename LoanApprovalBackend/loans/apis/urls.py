from django.urls import path, include

from loans.apis.views import PredictLoanAPIView

urlpatterns = [
    path('predict', PredictLoanAPIView.as_view(), name="predict-loan"),  # 'name' goes in 'path', not 'as_view()'
]