from django.shortcuts import get_object_or_404,render
from .models import Product ,Review
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import ProductSerializer
from .filters import ProductsFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework import status
from django.db.models import Avg


@api_view(['GET'])
def get_all_products(request):
   #products = Product.objects.all()
   filterset = ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
   #serializer = ProductSerializer(products,many =True) # many = True <=> all products
   #--------
   count = filterset.qs.count()
   paginator =  PageNumberPagination()
   paginator.page_size = 3    # number pages 
   queryset = paginator.paginate_queryset(filterset.qs,request)
   #--------
   serializer = ProductSerializer(queryset,many =True)
   return Response({"product":serializer.data,"Number Products":count})

@api_view(['GET'])
def get_by_id_product(request,pk):
    product = get_object_or_404(product,id=pk)
    serializer= ProductSerializer(product,many=False)
    return Response({"product":serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def new_product(request):
   data = request.data 
   serializer= ProductSerializer(data = data)
   
   if serializer.is_valid():
      product = Product.objects.create(**data,user=request.user)
      res = ProductSerializer(product , many =False)
      return Response({'product':res.data})
   else:
      return Response(serializer.errors)
   
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])

def update_product(request,pk):
   product=get_by_id_product(Product,id=pk)
   if product.user != request.user :
      return Response({"error":"Sorry you can not update this product"},
                      status=status.HTTP_403_FORBIDDEN)
   product.name = request.data['name']
   product.description =request.data['description']
   product.price=request.data['price']
   product.brand =request.data['brand']
   product.category= request.data['category']
   product.ratings =request.data['ratings ']
   product.stock =request.data['stock']
   product.save()
   serilaizers= ProductSerializer(product,many=False)
   return Response({'product':serilaizers.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])

def delete_product(request,pk):
   product=get_by_id_product(Product,id=pk)
   if product.user != request.user :
      return Response({"error":"Sorry you can not update this product"},
                      status=status.HTTP_403_FORBIDDEN)
   product.delete()
   return Response({'details':'Delete is done '}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request,pk):
   user = request.user
   product = get_object_or_404(request,pk)
   data = request.data
   review= product.reviews.filter(user = user)
   
   if data['rating']<0 or data['rating']>10:
      return Response({'error':'please select betwen 0 to 10 only'} 
                      ,status= status.HTTP_400_BAD_REQUEST)
   elif review.exists():
      new_review = {'rating':data['rating'], 'comment':data['comment']}
      review.update(**new_review)

      rating = product.reviews.aggregate(avg_rating= Avg('rating'))
      product.rating = rating['avg_rating']
      product.save()
      return Response({'details':'Product review created'})
   else :
      Review.objects.create(
         user = user,
         product =product,
         rating = data['rating'],
         comment = data['comment']
         )
      rating = product.reviews.aggregate(avg_rating= Avg('rating'))
      product.rating = rating['avg_rating']
      product.save()
      return Response({'details':'Product review created'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
   user = request.user
   product = get_object_or_404(request,pk)
   review= product.reviews.filter(user = user)
   
   if review.exists():
      review.delete()
      rating = product.reviews.aggregate(avg_rating= Avg('rating'))
      if rating['avg_rating'] is None:
        rating['avg_rating']=0
        product.rating = rating['avg_rating']
        product.save()
        return Response({'details':'Product review Delete'})
   else :
      return Response({'errore':'Review Not Found'},status=status.HTTP_404_NOT_FOUND)

