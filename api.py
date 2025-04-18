import requests

class ImfAPI:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'X-Api-Key': self.api_key
        }
    def get_shengchen(self,year,month,day,hour):
        requestParams = {
            'key': self.api_key,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
        }
        # 发起接口网络请求
        response = requests.get(self.base_url, params=requestParams)

        # 解析响应结果
        if response.status_code == 200:
            responseResult = response.json()
            
            if responseResult['error_code'] == 0:
                result = responseResult['result']
                
                # 按需提取并格式化输出
                return {
                    "农历年份": result['year'],
                    "农历月份": result['ImonthCn'],
                    "农历日期": result['IDayCn'],
                    "属相": result['Animal'],
                    "公历日期": f"{result['cYear']}年{result['cMonth']}月{result['cDay']}日",
                    "干支纪年": result['gzYear'],
                    "干支纪月": result['gzMonth'],
                    "干支纪日": result['gzDay'],
                    "是否闰月": '是' if result['isLeap'] else '否',
                    "星期": result['ncWeek'],
                    "星座": result['astro'],
                    "八字": ' '.join(result['eightAll']['eight']),
                    "五行": ' '.join(result['fiveAll']['five']),
                    "缺木火": result['fiveAll']['lose'],
                }
                
                # for key, value in formatted_result.items():
                #     print(f"{key}: {value}")
            else:
                print('接口返回错误,error_code:', responseResult['error_code'])
        else:
            print('请求异常')
    def get_huangli(self,date):
        requestParams = {
            'key': self.api_key,
            'date': date,
        }
        # 发起接口网络请求
        response = requests.get(self.base_url, params=requestParams)

        # 解析响应结果
        if response.status_code == 200:
            responseResult = response.json()
            
            if responseResult['error_code'] == 0:
                result = responseResult['result']
                
                # 按需提取并格式化输出
                return {
                    "阳历": result['yangli'],
                    "阴历": result['yinli'],
                    "五行": result['wuxing'],
                    "冲煞": result['chongsha'],
                    "彭祖百忌": result['baiji'],
                    "吉神宜趋": result['jishen'],
                    "宜": result['yi'],
                    "凶神宜忌": result['xiongshen'],
                    "忌": result['ji'],
                }
                
                # for key, value in formatted_result.items():
                #     print(f"{key}: {value}")
            else:
                print('接口返回错误,error_code:', responseResult['error_code'])
        else:
            print('请求异常')
        

if __name__ == "__main__":
    ShengChen=ImfAPI("1719bf34f427805f0a1443b2ce5edf23", "http://apis.juhe.cn/birthEight/query")
    ShengChen.get_shengchen(2004, 6, 25, 11)

    HuangLi=ImfAPI("11ca56d611cb18c09791dc23b14bb1e7", "http://v.juhe.cn/laohuangli/d")
    HuangLi.get_huangli("2025-4-11")