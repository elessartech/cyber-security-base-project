# Cyber Security Base 2022 Project I

This intentionally made vulnerable app is a part of the [Cyber Security Base course](https://cybersecuritybase.mooc.fi/) by University of Helsinki. The idea is to have an app that contains flaws from the [OWASP list](https://owasp.org/www-project-top-ten/).

## Repository 

Link: https://github.com/IlmastMaksim/cyber-security-base-project

## Installation Instructions

1. Clone the app:

```
    git clone https://github.com/IlmastMaksim/cyber-security-base-project.git
```

2. Install dependencies:
```
    pip install -r requirements.txt
```

3. Run server:
```
    python manage.py runserver
```

4. If needful, apply migrations:
```
    python manage.py makemigrations
    python manage.py migrate
```

## Credentials 

Username: admin

Password: secretsecret

## Flaws

### 1. [Injection]('https://owasp.org/Top10/A03_2021-Injection/)

https://github.com/IlmastMaksim/cyber-security-base-project/blob/main/polls/views.py#L43

Injection is a way of cyber attack, where the attacker tries to inject into the apps database and execute additional malicious commands.This may result in data leaks or destruction. So, for example if Django uses the following syntax to retrieve required data
```
    Poll.objects.get(id=poll_id)
```
it will completely correspond to such sql query 
```
    SELECT ... WHERE id = poll_id;
```
However, the intruders may input something like ```1 UNION DROP DATABASE polls;``` and consequently the end query would look like ```SELECT ... WHERE id = 1 UNION DROP DATABASE polls;``` or similar, so that the whole ```polls``` database is vanished.

The way to prevent the following type of intrusion, would be to take up server-side input sanitization, meaning that everytime the server receives a post request, it validates the provided parameters excluding any possible malicious intervention coming along with the receiving data. Additionally, database usage permissions could be adjusted set in order to minimize the risk of the data amount to be exploited.

### 2. [CSRF]('https://owasp.org/www-community/attacks/csrf)

https://github.com/IlmastMaksim/cyber-security-base-project/blob/main/polls/views.py#L41

CSRF protection is required against Cross Site Request Forgery attacks. These attacks take place when malicious website contains Javascript code that is supposed to damage your website when intruder is logged in with proper credentials or if your web application allows to insert custom code into its url. For example, the attacker can send an email being disquised and present oneself as trusted authority that asks to navigate to a website via link button and pushing it triggers some malicious Javascript code. 

Good approach to mitigate CSRF risks includes using built-in Django protection, double submit cookies, only using POST requests for state changing operations. Particularly for this application, the views module in polls app should have *csrf_protect* decorator instead of *csrf_exempt* above the post request receiver for the PollView.

### 3. [Security Logging and Monitoring Failures]('https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)

https://github.com/IlmastMaksim/cyber-security-base-project/blob/main/polls/views.py#L20

There is no particular direct vulnerability related to the absence of a qualitative logging and monitoring system in the app, however if the app falls under attack or get affected by some outer malicious software, then the logging system would play a similar role to the black box in airplanes. Thus, it would be much easier to detect a threat, be it a botnet or ransomware attack, and see how it has damaged the app in order to properly neutralize the consequences.

For this case, a good option would be to make sure that every request made to the app is logged correctly and intruders have no access to the logs. Additionally, its important to select a powerful logging framework([this one]('https://github.com/Delgan/loguru') seems as a solid candidate).  

### 4. [Security Misconfiguration]('https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)

https://github.com/IlmastMaksim/cyber-security-base-project/blob/main/vulnerablewebsite/settings.py

This topic related errors occur when required security settings are either not implemented or implemented incorrectly. Intruders, relying on these security vulnerabilities, strive to exploit that to organize cyber attacks and data breaches. Security misconfiguration can be presented in the app as an unsecure, predictable password assigned to an administrator user, unpublished urls being unblocked from non-administrative users.

In this application there is an administrative user, which is created by default not following the secure password policy. The users password is secretsecret, so it doesnt contain symbols as numbers, uppercase letters or punctuals, what makes it possible for an intruder to hack such account. Also, the admin panel of this app, which is located under the address http://127.0.0.1:8000/admin is not hidden from the common user traffic, so that it can be scanned and found by intruders. When deploying the application needful to keep in mind that the configuration should be adjusted specifically for the production mode, meaning that such parameters as Debug should be modified to False correspondingly.

### 5. [Insecure Design]('https://owasp.org/Top10/A04_2021-Insecure_Design/)

https://github.com/IlmastMaksim/cyber-security-base-project/blob/main/polls/templates/polls/poll.html

Insecure design is essentially an unreliable approach of organizing the application structure. Reliable design approaches include for an instance the implementation of various measures that would allow to prevent possible intrusion like checks, specific tools and pipelines, intended randomization of various data element attributes. 

In this app, for example, there is a bug that every time a user has sent a vote, the page, even though its showing the highlighted alert, still allows to cast votes infinitely simultaneously not showing results. That is an unpatched flaw that if not handled, could potentially lead to a security breach or a target for a facilitated botnet attack with purpose of winding up votes for a certain poll, which may even result in complete denial of service. Thus, fine option would be to either redirect voter to the main page once voted or leave one on the poll page and reload it completely, so that there is no opportunity of winding up votes. Additionally, a way to fix that would be to obligate users to pass challenge-response test like CAPTCHA in order to detect malicious bots and block the access for such if detected.