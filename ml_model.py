import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Dummy training data (GC%, ORFs, genes)
X = np.array([
    [40, 1, 0],
    [55, 3, 1],
    [60, 5, 2],
    [30, 0, 0],
    [70, 6, 3]
])

y = np.array([0, 1, 1, 0, 1])

model = RandomForestClassifier()
model.fit(X, y)

def predict_resistance(gc, orfs, genes):
    pred = model.predict([[gc, orfs, genes]])
    return "Resistant" if pred[0] else "Sensitive"
