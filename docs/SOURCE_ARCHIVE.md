# 의정부 자료·이미지 출처 및 백업 감사 — 2026-11-17

## 실제 범위
`1c0449b` 이후 현 저장소의 출처·데이터·이미지·개발기와 남아 있는 v14~v18 복구 자료를 확인했다. 이 문서는 **과거에 본 모든 웹페이지와 이미지를 전부 백업했다는 주장이 아니다.** 임시 폴더 및 전체 조회 이력은 완전히 복구되지 않았다.

## 출처별 연결
|구분|출처|사용 및 보존|
|---|---|---|
|지도/도시 지형|https://www.openstreetmap.org/copyright|ODbL, `data/map.osm.gz`, `city/data/manifest.json`, 도시 타일 및 추출본|
|철도 경로|https://www.openstreetmap.org/relation/8691899 / https://www.openstreetmap.org/relation/7530882|6개 파생 경로 `web/rail/network.json`; relation ID/제약은 `docs/RAIL_NETWORK_SOURCES.md`|
|역사 외관|https://www.haeahn.com/ko/project/detail.do?prjctSeq=625|설계사 사진별 URL/관찰 `reference/RESEARCH.md`; 사진 재배포 권리는 미확인|
|방문사진|https://zenith2.tistory.com/15862539 / https://hhk2001.tistory.com/8063|후속 외관/유리띠/자전거시설 대조. `scripts/recovery-20261117/v14-v18`의 개발기·research-manifest 유지|
|한화생명 건물|https://www.63realty.co.kr/comm/oneFileDownload?file_sq=1|공식 임대자료 및 사진 관찰은 `docs/HANWHA_FACADE.md`. 담당자 연락처는 복사하지 않음|
|공원|https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=eecbe743-aaf1-43c1-8b43-b3f0bbc992e5|관찰 기록과 원본 URL은 `reference/RESEARCH.md`, 공공누리 조건을 확인해야 함|
|나무|https://polyhaven.com/a/tree_small_02|CC0 원본 다운로드 manifest·파생 blend `assets/`; 의정부 현장 수종이라는 증거가 아님|
|표지 글꼴|`scripts/recovery-20261117/korail-font` 및 `LICENSES/OFL.txt`|폰트 출처와 허용범위는 해당 기록을 읽을 것. 모든 글꼴이 동일 라이선스라는 뜻 아님|
|절차적 수목/노면/가상 열차|프로젝트 스크립트|생성 소스·검증 기록. 실제 신호/실시간 도착 API가 아님|

## 새 색인·백업
- `reference/audit-20261117/source-urls.json`: 문서/스크립트에 남은 URL과 근거 파일을 전수 추출. 출처·검토 후보·단순 기술 링크가 섞여 있다. 모든 URL을 이번에 새로 열람했다는 의미가 아니다.
- `reference/audit-20261117/existing-assets.json`: 기존 렌더·데이터·모델·압축원본 해시 목록.
- `reference/generated-renders/`: 로컬에서 복구된 v14~v18 자체 제작 렌더 원본 추가 보존. Blender 미리보기이며 앱 캡처/현장 사진이 아니다.
- `reference/audit-20261117/withheld-third-party.json`: 현재 복구 가능하나 공개 재배포 권리가 확인되지 않은 타인 사진의 원본 게시물·SHA256·보류 이유.
- `reference/backup-checksums.json`: 이 reference 디렉터리의 해시 목록.

## 공개 저장소의 권리 경계
GitHub API에서 이 저장소가 public임을 확인했다. 출처를 적었다는 사실만으로 사진 재배포 허가가 생기지는 않는다. 따라서 권리 미확인 타인 원본 사진은 이 공개 저장소에 새로 올리지 않았다. URL, 관찰, 이미 존재하는 연구 manifest는 유지했다. 사용자에게 전달된 모든 과거 렌더가 현 작업공간에 남아 있지 않아 현재 복구 가능 목록을 보존했으며 누락이 없다고 주장하지 않는다.

## 모델 정확도와 출처의 차이
OSM 높이·층수는 측량도와 다르며, 내부는 사진 연구/근사 구성이 섞여 있다. 고도 DEM·계단과 외피 정합·전 역 스크린도어·정밀 차량 외형은 출처 목록을 갖추었다고 완성된 것이 아니다. 최신 구현 상태는 `docs/DELIVERY_STATUS_2026-11-17.md`를 함께 읽어야 한다.
