import datetime
from django.http import JsonResponse
from QuanLyNhaSach.models.promotion import Promotion


def check_promotion(request):
    promotion_code = request.GET['promotion_code']
    total = request.GET['total']
    if promotion_code == "":
        return JsonResponse({'status': 0})
    else:
        query = Promotion.objects.filter(code=promotion_code)
        if query.count() == 0:
            return JsonResponse({'status': 1})
        promotion = query[0]
        if promotion.min > int(total) or datetime.date.today() > promotion.date_expired or promotion.is_used:
            return JsonResponse({'status': 1})
        else:
            return JsonResponse({'status': 2, 'value': {'id': promotion.id, 'discount': promotion.money_discount,
                                                        'min': promotion.min}})
