"""
02. 여러 값을 담는 그릇: 리스트, 튜플, 딕셔너리, 세트

    자료형        모양                       이럴 때 씁니다
    리스트 list   [1.0, 1.2, 1.5]            순서가 있고 바뀌는 값들 (시계열)
    튜플 tuple    (37.5, 127.0)              바뀌지 않는 묶음 (좌표, 데이터 크기)
    딕셔너리 dict {"name": "vanillin"}       이름으로 값을 찾을 때 (분자 정보)
    세트 set      {"sweet", "vanilla"}       중복 없는 모음 (냄새 표현 비교)

실행: python lessons/02_collections.py
"""

# ---------------------------------------------------------------------
# 1. 리스트: 순서가 있는 값들
# ---------------------------------------------------------------------
readings = [1.01, 1.03, 1.42, 1.78, 1.65]  # 센서가 1초마다 기록한 값

print(readings[0])  # 첫 번째 값
print(readings[-1])  # 마지막 값
print(readings[1:3])  # 1번 이상 3번 미만
print(len(readings), max(readings), min(readings), sum(readings))

readings.append(1.40)  # 맨 뒤에 추가
readings[0] = 1.00  # 값 바꾸기
print(readings)
print(sorted(readings))  # 정렬된 새 리스트를 돌려주고, 원본은 그대로입니다.

# ⚠️ 함정: 리스트를 다른 변수에 '대입'해도 복사되지 않습니다.
#    같은 리스트에 이름표만 하나 더 붙습니다.
original = [1, 2, 3]
same_list = original
same_list.append(4)
print(original)  # [1, 2, 3, 4] ← 원본도 바뀌었습니다!

real_copy = original.copy()  # 진짜 복사본이 필요하면 copy()
real_copy.append(5)
print(original, real_copy)

# ---------------------------------------------------------------------
# 2. 튜플: 바꿀 수 없는 리스트
# ---------------------------------------------------------------------
data_shape = (90, 4)  # 측정 90회, 센서 4개
print(data_shape[0])
trials, sensors = data_shape  # 언패킹: 값을 나누어 담기
print(f"측정 {trials}회, 센서 {sensors}개")
# data_shape[0] = 100  # ← 주석을 풀면 오류가 납니다. 튜플은 수정할 수 없습니다.

# ---------------------------------------------------------------------
# 3. 딕셔너리: 이름(key)으로 값(value)을 찾기
# ---------------------------------------------------------------------
vanillin = {
    "name": "vanillin",
    "smiles": "COc1cc(C=O)ccc1O",
    "odors": ["sweet", "vanilla"],  # 값으로 리스트도 넣을 수 있습니다.
}

print(vanillin["name"])
print(vanillin["odors"][0])  # 안쪽 리스트의 첫 번째 값
vanillin["heavy_atoms"] = 11  # 새 항목 추가

# 없는 key를 []로 찾으면 KeyError가 납니다. get은 대신 기본값을 돌려줍니다.
print(vanillin.get("boiling_point", "정보 없음"))

print(list(vanillin.keys()))  # key 목록
print("smiles" in vanillin)  # key가 있는지 확인

# 분자 데이터는 흔히 '딕셔너리의 리스트' 형태로 다룹니다.
molecules = [
    {"name": "vanillin", "odors": ["sweet", "vanilla"]},
    {"name": "limonene", "odors": ["citrus", "fresh"]},
]
print(molecules[1]["odors"][0])  # 두 번째 분자의 첫 번째 냄새 → citrus

# ---------------------------------------------------------------------
# 4. 세트: 중복 없는 모음, 집합 연산
# ---------------------------------------------------------------------
geraniol_odors = {"floral", "rose", "sweet"}
linalool_odors = {"floral", "fresh", "sweet"}

print(geraniol_odors & linalool_odors)  # 교집합: 둘 다 있는 표현
print(geraniol_odors | linalool_odors)  # 합집합: 하나라도 있는 표현
print(geraniol_odors - linalool_odors)  # 차집합: 왼쪽에만 있는 표현
# 세트는 순서가 없어서 실행할 때마다 출력 순서가 달라질 수 있습니다.

# 자카드 유사도: 냄새 표현이 얼마나 겹치는지를 0~1로 나타냅니다.
shared = len(geraniol_odors & linalool_odors)
total = len(geraniol_odors | linalool_odors)
print(f"자카드 유사도: {shared / total:.2f}")

# 리스트의 중복을 없앨 때도 편리합니다.
all_labels = ["sweet", "floral", "sweet", "fresh", "floral"]
print(sorted(set(all_labels)))  # ['floral', 'fresh', 'sweet']

# ---------------------------------------------------------------------
# 연습문제 (정답: lessons/answers.py)
# ---------------------------------------------------------------------
# 1) [1.0, 1.1, 1.9, 1.7]에서 최댓값과 첫 값의 차이를 출력하세요.
num_list = [1.0, 1.1, 1.9, 1.7]
print(round(max(num_list) - num_list[0], 2))

# 2) limonene 딕셔너리를 만들고 "smiles" 항목으로 "CC1=CCC(CC1)C(=C)C"를 추가하세요.
limonene = {"name" : "limonene"}
limonene["smiles"] = "CC1=CCC(CC1)C(=C)C"
print(limonene)

# 3) {"fruity", "sweet", "banana"}와 {"fruity", "green"}의 자카드 유사도를 구하세요.
a = {"fruity", "sweet", "banana"}
b = {"fruity", "green"}
print(f"{len(a & b) / len(a | b):.2f}")