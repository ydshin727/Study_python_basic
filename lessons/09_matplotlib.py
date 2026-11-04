"""
09. matplotlib: 데이터를 그림으로 확인하기

모델을 만들기 전에 먼저 그려 봐야 합니다. 숫자표로는 보이지 않던 문제가 그림에서 보입니다.
이 레슨은 두 가지 그림을 만듭니다.
  - 선 그래프: 시간에 따른 변화      → outputs/sensor_response.png
  - 산점도: 두 값의 관계, 그룹 구분  → outputs/peak_scatter.png

실행: python lessons/09_matplotlib.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 창을 띄우지 않고 파일로만 저장합니다.
import matplotlib.pyplot as plt
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 냄새마다 색과 마커를 고정해 두면 어느 그림에서든 같은 냄새는 같은 모습으로 보입니다.
STYLE = {
    "coffee": {"color": "#2a78d6", "marker": "o", "label_ko": "커피"},
    "lemon": {"color": "#eb6834", "marker": "s", "label_ko": "레몬"},
    "rose": {"color": "#1baf7a", "marker": "^", "label_ko": "장미"},
}
TEXT = "#0b0b0b"
MUTED = "#52514e"
GRID = "#e4e3df"
SURFACE = "#fcfcfb"

# macOS에서 한글이 네모(□)로 깨지지 않도록 글꼴을 지정합니다.
# Windows는 "Malgun Gothic"을 쓰면 됩니다.
plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False  # 음수 기호가 깨지는 것을 막습니다.


def clean_axes(ax):
    """눈금과 테두리를 옅게 해서 데이터가 눈에 먼저 들어오게 합니다."""
    ax.set_facecolor(SURFACE)
    ax.grid(color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)  # 격자를 데이터 뒤로 보냅니다.
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, length=0)


df = pd.read_csv(PROJECT_DIR / "data" / "enose_readings.csv")

# ---------------------------------------------------------------------
# 1. 선 그래프: 냄새별 s1 센서의 평균 반응
#    기본 구조: fig(도화지) 위에 ax(그래프 한 칸)를 놓고, ax에 그립니다.
# ---------------------------------------------------------------------
mean_curve = df.groupby(["smell", "time_s"])["s1"].mean().reset_index()
LABEL_OFFSET = {"coffee": 12, "rose": 12, "lemon": -12}  # 이름표를 띄울 거리(위 +, 아래 -)

fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=SURFACE)
for smell, group in mean_curve.groupby("smell"):
    style = STYLE[smell]
    ax.plot(group["time_s"], group["s1"], color=style["color"], linewidth=2,
            label=style["label_ko"])
    # 선 옆에 이름을 직접 적으면 범례를 오가지 않아도 됩니다.
    # 값이 안정되는 35초 지점에 적고, 서로 겹치지 않게 위아래로 띄웁니다.
    ax.annotate(style["label_ko"], (35, group["s1"].iloc[35]),
                xytext=(0, LABEL_OFFSET[smell]), textcoords="offset points",
                ha="center", va="center", color=TEXT)

ax.axvspan(20, 40, color="#f0efec", zorder=0)  # 냄새를 주입한 구간 표시
ax.set_ylim(0.9, 2.15)
ax.text(30, 2.12, "냄새 주입 구간", ha="center", va="top", color=MUTED)
ax.set_title("커피 냄새에 s1 센서가 가장 크게 반응합니다", loc="left", color=TEXT)
ax.set_xlabel("시간 (초)", color=MUTED)
ax.set_ylabel("s1 센서 값", color=MUTED)
ax.set_xlim(0, 59)
clean_axes(ax)
ax.legend(frameon=False, loc="upper right", labelcolor=TEXT)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "sensor_response.png", dpi=150)
plt.close(fig)  # 다 쓴 그림은 닫아 메모리를 돌려줍니다.

# ---------------------------------------------------------------------
# 2. 산점도: 점 하나가 측정 한 번
#    냄새별 덩어리가 뚜렷할수록 분류가 쉽습니다. 겹치는 부분이 있으면
#    센서를 더 쓰거나 다른 특징을 만들어야 합니다. 10번에서 네 센서를 모두 씁니다.
# ---------------------------------------------------------------------
sensors = ["s1", "s2"]
baseline = df[df["time_s"] < 20].groupby(["trial", "smell"])[sensors].mean()
peak = df.groupby(["trial", "smell"])[sensors].max()
response = (peak - baseline).reset_index()

fig, ax = plt.subplots(figsize=(6.5, 5), facecolor=SURFACE)
for smell, group in response.groupby("smell"):
    style = STYLE[smell]
    ax.scatter(group["s1"], group["s2"], color=style["color"], marker=style["marker"],
               s=64, edgecolors=SURFACE, linewidths=1, label=style["label_ko"])

ax.set_title("센서 두 개만으로는 장미가 다른 냄새와 일부 겹칩니다", loc="left", color=TEXT)
ax.set_xlabel("s1 최대 반응", color=MUTED)
ax.set_ylabel("s2 최대 반응", color=MUTED)
clean_axes(ax)
ax.legend(frameon=False, labelcolor=TEXT)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "peak_scatter.png", dpi=150)
plt.close(fig)

print("그림을 outputs 폴더에 저장했습니다.")

# ---------------------------------------------------------------------
# 💡 정리
#    fig, ax = plt.subplots()   도화지 만들기
#    ax.plot / ax.scatter       그리기
#    ax.set_xlabel / set_title  설명 달기
#    fig.savefig(...)           저장하기
#
# 연습문제 (정답: lessons/answers.py)
# ---------------------------------------------------------------------
# 1) lemon의 측정 하나(trial=30)에서 s1~s4를 한 그래프에 선으로 그려
#    outputs/trial30.png로 저장하세요.
