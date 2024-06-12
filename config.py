import os

# Determine the path separator based on the operating system
sep = '\\' if os.name == 'nt' else '/'

# Raw data directories
REDDIT_RAW_DATA_DIR = f"data{sep}raw{sep}reddit{sep}reddit_date"
GITHUB_RAW_DATA_DIR = f"data{sep}raw{sep}github"
STACKOVERFLOW_RAW_DATA_DIR = f"data{sep}raw{sep}stack_overflow"
GOOGLE_RAW_DATA_DIR = f"data{sep}raw{sep}google_map"

# Processed data directories
MERGED_DATA_DIR = f"data{sep}intermediate"

# Analysis directories
INTERMEDIATE_ANALYSIS_DIR = f"data{sep}intermediate{sep}analysis"
IMAGE_DIR = f"assets{sep}images"

# Public platform keywords
EXCEL_KEYWORDS_LIST = f"data{sep}inputs{sep}keywords{sep}Gov_keywords.xlsx"
