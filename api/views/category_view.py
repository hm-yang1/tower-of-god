from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models.category import Category
from ..serial.category_serializer import CatergorySerializer

class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CatergorySerializer
    permission_classes = [AllowAny]
    