# 후각 AI 개발자를 위한 Python 입문

Python 기초부터 시작해 전자코 데이터 분류와 분자 냄새 예측까지 따라가는 자료입니다.
예제는 처음부터 끝까지 분자와 센서 데이터를 사용합니다.

## 시작하기

터미널에서 이 폴더로 이동한 뒤 가상환경을 켭니다. 가상환경은 이 프로젝트 전용 Python 공간입니다.

```bash
source .venv/bin/activate      # 앞에 (.venv)가 보이면 성공
python lessons/01_basics.py    # 레슨 실행
```

VS Code에서는 `Cmd+Shift+P` → **Python: Select Interpreter** → `.venv`를 고른 뒤, 파일 오른쪽 위의 ▶ 버튼으로 실행할 수 있습니다.

다른 컴퓨터에서 처음 준비할 때는 아래 명령을 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 학습 순서

| 단계 | 파일 | 배우는 것 | 후각 AI와의 연결 |
|---|---|---|---|
| 기초 | [01_basics.py](lessons/01_basics.py) | 변수, 자료형, 문자열 | SMILES 문자열, 센서 값 계산 |
| 기초 | [02_collections.py](lessons/02_collections.py) | 리스트, 튜플, 딕셔너리, 세트 | 분자 정보, 냄새 표현 비교 |
| 기초 | [03_control_flow.py](lessons/03_control_flow.py) | 조건문, 반복문, 컴프리헨션 | 감지 시점 찾기, 값 거르기 |
| 기초 | [04_functions.py](lessons/04_functions.py) | 함수, 타입 힌트, lambda | 코사인 유사도 직접 구현 |
| 기초 | [05_classes.py](lessons/05_classes.py) | 클래스, 상속 | scikit-learn, PyTorch 코드 읽기 |
| 기초 | [06_files_errors.py](lessons/06_files_errors.py) | 파일, CSV, JSON, 오류 처리 | 분자 데이터 읽기, 나쁜 값 처리 |
| 도구 | [07_numpy.py](lessons/07_numpy.py) | 배열, shape, axis, 브로드캐스팅 | 센서 행렬 계산, 패턴 정규화 |
| 도구 | [08_pandas.py](lessons/08_pandas.py) | 표 데이터, groupby, 결측치 | 전자코 측정 데이터 정리 |
| 도구 | [09_matplotlib.py](lessons/09_matplotlib.py) | 선 그래프, 산점도 | 센서 반응 확인 |
| 프로젝트 | [10_enose_classifier.py](lessons/10_enose_classifier.py) | 특징 추출, 학습, 평가 | 센서 값으로 냄새 분류 |
| 프로젝트 | [11_molecule_odor.py](lessons/11_molecule_odor.py) | RDKit, 분자 지문, 유사도 | 구조에서 냄새 추측 |

연습문제는 각 레슨 맨 아래에 있고, 정답은 [answers.py](lessons/answers.py)에 있습니다.

## 공부하는 방법

1. **먼저 실행합니다.** 출력을 보고 나서 코드를 읽으면 이해가 빠릅니다.
2. **값을 바꿔 봅니다.** 숫자를 바꾸고, 줄을 지우고, 일부러 오류도 내 보세요.
3. **연습문제는 빈 파일에 직접 칩니다.** 눈으로 읽을 때와 손으로 칠 때의 이해도는 전혀 다릅니다.
4. **오류 메시지는 맨 아래 줄부터 읽습니다.** 읽는 법은 06번 레슨에 정리했습니다.

기초가 처음이라면 01~06번에 시간을 가장 많이 쓰세요. 특히 05번과 07번의 shape, axis는 이후 AI 코드를 읽는 데 바로 이어집니다.

## 사용하는 데이터

| 파일 | 내용 | 주의 |
|---|---|---|
| `data/enose_readings.csv` | 전자코 측정 90회, 센서 4개, 60초 | **학습용 합성 데이터**입니다. [make_enose_data.py](lessons/make_enose_data.py)로 만들었습니다. |
| `data/molecules.csv` | 잘 알려진 향 분자 24개 | 실제 분자지만, 냄새 표현은 학습용으로 간단히 붙인 것입니다. 연구 근거로 쓰면 안 됩니다. |

## 이 자료를 끝낸 다음

후각 AI는 크게 두 방향으로 나뉩니다. 맡을 프로젝트에 맞춰 고르면 됩니다.

**전자코 / 센서 쪽**
- 실제 공개 데이터로 연습: UCI의 Gas Sensor Array Drift 데이터셋
- 센서 드리프트 보정, 시계열 모델(1D CNN, RNN)

**분자 → 냄새 예측 쪽**
- 공개 데이터: Pyrfume 프로젝트, GoodScents와 Leffingwell 데이터
- 대표 연구: DREAM Olfaction Prediction Challenge, Principal Odor Map
- 그래프 신경망(GNN): PyTorch Geometric, DeepChem

**공통**
- PyTorch 기초 (텐서, 학습 루프)
- Jupyter Notebook으로 실험 정리하기
- Git으로 코드 관리하기
