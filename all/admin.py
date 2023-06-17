from django.contrib import admin
from all.models import *

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Member)
admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Reservation)
admin.site.register(AuthorBook)
admin.site.register(BookCategory)
admin.site.register(Favorite)
admin.site.register(Review)
