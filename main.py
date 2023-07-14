import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 "
    + "(KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
)


def login():
    """使用账号密码登陆 NSSCTF"""
    resp = requests.post(
        "https://www.nssctf.cn/api/user/login/",
        headers={"User-Agent": USER_AGENT},
        data={
            "username": os.environ["NSSCTF_USERNAME"],
            "password": os.environ["NSSCTF_PASSWORD"],
        },
    )
    cookies = dict(resp.cookies)
    cookies["token"] = resp.json()["data"]["token"]
    return cookies


def signin(cookies):
    """签到"""
    resp = requests.post(
        "https://www.nssctf.cn/api/user/clockin/",
        headers={"User-Agent": USER_AGENT},
        cookies=cookies,
    )
    return resp.json()["code"] == 200


def get_coin_num(cookies):
    """获取金币数量"""
    resp = requests.get(
        "https://www.nssctf.cn/api/user/info/opt/setting/",
        headers={"User-Agent": USER_AGENT},
        cookies=cookies,
    )
    data = resp.json()
    if data["code"] != 200:
        return None
    return data.get("data", {}).get("coin", None)


def send_email(coin_num):
    """发送邮件"""
    if coin_num is not None:
        plain_text_content = f"签到成功，当前金币数量为 {coin_num}"
    else:
        plain_text_content = "签到失败，请查看github action日志获取详细信息"
    message = Mail(
        from_email=os.environ["SENDGRID_FROM_EMAIL"],
        to_emails=os.environ["SENDGRID_TO_EMAIL"],
        subject="NSSCTF 签到结果",
        plain_text_content=plain_text_content,
    )
    try:
        sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
        sg.send(message)
        return True
    except Exception as e:
        print(e)
        return False


def send_ftqq(coin_num):
    """发送微信推送"""
    if coin_num is not None:
        content = f"签到成功，当前金币数量为 {coin_num}"
    else:
        content = "签到失败，请查看github action日志获取详细信息"
    resp = requests.post(
        f"https://sc.ftqq.com/{os.environ['FTQQ_SCKEY']}.send",
        data={"text": "NSSCTF 签到结果", "desp": content},
    )
    return resp.json()["data"]["errno"] == 0


def main():
    cookies = login()
    signin(cookies)
    coin_num = get_coin_num(cookies)
    if coin_num is None:
        print("签到失败")
    else:
        print(f"签到成功，当前金币数量为 {coin_num}")
        if (
            os.environ.get("SENDGRID_API_KEY") is not None
            and os.environ.get("SENDGRID_FROM_EMAIL") is not None
            and os.environ.get("SENDGRID_TO_EMAIL") is not None
        ):
            if send_email(coin_num):
                print("邮件发送成功")
            else:
                print("邮件发送失败")
        if os.environ.get("FTQQ_SCKEY") is not None:
            if send_ftqq(coin_num):
                print("微信推送发送成功")
            else:
                print("微信推送发送失败")


if __name__ == "__main__":
    main()
