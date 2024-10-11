from github import Github as gt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

g = gt("Get your own api key")

# Search for repositories based on keywords, stars, etc.
repositories = g.search_repositories(
    query="language:python stars:>1000", sort="stars", order="desc"
)

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

# Perform clustering

n_clusters = 5  # We can tune it based on the silluete score that i calculate at the end. But i dont think kmeans is very effective either. Look at dbscan ?
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X_tfidf)

# Add the cluster labels to the DataFrame
repos_df["cluster"] = kmeans.labels_

# Display the clustered repositories
print(repos_df[["repo_name", "cluster"]])

# Save the clustering result to a CSV file
repos_df.to_csv("clustered_repos.csv", index=False)

# Display top terms in each cluster

print("\n--- Top terms per cluster ---\n")

cluster_centers = kmeans.cluster_centers_

# Get the terms from the TF-IDF vectorizer
terms = vectorizer.get_feature_names_out()

# Display the top terms for each cluster
n_terms = 10  # Number of top terms to display
for i in range(n_clusters):
    print(f"Cluster {i}:")
    top_term_indices = cluster_centers[i].argsort()[-n_terms:][::-1]
    top_terms = [terms[ind] for ind in top_term_indices]
    print(", ".join(top_terms))
    print()

# Calculate the silhouette score
sil_score = silhouette_score(X_tfidf, kmeans.labels_)
print(f"Silhouette Score: {sil_score}")
