"""
用户认证视图
提供注册和登录功能
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


@csrf_exempt
def register_view(request):
    """
    用户注册接口
    POST /api/register/
    请求参数: {username, password, email}
    """
    if request.method != 'POST':
        return JsonResponse({'code': 405, 'message': '请求方法错误'}, status=405)
    
    try:
        # 解析请求数据
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        email = data.get('email', '').strip()
        
        # 验证必填字段
        if not username or not password:
            return JsonResponse({'code': 400, 'message': '用户名和密码不能为空'}, status=400)
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({'code': 400, 'message': '用户名已存在'}, status=400)
        
        # 检查邮箱是否已存在
        if email and User.objects.filter(email=email).exists():
            return JsonResponse({'code': 400, 'message': '邮箱已被注册'}, status=400)
        
        # 创建用户
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        return JsonResponse({
            'code': 200,
            'message': '注册成功',
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'code': 400, 'message': '请求数据格式错误'}, status=400)
    except Exception as e:
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)


@csrf_exempt
def login_view(request):
    """
    用户登录接口
    POST /api/login/
    请求参数: {username, password}
    """
    if request.method != 'POST':
        return JsonResponse({'code': 405, 'message': '请求方法错误'}, status=405)
    
    try:
        # 解析请求数据
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # 验证必填字段
        if not username or not password:
            return JsonResponse({'code': 400, 'message': '用户名和密码不能为空'}, status=400)
        
        # 验证用户
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # 登录成功
            login(request, user)
            
            return JsonResponse({
                'code': 200,
                'message': '登录成功',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'token': f'user_{user.id}_{user.username}'  # 简化的token，实际项目应使用JWT
                }
            })
        else:
            return JsonResponse({'code': 401, 'message': '用户名或密码错误'}, status=401)
        
    except json.JSONDecodeError:
        return JsonResponse({'code': 400, 'message': '请求数据格式错误'}, status=400)
    except Exception as e:
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)
