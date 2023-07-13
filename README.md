# NSSCTFAutoLogin

NSSCTF自动签到脚本，基于Github Action，添加了邮件通知和微信通知功能（可通过修改`.github/workflows/main.yml`文件关闭）。

使用[SendGrid](https://sendgrid.com/)的免费邮件额度发送邮件通知

使用[Server酱](http://sc.ftqq.com/3.version)的免费微信通知

## 使用方法

1. Fork本仓库
2. 转到`Actions`，点击`I understand my workflows, go ahead and enable them`，启用Actions
3. 在Fork后的仓库中，依次点击`Settings`->`Security`->`Secrets and variables`->`Actions`->`New repository secret`，添加以下secret：
   - `NSSCTF_USERNAME` : NSSCTF的用户名
   - `NSSCTF_PASSWORD` : NSSCTF的密码
4. 添加以下secret（可选），若不想配置邮件通知与微信通知，请使用`#`注释掉`.github/workflows/main.yml`文件中的相关字段：
   - `SENDGRID_API_KEY` : SendGrid的API Key，用于发送邮件通知
   - `SENDGRID_FROM_EMAIL` : SendGrid的发送邮箱地址
   - `SENDGRID_TO_EMAIL` : 接收邮件通知的邮箱地址
   - `FTQQ_SCKEY` : Server酱的SendKey，用于发送微信通知
