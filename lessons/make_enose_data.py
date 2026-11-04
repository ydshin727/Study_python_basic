"""
가상의 전자코(e-nose) 측정 데이터를 만드는 스크립트.

주의: 이 데이터는 학습용으로 지어낸 '합성 데이터'입니다. 실제 센서 측정값이 아닙니다.
지금은 내용을 이해하지 않아도 됩니다. 07_numpy를 끝낸 뒤 읽어 보면 좋아요.

실행: python lessons/make_enose_data.py  →  data/enose_readings.csv 생성
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# 냄새마다 센서 4개가 반응하는 '패턴'이 다르다고 가정합니다.
PROFILES = {
    "coffee": [1.0, 0.3, 0.6, 0.2],
    "lemon": [0.4, 1.0, 0.3, 0.5],
    "rose": [0.5, 0.5, 0.9, 0.7],
}
TRIALS_PER_SMELL = 30
DURATION_S = 60  # 측정 시간(초). 1초에 한 번 기록합니다.
ON_S, OFF_S = 20, 40  # 20초에 냄새를 주입하고 40초에 멈춥니다.


def response_curve(time, tau_rise=4.0, tau_decay=8.0):
    """주입 중에는 서서히 오르고, 멈추면 서서히 내려가는 0~1 곡선."""
    curve = np.zeros_like(time, dtype=float)
    on = (time >= ON_S) & (time < OFF_S)
    curve[on] = 1 - np.exp(-(time[on] - ON_S) / tau_rise)
    peak = 1 - np.exp(-(OFF_S - ON_S) / tau_rise)
    off = time >= OFF_S
    curve[off] = peak * np.exp(-(time[off] - OFF_S) / tau_decay)
    return curve


def main():
    rng = np.random.default_rng(42)  # 씨앗값을 고정하면 매번 같은 데이터가 나옵니다.
    time = np.arange(DURATION_S)
    curve = response_curve(time)
    tables = []
    trial = 0
    for smell, profile in PROFILES.items():
        for _ in range(TRIALS_PER_SMELL):
            concentration = rng.uniform(0.6, 1.4)  # 측정마다 농도가 다릅니다.
            amplitude = concentration * np.array(profile) * rng.normal(1, 0.35, 4)
            baseline = rng.normal(1, 0.05, 4)  # 센서마다 기준값이 조금 다릅니다.
            noise = rng.normal(0, 0.02, (DURATION_S, 4))
            signal = baseline + np.outer(curve, amplitude) + noise
            table = pd.DataFrame(signal.round(4), columns=["s1", "s2", "s3", "s4"])
            table.insert(0, "time_s", time)
            table.insert(0, "smell", smell)
            table.insert(0, "trial", trial)
            tables.append(table)
            trial += 1
    data = pd.concat(tables, ignore_index=True)
    # 실제 측정처럼 s3 센서 값의 일부를 일부러 비워 둡니다(결측치).
    data.loc[rng.random(len(data)) < 0.005, "s3"] = np.nan
    DATA_DIR.mkdir(exist_ok=True)
    data.to_csv(DATA_DIR / "enose_readings.csv", index=False)
    print(f"저장 완료: {len(data)}행, 측정 {trial}회")


if __name__ == "__main__":
    main()
