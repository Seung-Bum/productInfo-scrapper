# productInfo-scrapper

\*\* gsshop의 품절 상품 체크

- 품절은 [바로 구매] 버튼 문구 대신 [품절]이라고 나옴

* 상품링크

  - sectid에 의해서 카테고리가 나뉜다  
    https://www.gsshop.com/shop/sect/sectL.gs?sectid=

  - 링크예시  
    . 린스컨디셔너  
    http://localhost:5000/extract?sectid=1661646

    . 포인트메이크업  
    http://localhost:5000/extract?sectid=1660623

* 페이지 정보 base64 encoding 예시  
  eyJwYWdlTnVtYmVyIjo3Nywic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9

* 페이지 정보 base64 decoding 예시  
  {"pageNumber":2,"selected":"opt-page"}  
  {"pageNumber":3,"selected":"opt-page"}  
  {"pageNumber":9,"selected":"opt-page"}

* reference

  - 파이썬 웹 스크래퍼 강의  
    https://nomadcoders.co/python-for-beginners

  - 온라인 base64 디코딩/인코딩  
    https://www.base64decode.org/ko/

  - 리플릿  
    . 간단한 토이프로젝트를 배포할때 유용  
     https://programming4myself.tistory.com/4

- request url  
  https://auto-trading.tistory.com/entry/%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%95%88%EB%90%A0-%EB%95%8C-%ED%95%B4%EA%B2%B0%EB%B2%95%EB%84%A4%EC%9D%B4%EB%B2%84%EB%8B%A4%EC%9D%8C%EA%B5%AC%EA%B8%80-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%B0%A8%EB%8B%A8-%ED%95%B4%EA%B2%B0

- pip install lxml  
  . html로 파싱할때보다 파싱 속도를 높인다고함  
   https://balsamic-egg.tistory.com/15

- lxml install 후 프로그램 예외발생 시 확인  
  https://intostock.tistory.com/50

- .exe 실행파일 생성하기  
  https://www.youtube.com/watch?app=desktop&v=Es1fQqqxIFQ

- gsmtp 인증 에러 발생시 참고  
  (smtplib.SMTPAuthenticationError: (534, b'5.7.9 Application-specific password required. Learn more)  
  https://greensul.tistory.com/31  
  https://myaccount.google.com/
