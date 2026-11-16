# 수목 자산 조사·생성 기록 (2026-11-16)

## 환경 실조회
Blender 4.3.2. 일반 실행 및 factory startup 모두 Preferences의 asset_libraries는 빈 배열. 설치 애드온은 기본 입출력·Cycles·Pose Library·extension manager뿐. 등록 무료 수목 라이브러리, Sapling, BlenderKit/Blendkit는 확인되지 않았다.

## 현재 포함한 자산
`assets/trees.blend`는 이 프로젝트를 위해 직접 생성한 절차적 근사 수목이다. 외부 라이브러리 다운로드본, 사진측량본 또는 의정부 현장 수종 확정 자료가 아니다. Blender Asset Browser용 asset mark가 되어 있다. 소스는 `scripts/generate_trees.py`. 생성 데이터는 프로젝트에서 자유롭게 수정·재사용 가능하다.

- Ginkgo_Autumn_LOD0/LOD1: 부채형 잎, 황금빛 4색
- Maple_Autumn_LOD0/LOD1: 손바닥형 잎, 적색·주황 4색
- Pine_Evergreen_LOD0/LOD1: 침엽형 잎, 녹색 4색
- 원점은 지표 z=0. 높이 약 6.8~8m. 원본은 hide_render=True이므로 배치 복제본은 False로 설정.
- LOD0 각 2,770 polygons, LOD1 각 732 polygons. 삼각형 수와 다르므로 수치 혼용 금지.
- 잎은 알파 billboard가 아닌 독립 면이며 잔가지와 통합 mesh. 가까이서 실제 잎맥/수피를 재현한 고해상도 수목은 아니다.

## 무료 외부 후보 조사
1. Poly Haven Tree Small 02: https://polyhaven.com/a/tree_small_02
   - CC0: https://polyhaven.com/license
   - 공식 페이지에 burkea africana, 약 4.6m, 5M tris. 한국 가로수 일치종으로 취급하지 않는다.
   - 공식 API files 조회 성공. 1K blend 자체 63,805,841 bytes, 별도 텍스처 필요. 현재 파일 미다운로드·미통합.
   - API: https://api.polyhaven.com/files/tree_small_02
2. Blendkit Trident Maple Tree: https://www.blendkit.com/asset-gallery-detail/4f13cb8d-55e4-482c-9901-20e3c551051a/
   - Free, Royalty free, 38MiB, 886,598 polygons 표시. 무료는 CC0와 다름. 공개 저장소에 원본 재배포하기 전 라이선스 별도 확인 필요.
   - 현 환경 add-on/계정 연결 미확인. 미다운로드·미사용.

## 최적화 적용 안내
원본 mesh를 복사하지 말고 `obj.copy(); obj.data = master.data` 또는 collection instance로 배치한다. 각 수목의 회전·균일 크기를 미세 변경한다. 가까운 나무는 LOD0, 멀리 있는 나무는 LOD1을 사용하고 전환거리와 프레임 성능은 장면에서 실측한다. 실제로 벤치마크하지 않은 FPS는 기록하지 않는다. 현장종/위치 확인 전 수목은 근사 조경으로 관리한다.

Blender 공식 인스턴스 설명: https://docs.blender.org/manual/en/3.6/modeling/geometry_nodes/instances.html
Asset Browser 공식 설명: https://docs.blender.org/manual/en/5.0/editors/asset_browser.html

## 후속 실제 확보·LTS 검증
사용자의 후속 지시에 따라 외부 무료 에셋을 실제 확보했다. 위 미다운로드 표기는 최초 조사 시점이며 다음 상태가 최신이다.

- 공식 Blender 5.2.4 LTS Linux x64를 공식 mirror에서 받아 공식 SHA256 검증 성공, 버전 실행 확인. 기존 4.3.2를 덮어쓰지 않고 별도 설치.
- https://download.blender.org/release/Blender5.2/ / https://www.blender.org/download/lts/
- 설치본 Essentials에는 brush/node assets가 있으며 온라인 Essentials도 지원한다. 설치 기본수목 mesh는 발견되지 않았다. '기본 무료 에셋 자체가 없다'는 의미가 아니다.
- Poly Haven Tree Small02 원본 .blend 63,805,841 bytes와 텍스처10개 실제 다운로드. 각각 공식 API MD5 검증 성공. 원본은 외부 캐시에 유지하며 `polyhaven-download-manifest.json`으로 출처·해시·재다운로드 정보 보존.
- `polyhaven-tree-small02-seasonal.blend`는 실제 CC0 원본의 도시용 파생이다. 256px 패킹텍스처, 오브젝트 asset mark, 잎과 가지 개별 형태 유지. 여름/가을색 LOD1 각각120,155 polygons, 가을LOD2 30,457 polygons. 반복 배치는 mesh 공유 권장.
- 가을색은 shader 색 변형이며 원본 식물은 Burkea africana다. 의정부 실측 수종, 실제 단풍나무 종, 촬영된 가을 상태라고 주장하지 않는다.
- Blender 5.2.4에서 실제 재열기와 Cycles 렌더했고 `polyhaven-tree-small02-preview.png`에 여름/가을을 나란히 비교하였다.
