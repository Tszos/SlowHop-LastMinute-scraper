import pandas as pd
from scrap import scrap_slowhop
from IPython.display import display

df = pd.DataFrame(scrap_slowhop())
dupa = 1


# styled = df.style.applymap(lambda x: 'background-color: %s' % 'green' if x > dupa else '' for x in df['oszczędność'])
df.to_excel('df.xlsx', index=False)
# styled.to_excel('df.xlsx', index=False)

display(df)
