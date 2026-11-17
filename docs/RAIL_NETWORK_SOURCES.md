# Railway route data research, 2026-11-17

## Delivered data
`web/rail/network.json` contains ordered OpenStreetMap node geometry from six route relations, downloaded through OSM API 0.6. Each route's consecutive ways shares an exact endpoint node ID; no synthetic links bridge missing geometry. This is GIS centerline geometry, not rail engineering/survey data.

|Relation|Coverage|Points|Station stops|
|---|---|---:|---:|
|16850861|연천 → 인천|1542|65|
|8692707|광운대 → 신창|1450|58|
|8692928|광운대 → 서동탄|770|40|
|10881612|영등포 → 광명|112|7|
|13738410|발곡 → 차량기지임시승강장|218|16 incl depot|
|13738411|차량기지임시승강장 → 발곡|207|16 incl depot|

These selected services cover the extremities/branches; they do not constitute every service, every track, every siding, or every switch. Opposite tracks and service patterns require further data extraction. Shared portions overlap deliberately. Station stops are OSM stop positions, not detailed station buildings.

## Important data discrepancy
Relation 13738411 is named 차량기지임시승강장 → 탑석 in OSM but its actual continuous track path and stop list continue to 발곡; display name corrected from the geometry. Both U Line paths exactly reach node 9221654398 (127.0949069,37.7286629), the depot platform. Both relations mark that stop `inactive_stop`. The official operator timetable lists 차량기지 임시승강장, and recent KTDB report lists 발곡–차량기지. Data includes the physical platform, retains this operational uncertainty, and does not invent a live operating timetable.

## Sources
- https://www.openstreetmap.org/relation/8691899 (Line 1 route master, 96 child service relations)
- https://www.openstreetmap.org/relation/7530882 (U Line route master, four children)
- https://www.openstreetmap.org/api/0.6/relation/16850861/full.json (replace relation ID for other inputs)
- https://wiki.openstreetmap.org/wiki/Seoul_Subway (route IDs and branch endpoints)
- https://www.ulrt.co.kr/doc/contents/information/time.php (operator timetable, search index confirms depot platform; direct web fetch timed out)
- https://www.ktdb.go.kr/DATA/pblcte/20261020050440656.pdf (2026 transport-network report, lists Line 1 연천–인천/신창 and U Line 발곡–차량기지)
- https://www.ui4u.go.kr/depart/contents.do?mId=0200000000 (city's U Line introduction, elevated automatic system)

## License and limitations
OSM database is ODbL 1.0. Display © OpenStreetMap contributors and link https://www.openstreetmap.org/copyright. Publish the derived route database with ODbL notices and source links, separate from application-code licensing. Do not treat Google/Naver screenshots as openly reusable geometry. OSM source is community maintained, not guaranteed exact/current. No elevation profile, civil dimensions, station architecture, switch operational controls or signalling data supplied. Headways, dwell times and train displays should say simulation unless sourced separately. Intended scope is harmless visual railway simulation, not real signalling/control.
