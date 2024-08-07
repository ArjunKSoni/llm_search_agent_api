
ChatGroq API
============

This repository contains a FastAPI application that leverages LangChain to initialize various tools and an LLM (Language Learning Model) for handling user inputs. The application is designed to handle multiple types of queries using integrated tools such as SerpAPI, Wikipedia, DuckDuckGo, ArXiv, PubMed, and more.

Table of Contents
-----------------

*   [Getting Started](#getting-started)
*   [Environment Variables](#environment-variables)
*   [Available Endpoints](#available-endpoints)
*   [Running the Application](#running-the-application)
*   [Testing](#testing)
*   [License](#license)

Getting Started
---------------

### Prerequisites

*   Python 3.12

### Installation

1.  Clone the repository:

    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    

2.  Create and activate a virtual environment:

    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    

3.  Install the required packages:

    pip install -r requirements.txt
    

Environment Variables
---------------------

Create a `.env` file in the root directory of the project and add the necessary API keys:

    GROQ_API_KEY=your_groq_api_key
    SERPAPI_API_KEY=your_serpapi_api_key
    

Available Endpoints
-------------------

### POST /search

Endpoint to handle search queries using the initialized agent.

**Request Body:**

    {
      "input": "your query here"
    }
    

**Response:**

    {
      "result": "search result"
    }
    

Running the Application
-----------------------

1.  Ensure you have set up the virtual environment and installed the dependencies as shown above.
2.  Run the FastAPI application:

    uvicorn main:app --reload
    

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

Testing
-------

You can test the API using the base URL: [https://llamachat-ipea.onrender.com/](https://llamachat-ipea.onrender.com/)
