from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from todolist.models import Todo
from todolist.serializers import TodoSerializer


def getlist(request):
    return render(request,'baseFile.html')



# # APIs using APIView **********************************************************************************************************************************
class TodoAPIView(APIView):
    def get(self,request):
        todoList=Todo.objects.all()
        serializer=TodoSerializer(todoList,many=True)
        return Response(serializer.data)
    
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