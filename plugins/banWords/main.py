# 敏感词过滤模块
import re
import requests
import json

import Events
from .Events import *
from Models.Plugins import *


@register(
    description="敏感词屏蔽",
    version="0.1",
    author="For_Lin0601",
    priority=1000,
)
class banWordsUtil(Plugin):

    sensitive_words = []
    mask = "*"
    mask_word = ""

    # 默认值( 兼容性考虑 )
    baidu_check = False
    baidu_api_key = ""
    baidu_secret_key = ""
    inappropriate_message_tips = "[百度云]请珍惜机器人, 当前返回内容不合规"

    # 插件加载时触发
    # plugin_list 提供了全部插件列表, 详细请查看其源码
    def __init__(self):
        json_file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "sensitive.json")
        with open(json_file_path, "r", encoding="utf-8") as f:
            sensitive_json = json.load(f)
        self.sensitive_words = sensitive_json['words']
        self.mask = sensitive_json['mask'] if 'mask' in sensitive_json else '*',
        self.mask_word = sensitive_json['mask_word'] if 'mask_word' in sensitive_json else ''

    @on(PluginsLoadingFinished)
    def get_config(self, event: EventContext, **kwargs):
        config = self.emit(Events.GetConfig__)
        self.baidu_check = config.baidu_check
        self.baidu_api_key = config.baidu_api_key
        self.baidu_secret_key = config.baidu_secret_key
        self.inappropriate_message_tips = config.inappropriate_message_tips

    @on(BanWordCheck__)
    def is_illegal(self, event: EventContext, **kwargs) -> bool:
        message = kwargs['message']
        processed = self.process(message)
        if processed != message:
            event.return_value = True
            return
        event.return_value = False
        return

    @on(BanWordProcess__)
    def process(self, event: EventContext, **kwargs) -> str:
        # 本地关键词屏蔽
        message = kwargs['message']
        for word in self.sensitive_words:
            match = re.findall(word, message)
            if len(match) > 0:
                for i in range(len(match)):
                    if self.mask_word == "":
                        message = message.replace(
                            match[i], self.mask * len(match[i]))
                    else:
                        message = message.replace(match[i], self.mask_word)

        # 百度云审核
        if self.baidu_check:

            # 百度云审核URL
            baidu_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined?access_token=" + \
                str(requests.post("https://aip.baidubce.com/oauth/2.0/token",
                                  params={"grant_type": "client_credentials",
                                          "client_id": self.baidu_api_key,
                                          "client_secret": self.baidu_secret_key}).json().get("access_token"))

            # 百度云审核
            payload = "text=" + message
            logging.info("向百度云发送:" + payload)
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Accept': 'application/json'}

            if isinstance(payload, str):
                payload = payload.encode('utf-8')

            response = requests.request(
                "POST", baidu_url, headers=headers, data=payload)
            response_dict = json.loads(response.text)

            if "error_code" in response_dict:
                error_msg = response_dict.get("error_msg")
                logging.warning(f"百度云判定出错, 错误信息: {error_msg}")
                conclusion = f"百度云判定出错, 错误信息: {error_msg}\n以下是原消息: {message}"
            else:
                conclusion = response_dict["conclusion"]
                if conclusion in ("合规"):
                    logging.info(f"百度云判定结果: {conclusion}")
                    event.return_value = message
                    return
                else:
                    logging.warning(f"百度云判定结果: {conclusion}")
                    conclusion = self.inappropriate_message_tips
            # 返回百度云审核结果
            event.return_value = conclusion
            return

        event.return_value = message
        return
