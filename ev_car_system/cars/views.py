# cars/views.py
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'detail': '用户名和密码不能为空'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 获取或创建 Token（使用 DRF 的 Token）
            from rest_framework.authtoken.models import Token
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        else:
            return JsonResponse({'detail': '用户名或密码错误'}, status=400)
    except Exception as e:
        return JsonResponse({'detail': '请求格式错误'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email', '')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'detail': '用户名和密码不能为空'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username': ['该用户名已存在']}, status=400)

        if email and User.objects.filter(email=email).exists():
            return JsonResponse({'email': ['该邮箱已被使用']}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        # 登录并返回 token
        login(request, user)
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({'detail': '注册失败'}, status=400)