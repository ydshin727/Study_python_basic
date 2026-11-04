"""
05. 클래스: 데이터와 기능을 하나로 묶기

클래스는 '설계도', 객체는 그 설계도로 만든 '실물'입니다.
scikit-learn의 모델과 PyTorch의 신경망이 모두 클래스이므로,
직접 큰 클래스를 설계하지 않더라도 읽을 줄은 알아야 합니다.

실행: python lessons/05_classes.py
"""

# ---------------------------------------------------------------------
# 1. 클래스 만들기
# ---------------------------------------------------------------------


class Molecule:
    def __init__(self, name, smiles, odors):
        """객체를 만들 때 자동으로 실행되는 초기 설정 함수입니다."""
        # self는 '지금 만들어지는 바로 그 객체'를 뜻합니다.
        # self.xxx에 담은 값은 객체가 계속 기억합니다(속성).
        self.name = name
        self.smiles = smiles
        self.odors = set(odors)

    def has_odor(self, odor):
        """클래스 안의 함수를 메서드라고 합니다. 첫 매개변수는 항상 self입니다."""
        return odor in self.odors

    def similarity(self, other):
        """다른 분자와 냄새 표현이 얼마나 겹치는지 계산합니다."""
        return len(self.odors & other.odors) / len(self.odors | other.odors)

    def __repr__(self):
        """print로 출력할 때 보일 모습을 정합니다."""
        return f"Molecule({self.name}, odors={sorted(self.odors)})"


geraniol = Molecule("geraniol", "CC(C)=CCCC(C)=CCO", ["floral", "rose"])
linalool = Molecule("linalool", "CC(C)=CCCC(C)(O)C=C", ["floral", "fresh"])

print(geraniol)  # __repr__ 덕분에 읽기 좋게 나옵니다.
print(geraniol.name)  # 속성 읽기
print(geraniol.has_odor("rose"))  # 메서드 호출. self는 Python이 알아서 넣습니다.
print(f"{geraniol.similarity(linalool):.2f}")

# ---------------------------------------------------------------------
# 2. 상태를 기억하는 객체
#    fit()으로 배운 내용을 기억하고 predict()로 쓰는 구조는
#    scikit-learn 모델과 똑같습니다. (10번 레슨에서 다시 만납니다)
# ---------------------------------------------------------------------


class BaselineDetector:
    """기준값보다 충분히 높은 값을 '냄새 감지'로 판단하는 간단한 모델."""

    def __init__(self, margin=0.3):
        self.margin = margin
        self.baseline = None  # 아직 학습 전

    def fit(self, clean_air_readings):
        self.baseline = sum(clean_air_readings) / len(clean_air_readings)
        return self

    def predict(self, value):
        if self.baseline is None:
            raise ValueError("fit을 먼저 호출해야 합니다.")
        return value > self.baseline + self.margin


detector = BaselineDetector(margin=0.3)
detector.fit([1.0, 1.02, 0.98])  # 깨끗한 공기로 기준값 학습
print(detector.baseline)
print(detector.predict(1.5), detector.predict(1.1))

# ---------------------------------------------------------------------
# 3. 상속: 기존 클래스를 물려받아 일부만 바꾸기
# ---------------------------------------------------------------------


class Sensor:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id

    def describe(self):
        return f"{self.sensor_id}: 일반 센서"

    def read(self, raw):
        return raw


class CalibratedSensor(Sensor):  # 괄호 안이 물려받을 클래스입니다.
    def __init__(self, sensor_id, offset):
        super().__init__(sensor_id)  # 부모의 초기 설정을 먼저 실행합니다.
        self.offset = offset

    def read(self, raw):  # 부모의 메서드를 다시 정의합니다(오버라이딩).
        return raw - self.offset


plain = Sensor("s1")
calibrated = CalibratedSensor("s2", offset=0.5)
print(plain.read(1.5), calibrated.read(1.5))
print(calibrated.describe())  # 고치지 않은 메서드는 그대로 물려받습니다.

# ---------------------------------------------------------------------
# 4. 미리보기: PyTorch 신경망을 읽어 봅시다
#    PyTorch는 아직 설치하지 않았으니 눈으로만 읽으세요.
#
#    class OdorNet(nn.Module):             # nn.Module을 상속
#        def __init__(self):
#            super().__init__()            # 부모 초기 설정
#            self.layer = nn.Linear(4, 3)  # 센서 4개 → 냄새 3종류
#
#        def forward(self, x):             # 입력이 어떻게 흘러가는지 정의
#            return self.layer(x)
#
#    이 레슨의 내용만으로 구조가 읽힙니다.
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# 연습문제 (정답: lessons/answers.py)
# ---------------------------------------------------------------------
# 1) 이름과 냄새 표현 목록을 받는 클래스 OdorSample(name, odors)을 만들고,
#    냄새 표현 개수를 돌려주는 odor_count 메서드를 넣으세요.
# 2) Sensor를 상속해 값을 scale배 해서 돌려주는 ScaledSensor를 만드세요.
