import requests
from bs4 import BeautifulSoup as bs

url = 'http://nu.ac.bd/results/cse/cse_result.php?roll_number=&reg_no={}&exm_code={}&exam_year={}'

def grab(reg, xm_code, year):
    req = requests.get(url.format(reg, xm_code, year))
    html = bs(req.text, 'html.parser')
    info = html.findAll(attrs={'id':'customers'})
    if info:
        std_info = _studentINFO(info[0])
        std_res = _studentRES(info[1])
        std_info['result'] = std_res
        return std_info
    return {'result': None}

def _studentINFO(info):
    td = info.findAll(name='td')
    data = {}
    for i, t in enumerate(td):
        if i%2 != 0:
            data[td[i-1].text.strip()] = t.text.strip()
    return data


def _studentRES(res):
    td = res.findAll(name='td')[5:]
    data = {}
    for i, dt in enumerate(td):
        if i%4 == 3:
            if len(str(int(td[i-3].text.strip()))) > 4:
                courese_code = '_'+str(int(td[i-3].text.strip()))
            else:
                courese_code = 'CSE_'+str(int(td[i-3].text.strip()))
            data[courese_code] = {
                    "name": td[i-2].text.strip(),
                    "cradit": td[i-1].text.strip(),
                    "grade": dt.text.strip(),
                }
    return data




