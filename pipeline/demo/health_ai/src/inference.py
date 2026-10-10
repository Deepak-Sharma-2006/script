class HealthRiskClassifier:
    def classify(self, systolic: int, diastolic: int) -> str:
        if systolic >= 140 or diastolic >= 90:
            return "STAGE_2_HYPERTENSION"
        elif systolic >= 130 or diastolic >= 80:
            return "STAGE_1_HYPERTENSION"
        return "NORMAL"
