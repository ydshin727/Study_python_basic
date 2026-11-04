"""
연습문제 정답 모음. 직접 풀어 본 뒤에 확인하세요!
정답은 하나가 아닙니다. 출력이 같다면 다르게 써도 괜찮습니다.

실행: python lessons/answers.py
"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import Descriptors, rdFingerprintGenerator
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
SENSORS = ["s1", "s2", "s3", "s4"]


def lesson_01():
    baseline, peak = 2.0, 3.5
    print(f"증가율: {(peak - baseline) / baseline:.1%}")
    print(len("citrus;fresh;sweet".split(";")))
    print("CCOC(C)=O".count("C"))


def lesson_02():
    readings = [1.0, 1.1, 1.9, 1.7]
    print(round(max(readings) - readings[0], 2))

    limonene = {"name": "limonene"}
    limonene["smiles"] = "CC1=CCC(CC1)C(=C)C"
    print(limonene)

    a = {"fruity", "sweet", "banana"}
    b = {"fruity", "green"}
    print(f"{len(a & b) / len(a | b):.2f}")


def lesson_03():
    values = [1.0, 1.05, 1.5, 1.9, 1.2]
    count = 0
    for value in values:
        if value > 1.4:
            count += 1
    print(count)

    print([round(value - values[0], 2) for value in values])
    print([smiles for smiles in ["CCO", "CC", "CCCO", "c1ccccc1"] if "O" in smiles])


def baseline_correct(readings):
    return [value - readings[0] for value in readings]


def normalize(values):
    largest = max(values)
    if largest == 0:
        return values
    return [value / largest for value in values]


def lesson_04():
    print(baseline_correct([1.0, 1.5, 2.0]))
    print(normalize([1.0, 2.0, 4.0]), normalize([0, 0]))

    molecules = [
        {"name": "vanillin", "heavy_atoms": 11},
        {"name": "ethanethiol", "heavy_atoms": 3},
        {"name": "hexanal", "heavy_atoms": 7},
    ]
    ordered = sorted(molecules, key=lambda m: m["heavy_atoms"], reverse=True)
    print([m["name"] for m in ordered])


class OdorSample:
    def __init__(self, name, odors):
        self.name = name
        self.odors = odors

    def odor_count(self):
        return len(self.odors)


class Sensor:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id

    def read(self, raw):
        return raw


class ScaledSensor(Sensor):
    def __init__(self, sensor_id, scale):
        super().__init__(sensor_id)
        self.scale = scale

    def read(self, raw):
        return raw * self.scale


def lesson_05():
    print(OdorSample("vanillin", ["sweet", "vanilla"]).odor_count())
    print(ScaledSensor("s1", scale=2).read(1.5))


def lesson_06():
    with open(DATA_DIR / "molecules.csv", encoding="utf-8") as file:
        molecules = list(csv.DictReader(file))
    with open(OUTPUT_DIR / "floral.txt", "w", encoding="utf-8") as file:
        for molecule in molecules:
            if "floral" in molecule["odors"].split(";"):
                file.write(molecule["name"] + "\n")

    converted = []
    for text in ["1.0", "abc", "2.5"]:
        try:
            converted.append(float(text))
        except ValueError:
            converted.append(None)
    print(converted)


def lesson_07():
    readings = np.array(
        [
            [1.0, 1.1, 0.9, 1.0],
            [1.8, 1.2, 1.5, 1.1],
            [2.2, 1.3, 1.9, 1.2],
            [1.6, 1.2, 1.4, 1.1],
        ]
    )
    print(readings[:, 2].max())
    print(readings.mean(axis=1).argmax())
    standardized = (readings - readings.mean(axis=0)) / readings.std(axis=0)
    print(standardized.mean(axis=0).round(6), standardized.std(axis=0).round(6))


def lesson_08():
    df = pd.read_csv(DATA_DIR / "enose_readings.csv")
    print(round(df.loc[df["smell"] == "rose", "s4"].mean(), 3))
    print(df.groupby("smell")["trial"].nunique())
    trial_max = df.groupby(["trial", "smell"])["s2"].max().reset_index()
    print(trial_max.groupby("smell")["s2"].mean().idxmax())


def lesson_09():
    df = pd.read_csv(DATA_DIR / "enose_readings.csv")
    trial = df[df["trial"] == 30]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for sensor in SENSORS:
        ax.plot(trial["time_s"], trial[sensor], linewidth=2, label=sensor)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("sensor value")
    ax.legend(frameon=False)
    fig.savefig(OUTPUT_DIR / "trial30.png", dpi=150)
    plt.close(fig)


def lesson_10():
    df = pd.read_csv(DATA_DIR / "enose_readings.csv")
    df[SENSORS] = df.groupby("trial")[SENSORS].transform(
        lambda column: column.interpolate(limit_direction="both")
    )
    rows = []
    for (_, smell), group in df.groupby(["trial", "smell"]):
        baseline = group.loc[group["time_s"] < 20, SENSORS].mean()
        peak = group[SENSORS].max() - baseline
        ratio = peak / peak.sum()
        row = {"smell": smell}
        row.update({f"peak_{s}": peak[s] for s in SENSORS})
        row.update({f"ratio_{s}": ratio[s] for s in SENSORS})
        rows.append(row)
    features = pd.DataFrame(rows)

    X = features.drop(columns="smell")
    y = features["smell"]
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    ratio_columns = [column for column in X.columns if column.startswith("ratio_")]
    print(f"전체 특징: {cross_val_score(model, X, y, cv=folds).mean():.3f}")
    print(f"ratio만: {cross_val_score(model, X[ratio_columns], y, cv=folds).mean():.3f}")


def lesson_11():
    molecules = pd.read_csv(DATA_DIR / "molecules.csv")
    molecules["mol"] = molecules["smiles"].apply(Chem.MolFromSmiles)

    fruity = molecules[molecules["odors"].str.split(";").apply(lambda o: "fruity" in o)]
    print(f"{fruity['mol'].apply(Descriptors.MolWt).mean():.1f}")

    generator = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    fingerprints = [generator.GetFingerprint(mol) for mol in molecules["mol"]]
    index = molecules.index[molecules["name"] == "menthol"][0]
    scores = DataStructs.BulkTanimotoSimilarity(fingerprints[index], fingerprints)
    scores[index] = -1
    print(molecules["name"].iloc[int(np.argmax(scores))])


if __name__ == "__main__":
    for number, lesson in enumerate(
        [lesson_01, lesson_02, lesson_03, lesson_04, lesson_05, lesson_06,
         lesson_07, lesson_08, lesson_09, lesson_10, lesson_11],
        start=1,
    ):
        print(f"\n--- {number:02d}번 정답 ---")
        lesson()
