from crewai import Crew, Process
from tasks import research_task, use_case_generation_task, resource_collection_task
from agents import industry_researcher, use_case_generator, resource_collector

# Forming the India-focused crew with the updated agents and tasks
crew = Crew(
    agents=[industry_researcher, use_case_generator, resource_collector],
    tasks=[research_task, use_case_generation_task, resource_collection_task],
    process=Process.sequential,  # Executes tasks in sequence, one after another
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'BigBasket'})
print(result)