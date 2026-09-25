# 데이터 특성별 처리 결정

| 데이터 특성 | 검증 | 처리와 모델 | 주의점 |
|---|---|---|---|
| 독립 정형 분류 | 계층화 홀드아웃 | 결측·OneHot·스케일링 + Logistic/ExtraTrees | 희소 클래스·ID 제외 |
| 정형 회귀 | 무작위 또는 시간/그룹 | Ridge/ExtraTrees | RMSE/MAE/R² 선택 |
| 사람·장비 반복 관측 | 그룹 홀드아웃 | 학습 그룹에서만 전처리 fit | 새 개체 일반화 평가 |
| 시간 순서 표 | 시간 경계와 gap | 과거 → 미래 | gap은 고유 시각 개수 |
| 단일/다중 미래 예측 | 개체 공통 시간 경계 | 과거 lag/rolling + Ridge/ExtraTrees/마지막 값 | 검증 horizon도 재귀 예측 |
| 센서 구간 | 사람/장비 그룹 | 통계·RMS·변화량·주파수 + 선형/트리 | 전체 구간 관측 후 판정 |
| 라벨 없는 이상탐지 | 정상 기준 학습 가정 | IsolationForest | contamination 가정, 점수는 확률 아님 |
| 문서 분류·회귀 | 중복/작성자 그룹 | 학습 TF-IDF + Logistic/Ridge | char/word, 희소 행렬 유지 |
| 정형·문서 군집 | 내부 지표는 탐색용 | MiniBatchKMeans | 군집 번호 ≠ 정답 라벨 |
| 이미지 분류 | 촬영 그룹 또는 동일 이미지 해시 | 픽셀/색/윤곽 + 선형/트리 | CPU 기준 모델 |
| 일정한 객체 탐지 | 이미지/촬영 그룹 | 패치 학습 + sliding window + NMS | 고정 임계 precision/recall, mAP 아님 |
| 일반 객체 탐지 | 촬영 세션별 분리 | 선택 YOLO 학습·검증·추론 | 패키지·가중치·CPU 시간 확인 |

## 계층

큰 범주 = 데이터 유형 디렉토리. 중간 범주 = EDA 또는 문제 유형 Notebook. 작은 범주 = Notebook 안의 전처리/특징/모델 선택 코드입니다.
기존 src 모듈과 configs는 초기 설계 참고용입니다. 실제 로직은 Notebook 내부에 있어 src를 수정해도 Notebook 동작은 바뀌지 않습니다.

## 공통 계약

전처리 fit 전에 분할합니다. ID를 특징에서 제외하고 학습·테스트 열을 확인합니다. 같은 분할·지표에서 비교한 모델을 전체 학습 데이터로 재학습합니다. 확률 클래스 순서와 sample_submission ID 대응을 확인합니다.

## 공식 문서

- https://scikit-learn.org/stable/common_pitfalls.html
- https://scikit-learn.org/stable/modules/cross_validation.html
- https://docs.ultralytics.com/modes/train/
