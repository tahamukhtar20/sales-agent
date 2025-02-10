# Sales Agent Prototype Documentation

Project is hosted at: [https://sales-agent-tahamukhtar20.streamlit.app/](https://sales-agent-tahamukhtar20.streamlit.app/)

This repository contains all the documentation for the multi-agent sales insights prototype. The following files provide detailed information on various aspects of the project:

## Running the project

To run this project, you may do it via docker-compose.yml by running
```
docker compose up
```
in the directory of project, and then once all the requirements are installed, visit the link: [http://localhost:8501](http://localhost:8501).

---

If you don't want to run the container, and want to setup uncontainerized, run
```
pip install -r requirements.txt
```

and once installed run
```
streamlit run app.py
```

- [Experimentation and Findings](docs/EXPERIMENTATION.md) – Documents experiments with different models, prompt engineering techniques, and agent architecture.
- [System Design](docs/SYSTEM_DESIGN.md) – Describes the overall system architecture, data flow, and component responsibilities (contains a small architecture diagram).
- [Time Management](docs/TIME_MANAGEMENT.md) – Details the planned versus actual timeline and overall hours spent.
- [Challenges and Solutions](docs/CHALLENGES_AND_SOLUTIONS.md) - Outlines the key challenges encountered during development and the corresponding solutions.

## Optional Enhancements

### Improving Output Results
To enhance the accuracy, relevance, and usefulness of the outputs, the system was designed with a chain-of-thought (CoT) meta-reasoning approach. Future improvements include:
- **Iterative Refinement:** Implementing feedback loops between agents so that outputs can be refined iteratively.
- **Ensemble Approaches:** Combining outputs from multiple specialized models to reduce variance and improve consistency.
- **Better Grounding:** Currently Gemini's own grounding feature is being used, but a better way of grounding would be creating a scrapping module or using something like SerpAPI.

### Alert System
An alert system can be designed to monitor new press releases, job postings, or other relevant content that contains user-selected keywords. A future implementation could include:
- **Scheduled Background Process:** Using a cron job to periodically query news APIs or job board feeds.
- **Login/Signup:** This is a nice feature, but would require a proper authentication system, which isn't very secure in streamlit.
- **Event-Driven Notifications:** Integrating with a message broker to trigger email alerts immediately upon detecting relevant content.
- **User Preferences:** Allowing users to set and update keyword lists via the interface.

### Production Deployment
For production deployment, the following considerations have been outlined:
- **Containerization:** Is already implemented, see docker-compose.yml.
- **Cloud Deployment:** This is hosted as is on streamlit cloud at [https://sales-agent-tahamukhtar20.streamlit.app/](https://sales-agent-tahamukhtar20.streamlit.app/).
- **Security:** Implementing robust authentication (e.g., OAuth2 or JWT).

### Using Different Types of Models for Extended Functionality
To generate additional outputs such as a presentation deck for sales reps or to provide deeper insights from shared documents, the architecture can be extended as follows:
- **Modular Model Usage:** Different models can be assigned to specific tasks. For example, one model can focus on generating the sales insights report while another specialized model can generate a slide deck.
- **Multi-Modal Integration:** If additional documents (or images) are shared, dedicated agents (like the Document Parsing Agent) will process the files and extract relevant information that can be used to create more detailed visual aids.
- **Ensemble and Hybrid Techniques:** A combination of models can be used to verify and refine outputs, ensuring that the final presentation material is coherent, accurate, and visually engaging.
- **Reasoning Models:** Models similar to R1 by deepseek or o1 and o3-mini by openai could be used here for better reasoning.
