from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from product.forms import ContactForm
from product.models import Product
# from your_app_name.models import 

def productForm(request):
    return render(request,'product/addProduct.html')

def addProduct(request):
    if(request.method=='POST'):
     productName=request.POST.get('product-name')
     description=request.POST.get('description')
     price=request.POST.get('price')
     category=request.POST.get('category')

    # required field validation
    if not productName or not description or not price or not category:
     return render(request, 'product/addProduct.html',{'error':"All fields are required"})
    
    try:
            price = float(price)
            if price <= 0:
                return render(request, 'product/addProduct.html', {'error': 'Price must be a positive number'})
    except ValueError:
            return render(request, 'product/addProduct.html', {'error': 'Invalid price'})

    product=Product(name=productName,description=description,price=price,category=category)
    product.save()
    return render(request,'product/viewProducts.html')
    

def viewProducts(request):
#    products=Product.objects.all()
   products=Product.objects.filter(id__gte=10)
   return render(request,'product/viewProducts.html',{'products':products})

def editProduct(request,product_id):
   product=get_object_or_404(Product,id=product_id)
   return render(request,'product/editProduct.html',{'product':product})

def updateProduct(request,product_id):
   product=get_object_or_404(Product,id=product_id)
   if(request.method=='POST'):
      product.name=request.POST.get('product-name')
      product.description=request.POST.get('description')
      product.price=request.POST.get('price')
      product.category=request.POST.get('category')
      product.save()
      return HttpResponse("Product updated successfully!") 

def deleteProduct(request,product_id):
   product=get_object_or_404(Product,id=product_id)
   product.delete()

   return HttpResponse("product deletion success") 

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Do something with the data (e.g., send email or save to database)
            return HttpResponse("Thank you for your message!")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})