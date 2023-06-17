# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'author'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'category'


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'member'


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'book'


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey(Member, models.DO_NOTHING, blank=True, null=True)
    loan_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loan'


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey(Member, models.DO_NOTHING, blank=True, null=True)
    reservation_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation'


class AuthorBook(models.Model):
    author_book_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, models.DO_NOTHING)
    book = models.ForeignKey(Book, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'author_book'


class BookCategory(models.Model):
    book_category_id = models.AutoField(primary_key=True)
    book = models.OneToOneField(Book, models.DO_NOTHING)
    category = models.ForeignKey(Category, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'book_category'


class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey(Member, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favorite'


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey(Member, models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'
