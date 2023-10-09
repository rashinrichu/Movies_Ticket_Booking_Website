from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.conf import settings
from .models import Member
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *

from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.

def index(request):
    movies = Movie.objects.all()
    theaters = Theater.objects.all()

    return render (request,'home/index.html' , {'movies': movies,'theaters':theaters})


def about(request):
    return render (request,'home/about.html')


def add_seats_admin(request):
    return render (request,'admin/add_seats.html')

def contact(request):
    return render (request,'home/contact.html')

def admin_home(request):
    movies = Movie.objects.all()
    theaters = Theater.objects.all()

    return render(request, 'admin/admin_home.html', {'movies': movies,'theaters':theaters})

def user_home(request):
    movies = Movie.objects.all()
    theaters = Theater.objects.all()
    
    return render(request, 'user/user_home.html', {'movies': movies, 'theaters': theaters})







def registration(request):
    default_image = settings.STATIC_URL + 'static/ice.png'

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('index')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('index')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if gender == 'M':
            avatar = 'static/avatar_male.png'
        elif gender == 'F':
            avatar = 'static/avatar_male.jpg'
        else:
            avatar = 'static/avatar_male.png'

        member = Member.objects.create(
            username=username,
            email=email,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            address=address,
            gender=gender,
            avatar=avatar
        )
        
        subject = 'Welcome to Movie Magic'
        message = f'Thank you for joining our Movie Magic. Your registration as a member was successful. We look forward to working with you.\n\nYour username: {username}\nYour password: {password}'        
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(request, 'Registration successful. Please log in to access your account.')
        return redirect('index')
    else:
        context = {'default_image': default_image}
        return render(request, 'home/index.html', context)



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                messages.success(request, 'Admin logged in successfully!')
                return redirect('admin_home')  
            else:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('user_home') 
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'home/index.html') 




def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        duration = request.POST.get('duration')
        release_date = request.POST.get('release_date')
        image = request.FILES.get('image')  

        movie = Movie.objects.create(
            title=title,
            genre=genre,
            duration=duration,
            release_date=release_date,
            image=image 
        )
        return redirect('movie_list')  
    return render(request, 'admin_home.html')


def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        duration = request.POST.get('duration')
        release_date = request.POST.get('release_date')
        image = request.FILES.get('image')  # Make sure your HTML form has enctype="multipart/form-data"

        movie.title = title
        movie.genre = genre
        movie.duration = duration
        movie.release_date = release_date
        if image:
            movie.image = image
        if release_date:  
            movie.release_date = release_date 
        movie.save()
        messages.success(request, 'updated successfully.')

        return redirect('movie_list')

    return render(request, 'admin/movie_list.html', {'movie': movie})

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'admin/movie_list.html', {'movie': movie})

def add_showtime(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        theater_id = request.POST.get('theater')
        start_time = request.POST.get('start_time')
        
        movie = get_object_or_404(Movie, pk=movie_id)
        theater = get_object_or_404(Theater, pk=theater_id)
        
        showtime = Showtime.objects.create(
            movie=movie,
            theater=theater,
            start_time=start_time
        )
        messages.success(request, 'Showtime added successfully.')
        return redirect('showtime_list')
    
    movies = Movie.objects.all()
    theaters = Theater.objects.all()
    context = {'movies': movies, 'theaters': theaters}
    return render(request, 'admin/admin_home.html', context)


def showtime_list(request):
    theaters = Theater.objects.all()
    movies = Movie.objects.all()
    showtimes = Showtime.objects.all()
    return render(request, 'admin/showtime_list.html', {'showtimes': showtimes,'movies': movies,'theaters': theaters,})



def update_showtime(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    
    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        theater_id = request.POST.get('theater')
        start_time = request.POST.get('start_time')
        
        movie = get_object_or_404(Movie, pk=movie_id)
        theater = get_object_or_404(Theater, pk=theater_id)
        
        showtime.movie = movie
        showtime.theater = theater
        showtime.start_time = start_time
        showtime.save()
        messages.success(request, 'Showtime updated successfully.')
        return redirect('showtime_list')
    
    movies = Movie.objects.all()
    theaters = Theater.objects.all()
    context = {'showtime': showtime, 'movies': movies, 'theaters': theaters}
    return render(request, 'update_showtime.html', context)

def delete_showtime(request, showtime_id):
    try:
        showtime = Showtime.objects.get(pk=showtime_id)
        showtime.delete()
        messages.success(request, 'Showtime Deleted successfully.')
        return redirect('showtime_list')
    except Showtime.DoesNotExist:
        raise Http404("Showtime does not exist")

def add_theater(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')

        theater = Theater.objects.create(
            name=name,
            address=address
        )
        messages.success(request, 'Theater added successfully.')
        return redirect('admin_home')  

    return render(request, 'admin_home.html')

def movie_list(request):
    theaters = Theater.objects.all()

    movies = Movie.objects.all()
    return render(request, 'admin/movie_list.html', {'movies': movies,'theaters': theaters,})

def theater_list(request):
    theaters = Theater.objects.all()
    movies = Movie.objects.all()

    return render(request, 'admin/theater.html', {'theaters': theaters,'movies': movies})



def delete_theater(request, theater_id):
    if request.method == 'POST':
        theater = Theater.objects.get(pk=theater_id)
        theater.delete()
        # You can add a success message here if you want
    return redirect('theater_list')  # Redirect back to the theater list page


@login_required
def movie_list_user(request):
    movies = Movie.objects.all()
    
    return render(request, 'user/movie_list_user.html', {'movies': movies})

@login_required
def theater_list_user(request):
    theaters = Theater.objects.all()
        
    return render(request, 'user/theater_user.html', {'theaters': theaters})






def logout(request):
    auth.logout(request)
    return redirect('index')



#user_profile
def user_profile(request):
    user = request.user  
    try:
        member = Member.objects.get(username=user.username)
    except Member.DoesNotExist:
        member = None

    context = {'user': user, 'member': member}
    return render(request, 'user/user_profile.html', context)



#edit profile

def edit_profile(request):
    user = request.user
    try:
        member = Member.objects.get(username=user.username)
    except Member.DoesNotExist:
        member = None
    
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')  # Get date_of_birth if it's present

        if member:
            member.email = email
            member.phone_number = phone_number
            member.address = address
            member.gender = gender
            if date_of_birth:  # Only update if date_of_birth is provided
                member.date_of_birth = date_of_birth
            member.save()
        else:
            Member.objects.create(
                username=user.username,
                email=email,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                address=address,
                gender=gender
            )
        messages.success(request, 'Updated successfully.')
        return redirect('user_profile')  

    context = {'user': user, 'member': member}
    return render(request, 'user/edit_profile.html', context)



def select_seats(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    seats = Seat.objects.filter(showtime=showtime)
    
    context = {'showtime': showtime, 'seats': seats}
    return render(request, 'select_seats.html', context)

def book_tickets(request):
    if request.method == 'POST':
        showtime_id = request.POST.get('showtime')
        selected_seats = request.POST.getlist('selected_seats')
        
        showtime = get_object_or_404(Showtime, pk=showtime_id)
        user = request.user  # Assuming you have authentication in place
        
        # Check if the selected seats are available
        available_seats = Seat.objects.filter(showtime=showtime, id__in=selected_seats)
        if available_seats.count() == len(selected_seats):
            # Create a booking
            booking = Booking.objects.create(
                user=user,
                showtime=showtime,
                num_tickets=len(selected_seats)
            )
            for seat in available_seats:
                booking.seat_set.add(seat)
            
            return redirect('booking_confirmation')  # Redirect to confirmation page
        else:
            # Handle seat unavailability
            return redirect('user_home')  # Redirect to an error page
        
    return redirect('movie_list')  # Redirect to some other page if no POST data

def select_seat(request):
    return render(request,'user/select_seat.html')




def add_seat(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)

    seat_numbers = list(range(1, 11))  # Convert range to a list
    
    if request.method == 'POST':
        row = request.POST.get('row')
        starting_seat_number = int(request.POST.get('starting_seat_number'))
        
        # Assuming each row has 10 seats
        for seat_number in range(starting_seat_number, starting_seat_number + 10):
            seat = Seat.objects.create(
                showtime=showtime,
                row=row,
                seat_number=seat_number
            )
            seat.save()  
        messages.success(request, 'Seat added successfully.')
        return redirect('admin_home')  
    
    return render(request, 'admin/add_seats.html', {'showtime': showtime, 'seat_numbers': seat_numbers})


def show_seats(request, showtime_id):
   

    showtime = get_object_or_404(Showtime, pk=showtime_id)
    seats = Seat.objects.filter(showtime=showtime).order_by('row', 'seat_number')
    rows = 'ABCDE'  # Assuming 5 rows
    seat_numbers = range(1, 11)  # Assuming 10 seats per row
    
    return render(request, 'admin/show_seats.html', {'showtime': showtime, 'seats': seats, 'rows': rows, 'seat_numbers': seat_numbers})

from django.http import HttpResponse

def now_playing(request, movie_id=None, theater_id=None):
    if movie_id is None or theater_id is None:
        # Handle the case when movie_id or theater_id is not provided
        # Redirect or render an appropriate response
        return HttpResponse("Movie ID and Theater ID are required.")

    selected_movie = get_object_or_404(Movie, pk=movie_id)
    selected_theater = get_object_or_404(Theater, pk=theater_id)
    
    theaters = Theater.objects.filter(showtime__movie=selected_movie).distinct()

    # Query all movies for the selected theater
    movies_for_theater = selected_theater.movies.all()

    theater_movie_showtime = []
    for theater in theaters:
        showtimes = Showtime.objects.filter(theater=theater, movie=selected_movie)
        theater_movie_showtime.append({'theater': theater, 'movies': movies_for_theater, 'showtimes': showtimes})

    return render(request, 'user/now_playing.html', {
        'selected_movie': selected_movie,
        'theater_movie_showtime': theater_movie_showtime,
        'selected_theater': selected_theater
    })


from django.db.models import Q
from django.shortcuts import render
from .models import Movie, Theater

def search_theaters(request):
    query = request.GET.get('q')
    theaters = Theater.objects.all()

    if query:
        theaters = theaters.filter(Q(name__icontains=query) | Q(address__icontains=query))

    return render(request, 'user/theater_search_results.html', {'theaters': theaters, 'query': query})


@login_required
def theater_movie_search(request):
    theaters_queryset = Theater.objects.all()  # Use a different variable name

    theater_name = request.GET.get('theater_name')
    theater_address = request.GET.get('theater_address')
    selected_movie_id = request.GET.get('movie')

    if theater_name:
        theaters_queryset = theaters_queryset.filter(name__icontains=theater_name)

    if theater_address:
        theaters_queryset = theaters_queryset.filter(address__icontains=theater_address)

    if selected_movie_id:
        selected_movie = get_object_or_404(Movie, pk=selected_movie_id)
        theaters_queryset = theaters_queryset.filter(showtime__movie=selected_movie)

    for theater in theaters_queryset:
        # Fetch all movies associated with the theater
        movies = Movie.objects.filter(showtime__theater=theater).distinct()
        theater.movie_titles = movies

    context = {
        'theaters': theaters_queryset,  # Use the modified queryset variable name
        'selected_movie_id': int(selected_movie_id) if selected_movie_id else None,
        'theater_name': theater_name,
        'theater_address': theater_address,
    }

    return render(request, 'user/theater_search.html', context)



from django.contrib.auth.decorators import login_required
from django.db.models import Sum


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404
from .models import Showtime, Seat, Booking, Payment
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404
from .models import Showtime, Seat, Booking, Payment, Member
from django.contrib.auth.decorators import login_required  # Import login_required decorator

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, Showtime, Seat, Member, Payment

from django.shortcuts import render, get_object_or_404, redirect
from .models import Showtime, Seat, Booking, Payment
from django.contrib.auth.decorators import login_required

@login_required
def show_seats_user(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    seats = Seat.objects.filter(showtime=showtime, is_booked=False).order_by('row', 'seat_number')
    
    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('selected_seats')
        
        if len(selected_seat_ids) > 5:
            messages.error(request, "You can only book up to 5 seats per show.")
            return redirect('show_seats_user', showtime_id=showtime_id)
        
        if selected_seat_ids:
            try:
                username = request.user.username
                member = Member.objects.get(username=username)
                
                booking = Booking.objects.create(user=member, showtime=showtime)
                
                for seat_id in selected_seat_ids:
                    seat = Seat.objects.get(pk=seat_id)
                    seat.is_booked = True
                    seat.save()
                    booking.seats.add(seat)  # Associate the seat with the booking
                
                total_amount = len(selected_seat_ids) * 170
                messages.success(request, "Seats successfully booked!")
                return redirect('confirm_payment', booking_id=booking.id)  # Redirect to the payment confirmation view with booking_id parameter
            except Exception as e:
                print("Error during booking:", str(e))
        else:
            messages.error(request, "No seats selected.")    
    context = {
        'showtime': showtime,
        'seats': seats,
    }
    
    return render(request, 'user/show_seats_user.html', context)


@login_required
def confirm_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    if request.method == 'POST':
        try:
            payment_amount = len(booking.seats.all()) * 170
            
            # Set the booked seats for the booking
            booked_seats = Seat.objects.filter(id__in=booking.seats.all())
            for seat in booked_seats:
                seat.is_booked = True
                seat.save()

            payment = Payment.objects.create(booking=booking, amount=payment_amount, payment_status='Paid')

            context = {
                'booking': booking,
                'payment': payment,
                'total_amount': payment_amount,
                'payment_amount': payment_amount,
            }
            messages.success(request, 'Payment confirmed and seats booked successfully.')  # Add success message
            return render(request, 'user/confirm_payment.html', context)
        except Exception as e:
            print("Error during payment:", str(e))
    
    context = {
        'booking': booking,
        'total_amount': len(booking.seats.all()) * 170,
        'payment_amount': len(booking.seats.all()) * 170,
    }

    return render(request, 'user/confirm_payment.html', context)


from datetime import date

@login_required
def payment_confirmation(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    return render(request, 'user/payment_confirmation.html', {'payment': payment})
@login_required
def theater_movie(request, movie_id):
    selected_movie = get_object_or_404(Movie, pk=movie_id)
    theaters = Theater.objects.filter(showtime__movie=selected_movie).distinct()

    current_datetime = timezone.now()  # Get the current datetime

    for theater in theaters:
        showtimes = Showtime.objects.filter(theater=theater, movie=selected_movie, start_time__gte=current_datetime)
        theater.showtimes = showtimes  # Add upcoming showtimes to the theater instance

    context = {
        'selected_movie': selected_movie,
        'theaters': theaters,
    }

    return render(request, 'user/theater_movie.html', context)


from django.db.models import Prefetch

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery

from .models import Booking, Seat, Payment

@login_required
def show_seats_user_booking(request):
    username = request.user.username

    payment_subquery = Payment.objects.filter(booking_id=models.OuterRef('pk')).order_by('-payment_date')
    user_bookings = Booking.objects.filter(user__username=username).select_related('showtime')
    user_bookings = user_bookings.annotate(payment_amount=models.Subquery(payment_subquery.values('amount')[:1]))

    seat_prefetch = Prefetch('seats', queryset=Seat.objects.filter(is_booked=True))

    user_bookings = user_bookings.prefetch_related(seat_prefetch)

    context = {
        'user_bookings': reversed(user_bookings),  # Reverse the list
    }

    return render(request, 'user/show_seats_user_booking.html', context)





def booking_list_with_payments(request):
    all_bookings = Booking.objects.all()

    booking_payment_info = []
    for booking in all_bookings:
        seats = booking.seats.all()  # Get the seats associated with the booking
        payments = Payment.objects.filter(booking=booking)
        booking_payment_info.append({'booking': booking, 'seats': seats, 'payments': payments})

    return render(request, 'admin/booking_list_with_payments.html', {'booking_payment_info': booking_payment_info})



@login_required
def theater_movie_search_admin(request):
    theaters = Theater.objects.all()

    theater_name = request.GET.get('theater_name')
    theater_address = request.GET.get('theater_address')
    selected_movie_id = request.GET.get('movie')

    if theater_name:
        theaters = theaters.filter(name__icontains=theater_name)

    if theater_address:
        theaters = theaters.filter(address__icontains=theater_address)

    if selected_movie_id:
        selected_movie = get_object_or_404(Movie, pk=selected_movie_id)
        theaters = theaters.filter(showtime__movie=selected_movie)  # Filter theaters by selected movie

    for theater in theaters:
        movies = Movie.objects.filter(showtime__theater=theater).distinct()  # Get distinct movies associated with the theater
        for movie in movies:
            showtimes = Showtime.objects.filter(theater=theater, movie=movie)
            movie.showtimes = showtimes  # Add showtimes to the movie instance
        theater.movie_titles = movies  # Add movie_titles attribute to the theater instance

    context = {
        'theaters': theaters,
        'selected_movie_id': int(selected_movie_id) if selected_movie_id else None,
        'theater_name': theater_name,
        'theater_address': theater_address,
    }

    return render(request, 'admin/theater_search_admin.html', context)

from .models import Member

def all_members(request):
    members = Member.objects.all()
    movies = Movie.objects.all()

    theaters = Theater.objects.all()

    context = {'members': members,'movies': movies,'theaters': theaters,}
    return render(request, 'admin/member.html', context)


def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        member.delete()
        return redirect('all_members')

    context = {
        'member': member
    }

    return render(request, 'admin/member.html', context)
