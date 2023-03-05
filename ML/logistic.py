#%%
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import pandas as pd

# %%
df= pd.read_csv('Customers.csv')
df["salary_range"] = pd.cut(df["Salary"], bins=10, labels=False)
df["age_range"] = pd.cut(df["Age"], bins=25, labels=False)
sample = df.groupby(["salary_range", "age_range"]).sample(100, replace=True)
#%%
plt.hist(sample["salary_range"])
#%%
plt.hist(sample["age_range"])
#%%
data = sample[['salary_range', 'age_range']].to_numpy()
target = sample['Purchased'].to_numpy()
#%%
x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.25, random_state=0)
# %%
model = LogisticRegression(max_iter=500000)
# %%
model.fit(x_train, y_train)
# %%
score = model.score(x_test, y_test)
print(score)
# %%
# %%
from sklearn import metrics
predictions = model.predict(x_test)
cm = metrics.confusion_matrix(y_test, predictions)
print(cm)

# %%
plt.figure(figsize=(9, 9))
sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5,
            square=True, cmap='Blues_r')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
all_sample_title = 'Accuracy Score: {0}'.format(score)
plt.title(all_sample_title, size=15)

# %%
