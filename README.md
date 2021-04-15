# insert-bjd

https://www.code.go.kr/stdcode/regCodeL.do

정부 사이트인 행정표준코드 관리시스템의 법정동 코드

에서 다운 받을 수 있는 "법정동 코드 전체 자료"

법정동코드 전체자료.txt

를 사용하기 편리한 컬럼으로 분할 해서 데이터베이스 삽입


|컬럼이름|자료형|크기|예시|설명|
|------|---|---|---|---|
|code|string|10|1168010500|법정동코드 10자리|
|sido_code|string|2|서울특별시 11, 부산시 26.. |시도 코드 2자리|
|sigungu_code|string|5|서울특별시 강남구 코드 11680|시군구 코드 5자리|
|bjd_code|string|5|서울특별시 강남구 삼성동 코드 10500|법정동 코드 5자리|
|sido_name|string|255(varchar)|서울특별시|시도 이름|
|sigungu_name|string|255(varchar)|강남구|시군구 이름|
|dong_name|string|255(varchar)|삼성동|음면동 이름|
|ri_name|string|255(varchar)|진관리|리 이름|

해당 코드에는 pymysql을 사용해서 mysql db에 삽입해주는데
다른 db를 사용 하려면
최종 리턴 값인 data 리스트 이후에 insert_data() 를 바꿔서 사용하면 됨