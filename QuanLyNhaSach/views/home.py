from datetime import datetime, timedelta
from QuanLyNhaSach.views.base import BaseITSAdminView
from django.db.models import Sum
from QuanLyNhaSach.models.stock_transfer_in import StockTransferIn
from QuanLyNhaSach.models.stock_transfer_out import StockTransferOut, StockTransferOutDetail
from QuanLyNhaSach.models.customer import Customer


def get_total_inbound_7days_ago():
    query = StockTransferIn.objects.filter(
        created_at__gte=(datetime.now() - timedelta(days=7)))
    result = sum([sum([detail.count for detail in item.list_detail.all()]) for item in query])
    return result


def get_total_outbound_7days_ago():
    query = StockTransferOut.objects.filter(
        created_at__gte=(datetime.now() - timedelta(days=7)))
    result = sum([sum([detail.count for detail in item.list_detail.all()]) for item in query])
    return result


def get_total_bill_7days_ago():
    return StockTransferOut.objects.filter(created_at__gte=(datetime.now() - timedelta(days=7))).count()


def get_total_income_7days_ago():
    query = StockTransferOut.objects.filter(created_at__gte=(datetime.now() - timedelta(days=7)))
    result = 0
    result += sum([item.total for item in query])
    return result


def get_data_chart_bill_7days_ago():
    query = StockTransferOut.objects.filter(created_at__gte=(datetime.now() - timedelta(days=7)))
    date_set = ([datetime.strftime(datetime.now() - timedelta(days=item), '%d-%m-%Y') for item in range(0, 7)])
    dict_data = {}
    for date in date_set:
        dict_data[date] = 0
    for item in query:
        dict_data[datetime.strftime(item.created_at, '%d-%m-%Y')] += 1
    return dict_data


def get_data_chart_money_7days_ago():
    query = StockTransferOut.objects.filter(created_at__gte=(datetime.now() - timedelta(days=7)))
    date_set = ([datetime.strftime(datetime.now() - timedelta(days=item), '%d-%m-%Y') for item in range(0, 7)])
    dict_data = {}
    for date in date_set:
        dict_data[date] = 0
    for item in query:
        dict_data[datetime.strftime(item.created_at, '%d-%m-%Y')] += item.total
    return dict_data


def get_top_best_seller():
    query = StockTransferOutDetail.objects.filter(
        inside__created_at__gte=(datetime.now() - timedelta(days=7))).values('unit__name', 'unit__id',
                                                                             'unit__merchandise_type').annotate(
        total=Sum('count') * 100).order_by('-total')
    length = query.count()
    if length < 10:
        return query[0:]
    else:
        return query[0:10]


class Home(BaseITSAdminView):

    def __init__(self):
        super(Home, self).__init__()
        self.template_name = 'pages/home.html'
        self.set_context_data(count_inbound=get_total_inbound_7days_ago(),
                              count_outbound=get_total_outbound_7days_ago(),
                              count_bill=get_total_bill_7days_ago(),
                              income=get_total_income_7days_ago(),
                              chart_bill=get_data_chart_bill_7days_ago(),
                              chart_money=get_data_chart_money_7days_ago(),
                              best_seller=get_top_best_seller())
