# 실행 검증

`python -m pip install -r requirements-dev.txt` 후 다음을 실행합니다.

- `python tests/run_notebooks.py`: nbformat 검증 및 23개 기본/설정 분기 실행
- `python tests/test_contracts.py`: 9개 누수·분할·제출·실제 CSV 모드 계약 검사

첫 명령은 Notebook 코드 셀을 순서대로 추출하여 독립 Python 프로세스와 임시 디렉토리에서 실행합니다. 실제 Jupyter 커널의 UI 동작 검증은 아닙니다. 실행 로그는 outputs/validation에 저장되고 git에서 제외됩니다. YOLO 사례는 기본 비활성 분기만 실행합니다.
