# Overview

An AI-powered ad creative generator that produces high-quality marketing content, ad ideas, and visuals tailored to your specific needs.


[Website](https://create-ad-images.streamlit.app/)

![UI](https://res.cloudinary.com/dfeirxlea/image/upload/v1731434658/portfolio/afcsewg7ojksnyebybb7.png)

![System process](https://res.cloudinary.com/dfeirxlea/image/upload/v1731435457/vvidnxofizaxhcc9v7kd.png)


## Features

- **AI-Driven Content Creation**: Generate high-quality marketing creatives in minutes.
- **Competitive Analysis**: Get content ideas tailored to your industry and target audience.


## Project Structure

This repository is structured as follows:

- `/src` - Contains the frontend codes


## Local deployment
- Frontend (run on streamlit - http://localhost:8501/)
    ```
    pipenv shell

    streamlit run src/app.py
    ```

- Backend (use fast-api framework - http://localhost:8000/)
    ```
    pipenv shell

    pip install "fastapi[standard]"
    
    fastapi dev main.py
    ```	

## Technical Approach
- Use FastAPI to call APIs
- Use Llama 3.1 8B model via TogetherAI framework.

