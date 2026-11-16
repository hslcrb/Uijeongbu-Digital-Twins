# 시 전역 윤곽 스트리밍

역 내부/외부 상세 모델과 동일한 원점(127.046E, 37.738N)·미터 단위를 사용한다. 웹 좌표는 x 동쪽, y 높이, z 남쪽이다. 도시 보기 버튼은 카메라만 이동하며 다른 장면으로 전환하지 않는다.

- 지상은 목표점 기준 가까운 32~48개 타일을 유지한다. 높이 4km 이상은 도시 윤곽 전체를 허용한다.
- 요청·Draco 디코딩 동시성은 2개로 제한한다. 역 모델을 먼저 표시하고 도시를 후속 로드한다.
- 타일 선택은 실제 AABB 중심/외접 반경을 사용한다. 긴 도로가 1km 격자 중심에서 멀리 뻗는 것을 고려한다.
- 화면 밖 geometry는 Three.js frustum culling을 사용한다. 거주 범위를 벗어나면 geometry/material.dispose를 호출한다.
- 실패는 2초·4초 백오프 후 총3회로 제한한다. 성공한 타일만 화면에 추가한다.
- 모든 타일은 원거리 도시 윤곽이다. 추정 높이와 DEM의 제한은 city/README.md를 참조한다.

## 재현/배포

원격 저장소 `web/city/city-tiles.tar.gz`는 104개 GLB의 무손실 보관이다. `npm ci && npm run build`에서 USTAR 안전 경로와 GLB 길이·manifest SHA를 검증하여 `web-dist/city/tiles/*.glb`로 복원한다. 서비스 중에는 별개 정적 GLB URL을 사용하므로 HTTP Range에 의존하지 않는다. GitHub Actions를 추가하지 않고 기존 Cloudflare main 네이티브 자동 빌드만 사용한다.

## 검수 범위

`node tests/city-stream.test.mjs`: 동시2개 상한, 이동 후 리소스 해제, 높은 조망의 전체 타일 로드. JavaScript 구문 검사·전체 빌드 및 타일 헤더·바이트수 검사. Blender에서는 동일좌표로 합친 조감·역 경계 렌더를 직접 확인한다. 클라우드 브라우저는 WebGL Disabled라 실제 모바일/데스크톱 GPU 프레임 수·투명 정렬 검증은 미완이다.
