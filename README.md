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

- retrieval is little slow
    - change chroma vector db to FAISS (blazing fast)

- retreivel of docs from vector store is done by similarity_search
    - this is good for text based search and faster results but
    - but similarity search isn't much efficient on retrieving logs with natural lang
    - elastic search may do the thing but requires an instance

- need for keyword in the query - related to above blocker
    - turns out to be, using only keyword search
    - have to do sematic search

- vector db created everytime casuing time
    - caching system created
    - created new cache for every new reduce

- context length problem when connect to aws ollama service (unresolved)
    - works well on local server
    - either decrease context length or scale up ollama server (or both)
        - reduce context length and relevancy by decreasing chunk size and increasing k value
        - increase context length using any summary technology or scalling up server resources

# Doing

- Markdown doesn't seem to work, have to check with custom
- The bottlenect slow down seem to happen in retreival part, check that
    - No, it's in creating vector db (solved by caching)
    - and in starting generation (trying to speedup using mutlithreading)




---

Generating response...

╭─────────────────╮
│  logrctx ai 🧠  │
╰─────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────╮
│ The SSH server log shows multiple failed authentication attempts, including those by    │
│ unauthorized or invalid users such as 'cisco', 'admin', and 'matlab'. These incidents   │
│ suggest a potential brute-force attack on your SSH service. It's also noteworthy that   │
│ there are repeated login failures for the root user from different IP addresses         │
│ ('103.99.0.122', '52.80.34.196', and another with a similar pattern). This could        │
│ indicate an attempt to gain unauthorized access, especially since the root account has  │
│ significant privileges.                                                                 │
│                                                                                         │
│ Here are some anomalies and potential issues based on these logs:                       │
│                                                                                         │
│  1 Repeated failed login attempts from '103.99.0.122' using various ports which is a    │
│    common sign of an attacker trying different combinations to guess the root password  │
│    or exploit known vulnerabilities (Port scanning).                                    │
│  2 Multiple invalid user attempts ('cisco', 'matlab') and failed authentications for    │
│    unfamiliar users such as 'admin'. This could be either an incorrect configuration    │
│    issue leading to false positives, a misconfigured client attempting access, or it    │
│    may indicate unauthorized attempts by intruders trying different usernames.          │
│  3 Multiple invalid user login attempts from the same IP address ('103.99.0.122') are   │
│    concerning and should be investigated further to ensure system security.             │
│                                                                                         │
│ Actions you can take include:                                                           │
│                                                                                         │
│  • Enforce strong password policies, ensuring users have complex passwords that cannot  │
│    be easily guessed or brute-forced.                                                   │
│  • Implement rate limiting on SSH port 22 to prevent automated login attempts and       │
│    potential denial-of-service attacks.                                                 │
│  • Review your SSH configuration for any misconfigurations leading to false positives   │
│    and ensure users with 'root' privileges have restricted access, ideally through the  │
│    use of key-based authentication instead of passwords.                                │
│  • Consider using Fail2ban or a similar tool to automatically block IPs that exhibit    │
│    malicious behavior like repeated failed login attempts.                              │
╰─────────────────────────────────────────────────────────────────────────────────────────╯
