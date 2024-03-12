import pandas as pd

data = []
for i in range(10):
    no_original_output = f"res1/with_original_{i}.xlsx"
    df = pd.read_excel(no_original_output)
    data_list = df.values.tolist()
    data.extend(data_list)

df = pd.DataFrame(data)
df.to_excel("res1/with_original.xlsx", index=False)