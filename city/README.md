# 의정부시 전체 윤곽 레이어

실제 OSM 의정부시 행정경계 relation 2409183에 대해 20개 API bbox를 다운로드하고 way ID로 중복 제거했다. 데이터 취득: 2026-11-16 UTC (2026-11-17 KST). 행정경계 안의 중심점을 가진 건물·도로를 사용한다. 경계로 모든 geometry를 정확히 잘라낸 지적도는 아니며 OSM 누락 객체는 존재하지 않는다. 이 결과를 '실제 시내 건물 전수 복원'이라고 부르지 않는다.

## 실제 데이터와 근사
- 건물 평면: OSM closed building way. 높이 태그 우선, 층수 있으면 층당3.1m, 둘 다 없으면 용도별7.5m/18m 근사. 외관·창문·간판 없음.
- 지형: Mapzen/Tilezen AWS `skadi/N37/N37E127.hgt.gz`, 3601×3601 1초각 샘플. 도시 윤곽은80m mesh로 재샘플링한다. SRTM 계열 표면고도이므로 건물/나무 영향과 수직오차가 있으며 정밀측량·지하차도엔 부적합.
- 원점: 127.046E,37.738N, East x/North y, meters. 기준 고도는 원점 DEM에서 읽는다. 기존 역 장면을 유지하려 역부지 근처 고도를0으로 blend하는 인위적 전이가150m 적용된다.
- 역부지 x=-265..355,y=-225..335는 중복방지 위해 제외. 경계연결은 정밀 CAD 정합 아님.
- 각1km tile·레이어별 batch. 건물/도로/지형3종. 도로를 tile별합집합하여 같은 높이 ribbon 중복 제거. 도시윤곽은 원경 LOD, 역 정밀장면 대체아님.

## 출처/라이선스
- © OpenStreetMap contributors, ODbL1.0 https://www.openstreetmap.org/copyright
- 행정경계 https://nominatim.openstreetmap.org/search?q=의정부시&format=json&polygon_geojson=1
- 지도 원자료 https://api.openstreetmap.org/api/0.6/map (20bbox, download-index.json)
- Elevation: Mapzen/Tilezen Terrain Tiles https://registry.opendata.aws/terrain-tiles/
- `SRTM data courtesy of the U.S. Geological Survey`.
- Terrain provider attribution and terms: https://github.com/tilezen/joerd/blob/master/docs/attribution.md
- Elevation source https://s3.amazonaws.com/elevation-tiles-prod/skadi/N37/N37E127.hgt.gz

## 통합
Blender 원점과 역 원점 같음. `city_` 접두사 메시 오브젝트를 append하면 공간적으로 정렬된다. 카메라 거리별 tile가시성 사용 권장. 웹은 전체GLB 즉시로딩보다 타일manifest+distance stream 권장. 단순 윤곽을 밀리미터 정밀 상세로 표시하지 않는다.

## 검증된 생성 수치
- 건물 9,094개: 높이 직접 태그 1,910개, 층수/기본값 기반 추정 7,184개.
- 도로 9,721개 OSM way. 도로 수는 실제 도로 이름 개수가 아니다.
- 지형 12,759개 80m 셀, 268개 tile-layer batch.
- 웹 원점변환: x=east, y=up, z=south. GLB 좌표에 이 변환이 적용되어 별도90도 회전 금지.
- 이 자료는 시 전역 OSM 기록의 윤곽이며 세부 간판/입면/역사 재현 완료판이 아니다.
- 타일 경계/행정경계는 객체 중심으로 분류해서 일부 도로가 경계를 넘는다. 도로 합집합은 각 타일 내부에만 적용되며 고가도로 다층 분리는 미구현이다.
- road/ground 간 거친 DEM 보간차를 줄이기 위해 도로 높이를80m terrain triangle interpolation +0.65m로 맞췄다. 이는 원경 도로 확인을 위한 시각적 offset이며 실측 지표 높이가 아니다.

## 재생성
시스템 Python에 Shapely 필요. Blender에서 build_city.py 실행 후 export_city.py 실행.
fetch_tiles.py, download-index.json, boundary-search.json 및 명시된 원본HGT URL 사용.
시스템 Python 실행경로는 각 컴퓨터 환경에 맞게 build_city.py의 subprocess 부분을 변경.

### 역 경계 교정
후속 접합검수에서 셀 중심 제외가 최대40m 가장자리 틈/겹침을 만들 수 있음을 확인했다. `clip_station.py`는 전체 terrain triangle을 정확한 역 제외사각형과 difference한 후 재삼각화한다. 따라서 XY지형 경계는 정확한 사각형이며, 역 바닥0m와 도시지형 간 수직정합은 여전히 고도blend 근사이다. 도로 역시 같은 사각형 차집합으로 처리된다.

실제 역 Study area 바닥은 x[-285,375],y[-250,360],z=0이므로 지형제외/고도blend는 해당 경계로 최종 교정했다. 도로제외는 기존작업crop[-265,355]×[-225,335]를 유지한다. 지형절단경계vertex는0m로 스냅하여 틈새를 막았으며 이 접합은 인위적근사이다.
