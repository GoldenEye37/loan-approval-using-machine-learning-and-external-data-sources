import os
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

    def post(self, request):
        try:
            payload = LoanSerializer(data=request.data)
            if payload.is_valid():

                # Load the pre-trained model
                # Get the absolute path to the current working directory
                absolute_path = "loans/ml_models/loan_model.pkl"
                model = pickle.load(open(absolute_path, "rb"))
                logger.info(f"Loan: model loaded successfully")

                # Load the category mapping (for consistent encoding)
                category_mapping_path = 'loans/ml_models/category_mapping.pkl'
                with open(category_mapping_path, 'rb') as f:
                    category_mapping = pickle.load(f)
                logger.info(f"Loan: category mapping loaded successfully")


                data = payload.data

                logger.info(f"Loan: data -> {data}")

                # unpack data
                company_name = data['company_name']
                gross_approval = data['gross_approval']
                term = data['term']
                number_of_employees = data['number_of_employees']
                new_business = data['new_business']
                urban = data['urban']
                industry = data['industry_name']

                logger.info(f"Loan: data unpacked successfully -> {industry}")
                # check if industry exists
                industry = Industry.objects.filter(name=industry).first()
                logger.info(f"Loan: industry: -> {industry}")

                if industry is None:
                    return JsonResponse({
                        'status_code': 400,
                        'message': "The industry you provided was not found",
                        'success': False
                    }, status=400)

                logger.info(f"Loan: data unpacked successfully -> {company_name}")

                # todo we now get industry trends from the database
                industry_trends = industry.trends
                logger.info(f"Loan: industry trends -> {industry_trends}")

                # dummy industry trend
                industry_trends = 'positive'

                # get industry instance from database
                industry = Industry.objects.get(industry_id=industry.industry_id)

                # create loan instance
                loan = Loan()
                loan.company_name = company_name
                loan.gross_approval = gross_approval
                loan.term = term
                loan.number_of_employees = number_of_employees
                loan.new_business = new_business
                loan.urban = urban
                loan.industry = industry

                # predict loan
                logger.info(f"Loan: prepare data for prediction -> {company_name}")

                loans_data = [
                    data["gross_approval"],
                    data["term"],
                    data["number_of_employees"],
                    data["new_business"],
                    data["urban"],
                    data["industry_name"],
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
                            'loan_approved': True,
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
                            'loan_approved': False,
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
                    'message': f"Invalid payload: {payload.errors}",
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


