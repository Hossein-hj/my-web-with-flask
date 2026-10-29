# posts = [
#     {
#         '_id' : 1,
#         'title': 'red toyota',
#         'discription': 'beutiful color!!!!!',
#         'pic': 'toyota0.jpg',
#         'comments': [
#             {'autor': 'ali', 'comment': 'bad'},
#             {'autor': 'mmd', 'comment': 'price?'},
#             {'autor': 'sina', 'comment': 'wow '},
#             {'autor': 'ahoo', 'comment': 'nice name model?'}]
#     },
#     {
#         '_id': 2,
#         'title': 'toyota',
#         'discription': ' my car is best!!!!',
#         'pic': 'toyota1.jpg',
#         'comments': [
#             {'autor': 'ali', 'comment': 'goood'},
#             {'autor': 'reza', 'comment': 'yeeeees'},
#             {'autor': 'ahmad', 'comment': 'No is not good '},
#             {'autor': 'parsa', 'comment': 'yes'}
#         ]
#     },
#     {
#         '_id': 3,
#         'title': 'for sell ',
#         'discription': 'this is my toyota ',
#         'pic': 'toyota2.jpg',
#     },
#     {
#         '_id': 4,
#         'title': 'who need?',
#     },
#     {
#         '_id': 5,
#         'title': 'is ladcruiser👍 ',
#         'discription': 'wow best offroad car👌',
#         'pic': 'toyota3.jpg',
#     },
# ]


import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["weblog"]
mycol = mydb["user"]

z = mycol.find()
for i in z:
    print(i)

