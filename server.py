import time
from opcua import ua, Server

if __name__ == "__main__":
    # --- Настроки сервера
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840") # Listen on all interfaces, port 4840
    
    # Имя сервера
    server.set_server_name("MyAwesomeOPCUAServer")

    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)
    
    # Говорим, что у нас обьекты
    objects = server.get_objects_node()

    # Добавляем папку MyObject
    my_object = objects.add_object(idx, "MyObject")
    my_variable = my_object.add_variable(idx, "MyVariable", 0.0)  
    my_variable1 = my_object.add_variable(idx, "MyVariable1", 0.0)  
    my_variable.set_writable()
    my_variable1.set_writable()    

    # --- Start the server ---
    server.start()
    print(f"Server started at {server.endpoint}")
    print("Press Ctrl-C to exit")

    try:
        count = 0
        while True:
            time.sleep(1)
            count += 0.1
            my_variable.set_value(count)
            my_variable1.set_value(count)            
    except KeyboardInterrupt:
        pass
    finally:
        # --- Stop the server ---
        server.stop()
        print("Server stopped")
