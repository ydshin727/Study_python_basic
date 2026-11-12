"""
06. 파일과 오류 처리

실제 데이터는 파일로 들어오고, 실제 데이터에는 항상 이상한 값이 섞여 있습니다.
이 레슨에서는 data/molecules.csv를 읽어 구조화하고, 나쁜 데이터를 안전하게 처리합니다.

실행: python lessons/06_files_errors.py
"""

import csv
import json
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------
# 1. 경로: pathlib을 쓰면 운영체제에 상관없이 경로를 다룰 수 있습니다.
#    __file__은 지금 실행 중인 이 파일의 위치입니다.
#    이렇게 하면 어느 폴더에서 실행해도 데이터를 찾습니다.
# ---------------------------------------------------------------------
PROJECT_DIR = Path(__file__).resolve().parent.parent # resolve: 절대경로로 변환 (Path 객체)
DATA_DIR = PROJECT_DIR / "data"  # '/'로 경로를 이어 붙입니다.
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)  # 폴더가 없으면 만듭니다. # exist_ok: 이미 존재하면 그냥 pass, 기본값 false

# ---------------------------------------------------------------------
# 2. 텍스트 파일 쓰기와 읽기
#    with를 쓰면 작업이 끝날 때 파일이 자동으로 닫힙니다.
#    encoding="utf-8"은 한글이 깨지지 않게 해 줍니다.
# ---------------------------------------------------------------------
note_path = OUTPUT_DIR / "note.txt"

with open(note_path, "w", encoding="utf-8") as file:  # "w": 새로 쓰기
    file.write("오늘 측정한 분자\n")  # \n은 줄바꿈입니다.
    file.write("vanillin\n")

with open(note_path, "a", encoding="utf-8") as file:  # "a": 뒤에 이어 쓰기
    file.write("limonene\n")

with open(note_path, encoding="utf-8") as file:  # 생략하면 읽기 모드
    for line in file:
        print(line.strip())  # strip(): 앞뒤 공백과 줄바꿈 제거

# ---------------------------------------------------------------------
# 3. CSV 읽기: 표 형식의 텍스트 파일
#    DictReader는 각 행을 {열 이름: 값} 딕셔너리로 줍니다.
# ---------------------------------------------------------------------
molecules = []
with open(DATA_DIR / "molecules.csv", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        row["odors"] = row["odors"].split(";")  # 문자열 → 리스트
        molecules.append(row)

print(f"분자 {len(molecules)}개를 읽었습니다.")
print(molecules[0])

# Counter: 개수를 세어 주는 도구
odor_counts = Counter(odor for molecule in molecules for odor in molecule["odors"])
print(odor_counts.most_common(3))  # 가장 많은 3개

# ---------------------------------------------------------------------
# 4. JSON: 딕셔너리와 리스트를 그대로 저장
# ---------------------------------------------------------------------
json_path = OUTPUT_DIR / "molecules.json"

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(molecules, file, ensure_ascii=False, indent=2)

with open(json_path, encoding="utf-8") as file:
    loaded = json.load(file)
print(loaded[0]["name"], loaded[0]["odors"])

# ---------------------------------------------------------------------
# 5. 오류 처리: try / except
#    오류가 나도 프로그램이 멈추지 않게 하고, 무엇이 문제였는지 기록합니다.
# ---------------------------------------------------------------------
raw_values = ["1.25", "0.98", "N/A", "", "1.31"]

clean_values = []
bad_rows = []
for row_number, text in enumerate(raw_values):
    try:
        clean_values.append(float(text))  # 여기서 오류가 날 수 있습니다.
    except ValueError:  # 숫자로 바꿀 수 없을 때만 잡습니다.
        bad_rows.append(row_number)
print(clean_values)
print(f"읽지 못한 행: {bad_rows}")

# 없는 파일을 열면 FileNotFoundError가 납니다.
try:
    with open(DATA_DIR / "없는파일.csv", encoding="utf-8") as file:
        file.read()
except FileNotFoundError as error:
    print(f"파일을 찾지 못했습니다: {error.filename}")

# ⚠️ 나쁜 습관: except: 만 쓰면 오타로 인한 오류까지 모두 삼켜서
#    무엇이 잘못됐는지 알 수 없게 됩니다. 어떤 오류를 잡을지 꼭 적으세요.


# ---------------------------------------------------------------------
# 6. 직접 오류 내기: raise
#    잘못된 입력은 조용히 넘기지 말고 바로 알려 주는 편이 낫습니다.
# ---------------------------------------------------------------------
def dilution_factor(initial, final):
    if final <= 0:
        raise ValueError(f"최종 농도는 0보다 커야 합니다: {final}")
    return initial / final


print(dilution_factor(100, 4))
try:
    dilution_factor(100, 0)
except ValueError as error:
    print(f"오류: {error}")

# ---------------------------------------------------------------------
# 💡 오류 메시지 읽는 법 (Traceback)
#    오류가 나면 맨 마지막 줄부터 읽으세요. 오류 종류와 이유가 적혀 있습니다.
#    그 위 줄들은 어느 파일 몇 번째 줄을 거쳐 왔는지 보여 줍니다.
#
#    NameError      변수 이름 오타
#    TypeError      자료형이 맞지 않음 ("1" + 1)
#    IndexError     리스트 범위를 벗어남
#    KeyError       딕셔너리에 없는 key
#    ValueError     자료형은 맞는데 값이 이상함 (float("N/A"))
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# 연습문제 (정답: lessons/answers.py)
# ---------------------------------------------------------------------
# 1) molecules에서 "floral" 표현을 가진 분자의 이름만 모아 outputs/floral.txt에
#    한 줄에 하나씩 저장하세요.
with open(DATA_DIR / "molecules.csv", encoding="utf-8") as file:
    molecules = list(csv.DictReader(file))
with open(OUTPUT_DIR / "floral.txt", "w", encoding="utf-8") as file:
    for molecule in molecules:
        if "floral" in molecule["odors"].split(";"):
            file.write(molecule["name"] + "\n")
with open(OUTPUT_DIR / "floral.txt", encoding="utf-8") as file:
    print(file.read())

# 2) ["1.0", "abc", "2.5"]를 float로 바꾸되 실패한 값은 None으로 채운 리스트를
#    만드세요.
floatList = []
for changeNum in ["1.0", "abc", "2.5"]:
    try:
        floatList.append(float(changeNum))
    except ValueError:
        floatList.append(None)
print(floatList)