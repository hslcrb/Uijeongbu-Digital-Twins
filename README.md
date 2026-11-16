# Uijeongbu-Digital-Twins
의정부시 디지털 트윈

## 최신 5차 결과

- [최신 Blender 원본 복원 안내](blender/v5/README.md): 두 조각을 표준 Python으로 무손실 결합하고 SHA256을 확인합니다. 루트 Blender 파일은 4차 호환 스냅샷입니다.
- [낮](renders/day-v5.jpg) · [밤](renders/night-v5.jpg) · [역 외장](renders/station-cladding-v5.jpg) · [철도](renders/rail-v5.jpg)
- [5차 검증 및 저장 방식](docs/V5_REVIEW.md)

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
