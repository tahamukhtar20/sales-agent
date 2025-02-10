# **Experimentation and Findings**

## **Overview**
This document details the various experiments conducted during the development of the multi-agent sales insights system. It covers experiments with different models, prompt engineering techniques, and architectural approaches. The goal was to optimize accuracy, coherence, and efficiency.


## **1. Experimenting with Prompt Engineering**

### **Objective:**
To refine prompt structures to enhance the accuracy, completeness, and coherence of responses.

### **Prompts Tested:**
#### **Baseline Prompt (Single Query Approach)**
> "Analyze the company strategy for {company_url} and summarize it."
**Outcome:** The model provided basic insights but lacked deep analysis.

#### **Step-by-Step CoT Prompt**
> "Let's think step by step. First, analyze public statements about {company_url}. Next, summarize competitor strategies. Then, evaluate leadership insights. Finally, synthesize a report."
**Outcome:** Improved logical flow and depth of responses.

#### **Few-Shot Prompting (Providing Examples)**
> "Here's an example of an analysis: [Example Output]. Now generate a similar insight for {company_url}."
**Outcome:** Helped generate more structured and well-organized insights.

## **2. Agent Architecture**

### **Objective:**
To test different approaches for structuring multi-agent reasoning and coordination.

### **Approaches Tested:**
#### **Basic Parallel Agents (Independent Execution)**
- Each agent (Company Strategy, Competitor Analysis, Leadership Insights, etc.) runs independently.
- **Issue:** Outputs sometimes conflicted or lacked logical connection.

#### **Sequential Agent Chaining (Ordered Execution)**
- Competitor insights were generated **before** company strategy to ensure comparisons.
- **Issue:** Increased latency but produced more coherent insights.

#### **Meta-Reasoning Combiner Agent (Final Layer Analysis)**
- A final "Combiner Agent" reviewed and refined all agent outputs.
- **Best results:** Ensured logical consistency and prevented contradictions.

## **Conclusion & Future Work**
Each experiment contributed to refining the architecture, performance, and user experience of the sales insights system. While the current implementation is effective, future improvements could include:
- **Enhancing inter-agent communication for iterative refinement.**
- **Introducing real-time API search grounding for even better insights. Instead of Gemini's own grounding feature.**
