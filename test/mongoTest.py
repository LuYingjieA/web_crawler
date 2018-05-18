#coding=utf8
import sys
from pymongo import MongoClient


fromdb = sys.argv[1]
todb = sys.argv[2]
fromhost = sys.argv[3]
client_to = MongoClient("127.0.0.1", 27017)
# client_from = MongoClient("192.168.89.129", 21119)
client_to.admin.command('copydb', fromdb=fromdb, todb=todb, fromhost=fromhost)