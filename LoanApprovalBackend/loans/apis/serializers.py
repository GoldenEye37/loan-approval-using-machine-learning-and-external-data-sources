from rest_framework import serializers

from loans.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'company_name',
            'gross_approval',
            'term',
            'number_of_employees',
            'new_business',
            'urban',
            'industry',
            ]
        model = Loan

