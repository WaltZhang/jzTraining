from sqlalchemy.orm import sessionmaker
import logging, random, sys, os, time, argparse
from datetime import datetime

import settings
from generators import Generator
from connectors import Connector
from models import SerialNumber
from data import DataPreparation
from workflow import WorkflowTrigger
from models import CustomerInfo, CustomerInfoToRole, Role


logging.config.dictConfig(settings.LOGGINGS)
logger = logging.getLogger('')


def data_preparation(jzdbtest_session, apply_prefix, apply_suffix, apply_code, user_id, organ_id, net_id):
    apply_sn = SerialNumber(insert_time=datetime.now(), update_time=datetime.now(), operator_id=0, delete_flag=0, type=2, prefix=apply_prefix, suffix=apply_suffix, number=apply_code)

    register_prefix, register_suffix, register_code = DataPreparation.create_serial_number('RE', jzdbtest_session)
    reg_sn = SerialNumber(insert_time=datetime.now(), update_time=datetime.now(), operator_id=0, delete_flag=0, type=1, prefix=register_prefix, suffix=register_suffix, number=register_code)

    product_code = ['1006', '1007'][random.randint(0, 1)]
    customer = Generator.generate_customer()
    cr = DataPreparation.customer_register(register_code, customer, product_code, user_id, organ_id, net_id)
    apply = DataPreparation.customer_apply(apply_code, register_code, customer, product_code, user_id, organ_id, net_id)

    id_card = DataPreparation.customer_id_card(apply_code, customer)

    check_file_1 = DataPreparation.customer_check_file(apply_code, 1)
    check_file_2 = DataPreparation.customer_check_file(apply_code, 2)
    check_file_3 = DataPreparation.customer_check_file(apply_code, 3)

    basic_info = DataPreparation.customer_application_info_pre(apply_code, customer)

    if product_code == '1007':
        policy = DataPreparation.customer_policy(apply_code)
        with jzdbtest_session.begin():
            jzdbtest_session.add(policy)
            jzdbtest_session.add(DataPreparation.customer_policy_photo(apply_code, policy.id))
            # jzdbtest_session.commit()

    with jzdbtest_session.begin():
        jzdbtest_session.add_all([apply_sn, reg_sn, cr, apply, id_card, check_file_1, check_file_2, check_file_3, basic_info])
        # jzdbtest_session.commit()

    pboc1, pboc2 = DataPreparation.api_pboc(apply_code, jzdbtest_session)
    file_result = DataPreparation.customer_check_file_result(apply_code)

    apply_confirm_result = DataPreparation.customer_applyconfirm_result(apply_code)
    application_info = DataPreparation.customer_application_info(apply_code)

    agreement2, agreement3, agreement4 = DataPreparation.customer_intermediary_agreement_file(apply_code)

    with jzdbtest_session.begin():
        jzdbtest_session.add_all([pboc1, pboc2, file_result, apply_confirm_result, application_info, agreement2, agreement3, agreement4])
        # jzdbtest_session.commit()

    media_file_result = DataPreparation.customer_intermediary_agreement_result(apply_code)

    with jzdbtest_session.begin():
        jzdbtest_session.add(media_file_result)
        # jzdbtest_session.commit()

    return product_code, customer


def telephone_verification_preparation(product, apply_code, jzdbtest_session):
    if product == '1007':
        result = DataPreparation.customer_phcheck_result_policy(apply_code)
        with jzdbtest_session.begin():
            jzdbtest_session.add(result)
            # jzdbtest_session.commit()
    else:
        result = DataPreparation.customer_phcheck_result_house(apply_code)
        with jzdbtest_session.begin():
            jzdbtest_session.add(result)
            # jzdbtest_session.commit()



def create_user_ids(sso_session, role):
    # user_id = sso_session.query(CustomerInfoToRole).join(Role, CustomerInfoToRole.role_id == Role.id).filter(Role.role_name == role).first().customer_info_id
    # organ_id = sso_session.query(CustomerInfoToOrgan).join(Organ, CustomerInfoToOrgan.organ_id == Organ.id).filter(Organ.grade == 1).filter(CustomerInfoToOrgan.customer_info_id == user_id).first().id
    # net_id = sso_session.query(CustomerInfoToOrgan).join(Organ, CustomerInfoToOrgan.organ_id == Organ.id).filter(Organ.grade == 3).filter(CustomerInfoToOrgan.customer_info_id == user_id).first().id
    user_id = 142
    organ_id = 105
    net_id = 127
    return user_id, organ_id, net_id


def get_session(database):
    connector = Connector(settings.CONNECTION[database]['theme'], settings.CONNECTION[database]['host'], settings.CONNECTION[database]['port'],
                          settings.CONNECTION[database]['user'], settings.CONNECTION[database]['password'], settings.CONNECTION[database]['database'])
    Session = sessionmaker(bind=connector.get_engine(), autocommit=True)
    return Session()


def get_auditor(sso_session, role):
    return sso_session.query(CustomerInfo).join(CustomerInfoToRole, CustomerInfoToRole.customer_info_id == CustomerInfo.id).join(Role, CustomerInfoToRole.role_id == Role.id).filter(Role.role_name == role).first().username


def branch_workflow(workflow):
    workflow.create_instance()
    workflow.id_upload_complete()
    workflow.credential_authentication_complete()
    workflow.basic_info_complete()


def file_audit_workflow(workflow, auditor):
    apply_code = None
    has_task = True
    while has_task:
        response = workflow.basic_info_audit(auditor)
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 'success':
                if apply_code == result.get('data').get('applyId'):
                    break
                if result.get('data').get('code') == 'success':
                    apply_code = result.get('data').get('applyId')
                    workflow.basic_info_audit_complete(auditor, result.get('data').get('applyId'), result.get('data').get('taskId'))
                else:
                    has_task = False
            else:
                has_task = False
        else:
            has_task = False
    counter = 0
    while counter < 31:
        response = workflow.machine_audit_1()
        counter += 1
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 'success':
                if result.get('data').get('nextUrl') == 'account/toSearchResult':
                    break
                else:
                    time.sleep(10)


def solution_confirm_workflow(workflow):
    response = workflow.solution_verification()
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 'success':
            workflow.solution_verification_complete()
            workflow.complete_apply()
            workflow.upload_agreements()


def intermedia_file_audit(workflow, auditor):
    apply_code = None
    has_task = True
    while has_task:
        response = workflow.intermedia_file_audit(auditor)
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 'success':
                if apply_code == result.get('data').get('applyId'):
                    break
                if result.get('data').get('code') == 'success':
                    apply_code = result.get('data').get('applyId')
                    workflow.intermedia_file_audit_complete(auditor, result.get('data').get('applyId'), result.get('data').get('taskId'))
                else:
                    has_task = False
            else:
                has_task = False
        else:
            has_task = False


def housing_loan_phone_verification(workflow):
    apply_code = None
    has_task = True
    while has_task:
        response = workflow.housing_loan_phone_verification()
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 'success':
                if apply_code == result.get('data').get('applyId'):
                    break
                if result.get('data').get('code') == 'success':
                    apply_code = result.get('data').get('applyId')
                    workflow.housing_loan_phone_verification_complete(result.get('data').get('applyId'), result.get('data').get('taskId'))
                else:
                    has_task = False
            else:
                has_task = False
        else:
            has_task = False


def policy_phone_verification(workflow):
    apply_code = None
    has_task = True
    while has_task:
        response = workflow.self_phone_verification()
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 'success':
                if apply_code == result.get('data').get('applyId'):
                    break
                if result.get('data').get('code') == 'success':
                    apply_code = result.get('data').get('applyId')
                    workflow.self_phone_verification_complete(result.get('data').get('applyId'), result.get('data').get('taskId'))
                else:
                    has_task = False
            else:
                has_task = False
        else:
            has_task = False
    apply_code = None
    has_task = True
    while has_task:
        response = workflow.contact_phone_verification()
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 'success':
                if apply_code == result.get('data').get('applyId'):
                    break
                if result.get('data').get('code') == 'success':
                    apply_code = result.get('data').get('applyId')
                    workflow.contact_phone_verification_complete(result.get('data').get('applyId'), result.get('data').get('taskId'))
                else:
                    has_task = False
            else:
                has_task = False
        else:
            has_task = False


def launch_phone_verification_workflow(workflow, product_code):
        if product_code == '1007':
            policy_phone_verification(workflow)
        else:
            housing_loan_phone_verification(workflow)


def launch_branch_registration_workflow(workflow, customer_name, customer_id_number):
    response = workflow.customer_branchbook(customer_name, customer_id_number)
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 'success':
            workflow.customer_branchbook_complete('108', result.get('data').get('taskId'))


def parse_args():
    parser = argparse.ArgumentParser(description='JunZheng training simulator CLI tool.')
    parser.add_argument('count', metavar='N', type=int, nargs='?', default='3', help='the record count of simulating data')
    parser.add_argument('-c', default='workflow', help="training tool's commands", choices=['workflow', 'export'])
    parser.add_argument('-x', nargs='?', default='interview', help='exported file name if -c assigned with export, other wise flow node', choices=['interview', 'branch'])
    return parser.parse_args()


if __name__ == '__main__':
    args = vars(parse_args())
    cmd = args['c']
    record_size = args['count']
    xarg = args['x']

    if cmd == 'workflow':
        logger.info('To import {} records.'.format(record_size))
        sso_session = get_session('sso')
        user_id, organ_id, net_id = create_user_ids(sso_session, '渠道管理')
        file_auditor = get_auditor(sso_session, '资料审核')
        agreement_auditor = get_auditor(sso_session, '居间协议审核')
        jzdbtest_session = get_session('jzdbtest')
        for i in range(int(record_size)):
            logger.info('To create data #{}'.format(str(i + 1)))
            apply_prefix, apply_suffix, apply_code = DataPreparation.create_serial_number('AP', jzdbtest_session)
            product_code, customer = data_preparation(jzdbtest_session, apply_prefix, apply_suffix, apply_code, user_id, organ_id, net_id)
            telephone_verification_preparation(product_code, apply_code, jzdbtest_session)
            logger.info('To create workflow #{}'.format(str(i + 1)))
            workflow = WorkflowTrigger(apply_code, user_id=user_id)
            branch_workflow(workflow)
            if xarg == 'interview':
                file_audit_workflow(workflow, file_auditor)
                solution_confirm_workflow(workflow)
                intermedia_file_audit(workflow, agreement_auditor)
                launch_phone_verification_workflow(workflow, product_code)
                launch_branch_registration_workflow(workflow, customer.name, customer.id_number)
        print('{} data have been imported.'.format(str(record_size)))
        sso_session.close()
        jzdbtest_session.close()
    else:
        with open(xarg + '.csv', 'w') as csv:
            for _ in range(int(record_size)):
                customer = Generator.generate_customer()
                csv.write(str(customer) + '\n')

