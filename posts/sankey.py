import pandas as pd
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

def code_role(x):
    if x == "Product/Project Manager":
        return "Project Manager"
    elif x == "Machine Learning Engineer":
        return "ML Engineer"
    elif x == "DBA/Database Engineer":
        return "DB Engineer"
    elif x == 'Data Analyst':
        return "Analyst"
    elif x == 'Business Analyst':
        return "Analyst"
    elif x == 'Statistician':
        return "Analyst"
    else:
        return x

def prep_role_duties_data(df):
    '''Function to prepare data for the Sankey - Role and Duties at Work subchapter.'''
    role = "Select the title most similar to your current role (or most recent title if retired): - Selected Choice"
    dutie = ["Analyze and understand data to influence product or business decisions",
         "Build and/or run the data infrastructure that my business uses for storing, analyzing, and operationalizing data",
         "Build prototypes to explore applying machine learning to new areas",
         "Build and/or run a machine learning service that operationally improves my product or workflows",
         "Do research that advances the state of the art of machine learning",
         "None of these activities are an important part of my role at work"]
    duties = []
    for k, d in enumerate(dutie):
        duties.append(f"Select any activities that make up an important part of your role at work: (Select all that apply) - Selected Choice - {d}")
    columns = [k for k in duties]
    columns.append(role)
    dt = df[df[role] != "Other"][columns]
    dt.columns = ["dutie1", "dutie2", "dutie3", "dutie4", "dutie5", "dutie6", "role"]
    dt["role"] = dt["role"].apply(lambda x: code_role(x))
    return dt

df = pd.read_csv('kaggle_survey_2020_responses.csv',skiprows=1)
dt = prep_role_duties_data(df)
dt = dt.drop(columns=["dutie6"], axis=1)
role_data = dt["role"].value_counts().reset_index()
role_data.columns = ["role", "count"]
dutie_data = dt.melt(id_vars=["role"], var_name="Name", value_name="Dutie")
dutie_data.dropna(inplace=True)
dutie_data = dutie_data.groupby("role")["Dutie"].value_counts().unstack().reset_index()
dutie_data = dutie_data.melt(id_vars=["role"], var_name="dutie", value_name="count")
dutie_data = dutie_data.sort_values(['count'], ascending=False).groupby('role').head(5).sort_values(['role', 'dutie'])
dutie_data = dutie_data[~dutie_data["role"].isin(["DB Engineer", "Data Engineer", "Research Scientist", "Project Manager"])]
label = ['Analyst', 'Data Scientist', 'ML Engineer', 'Software Engineer',
         'Analyze and Understand Data',
         'Build and run ML',
         'Build and run data infrastructure',
         'Create ML to explore new areas',
         'Research to advance the state of ML']

source = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
target = [4, 5, 6, 7, 8, 4, 5, 6, 7, 8, 4, 5, 6, 7, 8, 4, 5, 6, 7, 8]
value = dutie_data["count"].values

color_node = ["#00ff9f", "#00b8ff", "#001eff", "#bd00ff",
              "#d600ff", "#711c91", "#ea00d9", "#0abdc6", "#133e7c"]

color_link = [f'rgba({int(color[1:][0:2], 16)}, {int(color[1:][2:4], 16)}, {int(color[1:][4:6], 16)}, 0.4)' for color in color_node]*3

link = dict(source = source, target = target, value = value, color = color_link)# 
node = dict(label = label, pad=10, thickness=21, color = color_node,# color=px.colors.qualitative.Bold, 
            line = dict(color = "black", width = [5,10]))
data = [go.Sankey(link = link, node=node, arrangement='snap')]

layout = go.Layout(hovermode = 'x',
                   title="~ Чем заняты айтишники ~",
                   font=dict(size = 24, family="monospace"),
                   template = 'plotly_dark')

fig = go.Figure(data, layout)
fig.show()