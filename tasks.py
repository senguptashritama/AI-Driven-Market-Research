from crewai import Task
from tools import tool
from agents import industry_researcher, use_case_generator, resource_collector

# Task 1: Doorstep Delivery Operations Analysis
research_task = Task(
    description=(
        "Research {topic} and its industry. Gather insights on the current industry trends, key product offerings, strategic focus, and a competitor analysis, with a specific focus on AI/ML opportunities."
    ),
    expected_output=('''
        **Industry Overview**: AI/ML trends and challenges in the industry.
        **Company Product Offerings**: Overview of key products and how AI/ML can enhance them.
        **Competitor Analysis**: A detailed comparison of 2-3 competitors and their use of AI/ML technologies.
        **Strategic Gaps**: Identification of strategic areas where AI/ML can provide a competitive advantage.
    '''
    ),
    tools=[tool],
    agent=industry_researcher,
    output_file='industry-research.md'
)


# Task 2: AI Use Case Generation for Delivery Optimization
use_case_generation_task = Task(
    description=("Analyze industry AI/ML trends and generate 3-5 AI/ML use cases that could benefit {topic} in terms of operational efficiency, customer experience, and innovation."
    ),
    expected_output=('''
        List 3-5 AI/ML use cases, each with:
        - Objective: Specific business goal.
        - AI Application: Relevant AI/ML technique.
        - Benefits: How the solution impacts operations and customer experience.
    '''),
    tools=[tool],
    agent=use_case_generator,
    output_file='use-cases.md'
)


# Task 3: Dataset Curation for Delivery Optimization
resource_collection_task = Task(
    description=(
        "Search Kaggle, HuggingFace, and GitHub for datasets that can be applied directly to the generated AI/ML use cases."
    ),
    expected_output=('''
        - 10 high-quality datasets that match the use cases.
        - Links to datasets with metadata and feasibility assessment.
        - 7 relevant industry reports/articles that support AI/ML use case validity.
    '''),
    tools=[tool],
    agent=resource_collector,
    output_file='links.csv'
)
