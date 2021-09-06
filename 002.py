import _thread

import requests, threading
import re, hashlib
import time


def user_info():
    user_config = [
        {
            'bookholder': '',
            'mobile': '',
            'wxopenid': '',
            'unionid': ''
        }
    ]
    return user_config


def site_info(site):
    site_config = [
        {
            'price': '30.00',
            'fieldtype': '羽毛球A区',
            'homename': '苏州奥林匹克体育中心',
            'field': f'08:00-09:00|2021-09-08 08:00:00|{site}|30'.format(site),
        }
    ]
    return site_config


def md5_encrypt(code):
    m = hashlib.md5()
    m.update(code.encode("utf-8"))
    sign = "123" + m.hexdigest()
    return sign


class Wx_post():
    def select_site(self, a, b):
        for i in range(a, b):
            name = user_info()[0]["bookholder"]
            time_info = site_info(i)[0]["field"]
            changdi_url = "https://sapb.szosc.cn/index.php/wxplace/place/pay"
            date = {
                'price': site_info(i)[0]["price"],
                'fieldtype': site_info(i)[0]["fieldtype"],
                'homename': '苏州奥林匹克体育中心',
                'field': time_info,
                'openid': user_info()[0]["wxopenid"],
                'unionid': user_info()[0]["unionid"],
                'limit': '1.0000',
                'agree': '1'
            }
            response = requests.post(url=changdi_url, data=date)
            a = response.text
            outtradeno = re.findall('(name="outtradeno" value=")(.*)(" /)', a)[0][1]
            ordtotal_fee = re.findall('(name="ordtotal_fee" value=")(.*)(" /)', a)[0][1]
            homename = re.findall('(name="homename" value=")(.*)(" /)', a)[0][1]
            fieldtype = re.findall('(name="fieldtype" value=")(.*)(" /)', a)[0][1]
            fieldnum = re.findall('(name="fieldnum" value=")(.*)(" /)', a)[0][1]
            starttime = re.findall('(name="starttime" value=")(.*)(" /)', a)[0][1]
            bookinfo = re.findall('(name="bookinfo" value=")(.*)("/)', a)[0][1]
            uid = re.findall('(name="uid" value=")(.*)("/)', a)[0][1]
            paid = re.findall('(name="paid" value=")(.*)(" /)', a)[0][1]
            limit = re.findall('(name="limit" value=")(.*)("/)', a)[0][1]
            dttoken = re.findall('(name="dttoken" value=")(.*)("/)', a)[0][1]
            yhq = re.findall('(name="yhq" value=")(.*)("/)', a)[0][1]
            yhqid = re.findall('(name="yhqid" value=")(.*)("/)', a)[0][1]
            payType = re.findall('(name="payType" value=")(.*)(" /)', a)[0][1]
            vipCode = re.findall('(name="vipCode" value=")(.*)(" /)', a)[0][1]
            outTradeNo = re.findall('(name="outTradeNo" value=")(.*)(" /)', a)[0][1]
            totalFee = re.findall('(name="totalFee" value=")(.*)(" /)', a)[0][1]
            balanceMethod = re.findall('(name="balanceMethod" value=")(.*)(" /)', a)[0][1]
            cashAmount = re.findall('(name="cashAmount" value=")(.*)(" /)', a)[0][1]

            sign_old = user_info()[0]["wxopenid"] + outtradeno + bookinfo + paid + "Sport2021"
            sign = md5_encrypt(sign_old)

            pay_url = "https://sapb.szosc.cn/index.php/yinlian/index/pay"
            data = {
                'bookholder': '',
                'mobile': '',
                "idno": '',
                'outtradeno': outtradeno,
                'ordtotal_fee': ordtotal_fee,
                'homename': homename,
                'fieldtype': fieldtype,
                'wxopenid': user_info()[0]["wxopenid"],
                'unionid': user_info()[0]["unionid"],
                'fieldnum': fieldnum,
                'starttime': starttime,
                'bookinfo': bookinfo,
                'uid': uid,
                'paid': paid,
                'limit': limit,
                'dttoken': dttoken,
                'yhq': yhq,
                'yhqid': yhqid,
                'sign': sign,
                'payType': payType,
                'vipCode': vipCode,
                'outTradeNo': outTradeNo,
                'totalFee': totalFee,
                'balanceMethod': balanceMethod,
                'cashAmount': cashAmount,
                'groupName': '',
                'merchantCode': '',
                'groupVipId': ''
            }
            resp = requests.post(url=pay_url, data=data)
            time_now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
            print(f"{time_now}  姓名：{name}，{resp}，{time_info}".format(time_now, name, resp, time_info))
            bb = resp.text
            try:
                error = re.findall('(class="error">)(.*)(</)', bb)[0][1]
                if error == "该场地已被预订":
                    print(error, f"第{i}场抢票失败")
                elif error == "请勿频繁下单，稍后再试":
                    print(error, f"第{i}场抢票失败,等待6s")
                    time.sleep(6)
                elif error == "每人每日只能预订每个项目4场":
                    print(error, "退出脚本")
                    break
            except:
                print(f"第{i}场抢票成功")


if __name__ == '__main__':
    a = Wx_post()
    a.select_site(1, 23)
