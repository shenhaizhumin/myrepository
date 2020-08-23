from datetime import datetime
import time

# now = datetime.now()
#
# print(now.strftime("%Y--%m--%d %H:%M:%S"))
# print(time.time())
# timestamp = time.mktime(datetime.now().timetuple()) * 1000.0
#
# d = datetime.fromtimestamp(timestamp / 1000)
# arg = {'create': d}
# print(arg)
# arg.update({'create': time.mktime(arg['create'].timetuple()) * 1000.0})
# print(arg)
# print(d)
import logging

logging.basicConfig(level=logging.DEBUG)
logging.info("asdasdasd")