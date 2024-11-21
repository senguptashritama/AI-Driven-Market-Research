# AI-driven Market Research Multi-Agent System

This project is focused on developing a multi-agent system for AI-driven market research. The system is designed to identify AI/ML opportunities for businesses by automating the market analysis, generating AI/ML use cases, and gathering relevant datasets. Built with Python and utilizing tools like Streamlit, CrewAI, Google Gemini 1.5 (via LangChain), and various other external libraries, this system simplifies and enhances the research process by leveraging machine learning techniques.

## Key Features

- **Industry Analysis**: Investigates a company’s market to identify gaps and AI/ML innovation opportunities.
- **AI/ML Use Case Generation**: Proposes actionable AI/ML use cases tailored to business needs.
- **Resource Gathering**: Identifies datasets and technical resources required to implement AI/ML solutions.
  
## System Architecture

The system operates within a **multi-agent framework** where each agent is responsible for a specific aspect of the market research process. The architecture is managed using **CrewAI’s orchestration**, ensuring each agent performs tasks in the correct order and that the system remains efficient through task sequencing and parallel execution.

### Components

- **Streamlit UI**: An interactive user interface for inputting company details and visualizing research results.
- **Google Generative AI (Gemini 1.5)**: Provides natural language processing capabilities via LangChain to assist with text analysis and insight generation.
- **Agents**: The system employs three specialized agents:
  - **Industry Researcher Agent**: Performs market and competitive analysis.
  - **AI Solutions Architect Agent**: Generates AI/ML use cases based on the analysis.
  - **Resource Asset Finder Agent**: Sources relevant datasets and technical resources.
- **Task Execution**: Each agent is assigned specific tasks, and their results are passed sequentially to the next agent.
- **External Tools**: Libraries like **SerperDevTool** for web scraping and collecting external data, and caching tools like **nest_asyncio** for managing event loops.

### Asynchronous Task Management

The system employs **asynchronous processing** using Python’s `asyncio` library to manage multiple concurrent tasks without blocking execution. This ensures fast, non-blocking API calls and optimal resource use.

## Methodology

### 1. Agent Initialization

Each agent is initialized with clear roles and responsibilities:
- **Industry Researcher**: Gathers comprehensive market data and competitive analysis.
- **AI Solutions Architect**: Suggests AI/ML solutions tailored to business needs.
- **Resource Asset Finder**: Sources datasets and resources to support AI use cases.

The **Google Gemini 1.5 model** is cached and initialized once, ensuring efficient performance and reducing unnecessary API calls.

### 2. Task Flow

The research process is divided into three sequential tasks, each handled by a specific agent:
1. **Industry Research Task**: The Industry Researcher gathers market insights and identifies potential gaps. The results are saved as `industry-research.md`.
2. **Use Case Generation**: The AI Solutions Architect reviews the research and proposes 3-5 AI/ML use cases, saved in a detailed report.
3. **Resource Collection**: The Resource Asset Finder identifies relevant datasets and technical resources (e.g., from Kaggle, GitHub), and compiles them into a `links.csv` file.

### 3. Task Execution Flow

The agents execute their tasks in the following order:
1. The **Industry Researcher Agent** performs market research and generates a report.
2. The **AI Solutions Architect** analyzes the findings and generates AI/ML use cases.
3. The **Resource Asset Finder** gathers datasets and resources needed to implement the use cases.

All outputs are presented to the user via the **Streamlit UI**, allowing for real-time interaction and result visualization.

### 4. Caching & Asynchronous Execution

To improve efficiency, the system uses:
- **Caching** with Streamlit’s `@st.cache_resource` decorator to store intermediate results.
- **Asynchronous Task Execution**: Handled by `nest_asyncio.apply()` to manage nested event loops while making API calls without blocking the execution of other tasks.

## Setup and Installation

To run the project, you’ll need Python 3.7+ and several dependencies. Follow the steps below to get started:

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
