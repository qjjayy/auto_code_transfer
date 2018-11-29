#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from faker import Faker
from bson import ObjectId
fake = Faker()

create_box_order = dict()

create_box_order['operator'] = fake.name()
create_box_order['operator_no'] = fake.ean(length=8)
create_box_order['package_ids'] = ['P536818321263742822', 'P536664187206116961',
                                   'P536239352891114241', 'P536200693054105901',
                                   'P536200679754151162']  # 必须为真实包裹号
create_box_order['refer_codes'] = ['TPS' + fake.ean(length=8), 'TPS' + fake.ean(length=8), 'TPS' + fake.ean(length=8)]
create_box_order['seller_ids'] = ['5a151d9deb90b912e76ee832', '59ddca6fbb06cd730c3ae349', '5919628f82e3eb33b1bf5b07']
create_box_order['provider_id'] = ''

create_box_order['joint_type'] = 'pick_up'  # 提货
create_box_order['expect_delivery_time'] = int(time.mktime(fake.date_time_this_month(
    before_now=False, after_now=True).timetuple()))
if create_box_order['joint_type'] == 'delivery':  # 送货必填
    create_box_order['delivery_info'] = fake.ean(length=13)
else:  # 提货不填
    create_box_order['delivery_info'] = ''

create_box_order['customs_code'] = 'sh_custom'  # 上海口岸 'sh_custom'
create_box_order['whcode'] = ''  # MEL01

# 发货仓库地址信息
sender_address_dict = dict()
sender_address_dict['address_id'] = '5baa30018232e139c186ff07'  # 商家/发货组仓库ID
sender_address_dict['country_id'] = '57d24b42ecddce212b0e589f'  # USA
sender_address_dict['province_id'] = '57d24c4404a2cf1b205aabf4'  # New York
sender_address_dict['city_id'] = '57d24c5204a2cf1b205aaf16'  # New York City
sender_address_dict['post_code'] = fake.postcode()
sender_address_dict['street_line_one'] = fake.street_address()
sender_address_dict['street_line_two'] = ''
sender_address_dict['contact_info_id'] = str(ObjectId())
sender_address_dict['full_name'] = fake.name()
sender_address_dict['role'] = fake.job()
sender_address_dict['phone'] = fake.phone_number()
sender_address_dict['email'] = fake.company_email()
create_box_order['sender_address'] = sender_address_dict
# 出口申报公司信息
supplier_invoice_dict = dict()
supplier_invoice_dict['provider_id'] = str(ObjectId())
supplier_invoice_dict['invoice_id'] = '5b9fd5216c3178f8c3f6a75e'
supplier_invoice_dict['name'] = 'xiaohongshu'  # fake.company()
supplier_invoice_dict['country_id'] = '57d24b42ecddce212b0e589f'  # USA
supplier_invoice_dict['province_id'] = '57d24c4404a2cf1b205aabf4'  # New York
supplier_invoice_dict['city_id'] = '57d24c5204a2cf1b205aaf16'  # New York City
supplier_invoice_dict['post_code'] = fake.postcode()
supplier_invoice_dict['street_line_one'] = fake.street_address()
supplier_invoice_dict['street_line_two'] = ''
supplier_invoice_dict['full_name'] = fake.name()
supplier_invoice_dict['role'] = fake.job()
supplier_invoice_dict['phone'] = fake.phone_number()
supplier_invoice_dict['email'] = fake.company_email()
supplier_invoice_dict['company_code'] = '12121212'  # fake.ean(length=13)
create_box_order['supplier_invoice'] = supplier_invoice_dict

create_box_order['notes'] = fake.text(max_nb_chars=200, ext_word_list=None)

create_box_order['pallet_count'] = 2
create_box_order['carton_count'] = 2
create_box_order['package_count'] = len(create_box_order['package_ids'])

order_pallets_dict = list()
for i in range(2):
    order_pallet_dict = dict()
    order_pallet_dict['number'] = i + 1
    order_pallet_dict['length'] = 11
    order_pallet_dict['width'] = 11
    order_pallet_dict['height'] = 11
    order_pallet_dict['gross_weight'] = fake.pydecimal(left_digits=2, right_digits=3, positive=True)
    order_pallet_dict['material'] = fake.word(ext_word_list=['wood', 'plastic'])
    order_pallet_dict['photos'] = []
    order_pallet_dict['order_cartons'] = []
    order_pallet_dict['carton_count'] = 0
    order_pallet_dict['package_count'] = 3
    order_pallets_dict.append(order_pallet_dict)
create_box_order['order_pallets'] = order_pallets_dict

order_cartons_dict = list()
for i in range(2):
    order_carton_dict = dict()
    order_carton_dict['number'] = i + 1
    order_carton_dict['length'] = 5
    order_carton_dict['width'] = 5
    order_carton_dict['height'] = 5
    order_carton_dict['gross_weight'] = fake.pydecimal(left_digits=2, right_digits=3, positive=True)
    order_carton_dict['photos'] = []
    order_carton_dict['barcode'] = ''
    order_carton_dict['po_number'] = ''
    order_carton_dict['skucode'] = ''
    order_carton_dict['pcs'] = 0
    order_carton_dict['count'] = 1
    order_carton_dict['is_loose_carton'] = True
    order_carton_dict['package_count'] = 2
    order_cartons_dict.append(order_carton_dict)
create_box_order['order_cartons'] = order_cartons_dict

volume = 0
gross_weight = 0
for order_pallet_dict in order_pallets_dict:
    volume += order_pallet_dict['length'] * order_pallet_dict['width'] * order_pallet_dict['height']
    gross_weight += order_pallet_dict['gross_weight']
for order_carton_dict in order_cartons_dict:
    volume += order_carton_dict['length'] * order_carton_dict['width'] * order_carton_dict['height']
    gross_weight += order_carton_dict['gross_weight']

create_box_order['volume'] = volume
create_box_order['gross_weight'] = gross_weight

create_box_order['order_skus'] = list()
response = Services.OmsService.list_package_by_package_ids(create_box_order['package_ids'])
new_order_packages = response.data
skucode_list = list()
for order_package in new_order_packages:
    for item_info in order_package.items_info:
        skucode_list.append(item_info.skucode)
for skucode in skucode_list:
    order_sku = dict()
    order_sku['skucode'] = skucode
    order_sku['hs_code'] = fake.ean(length=8)
    order_sku['place_of_origin_id'] = '57d24b42ecddce212b0e589f'  # USA
    order_sku['description_en'] = fake.word(ext_word_list=None)
    order_sku['description_cn'] = fake.word(ext_word_list=None)
    order_sku['description_note'] = fake.word(ext_word_list=None)
    order_sku['pcs'] = 0
    order_sku['unit_price'] = 0
    order_sku['net_weight'] = 0
    order_sku['exchange_rate'] = 0
    # order_sku['amount'] = 0
    order_sku['barcode'] = ''
    order_sku['po_number'] = ''
    order_sku['delivered_pcs'] = 0
    order_sku['place_of_origin_type'] = 'country'
    order_sku['owner_id'] = ''
    create_box_order['order_skus'].append(order_sku)
