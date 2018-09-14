import uuid, random
import logging.config
from datetime import datetime
from sqlalchemy import desc

from models import SerialNumber, CustomerRegister, CustomerApply, IdCard, CheckFile, BasicInfo, Policy, PolicyPhoto
from generators import Generator

logger = logging.getLogger('data')


class DataPreparation:
    @staticmethod
    def create_serial_number(sn_type, session):
        prefix = sn_type + datetime.now().strftime('%Y%m%d')
        re_qs = session.query(SerialNumber).filter(SerialNumber.prefix == prefix).order_by(desc(SerialNumber.id))
        suffix = int(re_qs.first().suffix) + 1 if re_qs.count() > 0 else 1
        logger.info('Serial number: {}{:>08}'.format(prefix, suffix))
        return prefix, suffix, '{}{:>08}'.format(prefix, suffix)

    @staticmethod
    def customer_register(register_code, customer, product_code, user_id, organ_id, net_id):
        registration = CustomerRegister(insert_time=datetime.now(), update_time=datetime.now(),
                                    operator_id=0, delete_flag=0, organ_id=organ_id, net_id=net_id, organ_user_id=user_id,
                                    register_phone=customer.phone_number, register_code=register_code, product_code=product_code, register_time=datetime.now(),
                                    province=customer.province, city=customer.city, saleman_name=Generator.generate_name(), customer_source=Generator.generate_address())
        logger.info(registration)
        return registration

    @staticmethod
    def customer_apply(apply_code, register_code, customer, product_code, user_id, organ_id, net_id):
        product_name = '房供贷' if product_code == '1006' else '保单贷'
        apply = CustomerApply(insert_time=datetime.now(), update_time=datetime.now(), operator_id=0, delete_flag=0,
                              apply_id=apply_code, apply_time=datetime.now(), customer_register_code=register_code, register_time=datetime.now(),
                              organ_id=organ_id, net_id=net_id, organ_user_id=user_id, register_phone=customer.phone_number, product_code=product_code, product_name=product_name,
                              province=customer.province, city=customer.city, act_pid=str(uuid.uuid4()))
        logger.info(apply)
        return apply

    @staticmethod
    def customer_id_card(apply_code, customer):
        idcard = IdCard(insert_time=datetime.now(), update_time=datetime.now(), operator_id=0, delete_flag=0,
                      customer_apply_id=apply_code, name=customer.name, gender=customer.gender,
                      id_number=customer.id_number, birthday='{}年{:02}月{:02}日'.format(customer.year, customer.month, customer.day),
                      address=customer.address, valid_time='{}{:02}{:02}'.format(str(2050), customer.month, customer.day),
                      head_pic='20180605/31cd6135-1b58-447c-b353-40dca8df9fe7.jpg', authentication_organ='{}{}公安局{}分局'.format(customer.province, customer.city, customer.district))
        logger.info(idcard)
        return idcard

    @staticmethod
    def customer_check_file(apply_code, file_type):
        check_file = CheckFile(insert_time=datetime.now(), update_time=datetime.now(), operator_id=0, delete_flag=0,
                               customer_apply_id=apply_code, file_type=file_type, virtual_path=[
                '20170913/a61e47cc-b95c-423d-8850-1573313e6428.jpg',
                '20170913/e2f94cdc-e70c-4e2f-ba85-13f52cf88e3c.jpg',
                '20170913/e9e22e78-0bb9-4f11-8708-f79834fefe25.avi',
            ][file_type - 1])
        logger.info(check_file)
        return check_file

    @staticmethod
    def customer_application_info_pre(apply_code, customer):
        basic_info = BasicInfo(insert_time=datetime.now(), update_time=datetime.now(), operator_id=0, delete_flag=0,
                         customer_apply_id=apply_code, customer_apply_time=datetime.now(), loan_use=['经营用途', '个人消费用途', '农牧业用途'][random.randint(0, 2)],
                         loan_use_descr='购置设备', loan_use_self_descr='购置设备', apply_amount=['10万以下', '10-20万', '20-30万'][random.randint(0, 2)],
                         education=customer.education, marriage=customer.marriage, support_num=customer.family, income=customer.incoming, living_type=customer.property,
                         employment_type=customer.employment_type, transportation=customer.vehicle, loan_use_child='批发零售类', province=customer.province,
                         city=customer.city, districts=customer.district, street=customer.address)
        logger.info(basic_info)
        return basic_info

    @staticmethod
    def customer_policy(apply_code):
        policy = Policy(insert_time=datetime.now(), update_time=datetime.now(), operator_id=0, delete_flag=0,
                      customer_apply_id=apply_code, serial_number='{:04}'.format(random.randint(1, 9999)), pay_type='月缴', year_pay_amount=1200,
                      company_name='中国人民保险', insurance_type=['传统', '万能', '分红'][random.randint(0, 2)], effect_time='2018-01-01',
                      current_status=random.randint(1, 2), break_pay=random.randint(1, 2), revival=random.randint(1, 2), policy_holder_change=random.randint(1, 2))
        logger.info(policy)
        return policy

    @staticmethod
    def customer_policy_photo(apply_code, policy_id):
        policy_photo = PolicyPhoto(insert_time=datetime.now(), update_time=datetime.now(), operator_id=0, delete_flag=0,
                           customer_apply_id=apply_code, customer_policy_id=policy_id,
                           path='s3://jz-ui-uploads/20180904/AP2018090400000001/63eb46f0-2af7-433c-a323-1e1556c8d62b.jpg', order_num=1)
        logger.info(policy_photo)
        return policy_photo

