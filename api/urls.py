from rest_framework import routers

from QuanLyNhaSach.views.customer import CustomerViewSet, CustomerTypeViewSet
from QuanLyNhaSach.views.supplier import SupplierViewSet
from QuanLyNhaSach.views.merchandise import BookViewSet, BookTypeViewSet, StationeryTypeViewSet, StationeryViewSet
from QuanLyNhaSach.views.promotion import PromotionViewSet
from QuanLyNhaSach.views.store import StoreViewSet
from QuanLyNhaSach.views.stock_transfer_in import StockTransferInDetailViewSet, StockTransferInViewSet
from QuanLyNhaSach.views.stock_transfer_out import StockTransferOutDetailViewSet, StockTransferOutViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'customers-type', CustomerTypeViewSet, base_name='customer-type-api')
router.register(r'customers', CustomerViewSet, base_name='customer-api')
router.register(r'suppliers', SupplierViewSet, base_name='supplier-api')
router.register(r'books', BookViewSet, base_name='book-api')
router.register(r'stationeries', StationeryViewSet, base_name='stationery-api')
router.register(r'books-type', BookTypeViewSet, base_name='book-type-api')
router.register(r'stationeries-type', StationeryTypeViewSet, base_name='stationery-type-api')
router.register(r'promotions', PromotionViewSet, base_name='promotion-api')
router.register(r'stores', StoreViewSet, base_name='store-api')
router.register(r'stocktransferins', StockTransferInViewSet, base_name='stock-transfer-in-api')
router.register(r'stocktransferins-detail', StockTransferInDetailViewSet, base_name='stock-transfer-in-detail-api')
router.register(r'stocktransferouts', StockTransferOutViewSet, base_name='stock-transfer-out-api')
router.register(r'stocktransferouts-detail', StockTransferOutDetailViewSet, base_name='stock-transfer-out-detail-api')
