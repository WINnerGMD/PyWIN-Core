prefix = "!"

while True:
        console = input("")
        if f"{prefix}setup" in console:
                spliter = console.split(" ")
                print(f"spliter = {spliter}")
                args = 0
                for i in spliter:
                    args += 1
                args -= 1
                if args == 1:
                      print(spliter[1])
                else:
                       print("аргументов не 1")
        else:
               print("неизвестный запрос")