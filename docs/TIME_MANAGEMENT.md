# Time Management

## Overview

The initial assignment guidelines indicated that the project could be completed over 2–3 days. Based on this, the initial planning included ambitious enhancements such as adding a FastAPI server, implementing user authentication, maintaining history with SQLite, and even deploying the FastAPI server on AWS Fargate. However, due to an error in the assignment instructions, the submission deadline was moved up, requiring submission within 1.5 days.

## Breakdown of Effort

1. **Research and Experimentation (R&D):**  
   - **R&D Focus:**  
     - Began with experimenting using LangChain for multi-agent setups.  
     - Attempted to use OpenAI's API; encountered issues as the API was not accessible with my debit card due to some reason.  
     - Explored alternatives such as Google Cloud's SDK for Gemini.  
     - Faced confusion due to multiple available packages (e.g., Vertex AI) that were not fully compatible with Streamlit.
     - This took the most time during the whole process.
   - **Outcome:**  
     - After several trials, decided to proceed with a Streamlit-based implementation, as it eventually proved adequate for our needs.

2. **Architecture and Feature Planning:**  
   - Planned for additional features (e.g., a FastAPI server, user authentication, and SQLite-based history storage) to create a robust and production-ready system.
   - Intended to deploy the FastAPI server on AWS Fargate.
   - This took around 2 to 3 hours
   - **Outcome:**  
     - Due to the shortened deadline, only the core functionality was completed, with the enhancements noted for future improvements.

3. **Development and Code Refinement:**  
   - **Actual Coding Time:**  
     - The core development and making the code readable and maintainable took approximately 8–10 hours.
   - **Observations:**  
     - With a fully prepared initial setup, the development time could have been reduced.
     - Balancing full-time employment and other responsibilities meant that work was done in smaller increments, totaling 18 hours over the available time.

## Challenges and Reflections

- **R&D Overhead:**  
  A substantial portion of the time was spent on researching different approaches (e.g., LangChain, OpenAI's API, Gemini on Google Cloud, and FastAPI integration). This was necessary to overcome compatibility and cost issues but also contributed to the overall development time.

- **Balancing Responsibilities:**  
  As a full-time employee at another place, the available work time was limited. The project was managed alongside other responsibilities, which further compressed the development schedule.

- **Future Improvements:**  
  If given more time or with an established initial setup, further enhancements—such as a dedicated FastAPI server with user authentication and database-backed history, along with deployment on AWS Fargate—could be implemented to improve scalability, security, and maintainability.
