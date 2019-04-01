# 基础包等,模拟请求，多线程
import requests,threading,datetime,time
from bs4 import BeautifulSoup
import random

# 用于数据库存储
import pymongo
from pymongo import MongoClient

# 正则
import re

#
import html

#自定义模块
from module.handleData import handleData
from module.getHeader import getHeader
from module.gettimediff import gettimediff
from module.getIp import getAgentIp