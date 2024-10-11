# Data Mining Group 49 Project Proposal: Github Repository Clustering

## Research Question
What clusters and groups of repositories exist on Github? Is it possible to group Github repositories into clusters based on their metadata such as stars, watchers, README files etc. ?

## Introduction
The ability to mine connections and index repositories from a large collection of open source codebases would be helpful for sourcing information that is otherwise difficult to obtain. In programming and software development, engineers depend on open source packages to simplify and improve their efficiency and product(s). Often, there are many packages to choose from for similar usecases or to solve the same problems. It can be cumbersome to research and traverse the documentation and utility of different packages to identify the right ones for the task. We believe it is important to be able to quickly and easily find similar tools in order to evaluate their efficiency, effectiveness, performance, and overall suitibliity for a product. We believe such a goal is acheivable by utilizing clustering techniques on data from repositories in Github. We also have identified such data as a useful asset in the *Large Language Models and Societal Consequences for Artificial Intelligence (1RT730)* where we have been tasked with building an LLM application which would benefit from the relevant context of the mined Github data.

## Data Source
The data for this project will come from the Github API where we will query and collect data around the repositories. This will include all metadata fields associated with each repository as well as the tags and README.md files. We believe an exploration into this can help us reach conclusions about the similarities between repositories and give us an insight on the different fields/topics that are popular and thus have different implementation techniques.

## Approach
Firstly, the data obtained will need to be preprocessed in order to identify the relevant attributes required for our analysis. Since most of the metadata comes from developers setting them up, the possiblity of missing values is high, which needs to be handled as well. We plan to store the data in an indexed table that can eliminate the possibility of duplicate rows.
The group will then implement clustering techniques on the collected Github features in order to analyze the similarities between particular groups of repositories. The hope is that the clustering analysis will enable us to identify networks of similar codebases. We hope that the information obtained by clustering will enable more robust similarity search and retreival for contextualizing a large language model (in our LLM course mentioned above).
