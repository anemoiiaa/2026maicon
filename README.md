# 2026 MAICON · 데이터 유형별 실행 Notebook

**13개 독립 Notebook**: 정형·시계열/센서·텍스트·이미지 EDA와 실제 전처리·학습·평가·예측 코드입니다.
각 Notebook 안에 여러 방법과 설정 분기를 배치했습니다. 개인 Python 모듈을 import하지 않아 제공 Jupyter Notebook에 필요한 셀을 옮길 수 있습니다.

## 바로 시작

1. `requirements.txt`의 기본 패키지를 준비합니다. 설치 명령은 [사용 가이드](docs/usage.md)에 있습니다.
2. 아래에서 해당 데이터 유형의 EDA를 엽니다.
3. 학습 Notebook의 기본 `DEMO=True`로 합성 데이터 전체 흐름을 실행합니다.
4. 실제 연습 데이터는 `DEMO=False`로 바꾸고 경로·열·문제 유형·지표를 설정합니다.
5. `Restart Kernel → Run All`로 재현하고 제출 CSV를 확인합니다. **실제 데이터 모드는 기본 demo 데이터로 대체하지 않으며 경로 오류를 알립니다.**

| 유형 | EDA | 학습·예측 Notebook |
|---|---|---|
| 정형 | [EDA](notebooks/01_tabular/01_EDA.ipynb) | [분류·회귀](notebooks/01_tabular/02_supervised.ipynb), [이상탐지·군집](notebooks/01_tabular/03_anomaly_clustering.ipynb) |
| 시계열·센서 | [EDA](notebooks/02_time_series/01_EDA.ipynb) | [미래 예측](notebooks/02_time_series/02_forecasting.ipynb), [센서 구간 분류·회귀·이상탐지](notebooks/02_time_series/03_sensor_windows.ipynb) |
| 텍스트 | [EDA](notebooks/03_text/01_EDA.ipynb) | [분류·회귀](notebooks/03_text/02_supervised.ipynb), [문서 군집](notebooks/03_text/03_clustering.ipynb) |
| 이미지 | [EDA](notebooks/04_image/01_EDA.ipynb) | [CPU 분류](notebooks/04_image/02_classification.ipynb), [CPU 탐지](notebooks/04_image/03_detection_cpu.ipynb), [YOLO 선택 경로](notebooks/04_image/04_yolo_optional.ipynb) |

## 처리 원칙

- 정형: 수치/범주 분리, 학습 분할에서만 결측 처리·스케일링·인코딩 학습.
- 시계열: 개체 공통 시간 경계, 과거 lag/rolling만 사용, 다중 스텝 검증에서도 예측값을 재귀 입력.
- 센서: 구간 통계·주파수, 동일 사람/장비 GROUP 분리. 전체 구간 관측 후 판정하는 문제용.
- 텍스트: 중복 문서 그룹 분리, 학습 문서에만 TF-IDF 적합, word/char/char_wb 선택.
- 이미지: RGB·크기 정규화, 픽셀/색/윤곽 특징. 탐지는 이미지별 분할 후 패치를 학습.
- 제출: 고유 ID·행/열·결측·확률·클래스 순서 검사, sample_submission ID 순서에 맞춰 정렬.

## 범위와 한계

기본 경로는 CPU와 scikit-learn 기반입니다. 시간 제한은 후보 시작 전 확인하는 소프트 제한으로 fit을 강제 중단하지 않습니다.
시계열 예측은 등간격 단변량의 기존 개체에 대한 연속 미래 예측입니다. 센서 온라인 조기 판정, 일반 멀티모달·음성·분할 과제는 포함하지 않습니다.
CPU 탐지는 일정한 외형/크기의 객체에 적합한 간단한 패치 분류기입니다. 탐지 CSV는 범용 long 형식이며 **공식 제출 형식 변환이 추가로 필요합니다.**
YOLO는 실제 학습 코드가 있지만 별도 패키지·데이터·허용된 로컬 가중치가 필요하고 실제 학습은 이 환경에서 미검증입니다.

## 검증과 문서

- [사용법·설정 대응](docs/usage.md)
- [데이터 특성별 선택 가이드](docs/architecture.md)
- [실행 검증 범위](docs/validation.md)
- [Notion 프로젝트](https://app.notion.com/p/3e6c2faf8063817e9290c08925597cd8)

기존 `src/`, `configs/tabular.example.json`, `notebooks/baseline_template.ipynb`는 초기 설계 자료입니다. **현재 실행 기준은 새 데이터 유형별 Notebook의 설정 셀**입니다.
대회 제공 데이터·문제·인증 정보는 저장소에 업로드하지 않습니다. 예선은 사용자가 제공한 안내 PDF 기준 3문항·90분·CPU·Python3이며, 실제 지문과 최신 참가자 가이드가 우선합니다.
