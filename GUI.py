from pywebio import start_server
from pywebio.output import put_markdown, put_text, put_loading, use_scope, clear,put_html, put_buttons
from pywebio.input import input_group, select, actions
from pywebio.session import go_app
from pywebio.platform.page import config
from api import ImfAPI
from datetime import datetime
from deepseek import DeepSeekAPI
from deepseek_use import deepseek_wuxing, deepseek_huangli
from utils import get_date, get_huangli



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
    
    # 获取黄历信息
    selected_date = get_huangli()  # 获取用户输入的日期
    huangli = HuangLi.get_huangli(selected_date)

    if huangli:
        put_markdown("### 🧾 黄历查询结果")
        put_markdown(f"**阳历：** {huangli['阳历']}")
        put_markdown(f"**阴历：** {huangli['阴历']}")
        put_markdown(f"**五行：** {huangli['五行']}")
        put_markdown(f"**冲煞：** {huangli['冲煞']}")
        put_markdown(f"**彭祖百忌：** {huangli['彭祖百忌']}")
        put_markdown(f"**吉神宜趋：** {huangli['吉神宜趋']}")
        put_markdown(f"**宜：** {huangli['宜']}")
        put_markdown(f"**凶神宜忌：** {huangli['凶神宜忌']}")
        put_markdown(f"**忌：** {huangli['忌']}")
    else:
        put_text("❌ 查询失败，请稍后再试。")

        # 使用 actions 显示按钮
    option = actions(
        label="🔮 是否需要出行建议？",
        buttons=["出行建议", "退出"],  # 按钮列表
        
    )

    if option == "出行建议":
        clear()
        deepseek_huangli(huangli)
        put_buttons(["🔙 返回首页"], onclick=lambda btn: (clear(), index()))
    elif option == "退出":
        clear()  # 清除当前页面内容
        index()  # 跳转回首页
    else:
        put_text("感谢使用，欢迎下次再来！")


@config(title="五行查询")
def wuxing():
    """分析出生时间对应的五行属性，了解相生相克与五行平衡情况"""
    put_markdown("## ⚙️ 五行查询页面\n")
    
    date= get_date()  # 获取用户输入的日期和时辰
    result = ShengChen.get_shengchen(date['year'], int(date['month']), int(date['day']), date['shichen'])

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


    # 使用 actions 显示按钮
    option = actions(
        label="🔮 是否需要赛博算命？",
        buttons=["赛博算命", "退出"],  # 按钮列表
        
    )
    if option == "赛博算命":
        clear()
        deepseek_wuxing(result)
        put_buttons(["🔙 返回首页"], onclick=lambda btn: (clear(), index()))
    elif option == "退出":
        clear()  # 清除当前页面内容
        index()  # 跳转回首页
    else:
        put_text("感谢使用，欢迎下次再来！")


if __name__ == '__main__':
    ShengChen = ImfAPI("1719bf34f427805f0a1443b2ce5edf23", "http://apis.juhe.cn/birthEight/query")
    HuangLi = ImfAPI("11ca56d611cb18c09791dc23b14bb1e7", "http://v.juhe.cn/laohuangli/d")
    deepseek_api = DeepSeekAPI("d90a20d9-c192-4933-b39f-2db8387c6293", "https://ark.cn-beijing.volces.com/api/v3/chat/completions")
    
    start_server([index, calendar, wuxing], port=8080, debug=True)
