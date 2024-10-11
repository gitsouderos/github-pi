import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.cluster import DBSCAN
from sklearn import metrics
from project.config.settings import GITHUB_ACCESS_TOKEN
from project.config.github_client import github_client as gt



# Search for repositories based on keywords, stars, etc.
repositories = gt.search_repositories(
    query="language:python stars:>1000", sort="stars", order="desc"
)
#Reduce dimensionality then find meaningfull clusters
# list to save names and readme files
repos_data = []

# Loop through the repositories and fetch relevant data
for repo in repositories[:100]:  # Limit to top 100 repositories
    # print(f"Repository Name: {repo.name}")
    # print(f"Owner: {repo.owner.login}")
    # print(f"Stars: {repo.stargazers_count}")
    # print(f"URL: {repo.html_url}")
    # print("-----")

    # Fetch and display the content of the README file
    # Fetch and display the first 1000 characters of the README file, if available
    try:
        readme = repo.get_readme()  # Try to fetch the README file

        if readme:  # If the README exists
            try:
                # Decode the content to a string
                readme_content = readme.decoded_content.decode(
                    "utf-8"
                )  # important to include the UTF cuz i was getting weird results otherwise
                readme_content = readme_content[:100000]

                # Store the repo name and Readme file in a list
                repos_data.append(
                    {"repo_name": repo.name, "readme_content": readme_content}
                )

            except UnicodeDecodeError:
                print("README exists, but couldn't be decoded as 'utf-8'.")
        else:
            print(f"No README found for repository {repo.name}")

    except Exception as e:
        print(f"Error fetching README for repository {repo.name}: {e}")


print("\n --- Finished the fetching ---")

repos_df = pd.DataFrame(repos_data)

# We now have a dataframe that contains 2 columns, the repo name and the readme content

print(repos_df.head())

# ---------------------------------------------------------------------------------------------------#

# Perform TF-IDF encoding

# Initialize the TF-IDF vectorizer
# Not the best encoder we could pick but this is just for testing
vectorizer = TfidfVectorizer(
    max_features=1000, stop_words=["project", "code", "repository", "python"]
)  # Stop words are basically words in the readme file we dont want to take into account

# Fit the vectorizer on the README content
X_tfidf = vectorizer.fit_transform(repos_df["readme_content"])

# ------------------------------------------------------------------------------------------------------#

#Parameters of dbscan are:
#eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other
#min samples: The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. 
#High value -> High density neighborhood
#Low value -> Low density neighborhood
#Metric : euclidean

#Lets perform a form of grid_search to find parameters (not yet implemented)

# eps_n =[0.3,0.35,0.4,0.45,0.5,0.55]
# min_samples_n = [2,3,4,5]

# for value in eps_n:
#     for min_sample_value in min_samples_n:

#         clustering = DBSCAN(eps=value, min_samples=min_sample_value,metric = "cosine").fit(X_tfidf)
#         labels = clustering.labels_

#         n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
#         n_noise_ = list(labels).count(-1)
#         print(f'For eps ={value} and min_sample={min_sample_value} :')
#         print("Estimated number of clusters: %d" % n_clusters_)
#         print("Estimated number of noise points: %d" % n_noise_ ,"\n")
#print(f"Silhouette Coefficient: {metrics.silhouette_score(X_tfidf, labels):.3f}")

#Eps=0.99, min sample =2 is currently working the best

clustering = DBSCAN(eps=0.4, min_samples=2, metric="cosine").fit(X_tfidf)
labels = clustering.labels_

repos_df["cluster"] = labels

# Display the clustered repositories
print(repos_df[["repo_name", "cluster"]])

print(repos_df.query("cluster = 1"))

# Save the clustering result to a CSV file
#repos_df.to_csv("clustered_repos.csv", index=False)

# Display top terms in each cluster

print("\n--- Top terms per cluster ---\n")

# cluster_centers = clustering.cluster_centers_

# Get the terms from the TF-IDF vectorizer
terms = vectorizer.get_feature_names_out()

# Display the top terms for each cluster
# n_terms = 10  # Number of top terms to display
# for i in range(labels):
#     print(f"Cluster {i}:")
#     top_term_indices = cluster_centers[i].argsort()[-n_terms:][::-1]
#     top_terms = [terms[ind] for ind in top_term_indices]
#     print(", ".join(top_terms))
#     print()


