from django.http import JsonResponse
from .models import House
from accounts.models import User
from django.views.decorators.csrf import csrf_exempt
import json

def get_houses(request):
    if request.method == 'GET':
        houses = House.objects.select_related('salesperson').filter(status='available')
        data = []
        for house in houses:
            data.append({
                'id': house.id,
                'price': str(house.price),
                'area': str(house.area),
                'floor': house.floor,
                'status': house.status,
                'salesperson_id': house.salesperson.id,
                'salesperson_name': house.salesperson.username,
                'house_info': f"{house.area}㎡ {house.floor}层"
            })
        return JsonResponse(data, safe=False)

@csrf_exempt
def update_house(request, house_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            price = data.get('price')
            area = data.get('area')
            floor = data.get('floor')
            salesperson_id = data.get('salesperson_id')

            # 检查数据合法性
            if not all([price, area, floor, salesperson_id]):
                return JsonResponse({
                    'message': '所有字段都是必填的',
                    'status': 'error'
                }, status=400)

            try:
                # 转换数据类型
                price = float(price)
                area = float(area)
                floor = int(floor)
                salesperson_id = int(salesperson_id)
            except (ValueError, TypeError):
                return JsonResponse({
                    'message': '数据格式不正确',
                    'status': 'error'
                }, status=400)

            # 检查房产是否存在
            try:
                house = House.objects.get(id=house_id)
            except House.DoesNotExist:
                return JsonResponse({
                    'message': '房产不存在',
                    'status': 'error'
                }, status=404)

            # 检查销售员是否存在
            try:
                salesperson = User.objects.get(id=salesperson_id, role='salesperson')
            except User.DoesNotExist:
                return JsonResponse({
                    'message': '销售人员不存在',
                    'status': 'error'
                }, status=400)

            # 更新房产信息
            house.price = price
            house.area = area
            house.floor = floor
            house.salesperson = salesperson
            house.save()

            return JsonResponse({
                'message': '房产信息更新成功',
                'status': 'success'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'message': '无效的JSON数据',
                'status': 'error'
            }, status=400)
        except Exception as e:
            print(f"更新房产时发生错误: {str(e)}")
            return JsonResponse({
                'message': '服务器错误',
                'status': 'error'
            }, status=500)

@csrf_exempt
def create_house(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            price = data.get('price')
            area = data.get('area')
            floor = data.get('floor')
            salesperson_id = data.get('salesperson_id')

            # 检查数据合法性
            if not all([price, area, floor, salesperson_id]):
                return JsonResponse({
                    'message': '所有字段都是必填的',
                    'status': 'error'
                }, status=400)

            try:
                # 转换数据类型
                price = float(price)
                area = float(area)
                floor = int(floor)
                salesperson_id = int(salesperson_id)
            except (ValueError, TypeError):
                return JsonResponse({
                    'message': '数据格式不正确',
                    'status': 'error'
                }, status=400)

            # 检查销售员是否存在
            try:
                salesperson = User.objects.get(id=salesperson_id, role='salesperson')
            except User.DoesNotExist:
                return JsonResponse({
                    'message': '销售人员不存在',
                    'status': 'error'
                }, status=400)

            # 创建房产
            house = House.objects.create(
                price=price,
                area=area,
                floor=floor,
                salesperson=salesperson,
                status='available'
            )

            return JsonResponse({
                'message': '房产创建成功',
                'status': 'success',
                'house_id': house.id
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'message': '无效的JSON数据',
                'status': 'error'
            }, status=400)
        except Exception as e:
            print(f"创建房产时发生错误: {str(e)}")  # 服务器端日志
            return JsonResponse({
                'message': '服务器错误',
                'status': 'error'
            }, status=500)


def my_houses(request):
    """
    GET /houses/my_houses/?salesperson_id=xxx
    """
    if request.method == 'GET':
        salesperson_id = request.GET.get('salesperson_id')
        houses = House.objects.filter(salesperson_id=salesperson_id)
        data = []
        for h in houses:
            data.append({
                'id': h.id,
                'price': str(h.price),
                'area': str(h.area),
                'floor': h.floor,
                'status': h.status,
            })
        return JsonResponse(data, safe=False)

@csrf_exempt
def delete_house(request, house_id):
    if request.method == 'POST':
        try:
            house = House.objects.get(id=house_id)
            if house.status != 'available':
                return JsonResponse({
                    'message': '只能删除在售房产',
                    'status': 'error'
                }, status=400)
            
            house.delete()
            return JsonResponse({
                'message': '房产删除成功',
                'status': 'success'
            })
        except House.DoesNotExist:
            return JsonResponse({
                'message': '房产不存在',
                'status': 'error'
            }, status=404)
        except Exception as e:
            print(f"删除房产时发生错误: {str(e)}")
            return JsonResponse({
                'message': '服务器错误',
                'status': 'error'
            }, status=500)
