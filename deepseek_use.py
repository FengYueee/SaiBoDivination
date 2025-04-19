from pywebio import start_server
from pywebio.output import put_markdown, put_text, put_loading, use_scope, clear,put_html, put_buttons
from pywebio.input import input_group, select, actions
from pywebio.session import go_app
from pywebio.platform.page import config
from api import ImfAPI
from datetime import datetime
from deepseek import DeepSeekAPI

deepseek_api = DeepSeekAPI("d90a20d9-c192-4933-b39f-2db8387c6293", "https://ark.cn-beijing.volces.com/api/v3/chat/completions")

def deepseek_wuxing(result):
    with use_scope('loading', clear=True):
        put_html("""
        <div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh;">
            <div class="loader"></div>
            <p style="font-size:18px; color:#555;">🔮 正在召唤赛博大仙，请稍候片刻...</p>
        </div>
        <style>
            .loader {
                border: 8px solid #f3f3f3;
                border-top: 8px solid #3498db;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                animation: spin 1s linear infinite;
                margin: 20px;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
        """)
    messages = [
        {"role": "system", "content": "你是人工智能助手."},
        {"role": "user", "content": f"{result}请帮我进行算命"}
    ]

    # 调用 DeepSeekAPI 进行查询
    response = deepseek_api.send_request(messages)

    with use_scope('loading', clear=True):
        put_html("""
            <div style="max-width: 800px; margin: 40px auto 20px; font-family: 'Segoe UI', sans-serif;">
                <h2 style="color: #2c3e50; font-size: 28px; font-weight: 700; text-align: left; margin-bottom: 10px;">
                    🧾 您的命格为
                </h2>
            </div>
            """)

        # 用 Markdown 输出内容
        put_markdown(response)


def deepseek_huangli(result):
    with use_scope('loading', clear=True):
        put_html("""
        <div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh;">
            <div class="loader"></div>
            <p style="font-size:18px; color:#555;">🔮 正在召唤赛博大仙，请稍候片刻...</p>
        </div>
        <style>
            .loader {
                border: 8px solid #f3f3f3;
                border-top: 8px solid #3498db;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                animation: spin 1s linear infinite;
                margin: 20px;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
        """)
    messages = [
        {"role": "system", "content": "你是人工智能助手."},
        {"role": "user", "content": f"{result}帮我查询出行建议"}
    ]

    # 调用 DeepSeekAPI 进行查询
    response = deepseek_api.send_request(messages)

    with use_scope('loading', clear=True):
    # 美化标题部分
        put_html("""
        <div style="max-width: 800px; margin: 40px auto 20px; font-family: 'Segoe UI', sans-serif;">
            <h2 style="color: #2c3e50; font-size: 28px; font-weight: 700; text-align: left; margin-bottom: 10px;">
                🧾 您的出行建议
            </h2>
        </div>
        """)

        # 用 Markdown 输出内容
        put_markdown(response)
