1. cmd 창을 킨다.

2. mysql을 실행한다 
    - cmd로 실행할 경우 mysql이 있는 경로로 들어가서 실행해야한다.
    - 실행 코드는 ./mysql -u root -p
<br>

3. SET GLOBAL local_infile =1; 를 친다

4. quit 으로 나간다.

5. ./mysql --local-infile=1 -u root -p 를 친다
    - 안된다면 ./mysql --local-infile=1 -u root -p1 로 해보자 
<br>

6. 에러가 안난다면 mysql에 로컬로 들어가진다. 

7. 로컬로 들어간 mysql에서 LOAD DATA LOCAL INFILE '경로명/파일명' INTO TABLE 테이블명 FIELDS TERMINATED BY ','; 을 친다.
    - 안된다면 LOAD DATA INFILE '경로명/파일명' INTO TABLE 테이블명 FIELDS TERMINATED BY ',';
    - use 해당db명 쓰고 7번 쓰기
<br>

★주의★
맥에서 가동한 것이므로 cmd창에서 저 코드들이 실행안될경우 윈도우 버전으로 찾아보시길..
