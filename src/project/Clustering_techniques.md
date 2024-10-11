# Clustering Algorithms Overview

## K-Means
- **Description**: Groups data into K clusters based on similarity using Euclidean distance.
- **Process**:
  1. Embed readme -> convert to vectors -> calculate Euclidean distance -> perform clustering.
  2. The centroids are randomly placed, one for each cluster.
  
## DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
- **Description**: A density-based algorithm where points are clustered based on the density of their neighborhood.
- **Process**:
  1. A point’s neighborhood must contain at least `M` points within a radius `R`.
  2. Points are categorized as:
     - **Core Point**: Has at least `M` points in its neighborhood.
     - **Border Point**: Fewer than `M` points in the neighborhood or reachable from a core point within `R`.
     - **Outlier Point**: Neither a core nor a border point.
  3. Core points that are neighbors are grouped in the same cluster.
  4. Border points are assigned to clusters, and outliers are eliminated.

### Advantages over K-Means:
1. No need to specify the number of clusters, providing more flexibility.
2. DBSCAN handles arbitrary-shaped clusters, unlike K-Means, which forms convex (spherical) clusters.

### Important Notes:
- DBSCAN separates regions of high density from regions of low density.

## Clustering Based on Semantics
- **Research Paper**: [Clustering Based on Semantics Using K-Means and TFID](https://www.mdpi.com/2227-7390/11/3/548)
- **Shared Resource**: [Link](https://chatgpt.com/share/66eabc6a-e330-800a-aedc-5b00fea6798b)

## Preprocessing Techniques
- **Latent Semantic Analysis (LSA)**: Reduces dimensionality and helps discover latent patterns in the data.
- **Spacy**
-  **Create embeddings using a model, extending vectors with additional features.**
    1. **Potential Problems**:
      - Adding features may interfere with their semantic meaning, especially when using cosine similarity.
    2. **Possible Fixes**:
      - Weighted combination: `similarity = α * cosine_similarity + (1 - α) * distance(metadata)`
      - PCA after concatenation.
      - Multimodal embeddings: Text embeddings and metadata are learned together to preserve feature importance.

## Post-Processing Techniques
- **Selecting Number of Clusters**: Use silhouette score for selection.
  - [Example with scikit-learn](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html#sphx-glr-auto-examples-cluster-plot-kmeans-silhouette-analysis-py)

## TFIDF Vectorizer
- **What It Does**:
  - Maps the most frequent words to feature indices and computes word occurrence frequency (sparse) matrix.
  - Reweights word frequencies using Inverse Document Frequency (IDF).
- **Tuning Options**: `max_df` and `min_df` parameters.

## Other Choices for Semantic Clustering
- [Topic Modeling and Semantic Clustering with Spacy](https://fouadroumieh.medium.com/topic-modeling-and-semantic-clustering-with-spacy-960dd4ac3c9a)
  - Note: This isn't covered in class since it's not strictly clustering.
- **Other Algorithms**:
  - Nearest Neighbors
  - Hierarchical Clustering
