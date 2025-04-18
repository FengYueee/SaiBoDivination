from pywebio import start_server
from pywebio.output import put_markdown, put_text, put_loading, use_scope, clear,put_html
from pywebio.input import input_group, select, actions
from pywebio.session import go_app
from pywebio.platform.page import config
from api import ImfAPI
from datetime import datetime
from deepseek import DeepSeekAPI

@config(title="命理查询首页")
def index():
    """欢迎使用命理查询系统，这里你可以进入黄历和五行查询功能。"""
    put_markdown("""
# 🧙‍♂️ 命理查询系统

欢迎使用命理查询系统，请选择你要使用的功能：
    """)
    option = actions(
            label="选择你要进入的功能：",
            buttons=["黄历查询", "五行查询"]
        )

    if option == "黄历查询":
        clear()  # 清除当前页面内容
        calendar()  # 调用黄历查询页面
    elif option == "五行查询":
        clear()  # 清除当前页面内容
        wuxing()  # 调用五行查询页面
    else:
        put_text("感谢使用，欢迎下次再来！")


@config(title="黄历查询")
def calendar():
    """查看每日黄历，包含宜忌、节气、值日等信息"""
    put_markdown("## 📅 黄历查询页面\n")
    # 这里可以添加黄历的具体内容和功能


@config(title="五行查询")
def wuxing():
    """分析出生时间对应的五行属性，了解相生相克与五行平衡情况"""
    put_markdown("## ⚙️ 五行查询页面\n")
    current_year = datetime.now().year
    years = [str(y) for y in range(1900, current_year+1)]
    months = [str(m).zfill(2) for m in range(1, 13)]
    days = [str(d).zfill(2) for d in range(1, 32)]
    shichen = [
        "子时 (23:00-01:00)", "丑时 (01:00-03:00)", "寅时 (03:00-05:00)", "卯时 (05:00-07:00)",
        "辰时 (07:00-09:00)", "巳时 (09:00-11:00)", "午时 (11:00-13:00)", "未时 (13:00-15:00)",
        "申时 (15:00-17:00)", "酉时 (17:00-19:00)", "戌时 (19:00-21:00)", "亥时 (21:00-23:00)"
    ]

    data = input_group("请选择出生年月日和时辰", [
        select("出生年份", options=years, name='year'),
        select("出生月份", options=months, name='month'),
        select("出生日", options=days, name='day'),
        select("出生时辰", options=shichen, name='shichen'),
    ])

    data['shichen'] = get_shichen_index(shichen, data['shichen'])
    
    result = ShengChen.get_shengchen(data['year'], int(data['month']), int(data['day']), data['shichen'])

    if result:
        put_markdown("### 🧾 查询结果")
        put_markdown(f"**公历日期：** {result['公历日期']}")
        put_markdown(f"**农历日期：** {result['农历年份']}年 {result['农历月份']}{result['农历日期']}")
        put_markdown(f"**属相：** {result['属相']}")
        put_markdown(f"**干支纪年：** {result['干支纪年']}")
        put_markdown(f"**干支纪月：** {result['干支纪月']}")
        put_markdown(f"**干支纪日：** {result['干支纪日']}")
        put_markdown(f"**是否闰月：** {result['是否闰月']}")
        put_markdown(f"**星期：** {result['星期']}")
        put_markdown(f"**星座：** {result['星座']}")
        put_markdown(f"**八字：** {result['八字']}")
        put_markdown(f"**五行：** {result['五行']}")
        put_markdown(f"**缺木火：** {result['缺木火']}")
    else:
        put_text("❌ 查询失败，请检查输入的日期和时辰。")

    option = actions(
        label="是否需要赛博算命：",
        buttons=["赛博算命", "退出"]
    )

    if option == "赛博算命":
        deepseek(result)
        option1 = actions(
            buttons=[ "退出"]
        )
        if option1 == "退出":
            clear()
            index()  # 跳转回首页
    elif option == "退出":
        clear()  # 清除当前页面内容
        index()  # 跳转回首页
    else:
        put_text("感谢使用，欢迎下次再来！")
    
def get_shichen_index(shichen, shichen_str):
    """
    根据时辰字符串返回其在时辰列表中的索引
    """
    try:
        return shichen.index(shichen_str) * 2
    except ValueError:
        return -1  # 或者 raise 异常，视你想怎么处理

def deepseek(result):
    with use_scope('loading', clear=True):
        put_html("""
        <div style="text-align:center; padding:30px;">
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
                margin: auto;
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
        put_markdown("### 🧾 查询结果")
        put_markdown(response)
    

if __name__ == '__main__':
    ShengChen = ImfAPI("1719bf34f427805f0a1443b2ce5edf23", "http://apis.juhe.cn/birthEight/query")
    HuangLi = ImfAPI("11ca56d611cb18c09791dc23b14bb1e7", "http://v.juhe.cn/laohuangli/d")
    deepseek_api = DeepSeekAPI("d90a20d9-c192-4933-b39f-2db8387c6293", "https://ark.cn-beijing.volces.com/api/v3/chat/completions")
    
    start_server([index, calendar, wuxing], port=8080, debug=True)
