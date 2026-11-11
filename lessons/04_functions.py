"""
04. 함수: 반복되는 일을 묶어서 이름 붙이기

같은 코드를 두 번 쓰게 되면 함수로 만들 때가 된 것입니다.
함수는 '입력(매개변수)을 받아 → 처리하고 → 결과를 돌려주는(return)' 작은 기계입니다.

실행: python lessons/04_functions.py
"""

import math  # Python에 기본으로 들어 있는 수학 모듈을 불러옵니다.
from statistics import mean  # 모듈 안의 특정 함수만 불러올 수도 있습니다.

# ---------------------------------------------------------------------
# 1. 함수 만들기
# ---------------------------------------------------------------------


def peak_response(readings, baseline):
    """센서 값 목록에서 기준값 대비 최대 증가량을 구합니다."""  # 설명문(docstring)
    return max(readings) - baseline


result = peak_response([1.0, 1.4, 1.9], 1.0)
print(f"{result:.2f}")

# print와 return의 차이: print는 화면에 보여 주기만 하고,
# return은 값을 돌려주므로 그 값을 변수에 담아 계속 쓸 수 있습니다.

# ---------------------------------------------------------------------
# 2. 기본값과 이름 붙여 전달하기
# ---------------------------------------------------------------------


def classify(response, threshold=0.5):  # threshold를 생략하면 0.5
    return "감지" if response >= threshold else "미감지"  # 한 줄 if


print(classify(0.7))
print(classify(0.7, threshold=0.9))  # 이름을 붙이면 뜻이 분명해집니다.

# ---------------------------------------------------------------------
# 3. 여러 값 돌려주기
# ---------------------------------------------------------------------


def summarize(readings):
    return min(readings), max(readings), mean(readings)  # 튜플로 돌려줍니다.


low, high, average = summarize([1.0, 1.4, 1.9])
print(f"최소 {low}, 최대 {high}, 평균 {average:.2f}")

# ---------------------------------------------------------------------
# 4. 타입 힌트: 어떤 값이 오가는지 적어 두기
#    실행에는 영향이 없지만, 코드를 읽기 쉽고 편집기 도움도 잘 받습니다.
#    AI 라이브러리 코드에서 자주 보게 됩니다.
# ---------------------------------------------------------------------


def jaccard(a: set, b: set) -> float:
    """두 냄새 표현 집합이 얼마나 겹치는지 0~1로 계산합니다."""
    if not a and not b:  # 둘 다 비어 있으면 0으로 나누게 되므로 먼저 처리합니다.
        return 0.0
    return len(a & b) / len(a | b)


print(jaccard({"sweet", "floral"}, {"sweet", "fresh"}))  # 1/3


def cosine_similarity(a: list, b: list) -> float:
    """두 벡터가 가리키는 방향이 얼마나 비슷한지 계산합니다.

    전자코에서는 냄새의 진하기(크기)보다 센서 반응의 '패턴'이 중요해서 자주 씁니다.
    """
    dot = sum(x * y for x, y in zip(a, b)) # 내적
    size_a = math.sqrt(sum(x * x for x in a)) # 벡터의 길이
    size_b = math.sqrt(sum(y * y for y in b))
    return dot / (size_a * size_b) # 코사인 유사도


pattern = [1.0, 0.3, 0.6]
stronger = [2.0, 0.6, 1.2]  # 같은 패턴인데 두 배 진한 경우
different = [0.2, 1.0, 0.3]
print(f"{cosine_similarity(pattern, stronger):.3f}")  # 1.000
print(f"{cosine_similarity(pattern, different):.3f}")  # 훨씬 낮습니다.

# ---------------------------------------------------------------------
# 5. 변수의 범위
# ---------------------------------------------------------------------
scale = 2  # 함수 밖의 변수


def rescale(value):
    result = value * scale  # 밖의 변수를 읽을 수는 있습니다.
    return result


print(rescale(3))
# print(result)는 위쪽 result를 출력할 뿐, 함수 안 result는 함수가 끝나면 사라집니다.
# 함수에 필요한 값은 밖에서 가져오기보다 매개변수로 받는 편이 안전합니다.

# ---------------------------------------------------------------------
# 6. ⚠️ 함정: 기본값으로 리스트를 쓰지 마세요
# ---------------------------------------------------------------------


def add_bad(value, history=[]):  # 이 리스트는 호출할 때마다 재사용됩니다.
    history.append(value)
    return history


print(add_bad(1))  # [1]
print(add_bad(2))  # [1, 2] ← 새 리스트를 기대했는데 앞의 값이 남아 있습니다!


def add_good(value, history=None):  # None을 기본값으로 두고 안에서 만듭니다.
    if history is None:
        history = []
    history.append(value)
    return history


print(add_good(1))
print(add_good(2))

# ---------------------------------------------------------------------
# 7. 함수를 값처럼 전달하기: sorted의 key와 lambda
#    lambda는 이름 없는 한 줄짜리 함수입니다.
# ---------------------------------------------------------------------
molecules = [
    {"name": "vanillin", "heavy_atoms": 11},
    {"name": "ethanethiol", "heavy_atoms": 3},
    {"name": "hexanal", "heavy_atoms": 7},
]
by_size = sorted(molecules, key=lambda molecule: molecule["heavy_atoms"])
print([molecule["name"] for molecule in by_size])

# ---------------------------------------------------------------------
# 연습문제 (정답: lessons/answers.py)
# ---------------------------------------------------------------------
# 1) 리스트의 첫 값을 기준으로 삼아 각 값에서 빼는 함수 baseline_correct(readings)를
#    만드세요.
def baseline_correct(readings):
    return [listNum - readings[0] for listNum in readings]
print(baseline_correct([1, 4, 3, 6, 2]))

# 2) 값들을 최댓값으로 나누어 0~1로 만드는 normalize(values)를 만드세요.
#    최댓값이 0이면 원래 리스트를 그대로 돌려주세요.
def normalize(values):
    if max(values) == 0:
        return values
    return [round(data / max(values), 2) for data in values]
print(normalize([1, 6, 2, 0]), normalize([-4, 0]))

# 3) 위 molecules를 heavy_atoms가 큰 순서로 정렬하세요. (힌트: reverse=True)
topMolecules = sorted(molecules, key=lambda tm: tm["heavy_atoms"], reverse=True)
print([tm["name"] for tm in topMolecules])