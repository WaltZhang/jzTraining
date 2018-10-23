from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP
from sqlalchemy.dialects.mysql import LONGTEXT


Base = declarative_base()


class SerialNumber(Base):
    __tablename__ = 'customer_no_his'
    
    id = Column(Integer, primary_key=True)
    insert_time = Column(TIMESTAMP(True))
    update_time = Column(TIMESTAMP(True))
    operator_id = Column(Integer)
    delete_flag = Column(Integer)
    type = Column(Integer)
    prefix = Column(String(10))
    suffix = Column(String(10))
    number = Column(String(20))

    def __str__(self):
        return self.number


class CustomerRegister(Base):
    __tablename__ = 'customer_register'

    id = Column(Integer, primary_key=True)
    insert_time = Column(TIMESTAMP(True))
    update_time = Column(TIMESTAMP(True))
    operator_id = Column(Integer)
    delete_flag = Column(Integer)
    organ_id = Column(Integer)
    net_id = Column(Integer)
    organ_user_id = Column(Integer)
    saleman_id = Column(Integer)
    register_phone = Column(String(20))
    register_code = Column(String(20))
    register_time = Column(TIMESTAMP(True))
    product_code = Column(String(50))
    province = Column(String(50))
    city = Column(String(50))
    result = Column(Integer)
    saleman_name = Column(String(20))
    saleman_phone = Column(String(20))
    customer_source = Column(String(100))

    def __str__(self):
        return self.register_code + ':' + self.register_phone + '(' + str(self.register_time) + '):' + self.province + self.city


class CustomerApply(Base):
    __tablename__ = 'customer_apply'

    id = Column(Integer, primary_key=True)
    insert_time = Column(TIMESTAMP(True))
    update_time = Column(TIMESTAMP(True))
    operator_id = Column(Integer)
    delete_flag = Column(Integer)
    apply_id = Column(String(20))
    apply_time = Column(TIMESTAMP(True))
    customer_register_code = Column(String(20))
    register_time = Column(TIMESTAMP(True))
    organ_id = Column(Integer)
    net_id = Column(Integer)
    organ_user_id = Column(Integer)
    register_phone = Column(String(20))
    product_code = Column(String(20))
    product_name = Column(String(20))
    province = Column(String(50))
    city = Column(String(50))
    act_pid = Column(String(64))

    def __str__(self):
        return self.apply_id + ':' + self.customer_register_code + ', ' + str(self.organ_id) + ', ' + str(self.net_id) + ', ' + str(self.organ_user_id) + ', ' + self.register_phone\
            + ', ' + self.product_name + '(' + self.product_code + '), at: ' + self.province + self.city


class IdCard(Base):
    __tablename__ = 'customer_id_card'

    id = Column(Integer, primary_key=True)
    insert_time = Column(TIMESTAMP(True))
    update_time = Column(TIMESTAMP(True))
    operator_id = Column(Integer)
    delete_flag = Column(Integer)
    customer_apply_id = Column(String(20))
    name = Column(String(50))
    gender = Column(String(2))
    id_number = Column(String(50))
    birthday = Column(String(20))
    address = Column(String(100))
    valid_time = Column(String(20))
    head_pic = Column(String(100))
    authentication_organ = Column(String(100))

    def __str__(self):
        return self.customer_apply_id + ':' + self.name + '(' + self.id_number + '): ' + self.gender + ', ' + self.birthday + ', ' + self.address + ', ' + self.valid_time + ', ' + self.head_pic + ', ' + self.authentication_organ


class CheckFile(Base):
    __tablename__ = 'customer_check_file'

    id = Column(Integer, primary_key=True)
    insert_time = Column(TIMESTAMP(True))
    update_time = Column(TIMESTAMP(True))
    operator_id = Column(Integer)
    delete_flag = Column(Integer)
    customer_apply_id = Column(String(20))
    file_type = Column(Integer)
    virtual_path = Column(String(100))

    def __str__(self):
        return self.customer_apply_id + ':' + str(self.file_type) + ', ' + self.virtual_path


class BasicInfo(Base):
    __tablename__ = 'customer_application_info_pre'

    id = Column(Integer, primary_key=True)
    insert_time = Column(TIMESTAMP(True))
    update_time = Column(TIMESTAMP(True))
    operator_id = Column(Integer)
    delete_flag = Column(Integer)
    customer_apply_id = Column(String(20))
    customer_apply_time = Column(TIMESTAMP(True))
    loan_use = Column(String(100))
    loan_use_descr = Column(String(300))
    loan_use_self_descr = Column(String(500))
    apply_amount = Column(String(100))
    education = Column(String(100))
    marriage = Column(String(100))
    support_num = Column(String(100))
    income = Column(String(100))
    living_type = Column(String(100))
    employment_type = Column(String(100))
    transportation = Column(String(100))
    loan_use_child = Column(String(100))
    province = Column(String(100))
    city = Column(String(100))
    districts = Column(String(100))
    street = Column(String(100))

    def __str__(self):
        return self.customer_apply_id + ':' + self.loan_use + '>' + self.loan_use_descr + '>' + self.loan_use_self_descr + ':' + self.apply_amount + ', ' + self.education + ', ' + self.marriage + ', ' + self.support_num \
               + ', ' + self.income + ', ' + self.living_type + ', ' + self.employment_type + ', ' + self.transportation + ', ' + self.loan_use_child + ', ' + self.province + self.city + self.districts + self.street


class Policy(Base):
    __tablename__ = 'customer_policy'

    id = Column(Integer, primary_key=True)
    insert_time = Column(TIMESTAMP(True))
    update_time = Column(TIMESTAMP(True))
    operator_id = Column(Integer)
    delete_flag = Column(Integer)
    customer_apply_id = Column(String(20))
    serial_number = Column(String(30))
    pay_type = Column(String(20))
    year_pay_amount = Column(Numeric())
    company_name = Column(String(50))
    insurance_type = Column(String(20))
    effect_time = Column(String(20))
    current_status = Column(Integer)
    break_pay = Column(Integer)
    revival = Column(Integer)
    policy_holder_change = Column(Integer)

    def __str__(self):
        return self.customer_apply_id + ':' + self.serial_number + ', ' + self.pay_type + ', ' + str(self.year_pay_amount) + ', ' + self.company_name + ', '\
               + self.insurance_type + ', ' + self.effect_time + ', ' + str(self.current_status) + ', ' + str(self.break_pay) + ', ' + str(self.revival) + ', ' + str(self.policy_holder_change)


class PolicyPhoto(Base):
    __tablename__ = 'customer_policy_photo'

    id = Column(Integer, primary_key=True)
    insert_time = Column(TIMESTAMP(True))
    update_time = Column(TIMESTAMP(True))
    operator_id = Column(Integer)
    delete_flag = Column(Integer)
    customer_apply_id = Column(String(20))
    customer_policy_id = Column(Integer)
    path = Column(String(200))
    order_num = Column(Integer)

    def __str__(self):
        return self.customer_apply_id + ':' + str(self.customer_policy_id) + ', ' + self.path + ', ' + str(self.order_num)


class CustomerInfo(Base):
    __tablename__ = 'customer_info'

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    telphone = Column(String(100))

    def __str__(self):
        return self.username + ', ' + self.telphone


class CustomerInfoToRole(Base):
    __tablename__ = 'customer_info_to_role'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer)
    customer_info_id = Column(Integer)

    def __str__(self):
        return self.role_id


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    role_name = Column(String(100))

    def __str__(self):
        return self.role_name


class CustomerInfoToOrgan(Base):
    __tablename__ = 'customer_info_to_organ'

    id = Column(Integer, primary_key=True)
    organ_id = Column(Integer)
    customer_info_id = Column(Integer)


class Organ(Base):
    __tablename__ = 'organ'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    grade = Column(Integer)

    def __str__(self):
        return self.name


class CheckFileResult(Base):
    __tablename__ = 'customer_check_file_result'

    id = Column(Integer, primary_key=True)
    delete_flag = Column(Integer)
    customer_apply_id = Column(String(20))
    operator_id = Column(Integer)
    organ_user_id = Column(Integer)
    result = Column(Integer)

    def __str__(self):
        return self.customer_apply_id + ', ' + str(self.operator_id) + ':' + str(self.organ_user_id) + ', ' + str(self.result)


class PBOC(Base):
    __tablename__ = 'api_pboc'

    id = Column(Integer, primary_key=True)
    request_data = Column(LONGTEXT)
    response_data = Column(LONGTEXT)
    idNo = Column(String(50))
    name = Column(String(50))
    url = Column(String(200))
    supply = Column(String(200))

    def __str__(self):
        return self.name

class ApplyConfirmResult(Base):
    __tablename__ = 'customer_applyconfirm_result'

    id = Column(Integer, primary_key=True)
    delete_flag = Column(Integer)
    customer_apply_id = Column(String(20))
    customer_result = Column(Integer)

    def __str__(self):
        return self.customer_apply_id + ': ' + str(self.customer_result)


class ApplicationInfo(Base):
    __tablename__ = 'customer_application_info'

    id = Column(Integer, primary_key=True)
    delete_flag = Column(Integer)
    customer_apply_id = Column(String(20))

    def __str__(self):
        return self.customer_apply_id


class InterMediaFile(Base):
    __tablename__ = 'customer_intermediary_agreement_file'

    id = Column(Integer, primary_key=True)
    delete_flag = Column(Integer)
    operator_id = Column(Integer)
    customer_apply_id = Column(String(20))
    type = Column(Integer)
    path = Column(String(1000))
    is_skip = Column(Integer)

    def __str__(self):
        return self.customer_apply_id + ': ' + str(self.path) + '(' + str(self.type) + ')'


class InterMediaFileResullt(Base):
    __tablename__ = 'customer_intermediary_agreement_result'

    id = Column(Integer, primary_key=True)
    delete_flag = Column(Integer)
    operator_id = Column(Integer)
    customer_apply_id = Column(String(20))
    organ_user_id = Column(Integer)
    result = Column(Integer)

    def __str__(self):
        return self.customer_apply_id + ', operator id: ' + str(self.operator_id) + ', organ user id: ' + str(self.organ_user_id)


class PhoneCheckResullt(Base):
    __tablename__ = 'customer_phcheck_result'

    id = Column(Integer, primary_key=True)
    delete_flag = Column(Integer)
    customer_apply_id = Column(String(20))
    operator_id = Column(Integer)
    organ_user_id = Column(Integer)
    result = Column(Integer)
    self_result = Column(String(20))
    contact_result = Column(String(20))

    def __str__(self):
        return self.customer_apply_id + ', result: ' + str(self.result) + ', self result: ' + str(self.self_result) + ', contact result: ' + str(self.contact_result)
