from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from .serializers import ProductSerializer, CartSerializer, CategorySerializer, UserLoginSerializer,UserRegistrSerializer, OrderSerializer
from .models import Category, Cart, Product, MyUserManager, User, Order
from rest_framework.generics import CreateAPIView
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication


class RegUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['data']= serializer.data
            user = serializer.user
            token = Token.objects.create(user=user)
            print(token)
            return Response({'user_token': token.key}, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
@authentication_classes([TokenAuthentication,])
def OrderListView(request):
    if request.method == 'GET':
        Orders = Order.objects.all()
        serializer = OrderSerializer(Orders, many=True)
        return Response({'data': serializer.data}, status=HTTP_200_OK)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'order_id': serializer.data('id'),
                'message': 'OK'
                    }
            return Response(data,status=HTTP_201_CREATED)
        return Response(serializer.errors)

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser,])
@authentication_classes([TokenAuthentication,])
def OrderDitaliView(request, pk):
    try:
        orders = Order.objects.get(pk=pk)
    except:
        return Response(status=HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = OrderSerializer(orders)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderSerializer(orders, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer =OrderSerializer(orders, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=HTTP_200_OK)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        orders.delete()
        return Response({'data': {'messager': 'remove'}})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
@authentication_classes([TokenAuthentication,])
def CartListview(request):
    if request.method == 'GET':
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response({'data': serializer.data}, status=HTTP_200_OK)
    elif request.method == "POST":
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'cart_id': serializer.data('id'),
                'message': 'OK'
                    }
            return Response(data,status=HTTP_201_CREATED)
        return Response(serializer.errors)

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated,])
@authentication_classes([TokenAuthentication,])
def CartDetilView(request, pk):
    try:
        carts = Cart.ojects.get(pk=pk)
    except:
        return Response(status=HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CartSerializer(carts)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CartSerializer(carts, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = CartSerializer(carts, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=HTTP_200_OK)
    elif request.method == 'DELETE':
        carts.delete()
        return Response({'data': {'messager': 'remove'}})


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly,])
@authentication_classes([TokenAuthentication,])
def ProductListView(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'data': serializer.data}, status=HTTP_200_OK)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser,])
@authentication_classes([TokenAuthentication,])
def ProductDetilView(request, pk):
    try:
        products = Product.objects.get(pk=pk)
    except:
        return Response(status=HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(products)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(products, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = ProductSerializer(products,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=HTTP_200_OK)
    elif request.method == 'DELETE':
        products.delete()
        return Response({'data':{'message':'remove'}})

class LoginUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    def post(self, request: WSGIRequest, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return JesonResponse({
                'error': {
                    'code': 401,
                    'message': 'Authentication failed'
                }
            })
        user =serializer.validated_data
        if user:
            token_object, token_created = Token.get_or_create(user=user)
            token = token_object if token_object else token_created

            return Response({'user_token':token.key}, status=HTTP_200_OK)
        return Response({'error':{'message':'Authentication failed'}})