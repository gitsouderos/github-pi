import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from project.config.db import sync_engine
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
import os
import pickle
import datetime

EPS=0.2
MIN_SAMP=10
# Create a backup directory
backup_dir = os.path.join(os.getcwd(), 'backups', datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + f"_e{EPS}_m{MIN_SAMP}")
os.makedirs(backup_dir, exist_ok=True)


def save_object(obj, filename):
    filepath = os.path.join(backup_dir, filename)
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)
    print(f"Saved {filename} to {filepath}")


def save_figure(fig, filename):
    filepath = os.path.join(backup_dir, filename)
    fig.savefig(filepath)
    print(f"Saved {filename} to {filepath}")


def load_object(filename, backup_dir):
    filepath = os.path.join(backup_dir, filename)
    with open(filepath, 'rb') as f:
        return pickle.load(f)


# Select embeddings flattened
repos_df = pd.read_sql("""
SELECT
    r.id,
    r.full_name,
    r.stargazers_count,
    cf.id as fileid,
    e.embedding::text
FROM
    repositories r
INNER JOIN
    content_files cf ON r.id = cf.repository_id
INNER JOIN
    embeddings e ON cf.id = e.file_id
ORDER BY
    r.stargazers_count DESC;
""", sync_engine)

print(repos_df.head())
print(f'Entries: {repos_df.shape}')


def parse_embedding(embedding_str):
    return np.array([float(x) for x in embedding_str.strip('[]').split(',')])


repos_df['embedding'] = repos_df['embedding'].apply(parse_embedding)
repos_embeddings = repos_df['embedding']
repos_embeddings.index = repos_df['id']
print(repos_embeddings.head())

X = np.array(repos_df['embedding'].to_list(), dtype=np.float32)
print(f'x.shape: {X.shape}')

# tsne = TSNE(random_state=0, n_iter=1000)
# tsne_results = tsne.fit_transform(X)

# # Save tsne_results
# save_object(tsne_results, 'tsne_results.pkl')

# df_tsne = pd.DataFrame(tsne_results, columns=['TSNE1', 'TSNE2'])
# df_tsne['repo_name'] = repos_df['full_name']
# df_tsne['repo_read_me'] = repos_df['fileid']

# # Save df_tsne
# save_object(df_tsne, 'df_tsne.pkl')

# fig, ax = plt.subplots(figsize=(8, 6))
# sns.set_style('darkgrid', {"grid.color": ".6", "grid.linestyle": ":"})
# sns.scatterplot(data=df_tsne, x='TSNE1', y='TSNE2', hue='repo_name', palette='hls')
# sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
# plt.title('Scatter Plot of Embeddings Using t-SNE')
# plt.xlabel('TSNE1')
# plt.ylabel('TSNE2')
# plt.axis('equal')

# # Save the figure
# save_figure(fig, 'tsne_scatter.png')
#>>>begin recycled block (save time by loading my pickles)
old_backup_dir = "./backups/20241004_182325_e4_m2/"
df_tsne = load_object('df_tsne.pkl', old_backup_dir)
#<<<end recycling block


print("STARTING DBSCAN")
clustering = DBSCAN(eps=EPS, min_samples=MIN_SAMP, metric="cosine").fit(X)
labels = clustering.labels_

# Save clustering results
save_object(clustering, 'dbscan_clustering.pkl')
save_object(labels, 'dbscan_labels.pkl')

df_tsne['Cluster'] = labels

# Save updated df_tsne
save_object(df_tsne, 'df_tsne_with_clusters.pkl')

fig, ax = plt.subplots(figsize=(8, 6))
sns.set_style('darkgrid', {"grid.color": ".6", "grid.linestyle": ":"})
sns.scatterplot(data=df_tsne, x='TSNE1', y='TSNE2', hue='repo_name', palette='hls')
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
plt.title('Scatter Plot of Embeddings Using t-SNE (with DBSCAN clusters)')
plt.xlabel('TSNE1')
plt.ylabel('TSNE2')
plt.axis('equal')

# Save the final figure
save_figure(fig, 'tsne_scatter_with_clusters.png')

print(f"All backups saved to: {backup_dir}")
