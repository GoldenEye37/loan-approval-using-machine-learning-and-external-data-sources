import joblib
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from loguru import logger
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse


from loans.apis.serializers import LoanSerializer
from loans.models import Loan
from loans.services.fetch_industry_trend import fetch_industry_trends


# Create your views here.

class PredictLoanAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoanSerializer
    """GrAppv           687973 non-null  float64
 1   Term             687973 non-null  int64  
 2   NoEmp            687973 non-null  int64  
 3   NewExist         687973 non-null  float64
 4   UrbanRural       687973 non-null  int64  
 5   Industry         687973 non-null  int8   
 6   Industry Trends  687973 non-null  int8   
 7   MIS_Status
    """
    def post(self, request):
        try:
            payload = LoanSerializer(data=request.data)
            if payload.is_valid():
                model = joblib.load('loans/models/loan_model.pkl')
                data = payload.data

                # unpack data
                company_name = data['company_name']
                gross_approval = data['gross_approval']
                term = data['term']
                number_of_employees = data['number_of_employees']
                new_business = data['new_business']
                urban = data['urban']
                industry = data['industry']

                logger.info(f"Loan: data unpacked successfully -> {company_name}")

                # todo get live industry trend
                industry_trends = fetch_industry_trends(industry)

                # dummy industry trend
                industry_trends = 'positive'

                # create loan instance
                loan = Loan.objects.create(
                    company_name=company_name,
                    gross_approval=gross_approval,
                    term=term,
                    number_of_employees=number_of_employees,
                    new_business=new_business,
                    urban=urban,
                    industry=industry,
                    industry_trends=industry_trends
                )

                # predict loan
                logger.info(f"Loan: prepare data for prediction -> {company_name}")

                loan_data = [gross_approval, term, number_of_employees, new_business, urban, industry, industry_trends]
                columns = ['GrAppv', 'Term', 'NoEmp', 'NewExist', 'UrbanRural', 'Industry', 'Industry Trends']
                dataframe = pd.DataFrame([loan_data], columns=columns)

                prediction = model.predict(dataframe)

                logger.info(f"Loan: prediction -> {prediction}")


                if prediction[0] == 1:
                    loan.mis_status = "True"
                    # save
                    loan.save()
                    return JsonResponse({
                        'status_code': 200,
                        'message': 'Loan approved',
                        'success': True
                    }, status=200)
                else:
                    loan.mis_status = "False"
                    # save
                    loan.save()
                    return JsonResponse({
                        'status_code': 200,
                        'message': 'Loan denied',
                        'success': True
                    }, status=200)
        except Exception as e:
            # log error
            logger.error(f"Loan: error processing loan, -> {e.message}")
            return JsonResponse({
                'status_code': 500,
                'message': str(e),
                'success': False
            }, status=500)


