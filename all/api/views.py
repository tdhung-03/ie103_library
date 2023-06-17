from all.api.serializers import *
from all.models import *
from rest_framework import generics, parsers
from django.db import connection


class LoanCreate(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # Include MultiPartParser

    def perform_create(self, serializer):
        # Retrieve loan data from serializer
        loan_data = serializer.validated_data

        # Extract book name and member name from the loan data
        book_name = loan_data.get('book')
        member_name = loan_data.get('member')
        loan_date = loan_data.get('loan_date')

        # Get the book_id based on the provided book name
        try:
            book = Book.objects.get(title=book_name)
            book_id = book.book_id
        except Book.DoesNotExist:
            # Handle book not found error
            raise serializers.ValidationError("Book not found")

        # Get the member_id based on the provided member name
        try:
            member = Member.objects.get(name=member_name)
            member_id = member.member_id
        except Member.DoesNotExist:
            # Handle member not found error
            raise serializers.ValidationError("Member not found")

        # Call PostgreSQL stored procedure to handle loan creation
        with connection.cursor() as cursor:
            cursor.execute(
                'CALL create_loan(%s, %s, %s, NULL)',
                [book_id, member_id, loan_date]
            )
