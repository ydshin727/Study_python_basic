"""
08. pandas: 표 형태의 데이터 다루기

엑셀로 하던 일을 코드로 합니다. 불러오기 → 살펴보기 → 고르기 → 묶어서 요약하기.
이 레슨에서는 합성 전자코 데이터(data/enose_readings.csv)를 씁니다.

데이터 구조:
    trial    측정 번호 (0~89)
    smell    냄새 종류 (coffee, lemon, rose)
    time_s   측정 시작 후 경과 시간(초). 20초에 냄새 주입, 40초에 중단
    s1~s4    센서 4개의 값

실행: python lessons/08_pandas.py
"""

from pathlib import Path

import pandas as pd  # pd라는 줄임말이 관례입니다.

PROJECT_DIR = Path(__file__).resolve().parent.parent
SENSORS = ["s1", "s2", "s3", "s4"]

# ---------------------------------------------------------------------
# 1. 불러오기와 첫인상
#    새 데이터를 받으면 항상 이 네 줄부터 실행하세요.
# ---------------------------------------------------------------------
df = pd.read_csv(PROJECT_DIR / "data" / "enose_readings.csv")

print(df.head())  # 앞 5행
print(df.shape)  # (행, 열)
print(df.dtypes)  # 열마다 자료형
print(df.describe().round(3))  # 숫자 열의 요약 통계

# ---------------------------------------------------------------------
# 2. 열과 행 고르기
# ---------------------------------------------------------------------
print(df["smell"].head(2))  # 열 하나 → Series
print(df[["time_s", "s1"]].head(2))  # 여러 열 → DataFrame (대괄호가 두 겹!)
print(df["smell"].unique())  # 고유한 값
print(df["smell"].value_counts())  # 값마다 개수

print(df.iloc[0, 3])  # iloc: 번호로 고르기 (0행 3열)
print(df.loc[0, "s1"])  # loc: 행 이름과 열 이름으로 고르기

# ---------------------------------------------------------------------
# 3. 조건으로 거르기
#    조건을 여러 개 쓸 때는 and/or 대신 &, |를 쓰고 각각 괄호로 감쌉니다.
# ---------------------------------------------------------------------
coffee = df[df["smell"] == "coffee"]
print(len(coffee))

exposure = df[(df["time_s"] >= 20) & (df["time_s"] < 40)]  # 냄새 주입 구간
print(len(exposure))

print(df.query("smell == 'lemon' and s2 > 2").shape)  # query로도 쓸 수 있습니다.

# ---------------------------------------------------------------------
# 4. 결측치(비어 있는 값) 처리
# ---------------------------------------------------------------------
print(df.isna().sum())  # 열마다 결측치 개수

# 측정별로 앞뒤 값을 이어 메웁니다(선형 보간). 다른 측정의 값이 섞이면 안 되므로
# 반드시 trial별로 묶어서 처리합니다.
df[SENSORS] = df.groupby("trial")[SENSORS].transform(
    lambda column: column.interpolate(limit_direction="both")
)
print(f"보간 후 결측치: {df[SENSORS].isna().sum().sum()}개")

# ---------------------------------------------------------------------
# 5. 새 열 만들기
# ---------------------------------------------------------------------
df["total"] = df[SENSORS].sum(axis=1)  # 시점마다 네 센서의 합
df["phase"] = "before"
df.loc[df["time_s"] >= 20, "phase"] = "exposure"
df.loc[df["time_s"] >= 40, "phase"] = "after"
print(df["phase"].value_counts())

# ---------------------------------------------------------------------
# 6. groupby: 묶어서 요약하기. pandas에서 가장 중요한 기능입니다.
#    나누기(split) → 계산하기(apply) → 합치기(combine)
# ---------------------------------------------------------------------
print(df.groupby("smell")["s1"].mean().round(3))
print(df.groupby(["smell", "phase"])[SENSORS].mean().round(3))

# 측정 하나당 최댓값을 구한 뒤, 냄새별로 그 평균을 냅니다.
peaks = df.groupby(["trial", "smell"])[SENSORS].max().reset_index()
print(peaks.head(3))
print(peaks.groupby("smell")[SENSORS].mean().round(3))

# ---------------------------------------------------------------------
# 7. 다른 표와 합치기: merge (SQL의 JOIN, 엑셀의 VLOOKUP과 비슷합니다)
# ---------------------------------------------------------------------
notes = pd.DataFrame(
    {"smell": ["coffee", "lemon", "rose"], "family": ["roasted", "citrus", "floral"]}
)
merged = peaks.merge(notes, on="smell")
print(merged[["trial", "smell", "family"]].head(3))

# ---------------------------------------------------------------------
# 8. 분자 데이터 다루기: 문자열 열
# ---------------------------------------------------------------------
molecules = pd.read_csv(PROJECT_DIR / "data" / "molecules.csv")
floral = molecules[molecules["odors"].str.contains("floral")]
print(floral["name"].tolist())

# 세미콜론으로 묶인 표현을 행 단위로 펼치면 세기가 쉽습니다.
counts = molecules["odors"].str.split(";").explode().value_counts()
print(counts.head(5))

# ---------------------------------------------------------------------
# 9. 저장
# ---------------------------------------------------------------------
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)  # 폴더가 없으면 만듭니다.
peaks.to_csv(OUTPUT_DIR / "peaks.csv", index=False)

# ---------------------------------------------------------------------
# 연습문제 (정답: lessons/answers.py)
# ---------------------------------------------------------------------
# 1) rose 데이터에서 s4의 전체 평균을 구하세요.
# 2) 냄새별로 측정(trial)이 몇 번인지 세세요. 힌트: nunique()
# 3) 측정별로 s2의 최댓값을 구한 뒤, 이 값의 평균이 가장 큰 냄새를 찾으세요.
#    힌트: idxmax()
