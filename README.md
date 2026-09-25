# 2026 MAICON 모듈형 베이스라인

예선 준비를 위한 모듈 구조·설정 예시·Notebook 및 문서 템플릿입니다.

**현재 단계: 프로젝트 골격. 학습·예측 실행 코드는 아직 구현하지 않았습니다.**

## 시작하기

1. [사용 가이드](docs/usage.md)를 읽습니다.
2. [모듈 설계](docs/architecture.md)에서 책임과 입출력을 확인합니다.
3. configs/tabular.example.json을 복사하여 연습 데이터에 맞게 작성합니다. 현재는 설계 예시로, 실행기가 읽지 않습니다.
4. notebooks/baseline_template.ipynb의 단계에 맞춰 정형 데이터 경로부터 구현합니다.
5. docs/templates의 양식으로 모듈과 실험을 기록합니다.

## 폴더

| 경로 | 역할 |
|---|---|
| src/maicon_baseline/ | 공통 모듈 골격 |
| configs/ | 설정 예시 |
| notebooks/ | Notebook 작성 틀 |
| tests/ | 향후 핵심 검증 계획 |
| docs/ | 사용법·설계·기록 양식 |

## 연결

[Notion 프로젝트와 사용 설명](https://app.notion.com/p/3e6c2faf8063817e9290c08925597cd8)

## 기준

사용자가 제공한 예선 안내 PDF 기준: 3문항·90분·Python3·GPU 미지원. 최종 코드와 실행 결과는 제공 Notebook에 포함합니다. 실제 문제 지문과 참가자 가이드가 우선합니다.

대회 제공 데이터·실제 문제·인증 정보는 커밋하지 않습니다. 데이터 제외 규칙은 보조 장치이므로 커밋할 파일을 직접 확인합니다.
