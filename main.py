import pandas as pd
import pymysql

# input your env!
db_endpoint = ''
db_user = ''
db_psw = ''
db_name = ''
db_charset = ''

db_bjd_table_name = ''

conn = pymysql.connect(host=db_endpoint, user=db_user, password=db_psw,
                       db=db_name, charset=db_charset)
cursor = conn.cursor()

# 지역은 시도, 시군구, 읍면동, 리 4개로 분할
# 두번째 항목인 시군구에서 시와 구가 합쳐친 예외 지역들이 존재
# 아래 지역들이 예외
multi_sigungu = [
    '고양시 덕양구',
    '고양시 일산동구',
    '고양시 일산서구',
    '성남시 분당구',
    '성남시 수정구',
    '성남시 중원구',
    '수원시 권선구',
    '수원시 영통구',
    '수원시 장안구',
    '수원시 팔달구',
    '안산시 단원구',
    '안산시 상록구',
    '안양시 동안구',
    '안양시 만안구',
    '용인시 기흥구',
    '용인시 수지구',
    '용인시 처인구',
    '청주시 상당구',
    '청주시 서원구',
    '청주시 청원구',
    '청주시 흥덕구',
    '천안시 동남구',
    '천안시 서북구',
    '포항시 남구',
    '포항시 북구',
    '창원시 마산합포구',
    '창원시 마산회원구',
    '창원시 성산구',
    '창원시 의창구',
    '창원시 진해구',
    '전주시 덕진구',
    '전주시 완산구',
]


def extract_from_txt_file(file_name):
    raw_data = pd.read_csv(file_name, sep="\t", engine='python', encoding='CP949')
    bjd_dict_list = raw_data.to_dict('records')
    result = []
    for bjd in bjd_dict_list:
        if bjd['폐지여부'] != '존재':
            continue

        result_bjd = {}

        if '세종특별자치시' in bjd['법정동명']:
            split_bjd = bjd['법정동명'].split(' ')
            if len(split_bjd) > 1:
                if split_bjd[1] == '세종특별자치시':
                    del split_bjd[1]
                split_bjd.insert(1, '세종시')
            result_bjd = assign(split_bjd)
        elif any(ms in bjd['법정동명'] for ms in multi_sigungu):
            split_bjd = bjd['법정동명'].split(' ')
            parsed_sigungu = ' '.join([split_bjd[1], split_bjd[2]])
            del split_bjd[1]
            del split_bjd[1]
            split_bjd.insert(1, parsed_sigungu)
            result_bjd = assign(split_bjd)
        else:
            split_bjd = bjd['법정동명'].split(' ')
            result_bjd = assign(split_bjd)

        bjd_code_str = str(bjd['법정동코드'])

        result_bjd['code'] = bjd_code_str
        result_bjd['sido_code'] = bjd_code_str[:2]
        result_bjd['sigungu_code'] = bjd_code_str[:5]
        result_bjd['bjd_code'] = bjd_code_str[5:]

        result.append(result_bjd)
    return result


def assign(splited):
    res = {'sido_name': splited[0], 'sigungu_name': splited[1] if len(splited) >= 2 else '',
           'dong_name': splited[2] if len(splited) >= 3 else '', 'ri_name': splited[3] if len(splited) >= 4 else ''}
    return res


def insert_data(data):
    cols = ", ".join('`{}`'.format(k) for k in data[0].keys())
    val_cols = ', '.join('%({})s'.format(k) for k in data[0].keys())
    sql = "INSERT INTO %s(%s) VALUES(%s)"
    res_sql = sql % (db_bjd_table_name, cols, val_cols)
    cursor.executemany(res_sql, data)
    conn.commit()


if __name__ == '__main__':
    file = '법정동코드 전체자료.txt'
    data = extract_from_txt_file(file)
    insert_data(data)
    conn.close()