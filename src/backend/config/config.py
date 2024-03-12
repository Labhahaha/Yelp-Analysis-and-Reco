import socket
# 动态获取IP地址
Local_IP = socket.getaddrinfo('LAPTOP-SISP97O2',None)[0][4][0]
print('Mysql连接IP:'+str(Local_IP))
# 数据库连接配置
DATABASE_URL = f'mysql+pymysql://root:123456@{Local_IP}:3306/yelp'
TRACK_MODIFICATIONS = False

