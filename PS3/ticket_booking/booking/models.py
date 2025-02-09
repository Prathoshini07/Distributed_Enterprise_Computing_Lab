from django.db import models

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()

    def __str__(self):
        return self.event_name

class Show(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    show_time = models.TimeField()
    available_tickets = models.IntegerField()

    def __str__(self):
        return f"{self.event.event_name} - {self.show_time}"

class Booking(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    tickets_booked = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
