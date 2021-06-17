from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
# class flaskApp():
#     def __init__(self):
#         print('flaskApp')
#         self.app = Flask(__name__)
#         self.app.config.from_object('config')
    # def app(self):
    #     #     print('flaskApp app')
    #     #     return self.app1