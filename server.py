import grpc
import time
from concurrent import futures
from todolist_pb2 import (Todo,
                           TodoList,
                           OperationTodoResponse)
from todolist_pb2_grpc import (TodoServiceServicer,
                                add_TodoServiceServicer_to_server)
from database.connection import db_session
from database import models


class TodoServiceServicer(TodoServiceServicer):

    def GetAllTodos(self, request, context):
        todolist = []
        try:
            with db_session() as session:
                todos = session.query(models.Todo).all()
                if todos:
                    todolist = [Todo(**todo.asdict()) for todo in todos]
        except Exception as e:
            print("Exception occured,{0}".format(e.__str__()))
        return TodoList(todos=todolist)


    def GetTodo(self, request, context):
        todo_response = Todo()
        try:
            with db_session() as session:
                todo = session.query(models.Todo).get(request.id)
                todo_response = Todo(**todo.asdict())
        except Exception as e:
            print("Exception occured,{0}".format(e.__str__()))
        return todo_response


    def CreateTodo(self, request, context):
        todo_response = Todo()
        try:
            with db_session() as session:
                todo = models.Todo(id = request.id,
                                name = request.name)
                session.add(todo)
                todo_response = Todo(**todo.asdict())
        except Exception as e:
             print("Exception occured,{0}".format(e.__str__()))
             return OperationTodoResponse(op_status=OperationTodoResponse.ERROR)
        return OperationTodoResponse(todo=todo_response, op_status=OperationTodoResponse.CREATED)


    def DeleteTodo(self, request, context):
        todo = None
        try:
            with db_session() as session:   
                todo = session.query(models.Todo).get(request.id)
                todo.is_active = False
                todo_response = Todo(**todo.asdict())
        except Exception as e:
            return OperationTodoResponse(op_status = OperationTodoResponse.ERROR)
        return OperationTodoResponse(todo=todo_response, op_status=OperationTodoResponse.DELETED)


    def UpdateTodo(self, request, context):
        response = None
        try:
            with db_session() as session:
                todo = session.query(models.Todo).get(request.id)
                todo.name = request.name
                todo.is_completed = request.is_completed
                response = OperationTodoResponse(todo=Todo(**todo.asdict()), op_status = OperationTodoResponse.UPDATED)
        except Exception as e:
            response = OperationTodoResponse(op_status = OperationTodoResponse.ERROR)
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

add_TodoServiceServicer_to_server(
        TodoServiceServicer(), server)


print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()


try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)