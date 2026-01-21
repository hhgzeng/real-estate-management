from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
from django.db.models import Count, Sum
from orders.models import Order

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # 验证用户名和密码
            user = User.objects.filter(username=username, password=password).first()
            if user:
                return JsonResponse({
                    'status': 'success',
                    'role': user.role,
                    'message': 'Login successful',
                    'user_id': user.id,          # 返回用户ID
                    'username': user.username,   # 返回用户名
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid username or password'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Server error'}, status=500)

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists'}, status=400)
        User.objects.create(username=username, password=password, role=role)
        return JsonResponse({'message': 'Registration successful'})

def get_salespeople(request):
    if request.method == 'GET':
        salespeople = User.objects.filter(role='salesperson').annotate(
            sales_count=Count('salesperson_orders'),
            sales_amount=Sum('salesperson_orders__house__price')
        )
        data = []
        for sp in salespeople:
            data.append({
                'id': sp.id,
                'username': sp.username,
                'sales_count': sp.sales_count or 0,
                'sales_amount': str(sp.sales_amount or 0)
            })
        return JsonResponse(data, safe=False)

@csrf_exempt
def manage_salesperson(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            username = data.get('username')
            password = data.get('password')  # 新增密码字段

            if action == 'create':
                if not username or not password:  # 检查用户名和密码是否都提供
                    return JsonResponse({
                        'message': '用户名和密码都是必填的',
                        'status': 'error'
                    }, status=400)

                if User.objects.filter(username=username).exists():
                    return JsonResponse({
                        'message': '用户名已存在',
                        'status': 'error'
                    }, status=400)

                User.objects.create(
                    username=username,
                    password=password,  # 使用提供的密码
                    role='salesperson'
                )
                return JsonResponse({
                    'message': '销售人员创建成功',
                    'status': 'success'
                })
            elif action == 'delete':
                salesperson_id = data.get('salesperson_id')
                if not salesperson_id:
                    return JsonResponse({
                        'message': '未提供销售人员ID',
                        'status': 'error'
                    }, status=400)

                try:
                    salesperson = User.objects.get(id=salesperson_id, role='salesperson')
                    salesperson.delete()
                    return JsonResponse({
                        'message': '销售人员删除成功',
                        'status': 'success'
                    })
                except User.DoesNotExist:
                    return JsonResponse({
                        'message': '销售人员不存在',
                        'status': 'error'
                    }, status=404)
            else:
                return JsonResponse({
                    'message': '无效的操作',
                    'status': 'error'
                }, status=400)
        except Exception as e:
            print(f"管理销售人员时发生错误: {str(e)}")
            return JsonResponse({
                'message': '服务器错误',
                'status': 'error'
            }, status=500)

@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            old_password = data.get('old_password')
            new_password = data.get('new_password')

            # 验证所有必需字段都已提供
            if not all([user_id, old_password, new_password]):
                return JsonResponse({
                    'status': 'error',
                    'message': '所有字段都是必需的'
                }, status=400)

            # 获取用户
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': '用户不存在'
                }, status=404)

            # 验证旧密码
            if user.password != old_password:
                return JsonResponse({
                    'status': 'error',
                    'message': '旧密码不正确'
                }, status=400)

            # 更新密码
            user.password = new_password
            user.save()

            return JsonResponse({
                'status': 'success',
                'message': '密码修改成功'
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': '无效的JSON数据'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': '不支持的请求方法'
    }, status=405)
