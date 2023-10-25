import os

cmd = """waitress-serve --host 127.0.0.1 --port 8080 --ident "Foody WebApplication" app:app """

os.system(cmd)