from pywebio import start_server
from pywebio.output import put_markdown, put_text, put_loading, use_scope, clear,put_html, put_buttons
from pywebio.input import input_group, select, actions
from pywebio.session import go_app
from pywebio.platform.page import config
from api import ImfAPI
from datetime import datetime

def get_shichen_index(shichen, shichen_str):
    """
    根据时辰字符串返回其在时辰列表中的索引
    """
    try:
        return shichen.index(shichen_str) * 2
    except ValueError:
        return -1  # 或者 raise 异常，视你想怎么处理
    
def get_date():
    current_year = datetime.now().year
    years = [str(y) for y in range(1900, current_year+1)]
    months = [str(m).zfill(2) for m in range(1, 13)]
    days = [str(d).zfill(2) for d in range(1, 32)]
    shichen = [
        "子时 (23:00-01:00)", "丑时 (01:00-03:00)", "寅时 (03:00-05:00)", "卯时 (05:00-07:00)",
        "辰时 (07:00-09:00)", "巳时 (09:00-11:00)", "午时 (11:00-13:00)", "未时 (13:00-15:00)",
        "申时 (15:00-17:00)", "酉时 (17:00-19:00)", "戌时 (19:00-21:00)", "亥时 (21:00-23:00)"
    ]

    date = input_group("请选择出生年月日和时辰", [
        select("出生年份", options=years, name='year'),
        select("出生月份", options=months, name='month'),
        select("出生日", options=days, name='day'),
        select("出生时辰", options=shichen, name='shichen'),
    ])

    date['shichen'] = get_shichen_index(shichen, data['shichen'])
    return date

def get_huangli():
    # 获取用户输入的日期
    current_year = datetime.now().year
    years = [str(y) for y in range(2025, current_year+1)]
    months = [str(m).zfill(2) for m in range(1, 13)]
    days = [str(d).zfill(2) for d in range(1, 32)]

    # 让用户选择日期
    data = input_group("请选择日期", [
        select("年份", options=years, name="year"),
        select("月份", options=months, name="month"),
        select("日期", options=days, name="day")
    ])
    
    # 组合为日期格式
    selected_date = f"{data['year']}-{data['month']}-{data['day']}"
    return selected_date
