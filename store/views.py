from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View,ListView,CreateView
from store.models import Category, Product, CartModel, order
from store.forms import Register, SigninForm, OrderForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def sigin_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            return redirect("login")
    return wrapper    

class Home(ListView):
    # def get(self,request,*args,**kwargs):
    #     return render(request, "store\index.html")
    model = Category
    template_name = "store/index.html"
    context_object_name = "categories"
    

# class Collections(ListView):
#     model = Category 
#     template_name = "store/index.html"
#     context_object_name = "categories"  
    
class ProductView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        data = Product.objects.filter(category_id=id)
        names = Category.objects.get(id=id)
        return render(request,"store/product_list.html",{"data":data,"names":names})
          
class ProductDetail(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        products_data = Product.objects.filter(id=id)
        return render(request,"store/product_detail.html",{"products_data":products_data})
    
class RegisterView(CreateView):
    template_name = "store/register.html"
    form_class = Register
    model = User
    success_url = reverse_lazy("home")

class SigninView(View):
    def get(self,request,*args,**kwargs):
        form = SigninForm()
        return render(request,"store/signin.html",{"form":form})   

    def post(self,request,*args,**kwargs):
        form = SigninForm(request.POST)
        if form.is_valid():
            u_name = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            user_obj = authenticate(request,username=u_name,password=pwd)
            if user_obj:
                login(request,user_obj)
                return redirect("home")
            else:
                print("incorrect password or username")
        return redirect("signin")    
    
class AddtoCartView(View):
    def get(self,request,*args,**kwargs):
        product_id = kwargs.get("pk")
        data = Product.objects.get(id=product_id)   # id is the field name in product model 
        CartModel.objects.create(item=data, user=request.user)
        print("added successsfully")
        return redirect("home")
    
class CartDetails(View):
    def get(self,request,*args,**kwagrs):
        data = CartModel.objects.filter(user=request.user)
        return render(request,"store/cart.html",{"data":data})
    
class OrderView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Product.objects.get(id=id)
        form = OrderForm()
        return render(request,"store/orderpage.html",{"form":form,"data":data})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        CartModel.objects.get(id=id).delete()
        data=Product.objects.get(id=id)
        form = OrderForm(request.POST)
        if form.is_valid():
            qs=form.cleaned_data.get("address")
            order.objects.create(order_item=data,customer=request.user,address=qs)
            return redirect("home")
        return redirect("cart")    
    
class OrderList(View):
    def get(self,request,*args,**kwargs):
        data = order.objects.filter(customer = request.user)
        return render(request,"store/view_order.html",{"data":data})    
    
class RemoveOrder(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        order.objects.get(id=id).delete()
        return redirect("cart")    



class CartDelete(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        CartModel.objects.get(id=id).delete()
        return redirect("home")
    
class SignOut(View):
  def get(self,request,*args,**kwargs):
    logout(request)
    return redirect("home")           




