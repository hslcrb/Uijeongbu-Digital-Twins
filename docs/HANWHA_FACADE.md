# 한화생명 의정부 사옥 외관별 개선

- 정확한 대상: OSM way1466029481, 평화로516. 현재 OSM 객체 이름은 1층 입점 하나은행이지만 건물 자체는 한화생명빌딩이다.
- 교차근거: 하나은행 지점공식 https://openhanafn.ttmap.co.kr/mobile/content_m.jsp?seq_no=457 / 한화63시티 공식 2026년9월 임대안내 p9 https://www.63realty.co.kr/comm/oneFileDownload?file_sq=1 . PDF를 직접 열어 외관사진과 10F/B4를 확인했다. 자료 담당자 연락처는 기록/모델에 복사하지 않았다.
- 2025-03-23 방문사진 https://zenith2.tistory.com/15862539 의 23번째 사진도 직접 대조했다. brown/bronze mirror curtainwall, 좁은 격자, 상부 검은 띠, 모서리의 흰 옥상광고탑, 확인한 한화생명 텍스트를 구현했다. 공식 PDF에 보이는 하나은행 글자도 반영했다. 로고를 추측해 그리지는 않았다.
- 층수는 OSM11층 대신 공식10층 채택. 42m 높이는 OSM 태그를 사용했으며 실측높이로 단정하지 않는다. 패널간격, 후면, 실별 점등은 절차적 근사다. 지하4층은 외관 수치 기록이며 이번 지하층 모델 미구현.
- `hanwha_facade.enhance_hanwha()`를 전체창빛 생성후 호출한다. 기존 단순 건물과 해당footprint 내부의 공통창/room batch 면을 지운 뒤 새 모델만 넣어 중복표면을 방지한다. 같은 컬렉션 재호출은 no-op.
- 검증: 독립 사본으로 Cycles 외관 렌더·글자 확인. 본체 .blend를 직접 덮어쓰지 않았으며 주 모델러의 최종 통합/GLB 검증이 남아 있다.
