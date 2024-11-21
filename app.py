import streamlit as st
import time
import asyncio
import nest_asyncio
from crewai import Crew, Process
import os
from dotenv import load_dotenv
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
import contextlib

# Apply nest_asyncio to handle nested event loops
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Initialize LLM in a function to be called after event loop is established
@st.cache_resource
def initialize_llm():
    try:
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            verbose=True,
            temperature=0.5,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    except Exception as e:
        st.error(f"Error initializing LLM: {str(e)}")
        return None

# Initialize agents with the LLM
def initialize_agents(llm):
    from agents import Agent, tool
    
    industry_researcher = Agent(
        role="Industry Researcher",
        goal="Gather strategic insights about the {topic} and its industry, key products, and market positioning, with a focus on AI/ML opportunities.",
        verbose=False,
        memory=True,
        backstory=("You are a seasoned market researcher with 20+. years of experiance in indepth analysis, research, understanding competiton and findling potential bottlenecks."),
        tools=[tool],
        llm=llm,
        allow_delegation=False
    )

    use_case_generator = Agent(
        role="AI Solutions Architect",
        goal="Analyze industry AI/ML trends to generate 3-5 actionable use cases relevant to {topic} that improve operations, customer experiences, and strategic growth.",
        verbose=False,
        memory=True,
        backstory=("You specialize in generating AI-powered solutions which are pratical, innovative and gives competitive edge over others in the industry. "),
        tools=[tool],
        llm=llm,
        allow_delegation=True
    )

    resource_collector = Agent(
        role="Resource Asset Finder",
        goal="Gather high-quality, relevant datasets for the generated use cases, ensuring they are directly applicable for AI/ML model development.",
        verbose=False,
        memory=True,
        backstory=("""You are an expert at sourcing technical resources and datasets from various platforms. You focus on finding datasets, reports and articles to support the proposed use cases, ensuring {topic} has access to the necessary resources for implementation."""),
        tools=[tool],
        llm=llm,
        allow_delegation=True
    )
    
    return industry_researcher, use_case_generator, resource_collector

def initialize_tasks(agents):
    from tasks import Task, tool
    industry_researcher, use_case_generator, resource_collector = agents
    
    research_task = Task(
        description=("Conduct thorough market research of {topic}."),
        expected_output=('''
            **Competitive Analysis**:
            - Detailed comparison of {topic}'s key products, services, and market positioning against 2-3 major competitors
            - Identification of gaps and weaknesses in {topic}'s current offerings that could be improved through AI/ML.
            
            **Untapped Opportunities**:
            - Pinpoint specific industry segments, customer pain points, or operational challenges that {topic} has not adequately addressed
            - Highlight areas where AI/ML applications could help {topic} differentiate itself and gain a competitive edge
        '''),
        tools=[tool],
        agent=industry_researcher,
        output_file='industry-research.md'
    )

    use_case_generation_task = Task(
        description=("Based on the pain points indentified by the researcher generate 5 AI/ML use cases that could address the identified gaps and opportunities for {topic}."),
        expected_output=('''
            List 5 AI/ML use cases, each with:
            - Objective: Specific and measurable business goal
            - AI Application: Relevant AI/ML techniques and technologies
            - Benefits: Detailed explanation of how the solution will impact operations, customer experience, and strategic positioning
        '''),
        tools=[tool],
        agent=use_case_generator,
        output_file='use-cases.md'
    )

    resource_collection_task = Task(
        description=("Identify high-quality, relevant datasets and technical resources that can support the implementation of the proposed AI/ML use cases for {topic}."),
        expected_output=('''
            - 8-10 clickable links high-quality dataset from sources like Kaggle, HuggingFace, and GitHub that are directly applicable to the generated use cases
            - Detailed metadata for each dataset, including format, size, and feasibility assessment for model training
            - 5-7 clickable links of relevant industry reports, research papers, and articles that provide additional context and technical guidance
        '''),
        tools=[tool],
        agent=resource_collector,
        output_file='links.md'
    )
    
    return research_task, use_case_generation_task, resource_collection_task
    
    return research_task, use_case_generation_task, resource_collection_task

def run_analysis(company_name, llm):
    """Run the multi-agent analysis for the given company"""
    try:
        # Initialize agents and tasks
        agents = initialize_agents(llm)
        tasks = initialize_tasks(agents)
        
        # Create the crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential
        )
        
        # Execute the analysis
        with contextlib.suppress(RuntimeError):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = crew.kickoff(inputs={'topic': company_name})
            return result
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Set page config
st.set_page_config(
    page_title="AI Market Reseacher",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .output-container {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Initialize LLM
    llm = initialize_llm()
    if llm is None:
        st.error("Failed to initialize the AI model. Please check your API key and try again.")
        return

    # Header
    st.title("🤖 AI Market Researcher")
    st.markdown("#### Our agents understand your company's market and offer personalized recommendations for AI/ML opportunities. ")
    
    # Input section
    st.markdown("#### Enter Any Company Name")
    company_name = st.text_input("Company Name :", placeholder="e.g., Tesla")
    
    # Display agent information
    with st.expander("👥 Meet the AI Agents"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🔍 Industry Researcher")
            st.markdown("Specializes in gathering strategic insights about the company's industry and market positioning.")
        
        with col2:
            st.markdown("#### 💡 AI Solutions Architect")
            st.markdown("Generates actionable AI/ML use cases based on industry analysis.")
        
        with col3:
            st.markdown("#### 📊 Resource Asset Finder")
            st.markdown("Sources relevant datasets and technical resources for implementation.")

    # Analysis execution
    if st.button("Start Analysis", type="primary"):
        if not company_name:
            st.warning("Please enter a company name to begin the analysis.")
            return
        
        # Create progress bar and status updates
        progress_bar = st.progress(0)
        status = st.empty()
        
        # Show the analysis is starting
        status.info(f"Starting analysis for {company_name}...")
        progress_bar.progress(10)
        
        # Create tabs for different outputs
        tab1, tab2, tab3 = st.tabs(["Industry Research", "Use Cases", "Resources"])
        
        try:
            # Run the analysis
            with st.spinner("AI agents are working on the analysis..."):
                # Update progress as each agent works
                status.info("Industry Researcher is gathering information...")
                progress_bar.progress(30)
                
                status.info("AI Solutions Architect is generating use cases...")
                progress_bar.progress(60)
                
                status.info("Resource Asset Finder is collecting datasets...")
                progress_bar.progress(90)
                
                # Execute the actual analysis
                result = run_analysis(company_name, llm)
                
                if result:
                    # Update progress bar to completion
                    progress_bar.progress(100)
                    status.success("Analysis completed successfully!")
                    
                    # Display results in tabs
                    with tab1:
                        st.markdown("### Industry Research Results")
                        if os.path.exists('industry-research.md'):
                            with open('industry-research.md', 'r') as f:
                                st.markdown(f.read())
                    
                    with tab2:
                        st.markdown("### AI/ML Use Cases")
                        if os.path.exists('use-cases.md'):
                            with open('use-cases.md', 'r') as f:
                                st.markdown(f.read())
                    
                    with tab3:
                        st.markdown("### Available Resources")
                        if os.path.exists('links.md'):
                            with open('links.md', 'r') as f:
                                st.markdown(f.read())
                else:
                    st.error("Analysis failed to complete. Please try again.")
                    
        except Exception as e:
            status.error(f"An error occurred during analysis: {str(e)}")
            progress_bar.empty()

    # Footer
    st.markdown("---")
    st.markdown("*Powered by CrewAI and Streamlit*")

if __name__ == "__main__":
    main()