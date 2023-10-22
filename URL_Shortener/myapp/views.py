import re 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import LongToShort
# Create your views here.
def redirect_url(request, short_url):
    row = LongToShort.objects.filter(short_url=short_url)
    if not row:
        return HttpResponse("No such short URL exists")

    obj = row[0]
    Long_url = obj.long_url
    obj.clicks += 1

    # Detect the user's device
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    #print(user_agent)   Add this line to print the user agent string for debugging

    is_mobile = bool(re.search(r'Mobile|Android', user_agent))

    # Increment the corresponding counter in the database
    if is_mobile:
        obj.mobile_visits += 1
    else:
        obj.desktop_visits += 1

    obj.save()
    return redirect(Long_url)

def all_analytics(request):
	rows=LongToShort.objects.all()
	context={
	"rows":rows
	}
	return render(request,'all-analytics.html',context)

def home_page(request):
    context = {
        "submitted": False,
        "Error": False
    }

    if request.method == 'POST':
        data = request.POST
        long_url = data['longurl']
        customname = data['custom_name']
        

        try:
            # Creating the data in the database
            obj = LongToShort(
                long_url=long_url,
                short_url=customname
            )
            obj.save()
		  # Save the updated counts to the database

            # Reading the data from the database
            Date = obj.date
            Clicks = obj.clicks

            context["longurl"] = long_url
            context["shorturl"] = request.build_absolute_uri() + customname
            context["date"] = Date
            context["clicks"] = Clicks
            context["submitted"] = True
        except Exception as e:
            context["Error"] =True
            

    return render(request, 'index.html', context)