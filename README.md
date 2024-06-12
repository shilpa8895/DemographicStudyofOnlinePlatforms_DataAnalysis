#DemographicStudyofOnlinePlatforms_DataAnalysis
Demographic Analysis on scrape data from multiple services across various platforms​  ​

## Overview :earth_americas:

Welcome to the repository which aims to analyze and enhance online engagement with the public and stakeholders through digital channels, primarily focusing on social media platforms. Goal is to provide insightful data-driven strategies to improve communication, increase transparency, and foster public participation.


## Project Structure :file_folder:

```
├── config.py                             # Configuration settings for the project.
├── data                                  # Directory for all data files.
│   ├── final                             # Finalized data files.
│   ├── inputs                            # Input files including keywords and services lists.
│   │   ├── keywords                      # Keywords list for scraping.
│   │   └── services                      # Services list for scraping.
│   ├── intermediate                      # Intermediate data files including analysis results.
│   │   ├── analysis                      # Analysis results from various platforms.
│   │   ├── github                        # Intermediate GitHub data.
│   │   ├── reddit                        # Intermediate Reddit data.
│   │   ├── stackoverflow                 # Intermediate StackOverflow data.
│   ├── raw                               # Raw data files collected from various sources.
│   │   ├── github                        # Raw GitHub data.
│   │   ├── google_map                    # Raw Google Map data.
│   │   ├── reddit                        # Raw Reddit data.
│   │   ├── stack_overflow                # Raw StackOverflow data.
│   │   ├── youtube                       # Raw YouTube data.
├── notebooks                             # Jupyter notebooks for various tasks.
│   ├── exploration                       # Notebooks for exploring data.
│   └── scrape                            # Notebooks for scraping data from various APIs.
│       ├── unused APIs                   # Notebooks for unused APIs.
├── readme.txt                            # Readme file for the project.
├── requirements.txt                      # List of project dependencies.
├── scripts                               # Scripts for various tasks.
│   ├── merging                           # Scripts for merging data from different sources.
│   ├── scraping                          # Scripts for scraping data.
│   └── utils                             # Utility scripts for configuration and other helper functions.
├── setup.py                              # Setup script for the project.
├── tests                                 # Directory for unit and integration tests.
│   ├── integration                       # Integration test scripts.
│   └── unit                              # Unit test scripts.

```

Key Features

+ Data Collection: Scraping data from various platforms such as Reddit, YouTube, GitHub, and StackOverflow.
+ Data Preprocessing: Cleaning and standardizing the collected data.
+ Sentiment Analysis: Analyzing the sentiment of discussions and reviews.
+ Topic Modeling: Identifying key topics in the discussions.
+ Frequeny Modeling: Identifying the frequency in posting.
+ Visualizations: Creating visual representations of the data and analysis results.

<details><summary><h2> Platform Analysis</h2></summary>
<p>

### Reddit
+ Observations: 3,232,264
+ Years: 2009-2024
+ Upvotes per Post: Average - 18,369, Median - 6,070
+ Upvotes per Comment: Average - 16, Median - 2

### YouTube
+ Channels Analyzed: 9 services
+ Number of Videos: 30,474
+ Total Views: 1.53 billion
+ Total Likes: 19.46 million
+ Subscriber Count: 4.26 million

### GitHub
+ Observations: 82
+ Years: 2013-2024
+ Stars per Repository: Average - 3
+ Forks per Repository: Average - 1
+ Open Issues per Repository: Average - 0

### StackOverflow
+ Observations: 1792 questions about 112 Gov services keywords
+ Specific Observations: 596 on Australia Post
+ Average Views per Question: 1572
+ Answered Questions: All questions were at least answered once
+ Noteworthy Question: "How do I validate an Australian Medicare number?"
+ User Engagement: Peaked in 2017, declining due to AI tools like ChatGPT.
</p>
</details>


<details><summary><h2> How to run</h2></summary>
<p>

To get started with this project, clone this repository to your local machine:

```bash
git clone <SSH url>
```

Navigate to the project directory:

```bash
cd <Project name>
```


1. Ensure you have Python installed on your system.
2. Set up your Python environment by installing the required packages. You can use pip for this:

```
pip install -r requirements.txt
```

3. Setup:

Install the required dependencies using pip install -r requirements.txt.
Configure the project settings in config.py.

4. Data Collection:

Run the scraping scripts located in the scripts/scraping directory to collect data from various platforms.
For example in `scripts/scraping`:


5. Data Preprocessing:

Use the preprocessing scripts in the scripts/merging directory to clean and standardize the collected data.

6. Analysis:

Explore the data and perform analysis using the Jupyter notebooks in the notebooks/exploration directory.
7. Reporting:

Generate reports and visualizations based on the analysis results.
</p>
</details>


