from django.shortcuts import render, get_object_or_404, redirect
from .models import Show, Booking

def index(request):
    shows = Show.objects.all()
    return render(request, 'booking/index.html', {'shows': shows})

def book_tickets(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    if request.method == 'POST':
        customer_name = request.POST['name']
        tickets = int(request.POST['tickets'])

        if show.available_tickets >= tickets:
            Booking.objects.create(show=show, customer_name=customer_name, tickets_booked=tickets)
            show.available_tickets -= tickets
            show.save()
            return redirect('index')
        else:
            return render(request, 'booking/book.html', {'show': show, 'error': 'Not enough tickets available'})
    return render(request, 'booking/book.html', {'show': show})
