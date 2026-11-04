"""
11. 미니 프로젝트 2: 분자 구조에서 냄새 추측하기

후각 AI의 또 다른 큰 축은 "분자 구조만 보고 냄새를 예측하기"입니다.
흐름: SMILES 문자열 → RDKit 분자 객체 → 숫자 특징(지문) → 비교·예측

RDKit은 화학 정보학 라이브러리입니다.

주의: 분자 24개, 표현은 간단히 붙인 예시입니다. 성능을 내기 위한 데이터가 아니라
흐름을 익히기 위한 장난감 데이터입니다. 실제 연구는 수천 개 분자를 사용합니다.

실행: python lessons/11_molecule_odor.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import Descriptors, rdFingerprintGenerator

PROJECT_DIR = Path(__file__).resolve().parent.parent

molecules = pd.read_csv(PROJECT_DIR / "data" / "molecules.csv")
molecules["odor_set"] = molecules["odors"].str.split(";").apply(set)

# ---------------------------------------------------------------------
# 1. SMILES를 분자 객체로
#    SMILES 읽는 법: C=탄소, O=산소, 소문자 c=방향족 고리 탄소,
#                    =는 이중 결합, 괄호는 곁가지, 숫자는 고리 연결 표시
#    잘못된 SMILES는 None을 돌려주므로 확인이 필요합니다.
# ---------------------------------------------------------------------
molecules["mol"] = molecules["smiles"].apply(Chem.MolFromSmiles)
print(f"읽지 못한 분자: {molecules['mol'].isna().sum()}개")

# ---------------------------------------------------------------------
# 2. 분자 설명자: 분자의 성질을 나타내는 숫자
#    냄새를 맡으려면 분자가 공기 중으로 날아와야 하므로
#    분자량이 작고 극성이 낮은 편인 분자가 많습니다.
#      MolWt    분자량
#      MolLogP  물보다 기름을 얼마나 좋아하는가
#      TPSA     분자의 극성을 띤 표면적
# ---------------------------------------------------------------------
molecules["mol_wt"] = molecules["mol"].apply(Descriptors.MolWt)
molecules["log_p"] = molecules["mol"].apply(Descriptors.MolLogP)
molecules["tpsa"] = molecules["mol"].apply(Descriptors.TPSA)
print(molecules[["name", "mol_wt", "log_p", "tpsa"]].round(2).head(5))
print(f"분자량 범위: {molecules['mol_wt'].min():.1f} ~ {molecules['mol_wt'].max():.1f}")

# ---------------------------------------------------------------------
# 3. 분자 지문(fingerprint): 구조를 0과 1의 벡터로
#    각 원자 주변의 부분 구조가 있는지를 2048칸짜리 체크리스트로 표시합니다.
#    이렇게 숫자가 되어야 AI 모델에 넣을 수 있습니다.
# ---------------------------------------------------------------------
generator = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
molecules["fp"] = molecules["mol"].apply(generator.GetFingerprint)

as_array = generator.GetFingerprintAsNumPy(molecules["mol"].iloc[0])
print(f"지문 모양: {as_array.shape}, 켜진 칸 수: {int(as_array.sum())}")

# ---------------------------------------------------------------------
# 4. 타니모토 유사도: 두 지문이 얼마나 겹치는지 0~1로 계산합니다.
#    02번에서 배운 자카드 유사도와 같은 계산입니다.
# ---------------------------------------------------------------------
fingerprints = list(molecules["fp"])
names = list(molecules["name"])


def most_similar(index):
    """자기 자신을 제외하고 가장 비슷한 분자의 번호와 유사도를 돌려줍니다."""
    scores = DataStructs.BulkTanimotoSimilarity(fingerprints[index], fingerprints)
    scores[index] = -1  # 자기 자신은 제외
    best = int(np.argmax(scores))
    return best, scores[best]


index = names.index("geraniol")
best, score = most_similar(index)
print(f"{names[index]}와 가장 비슷한 분자: {names[best]} (유사도 {score:.2f})")

# ---------------------------------------------------------------------
# 5. 가장 가까운 이웃으로 냄새 추측하기
#    "구조가 비슷한 분자는 냄새도 비슷할 것이다"라는 가설을 검증합니다.
#    분자 하나를 가리고, 나머지 중 가장 비슷한 분자의 냄새로 추측합니다.
#    (Leave-One-Out: 하나씩 돌아가며 시험 문제로 삼는 평가 방법)
# ---------------------------------------------------------------------


def jaccard(a, b):
    return len(a & b) / len(a | b)


odor_sets = list(molecules["odor_set"])
neighbor_scores = []
for index in range(len(molecules)):
    best, _ = most_similar(index)
    neighbor_scores.append(jaccard(odor_sets[index], odor_sets[best]))

# 비교 기준: 구조를 보지 않고 아무 분자나 골랐을 때의 평균 점수
random_scores = [
    jaccard(odor_sets[i], odor_sets[j])
    for i in range(len(odor_sets))
    for j in range(len(odor_sets))
    if i != j
]
print(f"가장 비슷한 분자로 추측한 점수: {np.mean(neighbor_scores):.3f}")
print(f"아무 분자나 고른 점수(기준선): {np.mean(random_scores):.3f}")

# ---------------------------------------------------------------------
# 6. AI가 쓸 형태로 바꾸기: 멀티 라벨
#    분자 하나에 냄새 표현이 여러 개이므로, 표현마다 0/1 열을 만듭니다.
# ---------------------------------------------------------------------
X = np.array([generator.GetFingerprintAsNumPy(mol) for mol in molecules["mol"]])
y = molecules["odors"].str.get_dummies(sep=";")
print(f"X 모양: {X.shape} (분자 수, 지문 길이)")
print(f"y 모양: {y.shape} (분자 수, 냄새 표현 수)")
print(y.iloc[:3, :6])

# ---------------------------------------------------------------------
# 7. 지문의 한계: 거울상 분자
#    카르본은 원자 연결이 같고 입체 구조만 거울상처럼 다른 두 분자가 있습니다.
#      R형은 스피어민트, S형은 캐러웨이 향이 납니다.
#    SMILES의 @와 @@가 입체 구조의 차이를 나타냅니다.
#    기본 설정의 지문은 입체 구조를 보지 않아서 두 분자를 같게 봅니다!
# ---------------------------------------------------------------------
r_carvone = Chem.MolFromSmiles("CC1=CC[C@H](CC1=O)C(=C)C")
s_carvone = Chem.MolFromSmiles("CC1=CC[C@@H](CC1=O)C(=C)C")

same = DataStructs.TanimotoSimilarity(
    generator.GetFingerprint(r_carvone), generator.GetFingerprint(s_carvone)
)
chiral_generator = rdFingerprintGenerator.GetMorganGenerator(
    radius=2, fpSize=2048, includeChirality=True
)
different = DataStructs.TanimotoSimilarity(
    chiral_generator.GetFingerprint(r_carvone), chiral_generator.GetFingerprint(s_carvone)
)
print(f"카르본 R/S 유사도 - 입체 무시: {same:.2f}, 입체 고려: {different:.2f}")

# 입력 표현을 어떻게 만드느냐가 모델 성능의 상한을 정합니다.
# 후각 연구에서 분자를 그래프로 다루는 그래프 신경망(GNN)을 많이 쓰는 이유이기도 합니다.

# ---------------------------------------------------------------------
# 연습문제 (정답: lessons/answers.py)
# ---------------------------------------------------------------------
# 1) "fruity" 표현을 가진 분자들의 평균 분자량을 구하세요.
# 2) menthol과 가장 비슷한 분자를 찾으세요.
