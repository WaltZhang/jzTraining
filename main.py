from sqlalchemy.orm import sessionmaker
import logging, random, sys
from datetime import datetime

import settings
from generators import Generator
from connectors import Connector
from models import SerialNumber
from data import DataPreparation
from workflow import WorkflowTrigger
from models import CustomerInfoToRole, Role, CustomerInfoToOrgan, Organ


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
        jzdbtest_session.add(policy)
        jzdbtest_session.commit()
        jzdbtest_session.add(DataPreparation.customer_policy_photo(apply_code, policy.id))

    jzdbtest_session.add_all([apply_sn, reg_sn, cr, apply, id_card, check_file_1, check_file_2, check_file_3, basic_info])
    jzdbtest_session.commit()


def create_user_ids(sso_session):
    user_id = sso_session.query(CustomerInfoToRole).join(Role, CustomerInfoToRole.role_id == Role.id).filter(Role.role_name == '渠道管理').first().customer_info_id
    organ_id = sso_session.query(CustomerInfoToOrgan).join(Organ, CustomerInfoToOrgan.organ_id == Organ.id).filter(Organ.grade == 1).filter(CustomerInfoToOrgan.customer_info_id == user_id).first().id
    net_id = sso_session.query(CustomerInfoToOrgan).join(Organ, CustomerInfoToOrgan.organ_id == Organ.id).filter(Organ.grade == 3).filter(CustomerInfoToOrgan.customer_info_id == user_id).first().id
    return user_id, organ_id, net_id


def get_session(database):
    connector = Connector(settings.CONNECTION[database]['theme'], settings.CONNECTION[database]['host'], settings.CONNECTION[database]['port'],
                          settings.CONNECTION[database]['user'], settings.CONNECTION[database]['password'], settings.CONNECTION[database]['database'])
    Session = sessionmaker(bind=connector.get_engine())
    return Session()


if __name__ == '__main__':
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    logger.info('To import {} records.'.format(str(count)))
    sso_session = get_session('sso')
    user_id, organ_id, net_id = create_user_ids(sso_session)
    for i in range(count):
        logger.info('To create data #{}'.format(str(i + 1)))
        jzdbtest_session = get_session('jzdbtest')
        apply_prefix, apply_suffix, apply_code = DataPreparation.create_serial_number('AP', jzdbtest_session)
        data_preparation(jzdbtest_session, apply_prefix, apply_suffix, apply_code, user_id, organ_id, net_id)
        logger.info('To create workflow #{}'.format(str(i + 1)))
        workflow = WorkflowTrigger(apply_code, user_id=user_id)
        workflow.create_instance()
        workflow.id_upload_complete()
        workflow.credential_authentication_complete()
        workflow.basic_info_complete()
    print('{} data have been imported.'.format(str(count)))
