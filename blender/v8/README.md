# 의정부역 통합 Blender v8

이 폴더의 두 `.part` 파일, `manifest.json`, `restore.py`를 함께 내려받아 `python restore.py`를 실행한다. 표준 Python만 필요하며 각 파트와 복원 결과 SHA256을 검사한다. 복원된 `Uijeongbu_Station_v8.blend`를 Blender 5.2.4 LTS로 연다.

서측 사진 기반 처마·격자·측벽 및 절차적 창의 방향·깊이 교정을 포함한다. 역·실내외는 한 공간이고 시 전역 타일 자료는 별도 `blender/city`와 웹 스트리밍으로 보존된다. 저장소 루트 v1 파일은 최신본이 아닌 호환용 과거 스냅샷이다.

실제 창 위치와 방 배치, 미확인 시설 위치까지 실측 복원한 모델은 아니다. 개발과정기와 검증 JSON의 범위·한계를 함께 확인한다.
