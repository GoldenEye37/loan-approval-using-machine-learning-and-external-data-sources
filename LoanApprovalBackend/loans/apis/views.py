import pickle
import traceback

import joblib
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from loguru import logger
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse


from loans.apis.serializers import LoanSerializer
from loans.models import Loan, Industry
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

                # Load the pre-trained model
                absolute_path = '/loans/ml_models/loan_model.pkl'
                model = pickle.load(open(absolute_path, "rb"))
                logger.info(f"Loan: model loaded successfully")

                # Load the category mapping (for consistent encoding)
                category_mapping_path = '/loans/ml_models/category_mapping.pkl'
                with open(category_mapping_path, 'rb') as f:
                    category_mapping = pickle.load(f)
                logger.info(f"Loan: category mapping loaded successfully")


                data = payload.data

                # unpack data
                company_name = data['company_name']
                gross_approval = data['gross_approval']
                term = data['term']
                number_of_employees = data['number_of_employees']
                new_business = data['new_business']
                urban = data['urban']
                industry = data['industry']


                # check if industry exists
                industry = Industry.objects.filter(name=industry).first()
                logger.info(f"Loan: industry: -> {industry}")

                if not industry:
                    return JsonResponse({
                        'status_code': 400,
                        'message': "Industry not found",
                        'success': False
                    }, status=400)

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
                )

                # predict loan
                logger.info(f"Loan: prepare data for prediction -> {company_name}")

                loans_data = [
                    data["gross_approval"],
                    data["term"],
                    data["number_of_employees"],
                    data["new_business"],
                    data["urban"],
                    data["industry"],
                    industry_trends
                ]
                logger.info(f"Loan: loan data ->  {loans_data}")
                columns = ['GrAppv', 'Term', 'NoEmp', 'NewExist', 'UrbanRural', 'Industry', 'Industry Trends']
                prediction_data = pd.DataFrame([loans_data], columns=columns)

                # Apply the category mapping to ensure consistent encoding
                encoded_prediction_df = pd.DataFrame()

                for column in prediction_data.columns:
                    if column in category_mapping:
                        # Apply category mapping to convert to codes
                        prediction_data[column] = prediction_data[column].astype('category').cat.set_categories(
                            category_mapping[column], ordered=False)
                        encoded_prediction_df[column] = prediction_data[column].cat.codes
                    else:
                        encoded_prediction_df[column] = prediction_data[column]
                try:
                    prediction = model.predict(encoded_prediction_df)
                    logger.info(f"Loan: prediction -> {prediction}")
                    if prediction[0] == 1:
                        loan.mis_status = "True"
                        # save
                        loan.save()
                        logger.info(f"Loan: loan approved -> {company_name}")
                        return JsonResponse({
                            'status_code': 200,
                            'message': 'Loan approved',
                            'success': True
                        }, status=200)
                    else:
                        loan.mis_status = "False"
                        # save
                        loan.save()
                        logger.info(f"Loan: loan denied -> {company_name}")
                        return JsonResponse({
                            'status_code': 200,
                            'message': 'Loan denied',
                            'success': True
                        }, status=200)
                except Exception as e:
                    return JsonResponse({
                        'status_code': 500,
                        'message': f"Prediction error: {str(e)}",
                        'success': False
                    },
                        status=500
                    )
            else:
                return JsonResponse({
                    'status_code': 400,
                    'message': "Invalid payload",
                    'success': False
                }, status=400)
        except Exception as e:
            # log error
            logger.error(f"Loan: error processing loan, -> {traceback.format_exc()}")
            return JsonResponse({
                'status_code': 500,
                'message': str(e),
                'success': False
            }, status=500)


