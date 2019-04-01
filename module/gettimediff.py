import requests,threading,datetime,time
class gettimediff:
    # 计算时间差,格式: 时分秒
    # @param start 开始时间
    # @param end 结束时间
    def init(self,start, end):
        seconds = (end - start).seconds
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        diff = ("%02d:%02d:%02d" % (h, m, s))
        return diff

gettimediff = gettimediff().init