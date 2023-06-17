from all.api.serializers import *
from all.models import *
from rest_framework import generics, parsers
from django.db import connection
from django.shortcuts import get_object_or_404


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


class ReservationCreate(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # Include MultiPartParser

    def perform_create(self, serializer):
        # Retrieve reservation data from serializer
        reservation_data = serializer.validated_data

        # Extract book name and member name from the reservation data
        book_name = reservation_data.get('book')
        member_name = reservation_data.get('member')
        reservation_date = reservation_data.get('reservation_date')

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

        # Call PostgreSQL stored procedure to handle reservation creation
        with connection.cursor() as cursor:
            cursor.execute(
                'CALL create_reservation(%s, %s, %s, NULL)',
                [book_id, member_id, reservation_date]
            )


class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # Include MultiPartParser

    def perform_create(self, serializer):
        # Retrieve review data from serializer
        review_data = serializer.validated_data

        # Extract book name and member name from the review data
        book_name = review_data.get('book')
        member_name = review_data.get('member')
        review_date = review_data.get('review_date')
        comment = review_data.get('comment')
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

        # Call PostgreSQL stored procedure to handle review creation
        with connection.cursor() as cursor:
            cursor.execute(
                'CALL add_review(%s, %s, %s, %s, NULL)',
                [book_id, member_id, comment, review_date]
            )


class FavoriteCreate(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # Include MultiPartParser

    def perform_create(self, serializer):
        # Retrieve favorite data from serializer
        favorite_data = serializer.validated_data

        # Extract book name and member name from the favorite data
        book_name = favorite_data.get('book')
        member_name = favorite_data.get('member')

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

        # Call PostgreSQL stored procedure to handle favorite creation
        with connection.cursor() as cursor:
            cursor.execute(
                'CALL add_to_favorites(%s, %s, NULL)',
                [book_id, member_id]
            )


class LoanReturn(generics.UpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanForReturnSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # Include MultiPartParser

    def get_object(self):
        # Retrieve loan based on provided book title and member name
        book_title = self.request.data.get('book')
        member_name = self.request.data.get('member')
        try:
            book = Book.objects.get(book_id=book_title)
            member = Member.objects.get(member_id=member_name)
            loan = Loan.objects.get(book=book, member=member)
            return loan
        except (Book.DoesNotExist, Member.DoesNotExist, Loan.DoesNotExist):
            # Handle book, member, or loan not found error
            raise serializers.ValidationError("Book, member, or loan not found")

    def perform_update(self, serializer):
        loan = self.get_object()

        # Call PostgreSQL stored procedure to handle loan return
        with connection.cursor() as cursor:
            cursor.execute(
                'CALL handle_return(%s)',
                [loan.loan_id]
            )
