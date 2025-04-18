import requests
import json
import logging

class DeepSeekAPI:
    def __init__(self, api_key, base_url, default_model="deepseek-v3-250324", log_level=logging.INFO):
        """
        初始化 API 客户端

        :param api_key: API 密钥
        :param base_url: API 的基础 URL
        :param default_model: 默认模型名称 (如果没有提供则使用此模型)
        :param log_level: 日志记录级别
        """
         # 设置日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        self.api_key = api_key
        self.url = base_url
        self.default_model = default_model  # 设置默认模型
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def send_request(self, messages, method="POST", model=None):
        """
        发送请求到指定的 API 端点
        :param messages: 请求数据，消息列表
        :param method: HTTP 方法，默认为 POST
        :param model: 可选，指定使用的模型。如果为 None，则使用默认模型
        :return: API 响应数据
        """
        model = model or self.default_model  # 如果没有传入模型，使用默认模型
        data = {
            "model": model,
            "messages": messages
        }


        
        if method.upper() == "POST":
            self.logger.info(f"发送 POST 请求到 {self.url}，数据: {data}")
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        elif method.upper() == "GET":
            self.logger.info(f"发送 GET 请求到 {self.url}，参数: {data}")
            response = requests.get(self.url, headers=self.headers, params=data)
        else:
            raise ValueError("不支持的 HTTP 方法。")

        response.raise_for_status()  # 如果请求失败，会抛出异常
        response_data = response.json()  # 返回 JSON 格式的响应
        answer = response_data['choices'][0]['message']['content']

        return answer
    

if __name__ == "__main__":
    api_key = "d90a20d9-c192-4933-b39f-2db8387c6293"
    base_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    imf_api = DeepSeekAPI(api_key, base_url)

    # 请求数据
    messages = [
        {"role": "system", "content": "你是人工智能助手."},
        {"role": "user", "content": "常见的十字花科植物有哪些？"}
    ]

    # 调用 API
    try:
        response = imf_api.send_request(messages)
        print(response)
    except Exception as e:
        print(f"请求失败: {e}")

