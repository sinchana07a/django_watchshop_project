from django.shortcuts import render,redirect,get_object_or_404
from .forms import RatingCommentForm
from .models import RatingComment
from django.contrib.auth.decorators import login_required
from .models import Watches
from .forms import WatchForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.




def home(request): 
    # Get distinct brands from the Watches model
    brands = Watches.objects.values_list('brand', flat=True).distinct()
    
    # Get selected brands and price range from GET parameters
    selected_brands = request.GET.getlist('brands')
    price_min = request.GET.get('price_min', 0)
    price_max = request.GET.get('price_max', 1000)
    
    # Start with all watches
    watches = Watches.objects.all()
    
    # Filter by selected brands if any are chosen
    if selected_brands:
        watches = watches.filter(brand__in=selected_brands)
    
    # Apply the price range filter
    if price_min and price_max:
        watches = watches.filter(price__gte=price_min, price__lte=price_max)
    
    # Pass data to the template
    context = {
        'watches': watches,
        'brands': brands,
        'selected_brands': selected_brands,
    }
    return render(request, 'home.html', context)





def product(request, pk):
    watch = get_object_or_404(Watches, id=pk) 
    rate = watch.average_rating()
    reviews = watch.ratings.all()

    # Add a custom attribute 'star_range' to each review
    for review in reviews:
        review.star_range = range(review.rating)  # This will be used for the stars

    context = {
        'showproduct': watch,
        'reviews': reviews,
        'average_rate': rate,
    }
    
    return render(request, 'product.html', context)






@login_required
def addproduct(request):
    if request.method=='POST':
        fm=WatchForm(request.POST, request.FILES)
        if fm.is_valid():
            fm.save()
            return redirect('/')
    else:
        fm=WatchForm()

    context={'form':fm}
    return render(request,'addproduct.html',context)

@login_required
def edit(request, pk):
    selected_watch = get_object_or_404(Watches, pk=pk)
    
    if request.method == 'POST':
        form = WatchForm(request.POST,request.FILES,instance=selected_watch)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to the home page 
    else:
        form = WatchForm(instance=selected_watch)

    context = {'form': form, 'watch': selected_watch}
    return render(request, 'edit.html', context)


@login_required()
def deleteWatch(request, pk):
    selected_watch = get_object_or_404(Watches, pk=pk)
    
    if selected_watch:
        selected_watch.delete()
        
    return redirect('/')


from django.contrib.auth import login as auth_login, authenticate

from .models import LoginForm
def login(request):  # Renamed to avoid conflict
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Username is: {username}")
            print(f"Password is: {password}")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Uses Django's built-in login function without conflict
                return redirect('/')  # Redirect to the homepage or another URL
            else:
                print("Invalid username or password")
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'login.html', context)

from django.contrib.auth import logout


@login_required
def LogoutPage(request):
    logout(request)
    return redirect('home')


from .models import Watches
from django.http import JsonResponse
def search_product(request):
    query = request.GET.get('query', '').strip() 

    if not query:  
        return JsonResponse([], safe=False)  

    results = Watches.objects.filter(name__icontains=query)
    data = list(results.values('id', 'name', 'desc', 'price', 'image'))  

    return JsonResponse(data, safe=False)



#  ............class based ....................................#


class Reviews( LoginRequiredMixin,View):
    def get(self, request, pk):
        # Fetch the watch instance and the existing reviews
        watch = get_object_or_404(Watches, id=pk)
        form = RatingCommentForm()
        existing_reviews = RatingComment.objects.filter(product=watch)

        # Pass form and reviews to context
        context = {'form': form, 'reviews': existing_reviews}
        return render(request, 'comments.html', context)

    def post(self, request, pk):
        # Fetch the watch instance
        watch = get_object_or_404(Watches, id=pk)
        form = RatingCommentForm(request.POST)

        if form.is_valid():
            # Save the form with additional fields
            rating_form = form.save(commit=False)
            rating_form.user = request.user
            rating_form.product = watch
            rating_form.save()
            return redirect('product', pk=watch.id)

        context = {'form': form}
        return render(request, 'comments.html', context)