import sys, json, mysql.connector, colorama

colorama.init()

try:
    db_config = json.loads(open("config.json", "r").read())["database"]
except:
    print(colorama.Fore.RED + "\nERROR:" + colorama.Fore.WHITE + "    Не удалось открыть и/или взять данные с \"config.json\"\n")
    sys.exit()

def db(execute):
    try:
        mysql_connect = mysql.connector.connect(user = db_config["user"], password = db_config["password"], host = db_config["host"], port = db_config["port"], database = db_config["database"])
        db = mysql_connect.cursor(dictionary=True)
        db.execute(execute)
        result = db.fetchall()
        db.close()
        mysql_connect.close()
        return result
    except Exception as err:
        print(f"\n{colorama.Fore.RED}ERROR:     {colorama.Fore.WHITE}Не удалось подключиться к серверу MySQL\n{colorama.Fore.YELLOW}REASON:    {colorama.Fore.WHITE}{err}\n")
        sys.exit()

