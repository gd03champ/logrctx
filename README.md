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






---


# Without flat

Prompt: bring up any anamolies found in the logs
Context mapped successfully.
Retrieved docs 👇
╭─────────────────────────────────────────────────────────────────────────────────────────╮
│ logs/reduced_raw.log                                                                    │
│ Dec 10 07:13:43 LabSZ sshd[24227]: Failed password for root from 5.36.59.76 port 42393  │
│ ssh2                                                                                    │
│                                                                                         │
│ Dec 10 07:13:56 LabSZ sshd[24227]: message repeated 5 times: [ Failed password for root │
│ from 5.36.59.76 port 42393 ssh2]                                                        │
│                                                                                         │
│ Dec 10 07:13:56 LabSZ sshd[24227]: Disconnecting: Too many authentication failures for  │
│ root                                                                                    │
│                                                                                         │
│ Dec 10 08:39:59 LabSZ sshd[24408]: Disconnecting: Too many authentication failures for  │
│ root                                                                                    │
│                                                                                         │
│ Dec 10 07:13:56 LabSZ sshd[24227]: PAM 5 more authentication failures; logname= uid=0   │
│ euid=0 tty=ssh ruser= rhost=5.36.59.76.dynamic-dsl-ip.omantel.net.om  user=root         │
│                                                                                         │
│ Dec 10 07:13:56 LabSZ sshd[24227]: PAM service(sshd) ignoring max retries; 6 > 3        │
│                                                                                         │
│ Dec 10 10:14:13 LabSZ sshd[24833]: PAM service(sshd) ignoring max retries; 6 > 3        │
╰─────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────╮
│ logs/reduced_raw.log                                                                    │
│ Dec 10 08:25:22 LabSZ sshd[24369]: PAM 4 more authentication failures; logname= uid=0   │
│ euid=0 tty=ssh ruser= rhost=5.188.10.180                                                │
│                                                                                         │
│ Dec 10 09:11:41 LabSZ sshd[24437]: PAM 4 more authentication failures; logname= uid=0   │
│ euid=0 tty=ssh ruser= rhost=185.190.58.151                                              │
│                                                                                         │
│ Dec 10 08:25:22 LabSZ sshd[24369]: PAM service(sshd) ignoring max retries; 5 > 3        │
│                                                                                         │
│ Dec 10 09:11:41 LabSZ sshd[24437]: PAM service(sshd) ignoring max retries; 5 > 3        │
│                                                                                         │
│ Dec 10 08:25:28 LabSZ sshd[24371]: Failed password for invalid user admin from          │
│ 5.188.10.180 port 59647 ssh2                                                            │
│                                                                                         │
│ Dec 10 08:25:41 LabSZ sshd[24371]: Failed password for invalid user admin from          │
│ 5.188.10.180 port 59647 ssh2                                                            │
│                                                                                         │
│ Dec 10 08:25:50 LabSZ sshd[24373]: Failed password for invalid user admin from          │
│ 5.188.10.180 port 56345 ssh2                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────╮
│ logs/reduced_raw.log                                                                    │
│ Dec 10 09:11:51 LabSZ sshd[24460]: pam_unix(sshd:auth): authentication failure;         │
│ logname= uid=0 euid=0 tty=ssh ruser= rhost=103.99.0.122  user=sshd                      │
│                                                                                         │
│ Dec 10 11:04:21 LabSZ sshd[25505]: pam_unix(sshd:auth): authentication failure;         │
│ logname= uid=0 euid=0 tty=ssh ruser= rhost=103.99.0.122  user=sshd                      │
│                                                                                         │
│ Dec 10 09:11:52 LabSZ sshd[24460]: Failed password for sshd from 103.99.0.122 port      │
│ 51359 ssh2                                                                              │
│                                                                                         │
│ Dec 10 09:11:55 LabSZ sshd[24462]: Failed password for invalid user admin from          │
│ 103.99.0.122 port 54739 ssh2                                                            │
│                                                                                         │
│ Dec 10 09:11:56 LabSZ sshd[24464]: Invalid user cisco from 103.99.0.122                 │
│                                                                                         │
│ Dec 10 11:04:30 LabSZ sshd[25521]: Invalid user cisco from 103.99.0.122                 │
│                                                                                         │
│ Dec 10 09:11:56 LabSZ sshd[24464]: input_userauth_request: invalid user cisco           │
╰─────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────╮
│ logs/reduced_raw.log                                                                    │
│ Dec 10 08:39:49 LabSZ sshd[24408]: Failed password for root from 106.5.5.195 port 50719 │
│ ssh2                                                                                    │
│                                                                                         │
│ Dec 10 08:39:59 LabSZ sshd[24408]: message repeated 5 times: [ Failed password for root │
│ from 106.5.5.195 port 50719 ssh2]                                                       │
│                                                                                         │
│ Dec 10 08:39:59 LabSZ sshd[24408]: PAM 5 more authentication failures; logname= uid=0   │
│ euid=0 tty=ssh ruser= rhost=106.5.5.195  user=root                                      │
│                                                                                         │
│ Dec 10 08:44:20 LabSZ sshd[24410]: Invalid user matlab from 52.80.34.196                │
│                                                                                         │
│ Dec 10 10:21:01 LabSZ sshd[24841]: Invalid user matlab from 52.80.34.196                │
│                                                                                         │
│ Dec 10 08:44:20 LabSZ sshd[24410]: input_userauth_request: invalid user matlab          │
│                                                                                         │
│ Dec 10 10:21:01 LabSZ sshd[24841]: input_userauth_request: invalid user matlab          │
│                                                                                         │
│ Dec 10 08:44:27 LabSZ sshd[24410]: Failed password for invalid user matlab from         │
│ 52.80.34.196 port 46199 ssh2                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────╮
│ logs/reduced_raw.log                                                                    │
│ Dec 10 11:04:00 LabSZ sshd[25472]: Failed password for root from 103.99.0.122 port      │
│ 63012 ssh2                                                                              │
│                                                                                         │
│ Dec 10 11:04:02 LabSZ sshd[25476]: Failed password for root from 183.62.140.253 port    │
│ 56779 ssh2                                                                              │
│                                                                                         │
│ Dec 10 11:04:04 LabSZ sshd[25478]: Failed password for invalid user anonymous from      │
│ 103.99.0.122 port 63514 ssh2                                                            │
│                                                                                         │
│ Dec 10 11:04:04 LabSZ sshd[25480]: Failed password for root from 183.62.140.253 port    │
│ 57223 ssh2                                                                              │
│                                                                                         │
│ Dec 10 11:04:06 LabSZ sshd[25482]: Failed password for root from 183.62.140.253 port    │
│ 57631 ssh2                                                                              │
│                                                                                         │
│ Dec 10 11:04:08 LabSZ sshd[25487]: Failed password for root from 183.62.140.253 port    │
│ 57916 ssh2                                                                              │
│                                                                                         │
│ Dec 10 11:04:10 LabSZ sshd[25484]: Failed password for invalid user admin from          │
│ 103.99.0.122 port 64031 ssh2                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────╯
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
