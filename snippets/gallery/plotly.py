import plotly.express as px

fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
print(fig.to_html(full_html=False, include_plotlyjs="cdn"))
