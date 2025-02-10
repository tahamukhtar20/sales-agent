# Experimentation and Findings

## Overview
This document details the experiments conducted during the development of the multi-agent sales insights system. The experiments covered prompt engineering, agent architecture, and infrastructure planning. The goal was to optimize accuracy, coherence, and efficiency while also exploring additional features for a production-ready solution.

## 1. Experimenting with Prompt Engineering

### Objective:
To refine prompt structures to enhance the accuracy, completeness, and coherence of responses.

### Prompts Tested:
- **Baseline Prompt (Single Query Approach):**  
  > "Analyze the company strategy for {company_url} and summarize it."  
  *Outcome:* Basic insights were provided but lacked depth.
  
- **Step-by-Step CoT Prompt:**  
  > "Let's think step by step. First, analyze public statements about {company_url}. Next, summarize competitor strategies. Then, evaluate leadership insights. Finally, synthesize a report."  
  *Outcome:* Improved logical flow and deeper analysis.

- **Few-Shot Prompting (Providing Examples):**  
  > "Here's an example of an analysis: [Example Output]. Now generate a similar insight for {company_url}."  
  *Outcome:* Generated more structured and well-organized insights.

## 2. Experimenting with Agent Architecture

### Objective:
To test different approaches for structuring multi-agent reasoning and coordination.

### Approaches Tested:
- **Basic Parallel Agents (Independent Execution):**  
  Each agent (Company Strategy, Competitor Analysis, Leadership Insights, etc.) ran independently.  
  *Issue:* Outputs sometimes conflicted or lacked logical connection.

- **Sequential Agent Chaining (Ordered Execution):**  
  Some agents ran in a specific order (e.g., competitor insights before company strategy) to improve comparisons.  
  *Issue:* Increased latency but produced more coherent insights.

- **Meta-Reasoning Combiner Agent (Final Layer Analysis):**  
  A final "Combiner Agent" reviewed and refined all agent outputs, synthesizing them into a final report.  
  *Best results:* Ensured logical consistency and prevented contradictions.


## 3. Key R&D
- **API and SDK Exploration:**  
  - Began with LangChain for multi-agent setups.
  - Attempted to use OpenAI's API, but it was not available with the current payment method.
  - Explored Google Cloud's Gemini SDK; encountered confusion due to various packages (e.g., Vertex AI) and compatibility issues with Streamlit.
  
- **UI/Server Considerations:**  
  Initially, I considered integrating a FastAPI server with user authentication for added security. After experimenting, I realized that Streamlit's client-server model was sufficient for this prototype, so I proceeded with Streamlit.

## Conclusion & Future Work
The experiments contributed significantly to refining the architecture and overall approach. While the current implementation is effective for the assignment, future improvements could include:
- Integrating a FastAPI server with user authentication and history management using SQLite.
- Deploying the FastAPI server on AWS Fargate for scalable production deployment.
- Enhancing inter-agent communication for iterative refinement.

The learnings from these experiments laid a strong foundation for a scalable, intelligent sales insights tool, and the additional planned features will be explored in future iterations.
