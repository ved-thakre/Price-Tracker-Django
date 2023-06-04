from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from .models import Item
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from AmazonPriceTracker.settings import EMAIL_HOST_USER
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib import messages 

@login_required 

def search(request):
    if request.method == "POST":
        item_url = request.POST.get("searchbox")
        maximum_price = int(request.POST.get("max_price"))
        if item_url != "" and maximum_price != "":
            user = request.user
            item_model = Item(user=user, url = item_url, max_price = maximum_price)
            item_model.save()
            messages.success(request, "Product added sucessfully")
            return redirect('search')
    return render(request, 'main_app/search.html')

def search_price():
    # max_price = 21000 _30jeq3 _16Jk6d
    hdr = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    
    for element in Item.objects.all():
        if element.status == False:
            user = element.user
            user_email = user.email
            item_url = element.url
            item_url = element.url + ".html"
            max_price = element.max_price
            
            website_name = item_url[12:16]

            if(website_name == "flip"):

                url = requests.get(str(item_url), headers=hdr) 

                soup = BeautifulSoup(url.content, 'html.parser')
                #hyperlink_format = '<a href="{item_url}">{text}</a>'
                price_span = soup.find('div', class_= "_30jeq3 _16Jk6d")
                product_span = soup.find('span', class_= "B_NuCI")
                if product_span:
                    product_name = product_span.text
                    new_name = product_name.strip()
                else:
                    new_name = "product"    
                if price_span:
                    new_span = price_span.text[1:].split(',')
                    price = int("".join(new_span))
                    print(f"The price of {new_name} is ->",price)
                    if(price <= max_price):
                        print("Entered maximum price ->",max_price)
                        subjet = "Siiiuuuuuuuu......!!!!"
                        message = f"Hi {user.username}, your {new_name} {item_url}, that you set to track has now reduced to price {price}"
                        email_from = EMAIL_HOST_USER 
                        recipients_list = [user_email]
                        send_mail(subjet, message , email_from, recipients_list)
                        print("Mail sent") 
                        element.status = True
                        element.save()
                        
            elif(website_name == "amaz"):

                url1 = requests.get(str(item_url), headers=hdr) 
                
                soup1 = BeautifulSoup(url1.content, 'html.parser')
                price_span1 = soup1.find('span', class_= "a-price-whole") # productTitle
                product_span1 = soup1.find('span', class_= 'a-size-large product-title-word-break')
                if product_span1:
                    product_name1 = product_span1.text
                    new_name1 = product_name1.strip()
                else:
                    new_name1 = "Product"    
                if price_span1:
                    new_span1 = price_span1.text[:-1].split(',')
                    price1 = int("".join(new_span1))
                    print(f"The price of {new_name1} is ->",price1)
                    if(price1 <= max_price):
                        print("Entered maximum price ->",max_price)
                        subjet1 = "Siiiuuuuuuuu......!!!!"
                        message1 = f"Hi {user.username}, your {new_name1} {item_url}, that you set to track has now reduced to price {price1}"
                        email_from1 = EMAIL_HOST_USER 
                        recipients_list1 = [user_email]
                        send_mail(subjet1, message1 , email_from1, recipients_list1)
                        print("Mail sent") 
                        element.status = True
                        element.save()
                        


# search_price() 

def start():
    sechduler =  BackgroundScheduler()
    sechduler.add_job(search_price, 'interval', minutes = 1)
 
    sechduler.start()   

