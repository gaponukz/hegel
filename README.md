# hegel: dialectic app

<p align="center" width="100%">
    <img width="350" alt="image" src="https://github.com/user-attachments/assets/0190ff7b-e7b9-414e-ac26-f558109a4c4c">
</p>

The hegel is a discussion platform designed to support structured, dialectical reasoning inspired by Hegel's triadic approach. Users can engage with each other on various topics by creating thesis, antithesis, and synthesis articles. This process encourages users to collaboratively address complex issues, explore diverse perspectives, and work toward refined solutions.

## Key Features

- **Structured Discussion**: Users submit articles with three types:
  - **Thesis**: Presents an original problem or perspective.
  - **Antithesis**: Offers a contrasting viewpoint in response to a thesis.
  - **Synthesis**: Bridges the thesis and antithesis, aiming for a reconciled conclusion.
- **Graph-Based Topics**: Articles are interlinked to form topic graphs, visually depicting the relationships and progression between perspectives.
- **Collaborative Problem Solving**: Encourages users to explore, debate, and synthesize ideas, creating meaningful dialogue and deeper understanding.


## System dependencies

Python 3.11.9

Neo4j 5.10

## Local deployment

1. Install and activate a virtual environment

```bash
python3.11 -m venv venv
. venv/bin/activate
```

2. Install application dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env` and configure it using `.env.example` as an example

4. Run with uvicorn

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
