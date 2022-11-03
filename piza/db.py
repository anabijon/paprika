
from heapq import merge
import sys
from django.db import connections
from django.utils import translation
from itertools import groupby
from operator import itemgetter
import requests
import json

def post_pizaproduct_order(request, category):
    try:
        with connections['default'].cursor() as mycursor:
            
            phone='992927770004'
            time_delivery='2022-10-11 22:12:00'
            product_name='Тестов Тест'
            request_id=1222
            client_app_type='Web'
            client_app_version=1
            o_sms_code=0
            o_txn_id=""
            o_exit_location_id2=""
            o_responce_id2=0
            o_result2=-1
            o_err_msg2=""
            remote_address = "127.0.0.1" #request.META.get('REMOTE_ADDR')
            args = (phone,subs_id,lang_id,name,remote_address,request_id,client_app_type,client_app_version, o_sms_code, o_txn_id,o_exit_location_id2, o_responce_id2, o_result2, o_err_msg2)
            mycursor.callproc('generate_sms_code', args)
            mycursor.execute("select @_generate_sms_code_8,@_generate_sms_code_9,@_generate_sms_code_10,@_generate_sms_code_11,@_generate_sms_code_12,@_generate_sms_code_13")
            result=mycursor.fetchall()
            msg=translation.gettext("Код активации")+": "+str(result[0][0])
            print('phone===>>> ', phone)
            print('msg===>>> ', msg)
            # msg= "Activation Code: "+str(result[0][0])
            resp={"exit_location_id":result[0][2],"response_id":result[0][3],"result":result[0][4],"err_msg":result[0][5]}
            if result[0][4]==0:

                reqUrl = "http://my.tcell.tj/api/v1/send_sms/"
                headersList = {
                "Accept": "*/*",
                "User-Agent": "Thunder Client (https://www.thunderclient.com)",
                "Content-Type": "application/json" 
                }
                payload = json.dumps({
                                        "msisdn": phone,
                                        "text": msg,
                                        "login":"UserSms",
                                        "pass": "!Sendsms@pass"
                                        })
                response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

                resp = {
                            "result": 0,
                            "err_msg": "sms sent"
                            }
                resp["txn_id"]=result[0][1]
            
        return resp
    except:
        return {
            "status": "error", 
            "message":"authentification.db.post_sent_code -> " + str(sys.exc_info()[1])
            }

def get_orders_list(msisdn):
   with connections['default'].cursor() as cursor:
    i_msisdn = msisdn
    cursor.execute("""select po.order_id, po.date, po.phone, pp.name, po.product_value, os.status_name, po.paid, count(*) count_product
from piza_orders po, piza_products pp, piza_order_status os, piza_deliveryinfo di
where po.product_id=pp.id
and po.status=os.id
and po.phone=di.phone
and po.date=di.cre_date
and po.phone=""" + str(msisdn) +"""
group by po.phone, pp.name, po.product_value, os.status_name, di.delivery_time
order by date;""")
    colomns = [i[0] for i in cursor.description]
    order_list = [dict(zip(colomns, row)) for row in cursor]
    order_list = sorted(order_list,
                    key = itemgetter('order_id'))

    cursor.execute("""select di.order_id, di.phone, di.cre_date, di.delivery_time, di.adress, di.comment from piza_deliveryinfo di where di.phone=""" + str(msisdn) +""" and di.status=1;""")
    colomns_delivery = [i[0] for i in cursor.description]
    delivery = [dict(zip(colomns_delivery, row)) for row in cursor]

    cursor.execute("""select di.order_id, di.phone, di.cre_date, di.delivery_time, di.adress, di.comment from piza_deliveryinfo di where di.phone=""" + str(msisdn) +""" and di.status=1;""")
    colomns_delivery = [i[0] for i in cursor.description]
    delivery = [dict(zip(colomns_delivery, row)) for row in cursor]
    merged=[]
    for ol in order_list:
        for dl in delivery:
            if (ol['order_id']==dl['order_id'] and ol['phone']==dl['phone']):
                merged.append({
                 'order_id' :ol['order_id'],
                 'cre_date' :dl['cre_date'],
                 'count_product' :ol['count_product'],
                 'paid' :ol['paid'],
                 'product_name' :ol['name'],
                 'product_value' :ol['product_value'],
                 'status_name' :ol['status_name'],
                })

                merged.append({
                    "delivery_time": dl['delivery_time'],
                    "adress" : dl['adress'],
                    'order_id' :ol['order_id'],})

    cursor.execute("""select po.phone,  sum(po.paid) sum_product from piza_orders po where po.phone=""" + str(msisdn) +""" and po.status in (0,1);""")
    colomns_sum = [i[0] for i in cursor.description]
    sum_order = [dict(zip(colomns_sum, row)) for row in cursor]
    summ_orders = {
               "sum_order": sum_order[0]['sum_product']}
    merged.append(summ_orders)
    if order_list ==[]: 
        content = {
               "err_msg": "You didn't have orders",
               "err_code": -1}
        return content
    else:
        content = {
                "orders": merged,
                #"summ_order": sum_order[0]['sum_product'],
                #"orders": order_list,
                "err_msg": "Ok",
                "err_code": 0}
        return content


def post_add_orders(msisdn, delivery_status, delivery_time, delivery_address, delivery_comment, product):
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("""select coalesce(max(order_id),0)+1 as id_orders from piza_orders;""")
            colomns_orders_id = [i[0] for i in cursor.description]
            orders_id = [dict(zip(colomns_orders_id, row)) for row in cursor]

            cursor.execute("""Select ac1.device_token from auth_code ac1
 where ac1.stat_id=3 and ac1.msisdn=""" + str(msisdn) +""" and ac1.device_token !=""
and ac1.cre_dt = (Select max(ac2.cre_dt) from auth_code ac2 where ac2.stat_id=3 and ac2.msisdn=ac1.msisdn);""")
            colomns_orders_id = [i[0] for i in cursor.description]
            token_device = [dict(zip(colomns_orders_id, row)) for row in cursor]

            o_result = -1
            o_err_msg = ""
            
            for i in range(len(product)):
                args = (
                    msisdn, product[i]['product_id'], product[i]['count'], product[i]['paid'], product[i]['product_id'], orders_id[0]['id_orders'], o_result, o_err_msg)
                cursor.callproc('add_orders', args)
                cursor.execute(
                    "select @_add_orders_5,@_add_orders_6,@_add_orders_7")
                result = cursor.fetchall()
                resp = {"order_id": orders_id[0]['id_orders'],
                    "err_code": result[0][1],
                        "err_msg": result[0][2]}

            args = (
                msisdn, delivery_status, delivery_time, delivery_address, delivery_comment, orders_id[0]['id_orders'], o_result, o_err_msg)
            cursor.callproc('delivery_order', args)
            cursor.execute(
                "select @_delivery_order_5,@_delivery_order_6,@_delivery_order_7")
            result = cursor.fetchall()
            if token_device[0]['device_token'] !="not token":
                url = "https://fcm.googleapis.com/fcm/send"

                payload = json.dumps({
                "registration_ids": [
                    token_device[0]['device_token']
                ],
                "notification": {
                    "body": "Мы получили Ваш заказ и начали работу над ним.",
                    "title": "Ваш заказ принят!"
                }
                })
                headers = {
                'Authorization': 'key=AAAAv4PolTM:APA91bHn-kOynZHp461mj8j-SwYoMpyp3_BRGZRq_BXI4bNGzyEuunC4gkesH6X-jEplB8v45PiG3lA00O_tdxcGkaHVDcV5HyyU9ZXZxH2wH2JaLFxtP342AhT_88D4MpxqgWSytTGj',
                'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                print('PUSH ===> ',response.text)
            return resp
    except:
        return {
            "status": "error", 
            "message":"db.add_orders.post_addorders -> " + str(sys.exc_info()[1])
            }

def get_profil_list(msisdn):
   with connections['default'].cursor() as cursor:
    cursor.execute("""select max(id), name, adress from piza_contact_info where phone=""" + str(msisdn) +""";""")
    colomns_sum = [i[0] for i in cursor.description]
    contact_info = [dict(zip(colomns_sum, row)) for row in cursor]

    content = {
            "name": contact_info[0]['name'],
            "address": contact_info[0]['adress'],
            "err_msg": "Ok",
            "err_code": 0}
    return content