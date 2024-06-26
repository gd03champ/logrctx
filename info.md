# My Ideas

- Python based cli application that can pull in logs from loki, process the logs using llm and return reduced logs

- The application gets queries to gets logs from api from command line parameters while calling the application

- If any parameter is not given by user, no errors, the application runs and get's the input from user in runtime

- The result could probably contain some anamolies and analytics data from the reduced logs also preferably

---

# To Use

- Python as main lang
    - later let's migrate to go

- Typer for cli app

- Rich for cli interface

- Loki api to retrieve logs
    - stores to a file

- RapidFuzz - string matching processing before llm (new context)

- Transformer for llm runtime and rag
    - fuzzed logs passed to llm for further reduction and analysis
    - later lets migrate to llama.cpp

- Using RAG, raw logs will be fed to model finally
    - llm ready to answer any question in context to raw logs though rag


# Progress

- Setup sample logs
    - Get log contexts from yatin gmeet (ll)
        - Also get info on how to get alarms pod topic for anothet ticket
    - Setup loki api rtreival system (ll)

- Check Rapidfuzz with sample logs

- Cascade rapidfuzz ouput to phi-3 for analysis
    - Most analysys and further reduction

- rag for raw logs with llm finally
    - llm chat with md

- Interface and cli app struct (ll)


# Doing

- Markdown doesn't seem to work, have to check with custom
- The bottlenect slow down seem to happen in retreival part, check that