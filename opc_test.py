import opcua
import asyncio

plc = opcua.Client("opc.tcp://192.168.20.50:4840")

async def read_var():

    while True:
        try:
            plc.connect()
            value = plc.get_node("ns=4; s=|var|PLC210 OPC-UA.Application.PLC_PRG.i").get_value()
            print(f"plc_value:{value}")
        except Exception as e:
            print(f"Ошибка: {e}") 
        finally:
            plc.disconnect()              

        await asyncio.sleep(1) 


async def sum_var():
    while True:
        print("это вызов другой задачи")
        await asyncio.sleep(1)         

async def main():
    task1 = asyncio.create_task(read_var())
    task2 = asyncio.create_task(sum_var())    
    await task1
    await task2    

if __name__ == "__main__":
    asyncio.run(main())
