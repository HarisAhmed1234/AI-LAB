from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Network: Disease -> Fever, Cough, Fatigue, Chills
model = DiscreteBayesianNetwork([
    ('Disease', 'Fever'),
    ('Disease', 'Cough'),
    ('Disease', 'Fatigue'),
    ('Disease', 'Chills')
])

#cpds
cpd_disease = TabularCPD('Disease', 2, [[0.7], [0.3]], state_names={'Disease': ['Cold', 'Flu']})
cpd_fever = TabularCPD('Fever', 2, [[0.5, 0.1], [0.5, 0.9]], evidence=['Disease'], evidence_card=[2],
                       state_names={'Fever': ['No', 'Yes'], 'Disease': ['Cold', 'Flu']})
cpd_cough = TabularCPD('Cough', 2, [[0.4, 0.2], [0.6, 0.8]], evidence=['Disease'], evidence_card=[2],
                       state_names={'Cough': ['No', 'Yes'], 'Disease': ['Cold', 'Flu']})
cpd_fatigue = TabularCPD('Fatigue', 2, [[0.7, 0.3], [0.3, 0.7]], evidence=['Disease'], evidence_card=[2],
                         state_names={'Fatigue': ['No', 'Yes'], 'Disease': ['Cold', 'Flu']})
cpd_chills = TabularCPD('Chills', 2, [[0.6, 0.4], [0.4, 0.6]], evidence=['Disease'], evidence_card=[2],
                        state_names={'Chills': ['No', 'Yes'], 'Disease': ['Cold', 'Flu']})

#add cpds
model.add_cpds(cpd_disease, cpd_fever, cpd_cough, cpd_fatigue, cpd_chills)

#Verify
assert model.check_model()

#Inference
infer = VariableElimination(model)


print("P(Disease | Fever=Yes, Cough=Yes):")
result1 = infer.query(variables=['Disease'], evidence={'Fever': 'Yes', 'Cough': 'Yes'})
print(result1)

print("\nP(Disease | Fever=Yes, Cough=Yes, Chills=Yes):")
result2 = infer.query(variables=['Disease'], evidence={'Fever': 'Yes', 'Cough': 'Yes', 'Chills': 'Yes'})
print(result2)

print("\nP(Fatigue=Yes | Disease=Flu) = 0.7")