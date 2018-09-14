import requests, logging
from sqlalchemy.orm import sessionmaker
from connectors import Connector

import settings


logger = logging.getLogger('workflow')


class WorkflowTrigger:
    def __init__(self, apply_code, user_id):
        self.branch_user_id = user_id
        self.apply_code = apply_code
        self.workflow_url = '{}://{}:{}/{}/'.format(settings.WORKFLOW_URL['theme'], settings.WORKFLOW_URL['host'], settings.WORKFLOW_URL['port'], settings.WORKFLOW_URL['root'])

    # 创建流程
    def create_instance(self):
        data = {
            'userId': self.branch_user_id,
            'applyId': self.apply_code,
            'salemanId': self.branch_user_id,
        }
        logger.info('创建流程: ' + str(data))
        response = requests.post(self.workflow_url + 'flow/createNewProcessInstance', data=data)
        logger.info(response.json())
        return response

    # 身份证扫描
    def id_upload_complete(self):
        data = {
            'userId': self.branch_user_id,
            'applyId': self.apply_code,
            'url': 'account/checks',
        }
        logger.info('身份证扫描: ' + str(data))
        response = requests.post(self.workflow_url + '/flow/completeTask', data=data)
        logger.info(response.json())
        return response

    # 上传资料，客户照片，授权书，客户视频
    def credential_authentication_complete(self):
        data = {
            'userId': self.branch_user_id,
            'applyId': self.apply_code,
            'url': 'account/upVideo',
        }
        logger.info('上传资料: ' + str(data))
        response = requests.post(self.workflow_url + 'flow/completeTask', data=data)
        logger.info(response.json())
        return response

    # 客户基础信息
    def basic_info_complete(self):
        data = {
            'userId': self.branch_user_id,
            'applyId': self.apply_code,
            'url': 'account/toLoanBaseInfo',
        }
        logger.info('客户基础信息: ' + str(data))
        response = requests.post(self.workflow_url + 'flow/completeTask', data=data)
        logger.info(response.json())
        return response
