# Uijeongbu-Digital-Twins
의정부시 디지털 트윈

## 의정부역 Blender 외관 연구

- [Blender 장면 다운로드](Uijeongbu_Station_v1.blend)
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
