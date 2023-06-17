from all.models import *
from rest_framework import serializers


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['book', 'member', 'loan_date']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['book', 'member', 'reservation_date']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['book', 'member', 'comment', 'review_date']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['book', 'member']


class LoanForReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['book', 'member']
