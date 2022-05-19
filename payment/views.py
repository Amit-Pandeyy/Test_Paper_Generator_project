from django.shortcuts import redirect, render
from django.conf import settings
from .models import Transaction, Coupon
from .paytm import generate_checksum, verify_checksum
from django.contrib import messages
from register_login.models import School,Teacher,User1
from django.contrib.auth.decorators import login_required


def verify_amount(amount):
    if(amount>0):
        return True
    return False

def payment(request):
    return render(request, 'payment.html')

def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST['amount'])

        if not verify_amount(amount):
            messages.info(request, 'Enter Valid Amount')
            return redirect('teacher_dashboard')

        user = request.user
        transaction = Transaction.objects.create(user=user, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.user.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', settings.BASE_URL+'/payment/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        return render(request, 'redirect.html', context=paytm_params)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
        transaction = Transaction.objects.filter(order_id = received_data['ORDERID'][0]).first()
        user = transaction.user
        transaction.paytm_status = received_data
        print(received_data)
        if (received_data['RESPCODE'][0] == '01' and received_data['message'] == "Checksum Matched"):
            user.credit+=int(float(received_data['TXNAMOUNT'][0]))
            user.save()
            transaction.success = True
        transaction.save()

        messages.info(request, "Status : "+received_data['RESPMSG'][0])
        return redirect('teacher_dashboard')


def verify_code(user, code):
    if Coupon.objects.filter(coupon_code = code).exists():
        coupon_object = Coupon.objects.filter(coupon_code = code).first()
        if user in coupon_object.user.all():
            return False
        else:
            return True
    return False

@login_required
def verify_coupon(request):
    user = request.user
    if request.method == 'POST':
        coupon_code = request.POST['coupon_code']
        if(verify_code(user, coupon_code)):
            coupon_object = Coupon.objects.filter(coupon_code = coupon_code).first()
            amount = coupon_object.amount
            coupon_object.user.add(user)
            coupon_object.save()
            user.credit+=amount
            user.save()
            messages.success(request, "Success : "+str(amount)+" credits added successfully")
            if user.is_teacher:
                return redirect('teacher_dashboard')
            else:
                return redirect('school_dashboard')
        else:
            messages.info(request, "Invalid Coupon Code")
            if user.is_teacher:
                return redirect('teacher_dashboard')
            else:
                return redirect('school_dashboard')
    else:
        if user.is_teacher:
            return redirect('teacher_dashboard')
        else:
            return redirect('school_dashboard')

