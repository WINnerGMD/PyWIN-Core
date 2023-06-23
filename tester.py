class WebServer:
    def __init__(self):
        self.doit = {}

    def command(self,test):

        def decorator(function, *args):
            self.doit["func"] = function
            self.doit["args"] = args
        print(self.doit)
        return decorator

    def run(self):
        print(self.doit)
        print('Server is running')
        for i,key in enumerate(self.doit):
            print(i, key)
            self.doit[key]()

app = WebServer()

@app.command()
def hui(args):
    print(f"sprot {args}")
# if __name__ == "__main__":
#     app.run()