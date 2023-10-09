from django.contrib import admin
from .models import Member, Movie, Theater, Showtime, Booking, Seat, Ticket,Payment

# Register your models here
admin.site.register(Member)
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Showtime)
admin.site.register(Booking)
admin.site.register(Seat)
admin.site.register(Ticket)
admin.site.register(Payment)


