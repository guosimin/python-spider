# 用于做随机header
import fake_useragent
from fake_useragent import UserAgent
class getHeader:
    def init(self):
        newUserAgent = UserAgent().random;
        headers = {'User-Agent': newUserAgent}
        return headers

getHeader = getHeader().init