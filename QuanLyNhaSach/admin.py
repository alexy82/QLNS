from django.contrib import admin
from QuanLyNhaSach.models import customer, stock_transfer_out, stock_transfer_in, promotion, supplier, merchandise

# Register your models here.
admin.site.register(merchandise.Merchandise)
admin.site.register(merchandise.MerchandiseType)
admin.site.register(customer.Customer)
admin.site.register(customer.CustomerType)
admin.site.register(supplier.Supplier)
admin.site.register(stock_transfer_in.StockTransferIn)
admin.site.register(stock_transfer_in.StockTransferInDetail)
admin.site.register(stock_transfer_out.StockTransferOutDetail)
admin.site.register(stock_transfer_out.StockTransferOut)
admin.site.register(promotion.Promotion)
