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

    # 基础资料审核
    def basic_info_audit(self, auditor):
        data = {
            'userId': auditor,
        }
        logger.info('资料审核人员: ' + auditor)
        response = requests.post(self.workflow_url + 'fixed/getAuthDocReviewTask', data=data)
        logger.info(response.json())
        return response

    # 基础资料审核完成
    def basic_info_audit_complete(self, auditor, apply_code, task_id):
        data = {
            'userId': auditor,
            'applyId': apply_code,
            'taskId': task_id,
        }
        logger.info('基础资料审核完成: ' + str(data))
        response = requests.post(self.workflow_url + 'fixed/completeTask', data=data)
        logger.info(response.json())
        return response

    # 机审-1
    def machine_audit_1(self):
        data = {
            'userId': self.branch_user_id,
            'applyId': self.apply_code,
            'url': 'account/riskDecision',
        }
        logger.info('机器审核: ' + str(data))
        response = requests.post(self.workflow_url + 'flow/completeTask', data=data)
        logger.info(response.json())
        return response


    # 方案调整
    def solution_verification(self):
        data = {
            'applyId': self.apply_code,
        }
        logger.info('方案调整: ' + str(data))
        response = requests.post(self.workflow_url + 'notice/intoSolutionConfirmPage', data=data)
        logger.info(response.json())
        return response

    # 方案调整完成
    def solution_verification_complete(self):
        data = {
            'userId': self.branch_user_id,
            'applyId': self.apply_code,
            'url': 'account/toSearchResult'
        }
        logger.info('方案调整完成: ' + str(data))
        response = requests.post(self.workflow_url + 'flow/completeTask', data=data)
        logger.info(response.json())
        return response

    # 完善申请
    def complete_apply(self):
        data = {
            'userId': self.branch_user_id,
            'applyId': self.apply_code,
            'url': 'account/toCustomInfo'
        }
        logger.info('方案调整完成: ' + str(data))
        response = requests.post(self.workflow_url + 'flow/completeTask', data=data)
        logger.info(response.json())
        return response

    # 协议签署（居间文件上传）
    def upload_agreements(self):
        data = {
            'userId': self.branch_user_id,
            'applyId': self.apply_code,
            'url': 'protocolSignCallback'
        }
        logger.info('方案调整完成: ' + str(data))
        response = requests.post(self.workflow_url + 'flow/completeTask', data=data)
        logger.info(response.json())
        return response

    # 居间资料审核
    def intermedia_file_audit(self, auditor):
        data = {
            'userId': auditor,
        }
        logger.info('居间资料审核人员: ' + auditor)
        response = requests.post(self.workflow_url + 'fixed/getAppDocReviewTask', data=data)
        logger.info(response.json())
        return response

    # 居间资料审核完成
    def intermedia_file_audit_complete(self, auditor, apply_code, task_id):
        data = {
            'userId': auditor,
            'applyId': apply_code,
            'taskId': task_id,
        }
        logger.info('居间资料审核完成: ' + str(data))
        response = requests.post(self.workflow_url + 'fixed/completeTask', data=data)
        logger.info(response.json())
        return response

    # 房供贷电核
    def housing_loan_phone_verification(self):
        data = {
            'phone': '1234567890',
        }
        logger.info('房供贷电核: ' + str(data))
        response = requests.post(self.workflow_url + 'fixed/getPhoneVerificationTask', data=data)
        logger.info(response.json())
        return response

    # 房供贷电核完成
    def housing_loan_phone_verification_complete(self, apply_code, task_id):
        data = {
            'userId': '1234567890',
            'applyId': apply_code,
            'taskId': task_id,
        }
        logger.info('房供贷电核完成: ' + str(data))
        response = requests.post(self.workflow_url + 'fixed/completeTask', data=data)
        logger.info(response.json())
        return response

    # 本人电核
    def self_phone_verification(self):
        data = {
            'phone': '1234567890',
        }
        logger.info('本人电核: ' + str(data))
        response = requests.post(self.workflow_url + 'phoneVerification/self/getTask', data=data)
        logger.info(response.json())
        return response

    # 本人电核完成
    def self_phone_verification_complete(self, apply_code, task_id):
        data = {
            'userId': '1234567890',
            'applyId': apply_code,
            'taskId': task_id,
        }
        logger.info('本人电核完成: ' + str(data))
        response = requests.post(self.workflow_url + 'phoneVerification/completeTask', data=data)
        logger.info(response.json())
        return response

    # 联系人电核
    def contact_phone_verification(self):
        data = {
            'phone': '1234567890',
        }
        logger.info('联系人电核: ' + str(data))
        response = requests.post(self.workflow_url + 'phoneVerification/contact/getTask', data=data)
        logger.info(response.json())
        return response

    # 联系人电核完成
    def contact_phone_verification_complete(self, apply_code, task_id):
        data = {
            'userId': '1234567890',
            'applyId': apply_code,
            'taskId': task_id,
        }
        logger.info('联系人电核完成: ' + str(data))
        response = requests.post(self.workflow_url + 'phoneVerification/completeTask', data=data)
        logger.info(response.json())
        return response

    # 门店登记
    def customer_branchbook(self, customer_name, customer_id_number):
        data = {
            'applyId': self.apply_code,
            'customerName': customer_name,
            'customerIdCardNumber': customer_id_number,
        }
        logger.info('门店登记: ' + str(data))
        response = requests.post(self.workflow_url + 'tool/applyPoint', data=data)
        logger.info(response.json())
        return response

    # 门店登记完成
    def customer_branchbook_complete(self, user_id, task_id):
        data = {
            'userId': user_id,
            'applyId': self.apply_code,
            'taskId': task_id,
        }
        logger.info('门店登记完成: ' + str(data))
        response = requests.post(self.workflow_url + 'fixed/completeTask', data=data)
        logger.info(response.json())
        return response
