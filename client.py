import grpc
from todolist_pb2_grpc import TodoServiceStub
from todolist_pb2 import Todo, EmptyRequest

channel = grpc.insecure_channel('localhost:50051')
stub = TodoServiceStub(channel)

# print("Creating TODOs")
# print(stub.CreateTodo(Todo(id=1, name='first todo')))
# print(stub.CreateTodo(Todo(id=2, name='second todo')))
# print(stub.CreateTodo(Todo(id=3, name='third todo')))

print("----------- ALL TODOs -----------")
print(stub.GetAllTodos(EmptyRequest()))

print("-----------  GET TODO -------------")
todo = stub.GetTodo(Todo(id=2))
print(todo)
todo.is_completed = True
resp = stub.UpdateTodo(todo)

print("--------- TODO updated -----------")
print(stub.GetTodo(Todo(id=2)))

d_resp = stub.DeleteTodo(Todo(id=3))
print("---------- TODO DELETED -----------")
print(d_resp)

print("----------- ALL TODOs -----------")
response = stub.GetAllTodos(EmptyRequest())
print(response)