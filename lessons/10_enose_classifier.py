"""
10. 미니 프로젝트 1: 전자코 센서 값으로 냄새 분류하기

지금까지 배운 것을 모두 씁니다. AI 프로젝트의 기본 흐름은 항상 비슷합니다.

    데이터 불러오기 → 정리 → 특징 만들기 → 나누기 → 학습 → 평가 → 의심하기

주의: 합성 데이터의 점수이므로 실제 전자코 성능으로 받아들이면 안 됩니다.
실제 센서에는 시간이 지나면 값이 밀리는 드리프트, 습도와 온도 영향이 있습니다.

실행: python lessons/10_enose_classifier.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

PROJECT_DIR = Path(__file__).resolve().parent.parent
SENSORS = ["s1", "s2", "s3", "s4"]
SEED = 42


# ---------------------------------------------------------------------
# 1. 불러오기와 정리
# ---------------------------------------------------------------------
def load_readings():
    df = pd.read_csv(PROJECT_DIR / "data" / "enose_readings.csv")
    df[SENSORS] = df.groupby("trial")[SENSORS].transform(
        lambda column: column.interpolate(limit_direction="both")
    )
    return df


# ---------------------------------------------------------------------
# 2. 특징(feature) 만들기
#    측정 1회는 60초 × 센서 4개 = 240개의 숫자입니다.
#    모델이 배우기 쉽도록 의미 있는 숫자 몇 개로 줄입니다.
#      peak_*    기준값 대비 최대 반응 → 얼마나 세게 반응했나
#      ratio_*   네 센서 합에서 차지하는 비율 → 농도와 무관한 냄새 '패턴'
# ---------------------------------------------------------------------
def make_features(df):
    rows = []
    for (trial, smell), group in df.groupby(["trial", "smell"]):
        baseline = group.loc[group["time_s"] < 20, SENSORS].mean()
        peak = group[SENSORS].max() - baseline
        ratio = peak / peak.sum()

        row = {"trial": trial, "smell": smell}
        for sensor in SENSORS:
            row[f"peak_{sensor}"] = peak[sensor]
            row[f"ratio_{sensor}"] = ratio[sensor]
        rows.append(row)
    return pd.DataFrame(rows)


df = load_readings()
features = make_features(df)
print(features.round(3).head(3))

X = features.drop(columns=["trial", "smell"])  # 입력. 관례상 대문자 X를 씁니다.
y = features["smell"]  # 정답. 관례상 소문자 y를 씁니다.
print(f"입력 모양: {X.shape}, 정답 개수: {len(y)}")

# ---------------------------------------------------------------------
# 3. 학습용과 평가용으로 나누기
#    시험 문제를 미리 보여 주고 치른 시험 점수는 믿을 수 없습니다.
#    평가용 데이터는 학습에 절대 쓰지 않습니다.
#    stratify=y: 나눈 뒤에도 냄새 비율이 같도록 합니다.
# ---------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=SEED, stratify=y
)

# ---------------------------------------------------------------------
# 4. 모델 만들기와 학습
#    파이프라인으로 묶으면 전처리도 학습 데이터만 보고 맞춰집니다.
#    fit으로 배우고 predict로 예측합니다. 05번의 BaselineDetector와 같은 구조입니다.
# ---------------------------------------------------------------------
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print(f"\n로지스틱 회귀 정확도: {accuracy_score(y_test, predictions):.3f}")

# ---------------------------------------------------------------------
# 5. 자세히 평가하기
#    혼동 행렬: 행이 정답, 열이 예측. 대각선 밖의 숫자가 틀린 경우입니다.
# ---------------------------------------------------------------------
labels = sorted(y.unique())
matrix = confusion_matrix(y_test, predictions, labels=labels)
print(pd.DataFrame(matrix, index=labels, columns=labels))
print(classification_report(y_test, predictions, digits=3))

# ---------------------------------------------------------------------
# 6. 교차 검증: 데이터를 다섯 번 다르게 나누어 평균을 냅니다.
#    나누기 한 번의 운에 덜 좌우되고, 데이터가 적을 때 특히 중요합니다.
# ---------------------------------------------------------------------
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
candidates = {
    "로지스틱 회귀": model,
    "랜덤 포레스트": RandomForestClassifier(n_estimators=200, random_state=SEED),
}
for name, candidate in candidates.items():
    scores = cross_val_score(candidate, X, y, cv=folds)
    print(f"{name}: 평균 {scores.mean():.3f} (표준편차 {scores.std():.3f})")

# ---------------------------------------------------------------------
# 7. 의심하기: 정답을 뒤섞어 봅니다.
#    입력과 정답의 관계를 일부러 끊었으니 정확도가 찍기 수준(세 종류면 약 0.33)이어야
#    합니다. 여기서 점수가 높게 나오면 코드 어딘가에 정답이 새고 있다는 뜻입니다.
# ---------------------------------------------------------------------
rng = np.random.default_rng(SEED)
shuffled = rng.permutation(y.values)
scores = cross_val_score(model, X, shuffled, cv=folds)
print(f"정답을 섞었을 때: 평균 {scores.mean():.3f}")

# ---------------------------------------------------------------------
# 8. 어떤 특징이 중요했나 살펴보기
# ---------------------------------------------------------------------
forest = candidates["랜덤 포레스트"].fit(X_train, y_train)
importance = pd.Series(forest.feature_importances_, index=X.columns)
print(importance.sort_values(ascending=False).round(3).head(4))

# ---------------------------------------------------------------------
# ⚠️ 실제 프로젝트에서 꼭 기억할 점: 데이터 누수
#    같은 날, 같은 센서로 잰 측정이 학습과 평가에 나뉘어 들어가면 점수가 부풀려집니다.
#    실제로는 '다른 날 측정한 데이터'로 평가해야 합니다. GroupKFold를 찾아보세요.
#
# 연습문제 (정답: lessons/answers.py)
# ---------------------------------------------------------------------
# 1) ratio_ 특징만 써서 교차 검증 정확도를 구하고, 전체 특징을 쓴 결과와 비교하세요.
#    힌트: X[[column for column in X.columns if column.startswith("ratio_")]]
