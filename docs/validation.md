# 검증 결과

검증일: 2026-09-25. Python 3.12.14 / CPU.

## 실행 범위

Notebook 13개의 nbformat 스키마와 기본/설정 분기 총 23개를 검사했습니다. YOLO는 RUN_YOLO=False 비활성 경로만 검사했습니다. 나머지 22개 사례는 합성 데이터의 코드 셀을 순서대로 독립 Python 프로세스에서 실행했습니다.

Jupyter 커널 실행을 시도했으나 이 실행 환경의 소켓 제한으로 시작되지 않았습니다. 따라서 실제 Jupyter 커널·UI 실행 검증으로 주장하지 않습니다. 사용 환경에서 Restart Kernel → Run All 확인이 필요합니다.

| Notebook | 사례 | 결과 | 실행 시간(초) |
|---|---|---|---|
| notebooks/01_tabular/01_EDA.ipynb | default | passed | 1.81 |
| notebooks/01_tabular/02_supervised.ipynb | default | passed | 1.71 |
| notebooks/01_tabular/03_anomaly_clustering.ipynb | default | passed | 1.49 |
| notebooks/02_time_series/01_EDA.ipynb | default | passed | 1.54 |
| notebooks/02_time_series/02_forecasting.ipynb | default | passed | 2.05 |
| notebooks/02_time_series/03_sensor_windows.ipynb | default | passed | 1.45 |
| notebooks/03_text/01_EDA.ipynb | default | passed | 1.39 |
| notebooks/03_text/02_supervised.ipynb | default | passed | 1.39 |
| notebooks/03_text/03_clustering.ipynb | default | passed | 1.3 |
| notebooks/04_image/01_EDA.ipynb | default | passed | 1.58 |
| notebooks/04_image/02_classification.ipynb | default | passed | 1.51 |
| notebooks/04_image/03_detection_cpu.ipynb | default | passed | 1.54 |
| notebooks/04_image/04_yolo_optional.ipynb | default | passed | 0.25 |
| notebooks/01_tabular/02_supervised.ipynb | regression | passed | 1.47 |
| notebooks/01_tabular/02_supervised.ipynb | probability | passed | 1.55 |
| notebooks/01_tabular/03_anomaly_clustering.ipynb | clustering | passed | 1.42 |
| notebooks/02_time_series/03_sensor_windows.ipynb | regression | passed | 1.6 |
| notebooks/02_time_series/03_sensor_windows.ipynb | anomaly | passed | 1.49 |
| notebooks/03_text/02_supervised.ipynb | regression | passed | 1.43 |
| notebooks/03_text/02_supervised.ipynb | word | passed | 1.37 |
| notebooks/03_text/02_supervised.ipynb | probability | passed | 1.37 |
| notebooks/04_image/02_classification.ipynb | histogram | passed | 1.38 |
| notebooks/04_image/02_classification.ipynb | gradient | passed | 1.45 |

## 계약 검사: 9개 통과

- 학습 데이터만 사용한 결측 대치 통계
- 미지 범주와 전체 결측 열
- 그룹 비중복
- 같은 시각의 중복 관측과 시간 gap
- sample_submission ID 재정렬
- 중복 ID·NaN·무한대·잘못된 확률 거부
- 확률 클래스 열 순서
- 실제 CSV 경로 모드와 제출 예시 순서
- 미래 검증 정답을 바꿔도 재귀 예측 불변

## 환경 버전

- numpy: 2.3.5
- pandas: 2.2.3
- scipy: 1.17.0
- sklearn: 1.8.0
- matplotlib: 3.10.8
- PIL: 12.3.0
- nbformat: 5.11.1

## 해석의 한계

합성 데이터 통과는 실제 예선 데이터의 성능·메모리·실행 시간을 보장하지 않습니다. YOLO 실제 학습, Parquet 입력, 실제 대회 파일·제출 서버는 미검증입니다. 탐지 출력은 공식 규격별 변환이 필요합니다. CPU 탐지의 고정 임계 precision/recall은 mAP가 아닙니다.
