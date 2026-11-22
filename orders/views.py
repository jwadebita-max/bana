from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Order
from product.models import FoodItem


def create_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity', 1)
        order_type = request.POST.get('order_type', 'Individual')

        # البحث عن الطبق المطلوب
        food_item = get_object_or_404(FoodItem, id=product_id) if product_id else None

        # ربط الطلب بالمستخدم الحالي إذا كان مسجلاً للدخول
        current_user = request.user if request.user.is_authenticated else None

        # إنشاء وحفظ الطلبية مع حفظ الـ user
        Order.objects.create(
            user=current_user,
            food_item=food_item,
            full_name=full_name,
            phone_number=phone,
            delivery_address=address,
            dish_counter=quantity,
            request_type=order_type
        )

        messages.success(request, 'تم إرسال طلبك بنجاح! سنتصل بك قريباً.')
        return redirect(request.META.get('HTTP_REFERER', 'all'))

    return redirect('all')


@login_required(login_url='login')
def customer_dashboard(request):
    # جلب الطلبيات الخاصة بالمستخدم الحالي فقط
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # 🌟 تصفير وإبداء رؤية الطلبات الجديدة (تختفي شارة العداد من الـ Header)
    Order.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

    # حساب مجموع الطلبات الحقيقي
    total_orders = user_orders.count()

    # حساب مجموع المصاريف (سعر المنتج × الكمية لكل طلب)
    total_spent = sum((order.food_item.price * order.dish_counter) for order in user_orders if order.food_item)

    context = {
        'orders': user_orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    return render(request, 'pages/customer_dashboard.html', context)


# 🌟 1. دالة تسجيل حساب جديد (Register)
def register_user(request):
    if request.user.is_authenticated:
        return redirect('customer_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # التحقق من أن اسم المستخدم غير مستعمل من قبل
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken. Please choose another one.')
            return render(request, 'pages/register.html')

        # إنشاء المستخدم الجديد
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # تسجيل الدخول تلقائياً بعد إنشاء الحساب
        login(request, user)
        messages.success(request, f'Welcome to BENNA, {user.username}!')
        return redirect('customer_dashboard')

    return render(request, 'pages/register.html')


# 🌟 2. دالة تسجيل الدخول (Login)
def login_user(request):
    if request.user.is_authenticated:
        return redirect('customer_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            # التوجيه للتحويل للصفحة المباشرة أو الصالة الشخصية
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('customer_dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'pages/login.html')


# 🌟 3. دالة تسجيل الخروج (Logout)
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('all')