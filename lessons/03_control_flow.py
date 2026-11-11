"""
03. 흐름 제어: 조건문과 반복문

프로그램은 '판단하기(if)'와 '반복하기(for)'의 조합입니다.
데이터 전처리의 대부분이 "모든 측정값을 돌면서, 조건에 맞으면 처리하기"입니다.

실행: python lessons/03_control_flow.py
"""

# Python은 '들여쓰기(공백 4칸)'로 코드 묶음을 구분합니다.
# 콜론(:) 다음 줄은 반드시 들여써야 합니다.

# ---------------------------------------------------------------------
# 1. if / elif / else
# ---------------------------------------------------------------------
response = 0.45

if response >= 0.8:
    level = "강함"
elif response >= 0.3:  # 위 조건이 거짓일 때만 검사합니다.
    level = "보통"
else:
    level = "약함"
print(f"반응 세기: {level}")

# ---------------------------------------------------------------------
# 2. for: 하나씩 꺼내서 반복
# ---------------------------------------------------------------------
readings = [1.01, 1.03, 1.42, 1.78, 1.65]

total = 0
for value in readings:
    total = total + value
print(f"합계 {total:.2f}, 평균 {total / len(readings):.2f}")

# range: 숫자를 차례로 만듭니다. range(3)은 0, 1, 2입니다.
for i in range(3):
    print(f"{i}번째 측정 시작")

# enumerate: 순번과 값을 함께 꺼냅니다.
for second, value in enumerate(readings):
    print(f"{second}초: {value}")

# zip: 두 리스트를 나란히 꺼냅니다.
names = ["vanillin", "limonene", "menthol"]
odors = ["vanilla", "citrus", "minty"]
for name, odor in zip(names, odors):
    print(f"{name} → {odor}")

# 딕셔너리는 items()로 key와 value를 함께 꺼냅니다.
sensor_peaks = {"s1": 1.8, "s2": 1.2, "s3": 1.5}
for sensor, peak in sensor_peaks.items():
    print(sensor, peak)

# ---------------------------------------------------------------------
# 3. break, continue
# ---------------------------------------------------------------------
# 처음으로 임계값을 넘은 시점을 찾기
threshold = 1.3
for second, value in enumerate(readings):
    if value > threshold:
        print(f"{second}초에 냄새를 감지했습니다.")
        break  # 찾았으니 반복을 끝냅니다.

# 잘못된 값은 건너뛰기
raw = [1.0, None, 1.2, -999, 1.4]
clean = []
for value in raw:
    if value is None or value < 0:  # None 비교에는 'is'를 씁니다.
        continue  # 이번 차례만 건너뜁니다.
    clean.append(value)
print(clean)

# ---------------------------------------------------------------------
# 4. while: 조건이 참인 동안 반복
#    조건이 영원히 참이면 끝나지 않으니 주의하세요. 강제 종료는 Ctrl+C입니다.
# ---------------------------------------------------------------------
concentration = 100.0
dilutions = 0
while concentration > 1:  # 농도가 1 이하가 될 때까지 절반씩 희석
    concentration = concentration / 2
    dilutions += 1  # dilutions = dilutions + 1 의 줄임말
print(f"{dilutions}번 희석, 최종 농도 {concentration}")

# ---------------------------------------------------------------------
# 5. 리스트 컴프리헨션: for를 한 줄로
#    [결과 for 값 in 목록 if 조건]
# ---------------------------------------------------------------------
baseline = 1.0

# 일반 for문으로 쓰면
corrected = []
for value in readings:
    corrected.append(value - baseline)

# 같은 내용을 한 줄로 쓰면
corrected = [value - baseline for value in readings]
print([round(value, 2) for value in corrected])

# 조건을 붙이면 걸러낼 수 있습니다.
strong = [value for value in readings if value > 1.3]
print(strong)

# 딕셔너리 버전도 있습니다.
responses = {sensor: round(peak - baseline, 2) for sensor, peak in sensor_peaks.items()}
print(responses)

# ---------------------------------------------------------------------
# 6. 자주 쓰는 패턴: 개수 세기
# ---------------------------------------------------------------------
labels = ["sweet", "floral", "sweet", "fresh", "floral", "sweet"]
counts = {}
for label in labels:
    counts[label] = counts.get(label, 0) + 1  # 처음 보면 0에서 시작
print(counts)

# ---------------------------------------------------------------------
# 연습문제 (정답: lessons/answers.py)
# ---------------------------------------------------------------------
# 1) [1.0, 1.05, 1.5, 1.9, 1.2]에서 1.4보다 큰 값의 개수를 for로 세세요.
list1 = [1.0, 1.05, 1.5, 1.9, 1.2]
largeCount = 0
for large in list1 :
    if large > 1.4 :
        largeCount += 1
print(largeCount)

# 2) 위 리스트의 각 값에서 첫 값을 뺀 리스트를 컴프리헨션으로 만드세요.
print([round(minusFirst - list1[0], 2) for minusFirst in list1])

# 3) ["CCO", "CC", "CCCO", "c1ccccc1"] 중 "O"가 들어간 것만 골라내세요.
print([checkO for checkO in ["CCO", "CC", "CCCO", "c1ccccc1"] if "O" in checkO])