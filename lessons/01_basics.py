"""
01. Python 첫걸음: 변수, 자료형, 문자열

이 파일을 다 읽으면:
  - 값을 변수에 담고 출력할 수 있습니다.
  - 숫자, 문자열, 참/거짓의 차이를 압니다.
  - 측정값을 보기 좋게 출력할 수 있습니다.

실행: python lessons/01_basics.py
공부법: 먼저 실행해서 출력을 보고, 값을 바꿔 다시 실행해 보세요.
"""

# '#' 뒤의 글은 주석입니다. Python은 무시하고, 사람만 읽습니다.

# ---------------------------------------------------------------------
# 1. print: 화면에 출력하기
# ---------------------------------------------------------------------
print("안녕하세요, 후각 AI!")

# ---------------------------------------------------------------------
# 2. 변수: 값에 이름표를 붙이기
#    '=' 는 "같다"가 아니라 "오른쪽 값을 왼쪽 이름에 담는다"는 뜻입니다.
# ---------------------------------------------------------------------
molecule = "vanillin"  # 문자열(str): 따옴표로 감싼 글자
heavy_atoms = 11  # 정수(int): 소수점 없는 수
sensor_value = 1.25  # 실수(float): 소수점 있는 수
is_pleasant = True  # 불리언(bool): True 또는 False
next_sample = None  # None: "아직 값이 없음"

print(molecule, heavy_atoms, sensor_value, is_pleasant, next_sample)

# type()으로 자료형을 확인할 수 있습니다.
print(type(molecule), type(heavy_atoms), type(sensor_value), type(is_pleasant), type(next_sample))

# ---------------------------------------------------------------------
# 3. 계산
# ---------------------------------------------------------------------
baseline = 1.0  # 냄새가 없을 때 센서 값
peak = 1.8  # 냄새를 맡았을 때 가장 높은 값

response = peak - baseline  # 기준값 대비 증가량
ratio = peak / baseline  # 기준값 대비 몇 배인지
print("증가량:", response)
print("비율:", ratio)

print(7 / 2)  # 일반 나눗셈 → 3.5
print(7 // 2)  # 몫 → 3
print(7 % 2)  # 나머지 → 1
print(2**10)  # 거듭제곱 → 1024

# 실수는 컴퓨터에서 근삿값으로 저장되므로 작은 오차가 생깁니다.
print(0.1 + 0.2)  # 0.30000000000000004
print(round(0.1 + 0.2, 2))  # 소수 둘째 자리까지 반올림 → 0.3

# ---------------------------------------------------------------------
# 4. 문자열 다루기
# ---------------------------------------------------------------------
smiles = "COc1cc(C=O)ccc1O"  # SMILES: 분자 구조를 글자로 적는 표기법

print(len(smiles))  # 글자 수
print(smiles[0])  # 첫 글자. 번호는 0부터 시작합니다!
print(smiles[-1])  # 마지막 글자
print(smiles[0:3])  # 0번 이상 3번 미만 → "COc"
print(smiles.lower())  # 소문자로 변환
print(smiles.count("O"))  # 대문자 O가 몇 번 나오는지
print("c1" in smiles)  # 포함 여부 → True

# split: 글자를 기준으로 쪼개기, join: 다시 합치기
odors_text = "sweet;vanilla"
odors = odors_text.split(";")
print(odors)  # ['sweet', 'vanilla']
print(", ".join(odors))  # sweet, vanilla

# f-string: 문자열 앞에 f를 붙이면 {} 안에 변수를 넣을 수 있습니다.
# 앞으로 가장 자주 쓰게 될 출력 방법입니다.
print(f"{molecule}의 무거운 원자 수: {heavy_atoms}개")
print(f"센서 반응: {response:.3f}")  # :.3f → 소수 셋째 자리까지
print(f"비율: {ratio:.1%}")  # :.1% → 퍼센트로 표시

# ---------------------------------------------------------------------
# 5. 자료형 바꾸기
#    파일에서 읽은 값은 숫자처럼 보여도 문자열인 경우가 많습니다.
# ---------------------------------------------------------------------
text_value = "1.25"
print(text_value * 2)  # 문자열 × 2 → 글자가 반복됩니다: 1.251.25
print(float(text_value) * 2)  # 실수로 바꾸면 계산됩니다: 2.5
print(int("11") + 1)  # 12
print(str(11) + "개")  # 11개

# ---------------------------------------------------------------------
# 6. 비교와 논리
# ---------------------------------------------------------------------
print(response > 0.5)  # 크다
print(molecule == "vanillin")  # 같다. '=' 하나는 대입이므로 비교에는 '=='를 씁니다.
print(molecule != "limonene")  # 다르다
print(response > 0.5 and is_pleasant)  # 둘 다 참이면 참
print(response > 5 or is_pleasant)  # 하나만 참이어도 참
print(not is_pleasant)  # 반대로

# ---------------------------------------------------------------------
# 연습문제 (정답: lessons/answers.py)
# ---------------------------------------------------------------------
# 1) 기준값 2.0, 최고값 3.5일 때 증가율을 "증가율: 75.0%" 형태로 출력하세요.
baseline = 2.0
peak = 3.5
increase_rate = (peak - baseline) / baseline * 100
print(f"증가율: {increase_rate:.1f}%")

# 2) "citrus;fresh;sweet"을 쪼개 냄새 표현의 개수를 출력하세요.
odor_text = "citrus;fresh;sweet"
odors = odor_text.split(";")
print(f"냄새 표현 개수: {len(odors)}")

# 3) SMILES "CCOC(C)=O"에서 C(대문자)가 몇 개인지 출력하세요.
smiles = "CCOC(C)=O"
count_C = smiles.count("C")
print(f"C의 개수: {count_C}")