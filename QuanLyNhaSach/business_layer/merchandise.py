from QuanLyNhaSach.models.merchandise import Merchandise


class MerchandiseHelper(object):

    @staticmethod
    def get_available_count(id):
        obj = Merchandise.objects.filter(id=id)
        if obj.count() == 0:
            return -1
        return obj[0].available_count

    @staticmethod
    def get_unit_safety(id):
        obj = Merchandise.objects.filter(id=id)
        if obj.count() == 0:
            return None
        return obj[0]
