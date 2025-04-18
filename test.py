from pywebio import start_server
from pywebio.output import put_buttons, put_text,put_markdown,put_link
from pywebio.session import go_app
from pywebio.platform.page import config
from api import ImfAPI 

def task_1():
    put_text('task_1')
    put_buttons(['Go task 2'], [lambda: go_app('task_2')])

def task_2():
    put_text('task_2')
    put_buttons(['Go task 1'], [lambda: go_app('task_1')])

def index():
    put_link('Go task 1', app='task_1')  # Use `app` parameter to specify the task name
    put_link('Go task 2', app='task_2')
    put_buttons(
        ['黄历查询', '五行查询'],
        onclick=[lambda: go_app('task_1'), lambda: go_app('task_2')]
    )
# equal to `start_server({'index': index, 'task_1': task_1, 'task_2': task_2})`
start_server([index, task_1, task_2])