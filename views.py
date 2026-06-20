from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from DPG.models import volunterr, NGO, event, EventRegistration, contactus , review
import json
def index(request):
    return render(request, "index.html")

def login(request):
    error = None
    if request.method == "POST":
        role = request.POST.get("role")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if role == "volunteer":
            vol = volunterr.objects.filter(email=email, password=password).first()
            if vol:
                request.session["volunteer_id"] = vol.id
                return redirect('/volunteer-Home/')
            else:
                error = "Invalid email or password"
        elif role == "ngo":
            ngo = NGO.objects.filter(email=email, password=password).first()
            if ngo:
                request.session["ngo_id"] = ngo.id
                return redirect('/ngo-Home/')
            else:
                error = "Invalid email or password"
                
    return render(request, "login.html", {"error": error})

from django.db.models import Count

def signup(request):
    if request.method == "POST":
        role = request.POST.get("role")
        email = request.POST.get("email")
        password = request.POST.get("password")
        city = request.POST.get("city")
        Full_name = request.POST.get("Full_name")
        
        if role == "volunteer":
            volunterr.objects.create(Full_name=Full_name, email=email, city=city, password=password)
        elif role == "ngo":
            organization_name = request.POST.get("organization_name")
            NGO.objects.create(Full_name=Full_name, organization_name=organization_name, city=city, email=email, password=password)
        
        return redirect('/login/')
    return render(request, "signup.html")

def ngo_dashboard(request):
    ngo_id = request.GET.get('ngo_id') or request.session.get("ngo_id")
    if not ngo_id:
        return redirect('/login/')
    ngo_obj = NGO.objects.filter(id=ngo_id).first()
    if not ngo_obj:
        return redirect('/login/')
        
    if request.method == "POST":
        Event_title = request.POST["Event_title"]
        Event_type = request.POST["Event_type"]
        max_participants = request.POST["max_participants"]
        Start_time = request.POST["Start_time"]
        Event_date = request.POST["Event_date"]
        location = request.POST["location"]
        Green_credits = request.POST["Green_credits"]
        Full_address = request.POST["Full_address"]
        Event_description = request.POST["Event_description"]
        event.objects.create(ngo=ngo_obj, Event_title=Event_title, Event_type=Event_type,max_participants=max_participants,Start_time=Start_time,Event_date=Event_date,location=location,Green_credits=Green_credits,Full_address=Full_address,Event_description=Event_description)
        return redirect('/ngo-Home/')
    
    events_list = event.objects.filter(ngo=ngo_obj).annotate(registered_count=Count('eventregistration'))
    registrations = EventRegistration.objects.filter(event__ngo=ngo_obj).select_related('volunteer', 'event').order_by('-registration_date')
    context = {
        'ngo': ngo_obj,
        'events': events_list,
        'registrations': registrations,
    }
    return render(request, "ngo-dashboard.html", context)

def volunteer_dashboard(request):
    volunteer_id = request.session.get("volunteer_id")
    if not volunteer_id:
        return redirect('/login/')
    volunteer = volunterr.objects.filter(id=volunteer_id).first()
    if not volunteer:
        return redirect('/login/')
        
    events_list = event.objects.filter(eventregistration__volunteer=volunteer).select_related('ngo')
    context = {
        'volunteer': volunteer,
        'events': events_list,
    }
    return render(request, "volunteer-dashboard.html", context)

def events(request):
    events_list = event.objects.annotate(registered_count=Count('eventregistration')).all()
    ngo_obj = NGO.objects.first()
    volunteer_id = request.session.get("volunteer_id")
    registered_event_ids = []
    if volunteer_id:
        registered_event_ids = list(EventRegistration.objects.filter(volunteer_id=volunteer_id).values_list('event_id', flat=True))
        
    context = {
        'events': events_list,
        'ngo': ngo_obj,
        'is_volunteer_logged_in': bool(volunteer_id),
        'registered_event_ids': registered_event_ids
    }
    return render(request, "events.html", context)

def register_event(request):
    if request.method == "POST":
        volunteer_id = request.session.get("volunteer_id")
        if not volunteer_id:
            return JsonResponse({"status": "error", "message": "Not logged in as volunteer"}, status=403)
        
        try:
            data = json.loads(request.body)
            event_id = data.get('event_id')
            
            vol = volunterr.objects.get(id=volunteer_id)
            ev = event.objects.get(id=event_id)
            
            EventRegistration.objects.get_or_create(event=ev, volunteer=vol)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def blog(request):
    if request.method == "POST":
        Full_Name = request.POST["Full_Name"]
        Email = request.POST["Email"]
        Your_Review = request.POST["Your_Review"]
        Your_Role = request.POST["Your_Role"]
        review.objects.create(Full_Name=Full_Name, Email=Email, Your_Review=Your_Review, Your_Role=Your_Role)
    return render(request, "blog.html")
def index1(request): 
    return render(request, "index (1).html")
def about(request):
    return render(request, "about.html")
def contact(request):
    success = False
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        organisation = request.POST["organisation"]
        city = request.POST["city"]
        message = request.POST["message"]
        contactus.objects.create(first_name=first_name, last_name=last_name, email=email, organisation=organisation, city=city, message=message)
        success = True
    return render(request, "contact.html", {"success": success})
def privacy(request):
    return render(request, "privacy.html")
def greenstore(request):
    return render(request, "green-credits-store.html")   
