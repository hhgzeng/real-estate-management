from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from orders.models import Order
from houses.models import House
from accounts.models import User
from django.db.models import Count, Sum
import qrcode
import os
from datetime import datetime
import base64
from io import BytesIO
from django.core.cache import cache

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            house_id = data.get('house_id')
            customer_id = data.get('customer_id')

            house = House.objects.filter(id=house_id, status='available').first()
            if not house:
                return JsonResponse({'message': 'House not available', 'status': 'error'}, status=400)

            customer = User.objects.filter(id=customer_id, role='customer').first()
            if not customer:
                return JsonResponse({'message': 'Invalid customer ID', 'status': 'error'}, status=400)

            # 创建订单
            Order.objects.create(house=house, customer=customer, salesperson=house.salesperson)

            # 更新房产状态
            house.status = 'sold'
            house.save()

            return JsonResponse({'message': 'Order created successfully', 'status': 'success'})
        except Exception as e:
            return JsonResponse({'message': 'Server error', 'status': 'error'}, status=500)
        
from django.http import JsonResponse
from .models import Order

def get_sales_records(request):
    if request.method == 'GET':
        orders = Order.objects.all().values(
            'id', 'house__id', 'house__price', 'house__area', 'house__floor',
            'customer__username', 'salesperson__username', 'order_date'
        )
        return JsonResponse(list(orders), safe=False)

def my_orders(request):
    """
    GET /orders/my_orders/?customer_id=xxx
    """
    if request.method == 'GET':
        customer_id = request.GET.get('customer_id')
        orders = (Order.objects
                  .filter(customer_id=customer_id)
                  .select_related('house', 'salesperson'))
        data = []
        for o in orders:
            data.append({
                'id': o.id,
                'house_info': f"{o.house.area}㎡ {o.house.floor}层",
                'price': str(o.house.price),
                'salesperson_name': o.salesperson.username,
                'order_date': o.order_date,
            })
        return JsonResponse(data, safe=False)

@csrf_exempt
def my_sales(request):
    """获取销售人员的销售记录"""
    if request.method == 'GET':
        try:
            salesperson_id = request.GET.get('salesperson_id')
            if not salesperson_id:
                return JsonResponse({
                    'message': '未提供销售人员ID',
                    'status': 'error'
                }, status=400)

            # 获取该销售人员的所有订单
            orders = Order.objects.filter(salesperson_id=salesperson_id).values(
                'id',
                'house__id',
                'house__price',
                'house__area',
                'house__floor',
                'customer__username',  # 添加客户用户名
                'order_date'
            ).order_by('-order_date')  # 按时间倒序排序

            # 处理返回的数据
            sales_records = []
            for order in orders:
                sales_records.append({
                    'id': order['id'],
                    'house_info': f"面积:{order['house__area']}㎡, 楼层:{order['house__floor']}层",
                    'customer_name': order['customer__username'],  # 添加客户名字
                    'price': order['house__price'],
                    'order_date': order['order_date']
                })

            return JsonResponse(sales_records, safe=False)
        except Exception as e:
            return JsonResponse({
                'message': str(e),
                'status': 'error'
            }, status=500)

@csrf_exempt
def sales_stats(request):
    """获取销售人员的销售统计信息"""
    if request.method == 'GET':
        try:
            salesperson_id = request.GET.get('salesperson_id')
            if not salesperson_id:
                return JsonResponse({
                    'message': '未提供销售人员ID',
                    'status': 'error'
                }, status=400)

            # 获取该销售人员的所有订单
            orders = Order.objects.filter(salesperson_id=salesperson_id)
            
            # 计算总销售数量
            total_sales = orders.count()
            
            # 计算总销售金额
            total_amount = orders.aggregate(
                total=Sum('house__price')
            )['total'] or 0

            return JsonResponse({
                'status': 'success',
                'totalSales': total_sales,
                'totalAmount': float(total_amount)
            })
        except Exception as e:
            print(f"获取销售统计时发生错误: {str(e)}")
            return JsonResponse({
                'message': '服务器错误',
                'status': 'error'
            }, status=500)
    
@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            house_id = data.get('house_id')
            amount = data.get('amount')
            
            # 生成唯一的订单号
            order_number = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # 读取预设的微信收款码图片
            try:
                with open('real_estate/static/wechat_qr.png', 'rb') as img_file:
                    img_data = img_file.read()
                    img_str = base64.b64encode(img_data).decode()
            except FileNotFoundError:
                return JsonResponse({
                    'status': 'error',
                    'message': '收款码图片未找到'
                }, status=500)
            
            return JsonResponse({
                'status': 'success',
                'order_number': order_number,
                'qr_code': img_str
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': '不支持的请求方法'}, status=405)

@csrf_exempt
def payment_callback(request):
    """支付回调接口"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_number = data.get('order_number')
            
            return JsonResponse({
                'status': 'success',
                'message': '支付成功'
            })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': '不支持的请求方法'}, status=405)
    