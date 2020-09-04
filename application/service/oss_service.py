from application.util.token_util import generate_by_sha1_random
from application.schema.oss_schema import OssCallbackParamsSchema
from datetime import datetime, timedelta
from application.settings import logger
from application.settings import oss_conf
import json
import base64
import hmac
import re
import hashlib
from urllib import parse

policy_expire_time = int(oss_conf.get('policy_expire_time'))
access_key_secret = str(oss_conf.get('access_key_secret'))
callback_host = str(oss_conf.get('callback_host'))
bucket_name = str(oss_conf.get('bucket_name'))
external_endpoint = str(oss_conf.get('endpoint'))
access_key_id = str(oss_conf.get('access_key_id'))
scheme = 'https'
oss_notify_url = 'http://39.107.77.70:8888/aliyun/oss/callback'


class OssService(object):

    @classmethod
    def get_policy(cls, file_schema):
        callback_params = OssCallbackParamsSchema.from_orm(file_schema)
        params = parse.urlencode(callback_params.dict())
        file_path = f'{generate_by_sha1_random()}/'
        expire_time = datetime.now() + timedelta(
            seconds=policy_expire_time
        )
        policy_dict = dict(
            expiration=expire_time.isoformat() + "Z",
            conditions=[["starts-with", "$key", file_path]],
        )
        policy = json.dumps(policy_dict).strip().encode()
        policy_encode = base64.b64encode(policy)

        h = hmac.new(
            access_key_secret.encode("utf-8"), policy_encode, hashlib.sha1
        )
        sign_result = base64.encodebytes(h.digest()).strip()

        # if callback_host:
        #     oss_notify_url = re.sub(
        #         "^https?://.*?/", callback_host, oss_notify_url
        #     )

        callback_dict = dict()
        callback_dict["callbackUrl"] = oss_notify_url
        callback_dict["callbackBody"] = (
                "filepath=${object}&size=${size}&mimeType=${mimeType}"
                "&imageInfo.height=${imageInfo.height}&imageInfo.width=${imageInfo.width}"
                "&imageInfo.format=${imageInfo.format}&" + params
        )
        callback_dict["callbackBodyType"] = "application/x-www-form-urlencoded"

        callback_param = json.dumps(callback_dict).strip().encode()
        base64_callback_body = base64.b64encode(callback_param)
        result = dict(
            accessid=access_key_id,
            host="%s://%s.%s" % (scheme, bucket_name, external_endpoint),
            policy=policy_encode.decode(),
            signature=sign_result.decode(),
            dir=file_path,
            callback=base64_callback_body.decode(),
        )
        logger.info("policy:{}".format(result))
        return result

    @classmethod
    def decode_callback(cls, callback_str):
        return base64.b64decode(callback_str).decode()
