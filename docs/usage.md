# Notebook 사용 가이드

## 환경과 시작

로컬 연습 환경에서 `python -m pip install -r requirements.txt`로 설치한 뒤 `jupyter lab`을 실행합니다. 대회 환경에 패키지가 있으면 중복 설치하지 마세요. Python 3.12에서 검증했습니다. Parquet은 pyarrow, YOLO는 ultralytics/torch와 허용된 로컬 가중치가 추가로 필요합니다. 자동 설치·가중치 다운로드 셀은 없습니다.

각 데이터 유형의 01_EDA.ipynb에는 여러 탐색 방법이 있습니다. 학습 Notebook은 전처리부터 제출까지 독립 실행하므로 이전 Notebook이나 src 설치에 의존하지 않습니다.

## 실제 데이터 전환

1. 기본 DEMO=True로 합성 데이터 흐름을 확인합니다.
2. DEMO=False로 변경합니다. 실제 파일이 없으면 명시적으로 실패합니다.
3. 경로와 열 이름을 지정합니다. 경로는 커널 작업 디렉토리 기준이므로 필요하면 절대 경로를 쓰세요.
4. TASK와 METRIC을 함께 설정합니다. 회귀는 TASK='regression', METRIC='rmse' 또는 'mae'입니다.
5. 분할 방식과 제출 예시를 지정하고 커널 재시작 후 전체 실행합니다.

| Notebook | 입력 | 주요 설정 |
|---|---|---|
| 정형 분류·회귀 | train/test CSV·TSV·Parquet | TARGET, ID, DROP_COLUMNS, SPLIT, GROUP, TIME_COL, METRIC |
| 미래 예측 | series_id,timestamp,value; test에는 id 포함 | ENTITY(None이면 단일), FREQUENCY, LAGS, ROLLING, VALUE |
| 센서 구간 | window_id,subject_id,timestamp,센서 채널,target | WINDOW, GROUP, CHANNELS, SAMPLING_HZ, USE_FFT |
| 텍스트 | id,text,target | TEXT, ANALYZER, GROUP, SPLIT, METRIC |
| 이미지 분류 | id,path,label manifest CSV | IMAGE_ROOT, PATH_COL, GROUP, FEATURE, IMAGE_SIZE |
| CPU 탐지 | 이미지 manifest + id,class_id,xmin,ymin,xmax,ymax annotation | WINDOW_SIZES, STRIDE, CONFIDENCE, NMS_IOU, GROUP |
| YOLO | data.yaml, YOLO normalized xywh 라벨, 로컬 가중치, test 폴더 | RUN_YOLO, DATA_YAML, LOCAL_WEIGHTS, TEST_SOURCE |

## 데이터 특성별 선택

- 정형 이상치가 크면 ROBUST=True로 RobustScaler를 비교합니다. 자동 삭제하지 않습니다. 고유 범주가 많은 열의 메모리 사용을 확인하고 불필요한 ID/누수 열은 DROP_COLUMNS로 제외합니다.
- 시간 순서가 중요하면 SPLIT='time', TIME_COL을 설정하고 GAP으로 경계를 비웁니다. GAP은 고유 시각 개수 기준입니다.
- 같은 사람/장비 관측이 반복되면 SPLIT='group', GROUP을 지정합니다.
- 미래 예측은 등간격·단변량·기존 개체의 연속 미래 행을 요구합니다. 불규칙 간격은 EDA의 리샘플링 예시로 먼저 처리하고 미래 값으로 보간하지 마세요.
- 센서는 이미 구간화된 long 표를 받습니다. 겹친 구간은 같은 GROUP에 두세요. 전체 구간 관측 후 판정용이며 온라인 조기 판정과 다릅니다.
- 텍스트 word는 단어 조합, char/char_wb는 문자 조합을 봅니다. 기본적으로 숫자·부정어를 삭제하지 않습니다.
- 이미지 pixels는 위치에 민감하고 color_hist는 위치를 버립니다. gradient는 간단한 방향 히스토그램이며 표준 HOG 전체 구현은 아닙니다.

## 예측 형식

정형·텍스트·이미지 분류는 PREDICTION_KIND=label / probability / positive_probability를 지원합니다. 전체 확률은 CLASS_ORDER에 실제 클래스 값을 공식 열 순서대로 넣고 TARGET_COLUMNS를 맞춥니다. 예: CLASS_ORDER=[1,0], TARGET_COLUMNS=['p1','p0']. 양성 확률만 필요하면 POSITIVE_CLASS를 지정합니다.

SAMPLE_PATH에 제출 예시를 지정하면 ID로 예측을 정렬합니다. 행 수·열·결측·확률·고유 ID를 검사합니다. CSV에서 001 같은 문자열 ID가 필요하면 read_table의 dtype 정책을 수정하여 train/test/sample에서 동일하게 읽으세요.
센서와 비지도 경로는 현재 단일 라벨/점수 출력입니다. 센서 분류 확률이 필요하면 마지막 셀에서 공통 classification_output과 write_submission 함수를 사용하세요.
군집 번호는 정답 클래스가 아니며 이상 점수는 확률이 아닙니다.
탐지는 여러 박스가 한 이미지에 대응하므로 범용 long CSV와 detection_counts.csv를 저장합니다. 미탐지는 counts에 0으로 남습니다. 공식 제출이 JSON/문자열 등의 형식이면 변환 셀을 추가해야 합니다.

## 실행 시간과 개선

소프트 시간 예산은 후보 모델 시작 전만 확인하고 진행 중인 fit을 강제 중단하지 않습니다. 전체 재학습 시간도 따로 확보하세요. 실험은 동일한 분할·지표에서 한 요소씩 바꾸고 docs/templates/experiment.md 또는 Notion에 기록합니다. 반복 튜닝한 검증 점수는 낙관적일 수 있습니다.

## 제공 Notebook으로 이식

설정·공통 함수·데이터·학습·제출 셀을 필요한 만큼 복사합니다. 공통 함수는 한 번만 남깁니다. DEMO=False, 공식 지표, 제출 경로를 확인하고 새 커널에서 전체 실행하세요. 코드와 실행 결과를 제공 Notebook에 남긴 뒤 최종 제출을 별도로 확인합니다.
