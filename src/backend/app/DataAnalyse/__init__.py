from flask import Blueprint

#������ͼ
business = Blueprint('business', __name__)

#�ȴ�����ͼ���ٵ��빦���࣬����ѭ������
from . import Business


