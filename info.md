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


# Blockers solved

- string matching fuzzy algo
    - percentage similarity didn't work as the difference could be other than time
    - went with regular expression sorting - pretty good results
    - have to tweek it according to loki api response logs

- so much time
    - used llama.cpp instead of transformers (but limitted fucntionalities like rag)
    - so migrated to ollama that uses llama.cpp behind the scene and makes up chatgpt like api
    - generation speed fixed

- irrelevant outcomes
    - seems like embedding was done wrong like irrelevant chunks
    - fixed by limitting max and min chunk size

- retreivel of docs from vector store is done by similarity_search
    - this is good for text based search and faster results but
    - but similarity search isn't much efficient on retrieving logs with natural lang
    - elastic search may do the thing but requires an instance

- need for keyword in the query - related to above blocker
    - turns out to be, using only keyword search
    - have to do sematic search

# Doing

- Markdown doesn't seem to work, have to check with custom
- The bottlenect slow down seem to happen in retreival part, check that


