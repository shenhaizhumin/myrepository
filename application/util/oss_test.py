# -*- coding: utf-8 -*-
import json
import base64
import os
import oss2

# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录RAM控制台创建RAM账号。
auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')

# 准备回调参数。
callback_dict = {}
# 设置回调请求的服务器地址，如http://oss-demo.aliyuncs.com:23450或http://127.0.0.1:9090。
callback_dict['callbackUrl'] = 'http://oss-demo.aliyuncs.com:23450'
# （可选）设置回调请求消息头中Host的值，即您的服务器配置Host的值。
# callback_dict['callbackHost'] = 'yourCallbackHost'
# 设置发起回调时请求body的值。
callback_dict['callbackBody'] = 'filename=${object}&size=${size}&mimeType=${mimeType}'
# 设置发起回调请求的Content-Type。
callback_dict['callbackBodyType'] = 'application/x-www-form-urlencoded'
# 回调参数是JSON格式，并且需要Base64编码。
callback_param = json.dumps(callback_dict).strip()
base64_callback_body = base64.b64encode(callback_param)
# 回调参数编码后放在Header中发送给OSS。
headers = {'x-oss-callback': base64_callback_body}

# 上传并回调。
result = bucket.put_object('<yourObjectName>', 'a' * 1024 * 1024, headers)
