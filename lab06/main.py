import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

credit_history = ctrl.Antecedent(np.arange(0, 11, 1), "credit_history")
income_level = ctrl.Antecedent(np.arange(0, 11, 1), "income_level")
debt_ratio = ctrl.Antecedent(np.arange(0, 101, 1), "debt_ratio")
credit_risk = ctrl.Consequent(np.arange(0, 101, 1), "credit_risk")

credit_history["bad"] = fuzz.trimf(credit_history.universe, [0, 0, 5])
credit_history["satisfactory"] = fuzz.trimf(credit_history.universe, [0, 5, 10])
credit_history["good"] = fuzz.trimf(credit_history.universe, [5, 10, 10])

income_level["low"] = fuzz.trapmf(income_level.universe, [0, 0, 2, 4])
income_level["medium"] = fuzz.trimf(income_level.universe, [2, 5, 8])
income_level["high"] = fuzz.trapmf(income_level.universe, [6, 8, 10, 10])

debt_ratio["low"] = fuzz.trapmf(debt_ratio.universe, [0, 0, 20, 40])
debt_ratio["medium"] = fuzz.trimf(debt_ratio.universe, [20, 50, 80])
debt_ratio["high"] = fuzz.trapmf(debt_ratio.universe, [60, 80, 100, 100])

credit_risk["low"] = fuzz.trapmf(credit_risk.universe, [0, 0, 25, 50])
credit_risk["medium"] = fuzz.trimf(credit_risk.universe, [25, 50, 75])
credit_risk["high"] = fuzz.trapmf(credit_risk.universe, [50, 75, 100, 100])


rule1 = ctrl.Rule(income_level["high"] | credit_history["good"], credit_risk["low"])
rule2 = ctrl.Rule(income_level["medium"] & debt_ratio["medium"], credit_risk["medium"])
rule3 = ctrl.Rule(income_level["low"] & credit_history["bad"], credit_risk["high"])
rule4 = ctrl.Rule(debt_ratio["high"], credit_risk["high"])
rule5 = ctrl.Rule(income_level["low"] & debt_ratio["low"], credit_risk["medium"])


risk_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
risk_assessment = ctrl.ControlSystemSimulation(risk_ctrl)

risk_assessment.input["credit_history"] = 8.5
risk_assessment.input["income_level"] = 7
risk_assessment.input["debt_ratio"] = 60

risk_assessment.compute()

print(f"Рівень кредитного ризику: {risk_assessment.output['credit_risk']:.2f}%")

credit_risk.view(sim=risk_assessment)
input("Press any key to exit the program")
