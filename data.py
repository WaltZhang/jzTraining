import uuid, random
import logging.config
from datetime import datetime
from sqlalchemy import desc

from models import *
from generators import Generator
import settings

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

    @staticmethod
    def api_pboc(apply_code, session):
        logger.info('查询申请：' + apply_code)
        product = session.query(CustomerApply).filter(CustomerApply.apply_id == apply_code).one()
        logger.info('查询身份证信息')
        id_card = session.query(IdCard).filter(IdCard.customer_apply_id == apply_code).one()
        logger.info('创建' + ('房供贷' if product.product_code == '1006' else '保单贷，') + 'ID：' + id_card.id_number + '，姓名：' + id_card.name)
        pboc1 = PBOC(idNo=id_card.id_number, name=id_card.name, url=settings.HOUSE_LOAN_URL_SIMPLE, supply=settings.LOAN_SUPPLY_SIMPLE, request_data='', response_data=settings.HOUSE_LOAN_RESPONSE_SIMPLE)
        pboc2 = PBOC(idNo=id_card.id_number, name=id_card.name, url=settings.HOUSE_LOAN_URL_JINDIAN, supply=settings.LOAN_SUPPLY_JINDIAN, request_data='', response_data=settings.HOUSE_LOAN_RESPONSE_JINDIAN)
        if product.product_code == '1007':
            pboc1 = PBOC(idNo=id_card.id_number, name=id_card.name, url=settings.POLICY_LOAN_URL_SIMPLE, supply=settings.LOAN_SUPPLY_SIMPLE, request_data='', response_data=settings.POLICY_LOAN_RESPONSE_SIMPLE)
            pboc2 = PBOC(idNo=id_card.id_number, name=id_card.name, url=settings.POLICY_LOAN_URL_JINDIAN, supply=settings.LOAN_SUPPLY_JINDIAN, request_data='', response_data=settings.POLICY_LOAN_RESPONSE_JINDIAN)
        return pboc1, pboc2

    @staticmethod
    def customer_check_file_result(apply_code):
        check_file = CheckFileResult(delete_flag=0, customer_apply_id=apply_code, operator_id=0, organ_user_id=0, result=1)
        logger.info(check_file)
        return check_file

    @staticmethod
    def customer_applyconfirm_result(apply_code):
        apply_confirm_result = ApplyConfirmResult(delete_flag=0, customer_apply_id=apply_code, customer_result=1)
        logger.info(apply_confirm_result)
        return apply_confirm_result

    @staticmethod
    def customer_application_info(apply_code):
        application_info = ApplicationInfo(delete_flag=0, customer_apply_id=apply_code)
        logger.info(application_info)
        return application_info

    @staticmethod
    def customer_intermediary_agreement_file(apply_code, operator_id=0):
        media_file2 = InterMediaFile(operator_id=operator_id, delete_flag=0, customer_apply_id=apply_code, type=2, path=settings.INTERMEDIA_AGREEMENT_2, is_skip=0)
        logger.info(media_file2)
        media_file3 = InterMediaFile(operator_id=operator_id, delete_flag=0, customer_apply_id=apply_code, type=3, path=settings.INTERMEDIA_AGREEMENT_3, is_skip=0)
        logger.info(media_file3)
        media_file4 = InterMediaFile(operator_id=operator_id, delete_flag=0, customer_apply_id=apply_code, type=4, is_skip=0)
        logger.info(media_file4)
        return media_file2, media_file3, media_file4

    @staticmethod
    def customer_intermediary_agreement_result(apply_code, operator_id=0):
        media_file_result = InterMediaFileResullt(customer_apply_id=apply_code, delete_flag=0, result=1, operator_id=operator_id, organ_user_id=operator_id)
        logger.info(media_file_result)
        return media_file_result

    @staticmethod
    def customer_phcheck_result_house(apply_code, operator=0):
        house_result = PhoneCheckResullt(customer_apply_id=apply_code, delete_flag=0, result=1, operator_id=operator, organ_user_id=operator)
        logger.info(house_result)
        return house_result

    @staticmethod
    def customer_phcheck_result_policy(apply_code, operator=0):
        policy_result = PhoneCheckResullt(customer_apply_id=apply_code, delete_flag=0, self_result='通过', contact_result='通过', operator_id=operator, organ_user_id=operator)
        logger.info(policy_result)
        return policy_result
