from pymongo import MongoClient


client = MongoClient(
            'mongodb+srv://**********:**********@cluster0.nzrg5.mongodb.net/'
            'myFirstDatabase?retryWrites=true&w=majority'
        )
db = client.module_12_hw
