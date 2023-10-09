from django.contrib import admin
from django.urls import path,include
from movies_ticket import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),

    path('contact/',views.contact,name='contact'),
    path('registration/',views.registration,name='registration'),
    path('login_view/',views.login_view,name='login_view'),
     path('admin_home/',views.admin_home,name='admin_home'),
    path('user_home/',views.user_home,name='user_home'),

    path('add_movie/',views.add_movie,name='add_movie'),

    path('add_theater/',views.add_theater,name='add_theater'),

    path('movie_list/',views.movie_list,name='movie_list'),

    path('theater_list/',views.theater_list,name='theater_list'),
    path('logout/',views.logout,name='logout'),
    path('user_profile/',views.user_profile,name='user_profile'),
     path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('update_movie/<int:movie_id>/',views.update_movie,name='update_movie'),

    path('add_showtime/', views.add_showtime, name='add_showtime'),
    path('add_seat/<int:showtime_id>/', views.add_seat, name='add_seat'),

    path('select_seat/', views.select_seat, name='select_seat'),
    path('showtime_list/', views.showtime_list, name='showtime_list'),
  path('show_seats/<int:showtime_id>/', views.show_seats, name='show_seats'),


    path('movie_list_user/',views.movie_list_user,name='movie_list_user'),
    path('theater_list_user/',views.theater_list_user,name='theater_list_user'),
    path('now_playing/<int:movie_id>/<int:theater_id>/', views.now_playing, name='now_playing'),

    path('theater_search/', views.theater_movie_search, name='theater_movie_search'),

    path('movie_list_user/',views.movie_list_user,name='movie_list_user'),
    path('show_seats_user/<int:showtime_id>/', views.show_seats_user, name='show_seats_user'),

#    path('book_seats/<int:showtime_id>/', views.book_seats, name='book_seats'),
    path('payment_confirmation/<int:payment_id>/', views.payment_confirmation, name='payment_confirmation'),
    path('confirm_payment/<int:booking_id>/', views.confirm_payment, name='confirm_payment'),
    path('theater_movie/<int:movie_id>/', views.theater_movie, name='theater_movie'),
    path('show_seats_user_booking/', views.show_seats_user_booking, name='show_seats_user_booking'),
    path('booking_list_with_payments/',views.booking_list_with_payments,name='booking_list_with_payments'),
    path('theater_movie_search_admin/', views.theater_movie_search_admin, name='theater_movie_search_admin'),
    path('all_members/',views.all_members,name='all_members'),
    path('delete_member/<int:member_id>/',views.delete_member,name='delete_member'),
    path('delete_theater/<int:theater_id>/', views.delete_theater, name='delete_theater'),
    path('delete_movie/<movie_id>/', views.delete_movie, name='delete_movie'),
    path('add_seats_admin/', views.add_seats_admin, name='add_seats_admin'),

]
    




