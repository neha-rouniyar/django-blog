from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from todolist.models import Todo
from rest_framework import viewsets
from todolist.serializers import TodoSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView
from rest_framework.generics import mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TodoFilter
def getlist(request):
    return render(request,'baseFile.html')



# # APIs using ViewSet and DEfault Router configuration **********************************************************************************************************************************
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter  


# # APIs using mixins **********************************************************************************************************************************
class TodoMixinsView(
    GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
    ):
    queryset=Todo.objects.all()
    serializer_class=TodoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter 
    def get(self,request,*args,**kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request)

    def post(self,request):
        return self.create(request)
    
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)



# # APIs using Generic views **********************************************************************************************************************************
class TodoListCreateGenericView(ListCreateAPIView):
    queryset=Todo.objects.all()
    serializer_class=TodoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter 


class TodoRetrieveUpdateDestroyGenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset=Todo.objects.all()
    serializer_class=TodoSerializer


# # APIs using APIView **********************************************************************************************************************************
class TodoAPIView(APIView):
    def get(self,request):
        # todoList=Todo.objects.all()
        # serializer=TodoSerializer(todoList,many=True)
        # return Response(serializer.data)


        # # this code while including pagination - PageNumberPagination
        # todoList = Todo.objects.all()
        # paginator = PageNumberPagination()
        # paginator.page_size = 5  
        # result = paginator.paginate_queryset(todoList, request)
        # serializer = TodoSerializer(result, many=True)
        # return paginator.get_paginated_response(serializer.data)


        # # this code while including pagination - LimitOffsetPagination
        # todoList = Todo.objects.all()
        # paginator = LimitOffsetPagination()
        # paginator.default_limit = 5  
        # result = paginator.paginate_queryset(todoList, request)
        # serializer = TodoSerializer(result, many=True)
        # return paginator.get_paginated_response(serializer.data)
    
        # # pagination along with filter for completed=True/False
        todoList = Todo.objects.all()
        todoList=TodoFilter(request.query_params,queryset=todoList).qs
        paginator = LimitOffsetPagination()
        paginator.default_limit = 5  
        result = paginator.paginate_queryset(todoList, request)
        serializer = TodoSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self,request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # data=request.data
        # title=data.get('title')
        # description=data.get('description')
        # completed=data.get('completed')
        # if not all(title,description,completed):
        #     return Response({"error":"All fields are required"},status=status.HTTP_400_BAD_REQUEST)
        
        # todo=Todo.objects.create(
        #     title=title,
        #     description=description,
        #     completed=completed
        # )
        # return Response(
        #     {
        #         "message":"Task Added Successfully",
        #         "todo":{
        #             "title":todo.title,
        #             "description":todo.description,
        #             "completed":todo.completed
        #         },
        #     },
        #     status=status.HTTP_201_created
        # )

class TodoDetailAPIView(APIView):
    def get(self,request,pk):
        try:
            todoList=Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=TodoSerializer(todoList)
        return Response(serializer.data)
    
    def put(self,request,pk):
        todoExistng=Todo.objects.get(pk=pk)
        serializer=TodoSerializer(todoExistng,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,pk):
        try:
            todo=Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



