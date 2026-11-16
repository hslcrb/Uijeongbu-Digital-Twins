# 의정부역 일대 시각·지도 조사 / 2026-11-16

## 모델러가 바로 쓸 자료
- `map.osm`: OpenStreetMap API 실제 좌표. 요청 bbox 127.043,37.736,127.05,37.741.
- `map-features.json`: ways 1074개, building 태그 519개, highway 태그 444개. 좌표는 [경도, 위도]. 요청 영역에 걸친 way는 영역 밖으로 길게 이어질 수 있으므로 클리핑 필요.
- 다운로드 원본: https://www.openstreetmap.org/api/0.6/map?bbox=127.043,37.736,127.05,37.741
- 저작자표시 OpenStreetMap contributors, ODbL 유지. 관계 multipolygon은 원본 XML에 있으나 이 JSON은 way만 추출했다.
- 의정부역 way1364007203의 height=0.01은 비정상값. 실제 높이로 사용 금지. building:levels=3도 역동에만 해당하며 백화점 전체와 구별.
- 코레일 의정부역 중심 약37.738056,127.046111. 경전철 의정부역 약37.7373,127.0433과 혼동 금지.

## 설계사 공식 사진 5장 직접 확인
출처: https://www.haeahn.com/ko/project/detail.do?prjctSeq=625
설계2003, 준공2012, 지상11층·지하2층, 연면적150260㎡. 사진은 준공시기 계열로 보이며 현재 간판·조경의 증거로 단정하지 않는다. 사이트 위치 표기 '서울, 의정부'의 서울은 복제하지 않는다. 사진은 건축형상 참고용, 재배포 라이선스 별도 확인.

|파일|직접 본 모델링 관찰|원본|
|---|---|---|
|haeahn-0.jpg|높은 백화점 박스와 낮은 역동은 별개. 은색 세로 핀 코너, 큰 갈색/회색 패널, 세로 광고판. 중간 깊은 곡면 캐노피와 외부 상승 계단. 역 표지는 상부 파란 글자.|https://www.haeahn.com/upload/prjctmain/20150113175815574898.jpg|
|haeahn-1.jpg|주차동 긴 반복 베이, 금속망·유리 파사드. 외부 자동차 램프는 경사지고 끝에서 크게 곡선 회전하며 기둥으로 지지됨. 단순 평면 박스 아님.|https://www.haeahn.com/upload/prjctmain/20150113175815579900.jpg|
|haeahn-2.jpg|브릴리언트광장 역 출입구 곡면 유리벽과 매우 깊은 어두운 곡면 지붕. 110 의정부 Uijeongbu 파란 역명띠, 유리 아래 KORAIL. 줄무늬 포장, 원판머리 조명기둥.|https://www.haeahn.com/upload/prjctmain/20150113175815583901.jpg|
|haeahn-3.jpg|SHINSEGAE 출입구: 넓은 어두운 캐노피, 꽃로고와 영문명, 중앙 회전문, 양측 민트색 유리 전시박스, 갈색 수직·수평 몰리언.|https://www.haeahn.com/upload/prjctmain/20150113175815588902.jpg|
|haeahn-4.jpg|실내 화장품 매장 사진. 외관 작업에는 우선 사용하지 않아도 됨.|https://www.haeahn.com/upload/prjctmain/20150113175815592903.jpg|

옛 사진에서 보이는 BURGER KING, STARBUCKS, citi, CGV10F 등은 촬영 당시 표기일 뿐 현재 입점 검증과 구분한다. 현재 검증 없이 근처 상가에 임의 간판을 반복 배치하지 않는다.

## 동쪽 공원 직접 본 사진 4장
원 게시물: https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=eecbe743-aaf1-43c1-8b43-b3f0bbc992e5
이미지 목록 확인: https://www.wegive.co.kr/contents/wetownDetail/2999457
사진 촬영일 미확인. 목록 수정일2026-06-17은 촬영일이 아니다. 공공누리 제3유형 표기가 있어 출처표시·변경금지 조건 확인 필요. 모델 참고 자료로 취급, 원본 사진을 가공 텍스처로 무단 배포하지 않는다.
- kto-2999387.jpg: 잔디, 불규칙 돌 디딤길, 당근·무 조형물, 개방형 퍼골라, 소나무의 층진 수관. 뒤로 컬러 컨테이너와 공동주택.
- kto-2999390.jpg: 초록·보라·주황 컨테이너 조합, 데크와 파라솔 테이블, 녹색 낮은 경계재가 있는 화단과 오솔길, 코키아류 원추형 식재.
- kto-2999391.jpg: 돌사자/말 조형물, 목재 보행판, 얇은 줄기의 단풍형 활엽수, 하층 초본·관목을 혼합. 단색 구형 나무만 놓는 것과 확연히 다름.
- kto-2999392.jpg: 천사날개 사진벤치, 잔디 사이 가로 디딤석, 회색 블록 포장광장, 높이·종류가 다른 수목.
원본 경로 공통 https://tong.visitkorea.or.kr/cms/resource/ 마지막두자리/번호_image2_1.JPG
해당 번호: 2999387,2999390,2999391,2999392.

## 도시 배치 자료
- https://ui4u.go.kr/tour/contents.do?mId=0103000000 : 행복로는 역전교차로~파발교차로 약600m, 평화로·호국로·시민로·태평로 둘러싼 구역의 보행축. 조형물·벤치·소나무·공연공간·인공 물길.
- https://ui4u.go.kr/tour/contents.do?mId=0103040000 : 로데오거리, 행복로에서 제일시장 방면. 역쪽 진입부 이성계상 기준 오른편 네온 로데오 조형물 안내.
- https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=aca02a77-35ff-4359-b981-a54dbb90581a : 역 동쪽4/5번 출구 인근 역전근린공원. 미군기지 담장 보존, 우호기념물, 베를린장벽, 안중근상 등. 각각의 정확한 배치 좌표는 추가 대조 필요.
- https://s.shinsegae.com/store/main.do?storeCd=SC00010 : 신세계 의정부점 공식, 평화로525.

## 추가 대조 후보 / 아직 직접 영상 재생 안 함
- https://zenith2.tistory.com/15862539 : 2025-03-23 방문 / 2025-04-07 게시. 사진23·24 역 외부. 캐시 이미지 서명 만료410 때문에 최신 HTML 재취득 필요.
- https://www.youtube.com/watch?v=JaViZF7Lc8I : 2021-09-06 게시 의정부 거리 4K 걷기. 최신성 제한, 아직 시청하지 않음.
- https://commons.wikimedia.org/wiki/Category:Uijeongbu_Station_(Korail) : 외관 파일 A01~A04 및2025 교외선 자료, 파일별 날짜/라이선스 확인 후 활용.
- https://www.fnnews.com/news/202503192113443362 : 2025 야경 기사 후보, 아직 이미지 정밀 대조 전.

## 정확도 원칙
지리적 footprint는 실제 OSM 데이터이나 측량도와 동일하지 않다. 외관은 공식 사진으로 관찰한 요소를 우선 반영한다. 미확인 높이·신규 간판·현시점 공사상태·수목 위치는 추정으로 분리하고 완벽한 최신 실측이라고 표기하지 않는다. 고유 상호는 확인된 면에만 배치하고, 거리명·역명과 구체 상업간판을 구분한다.
