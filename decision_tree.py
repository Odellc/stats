import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt
import networkx as nx



clf = tree.DecisionTreeClassifier(random_state=0)
data = { 'States': ['S1', 'S2', 'S3', 'S4', 'S5'], 
        'Demand': [1000, 2000, 5000, 10000, 50000], 
        'Probability': [0.45, 0.20, 0.15, 0.10, 0.10], 
        'Payout_A': [12000, 14000, 20000, 30000, 110000], 
        'Payout_B': [6000, 10000, 22000, 42000, 202000], 
        'Weighted_A': [10900, 10800, 11500, 12000, 20000], 
        'Weighted_B': [3800, 3600, 5000, 6000, 22000] } 
df = pd.DataFrame(data)
# clf = clf.fit([[ 1,000 	 0.45 	 12,000 	 6,000 
# ]], [[]])
# print(iris.target)
# tree.plot_tree(clf)

# fig = plt.figure(figsize=(25,20))
# tree_plot = tree.plot_tree(clf,
#                    feature_names=iris.feature_names,
#                    class_names=iris.target_names,
#                    filled=True)

# fig.savefig('C:/Users/codel/Desktop/Applied Statistics Cornell/image.png')


def build_decision_tree(dataframe):
    G = nx.DiGraph()
    
    for index, row in dataframe.iterrows():
        state = row['States']
        prob = row['Probability']
        payout_a = row['Payout_A']
        payout_b = row['Payout_B']
        weighted_a = row['Weighted_A']
        weighted_b = row['Weighted_B']
        
        G.add_node(state, label=f"State: {state}\nProb: {prob}\nPayout A: {payout_a}\nPayout B: {payout_b}\nWeighted A: {weighted_a}\nWeighted B: {weighted_b}")
    
    return G

def plot_decision_tree(G):
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    
    nx.draw(G, pos, with_labels=False, node_size=3000, node_color="skyblue", node_shape="o", alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="black")
    
    plt.title('Decision Tree')
    plt.show()

G = build_decision_tree(df)
plot_decision_tree(G)
