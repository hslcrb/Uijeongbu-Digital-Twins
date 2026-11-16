# Uijeongbu-Digital-Twins
의정부시 디지털 트윈

## 의정부역 Blender 외관 연구

- [최신 7차 Blender 복원·다운로드](blender/v8/README.md)
- [도시 전체 윤곽 Blender](blender/city/Uijeongbu_City_Outline.blend)
- [기존 v4 호환 스냅샷](Uijeongbu_Station_v1.blend), [v5 보존본](blender/v5/README.md)
- [최신 서측 낮](renders/west-v7.jpg) · [서측 밤](renders/west-night-v7.jpg) · [도시 통합 전경](renders/city-integration.jpg)
- [낮 전경](renders/day-overview.jpg) · [야경](renders/night-overview.jpg) · [광장](renders/plaza.jpg)
- [모델 범위·사용법·미검증 사항](docs/README_MODEL.md)
- [사진 및 지도 근거](reference/RESEARCH.md)
- [무료 수목 자산·라이선스](docs/TREE_ASSETS.md)

Blender 5.2.4 LTS, 지도 기반 494동 주변 건물과 역사/백화점 22매스, 편집 가능한 낮·석양·밤 조명. 사진에 근거한 첫 외관 연구 모델이며 완전한 현장 실측이나 최신 간판 전수 복제는 아닙니다.

## 웹 보기
https://twin.uijeongbu.rhee.life/

`npm ci && npm run build`로 웹을 빌드합니다. Cloudflare 네이티브 Git main 자동배포를 사용하며 GitHub Actions는 사용하지 않습니다. 대합실은 별도 장면 전환이 아닌 외관과 동일 좌표의 단일 모델에 연결됩니다.

## 도시 윤곽 레이어 (6차)

웹의 **시 전역 윤곽** 버튼으로 의정부시 지형·건물·도로 윤곽을 같은 공간에서 조망할 수 있다. 104개 타일(약4MB)을 거리 기반으로 순차 로드한다. 원본 지도 기록은 9,094개 건물과 9,721개 도로 way이며, 확인되지 않은 높이·외장은 근사이다. 실제 시내 건물 전수 정밀 복원은 아니다. 지형은 SRTM계열 DEM의80m 재표본 윤곽이고 역 경계에 인위적 고도 전이를 사용한다.

타일은 `web/city/city-tiles.tar.gz`에 보관하며 빌드시104개의 독립 GLB로 복원된다. [스트리밍 검수와 한계](docs/CITY_STREAMING.md), [개발과정기](docs/DEVELOPMENT_JOURNAL.md)를 참조한다.

## 7차 서부 접근 개선

2025년 사진과 지도 계단 방향을 기준으로 서측 접근·유리 캐노피·보조동 루버를 보강하고, 중복 계단·떠 있는 지면 측면·데크 아래에 있던 조명 기둥을 교정했다. 새 부품은 재질별5개 메시로 묶었다. [근거와 추정 구분](docs/WEST_V7_EVIDENCE.md)을 참조한다. 포켓쉼터 가구와 택시쉼터는 정확한 위치가 아직 확인되지 않아 임의 배치하지 않았다.

최신 역 Blender는 `python blender/v7/restore.py`로 분할 보존본을 검증·복원한다. 루트의 `Uijeongbu_Station_v1.blend`는 최신 파일이 아니라 이전 v4 스냅샷이다. 웹은 `web/assets/station.glb.gz`를 빌드시 복원하여 최신 모델을 사용한다.

## 8차 창 형상 교정 및 서측 사진 세부

최신 원본은 [v8 복원 안내](blender/v8/README.md)를 따른다. 493개 footprint 방향을 검증하고, 안쪽 여유 두께를 넘어가는 절차적 방을 제한했다. 서측 수평 진입처마·유리 격자·원형 주기둥·석재 측벽을 추가했다. [변경 전](renders/windows-before-v8.png) · [변경 후](renders/windows-after-v8.png) · [서측 낮](renders/west-v8.jpg) · [서측 밤](renders/west-night-v8.jpg). 실제 창 배치·실내 점유는 측량 자료가 아닌 근사다.
