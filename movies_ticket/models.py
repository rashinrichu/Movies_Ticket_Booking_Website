from django.db import models

class Member(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

 

    def __str__(self):
        return self.username



    

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()  
    release_date = models.DateField()
    image = models.ImageField(upload_to='movies/', blank=True, null=True)

    def __str__(self):
        return self.title

class Theater(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.name


    
   
    
class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie} - {self.theater} - {self.start_time}"


class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    row = models.CharField(max_length=5)
    seat_number = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.showtime} - Row {self.row}, Seat {self.seat_number}"


class Booking(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)

    def __str__(self):
        return f"{self.user} - {self.showtime} - {self.num_tickets}"



class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.booking} - {self.seat}"

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,null=True,blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust as needed
    payment_status = models.CharField(max_length=20)  # Success, Failed, etc.

    def __str__(self):
        return f"{self.booking} - {self.amount} - {self.payment_status}"