from pgmpy.models import DiscreteBayesianNetwork  
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Step 1: Define the Bayesian Network structure
# Intelligence (I), StudyHours (S), Difficulty (D) -> Grade (G) -> Pass (P)
# Network Diagram:
#     I       S       D
#      \      |      /
#       v     v     v
#            G ----> P
model = DiscreteBayesianNetwork([
    ('Intelligence', 'Grade'),
    ('StudyHours', 'Grade'),
    ('Difficulty', 'Grade'),
    ('Grade', 'Pass')
])

# Step 2:defne conditional probability tables (cpts)
# p(intelligence): high=0.7, low=0.3
cpd_intelligence = TabularCPD(
    variable='Intelligence', variable_card=2,
    values=[[0.3], [0.7]], state_names={'Intelligence': ['Low', 'High']}
)

cpd_studyhours = TabularCPD(
    variable='StudyHours', variable_card=2,
    values=[[0.4], [0.6]], state_names={'StudyHours': ['Insufficient', 'Sufficient']}
)

cpd_difficulty = TabularCPD(
    variable='Difficulty', variable_card=2,
    values=[[0.6], [0.4]], state_names={'Difficulty': ['Easy', 'Hard']}
)

cpd_grade = TabularCPD(
    variable='Grade', variable_card=3,
    values=[
        [0.2, 0.1, 0.5, 0.3, 0.6, 0.4, 0.9, 0.7],
        [0.5, 0.3, 0.4, 0.5, 0.3, 0.4, 0.1, 0.2],
        [0.3, 0.6, 0.1, 0.2, 0.1, 0.2, 0.0, 0.1]
    ],
    evidence=['Intelligence', 'StudyHours', 'Difficulty'], evidence_card=[2, 2, 2],
    state_names={'Grade': ['A', 'B', 'C'], 'Intelligence': ['Low', 'High'],
                 'StudyHours': ['Insufficient', 'Sufficient'], 'Difficulty': ['Easy', 'Hard']}
)

cpd_pass = TabularCPD(
    variable='Pass', variable_card=2,
    values=[
        [0.95, 0.80, 0.50],  # P(Yes | A, B, C)
        [0.05, 0.20, 0.50]   # P(No | A, B, C)
    ],
    evidence=['Grade'], evidence_card=[3],
    state_names={'Pass': ['Yes', 'No'], 'Grade': ['A', 'B', 'C']}
)

# Step 3:add CPDs to the model
model.add_cpds(cpd_intelligence, cpd_studyhours, cpd_difficulty, cpd_grade, cpd_pass)

# Step 4:verify the model
assert model.check_model(), "Model verification failedd"

# Step 5:perform inference
infer = VariableElimination(model)

# Query 1:P(Pass | StudyHours=Sufficient, Difficulty=Hard)
print("Probability of passing given Sufficient StudyHours and Hard Difficulty:")
result1 = infer.query(variables=['Pass'], evidence={'StudyHours': 'Sufficient', 'Difficulty': 'Hard'})
print(result1)

# Query 2:P(Intelligence=High | Pass=Yes)
print("\nProbability of High Intelligence given Pass=Yes:")
result2 = infer.query(variables=['Intelligence'], evidence={'Pass': 'Yes'})
print(result2)