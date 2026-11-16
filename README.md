# Football Pick

챔피언스리그 감성의 축구 승부 예측 웹사이트 (시연용 가상 경기·전적·배당률).

## 실행

```powershell
py -m pip install -r requirements.txt
py app.py
```

브라우저: http://127.0.0.1:5000

## API

- `GET /api/matches` 경기 목록
- `POST /api/predict` 예측 저장. JSON 예시: `{"match_id":1,"choice":0}`
- `GET /api/results/1` 투표 결과

## 현재 제한

- 투표할 때마다 1표가 추가되며 중복 투표 방지 및 예측 변경 기능은 아직 없습니다.
- 최근 전적, 배당률, 경기 일정은 실제 데이터가 아닌 시연용입니다.
- AWS 배포 및 기능 검증은 아직 수행하지 않았습니다.
- GitHub README의 AWS 구성도, ELB/Auto Scaling 판단, 검증 결과는 실제 배포 후 직접 작성해야 합니다.
