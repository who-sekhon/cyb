# CMP-X305 Cyber Security Coursework Portfolio 1

**Student name:** Sukhjeet Singh Sekhon

**Student ID:** [INSERT STUDENT ID]

**Module:** Cyber Security (CMP-X305)

**Submission date:** 31 March 2026

## 1. Introduction

This portfolio documents four practical cyber security labs completed during Weeks 05, 07, 08 and 09. The work covers WordPress assessment with WPScan [2], [3], exploitation of web application weaknesses in OWASP Juice Shop [4]–[6], network discovery and secure administration with Nmap [7], [8] and SSH [9], [10], and vulnerability scanning with Nessus [11]–[14].

The evidence used in this report comes from my own screenshots, the exported Nessus PDF reports [14], and the module worksheets provided for each lab [2], [4], [7], [9], [11]. Representative screenshots are embedded throughout the report, while the full evidence pack remains in the week folders stored alongside this file. In the submission version of the report, each figure is presented with a consistent on-image label panel, a precise caption, and short key-point notes so that the evidence is easy to follow and directly linked to the analysis.

This report is structured to match the coursework brief [1], with each lab section including a clear aim, method, evidence, findings and analysis, and reflection.

This portfolio addresses the module learning outcomes stated in the assessment brief [1] in the following ways:

- **LO1:** identifying vulnerabilities and recommending mitigations
- **LO2:** applying secure remote access and discussing confidentiality, integrity and availability
- **LO3:** evaluating privacy and anonymity risks caused by information leakage and insecure web behaviour

---

## 2. Week 05 - Web Application Security Lab (WPScan)

### 2.1 Aim

The purpose of this lab was to assess a WordPress installation using WPScan [2], [3] and demonstrate how a scanner can reveal themes, plugins, configuration weaknesses and authentication attack surface. This directly relates to privacy and anonymity because version disclosure and exposed directories make targeted attacks easier.

### 2.2 Method

I first verified that the WordPress site and admin area were reachable from Kali Linux. I then prepared the target by managing themes and testing the login and registration pages so that WPScan had a realistic target to assess. After that, I updated WPScan [3] and used it to enumerate installed themes, plugins, configuration backups and password attack options against XML-RPC.

This lab links most directly to LO1 and LO3 because WPScan showed how exposed versions, directories and plugins can make a WordPress site easier to profile and target, while the reflection and mitigation discussion identify practical hardening actions [2], [3].

### 2.3 Evidence

![Figure 1 - WordPress admin dashboard](<Week 5/Screenshot 2026-02-17 185619.png>)

*Figure 1. WordPress administrator dashboard confirming authenticated access to the target site before WPScan testing.*

**Key points shown in Figure 1:**

- The WordPress dashboard loads successfully in the browser.
- Administrative menus confirm that the site is operational and manageable.
- The screenshot establishes the correct live target before enumeration begins.

![Figure 2 - User registration and authentication testing](<Week 5/Screenshot 2026-02-24 123904.png>)

*Figure 2. WPScan account registration page and login access used during scanner setup.*

**Key points shown in Figure 2:**

- The screenshot shows the WPScan account setup page in the browser.
- Login access is visible in the same interface.
- This evidence relates to preparing the scanning tool rather than demonstrating a target-side vulnerability.

![Figure 3 - Theme installation and WPScan update](<Week 5/Screenshot 2026-02-24 132411.png>)

*Figure 3. Theme management in WordPress and WPScan preparation in Kali Linux before enumeration.*

**Key points shown in Figure 3:**

- The WordPress theme configuration is visible in the administration interface.
- The Kali environment is being prepared to run WPScan against the site.
- The screenshot connects target setup with the assessment tool used later in the lab.

![Figure 4 - WPScan enumeration](<Week 5/Screenshot 2026-02-24 134832.png>)

*Figure 4. WPScan enumeration identifying the target URL, `robots.txt`, XML-RPC endpoint and WordPress assets.*

**Key points shown in Figure 4:**

- WPScan has connected to the target successfully.
- The enumeration output lists exposed WordPress resources and endpoints.
- XML-RPC and supporting files are visible to the scanner.
- This is the main evidence that automated reconnaissance was performed in Week 05.

![Figure 5 - Akismet advisory](<Week 5/Screenshot 2026-02-24 151515.png>)

*Figure 5. WPScan output referencing the Akismet plugin path and a historical stored XSS advisory.*

**Key points shown in Figure 5:**

- The plugin path is identified in the WPScan output.
- WPScan associates the plugin with a historical XSS advisory.
- The version could not be fully determined from the captured evidence.
- This makes the result a lead for validation rather than conclusive proof of exploitation.

![Figure 6 - Directory listing exposure](<Week 5/Screenshot 2026-02-24 151649.png>)

*Figure 6. WPScan reporting directory listing on the theme path and completing the WordPress assessment.*

**Key points shown in Figure 6:**

- Directory listing is explicitly reported in the WPScan results.
- Internal content structure is exposed unnecessarily through the theme path.
- The scan completed successfully, so this finding forms part of the captured evidence set.
- Disabling directory indexing is the most direct mitigation supported by this screenshot.

### 2.4 Findings and analysis

| Finding | Evidence | Security impact | Assessment |
|---|---|---|---|
| Theme metadata exposed | WPScan detected the Blockskit Base theme and version `1.1.7`. | Version disclosure makes it easier to match the site to known vulnerabilities. | This is reconnaissance rather than compromise, but it reduces attacker uncertainty. |
| Directory listing enabled | WPScan reported directory listing on the theme path. | File names and structure can be browsed and used to support later attacks. | This should be remediated by disabling directory indexes. |
| Potential vulnerable plugin history | WPScan referenced `Akismet 2.5.0-3.1.4 - Unauthenticated Stored Cross-Site Scripting (XSS)` but did not confirm the installed version. | If the vulnerable version were present, stored XSS could affect integrity and trust. | This should be treated as a lead for manual validation, not an automatically confirmed exploit. |
| Patch lag visible | The WordPress UI showed that version `6.9.1` was available. | Delayed updates increase exposure to known weaknesses. | Regular patching is a basic hardening requirement. |
| XML-RPC password attack unsuccessful | WPScan attempted a password attack against XML-RPC but returned no valid passwords. | The test did not compromise the account in the captured run. | Even so, XML-RPC remains an attractive attack surface and should be restricted if not needed. |

The strongest confirmed weakness in the captured evidence was the directory listing exposure shown in Figure 6, because it clearly leaked information without any real business need. Figures 4-6 also showed an important limitation of automated scanning: tools such as WPScan [3] can identify both confirmed weaknesses and plausible leads that still require human judgment before they can be reported as genuine vulnerabilities.

From a privacy and anonymity perspective, the combination of theme disclosure, directory indexing and plugin identification reduced the amount of uncertainty facing an attacker and therefore made the site easier to profile. From a mitigation perspective, the same evidence supported practical defensive steps such as removing unnecessary content exposure, restricting XML-RPC where it is not required, and maintaining WordPress patching discipline [2], [3]. This strengthens the LO1 and LO3 connection because the lab showed both how information leakage supports targeting and how straightforward hardening can reduce that risk.

### 2.5 Reflection

This lab showed that web application assessment is not only about running a scanner but also about interpreting its output critically. WPScan [3] was effective at gathering reconnaissance data quickly, but understanding whether a result was a genuine vulnerability or just an indicator was equally important. If I were hardening this system, I would disable directory indexing, remove unused themes and plugins, patch WordPress promptly, enforce stronger passwords and restrict XML-RPC.

---

## 3. Week 07 - OWASP Juice Shop Lab

### 3.1 Aim

The Juice Shop lab, based on the coursework guide and OWASP Juice Shop resources [4]–[6], focused on exploiting deliberately vulnerable web application behaviour. Instead of passive scanning, this lab required direct interaction with the application in order to complete multiple challenges and understand how poor input validation, weak authentication and insecure business logic can be abused.

This lab links directly to LO1, LO2 and LO3 because the exploited weaknesses affected application trust, session safety and user privacy in a live web environment [4]–[6].

### 3.2 Method

Using the Juice Shop environment and the supporting lab resources [4]–[6], I interacted with the application's login, search, chatbot, basket and content pages to attempt low-difficulty challenges. I recorded the in-application completion banners shown below so that each result was evidenced within the platform itself rather than described only in narrative form.

### 3.3 Evidence

The screenshots below document ten solved one-star challenges and link each activity to the specific weakness it demonstrates:

| Challenge | Difficulty | Technique / weakness demonstrated | Security lesson |
|---|---|---|---|
| Login Admin | 1 star | Authentication abuse and access to the administrator account | Administrative accounts require strong protection and monitoring. |
| Bully Chatbot | 1 star | Abusing chatbot logic to obtain a coupon | Business logic flaws can be as serious as coding bugs. |
| Outdated Allowlist | 1 star | Redirecting to an outdated trusted cryptocurrency address | Stale allowlists create integrity risk. |
| Bonus Payload | 1 star | DOM XSS using a richer iframe payload in the search feature | Unsanitised input can result in active content execution. |
| DOM XSS | 1 star | Injecting `<iframe src="javascript:alert('xss')">` into search | Client-side input handling can undermine integrity and confidentiality. |
| Confidential Document | 1 star | Accessing a confidential file or document that should not have been openly reachable | Sensitive files must be protected by proper access control and data handling. |
| Privacy Policy | 1 star | Discovering and visiting a public policy page | Small information disclosures support reconnaissance. |
| Score Board | 1 star | Discovering the hidden score board page through direct browsing | Security through obscurity is not an effective control. |
| Mass Dispel | 1 star | Closing multiple challenge banners in one action | Weak state management creates unexpected behaviour. |
| Error Handling | 1 star | Triggering an error that was not handled cleanly | Poor exception handling helps attackers understand an application. |

The solved-challenges overview submitted with the Week 07 evidence also confirmed completion of the `Confidential Document` task. That mattered because it showed access to content that should have remained restricted, strengthening the confidentiality and privacy dimension of this lab even though the original local screenshot folder did not contain a separate full-page capture of that document view.

![Figure 7 - Login Admin](<week 7/Screenshot 2026-03-10 134802.png>)

*Figure 7. OWASP Juice Shop administrator login challenge completed, confirming successful access to an administrative account.*

**Key points shown in Figure 7:**

- The challenge completion banner confirms that the task was solved.
- The evidence indicates successful abuse of authentication or access control.
- Administrative access would expose privileged functions and sensitive data.

![Figure 8 - Bully Chatbot](<week 7/Screenshot 2026-03-10 135442.png>)

*Figure 8. Bully Chatbot challenge completed by manipulating the support bot into disclosing a coupon.*

**Key points shown in Figure 8:**

- The completion banner confirms that the chatbot interaction succeeded.
- The result comes from abusing application logic rather than code execution.
- This demonstrates that workflow weaknesses can still create real business impact.

![Figure 9 - Outdated Allowlist](<week 7/Screenshot 2026-03-10 141507.png>)

*Figure 9. Outdated allowlist challenge completed by following a deprecated but still trusted destination.*

**Key points shown in Figure 9:**

- The completion banner confirms that the outdated allowlist condition was triggered.
- Trust in an obsolete destination creates an integrity risk.
- The screenshot shows how weak configuration governance can enable misuse without exploiting memory or code directly.

![Figure 10 - Bonus Payload](<week 7/Screenshot 2026-03-03 150443.png>)

*Figure 10. Bonus Payload challenge solved using an advanced DOM XSS payload in the Juice Shop search feature.*

**Key points shown in Figure 10:**

- The challenge completion banner verifies that the richer payload worked.
- The search feature accepted attacker-controlled input.
- Successful execution points to inadequate client-side validation or sanitisation.

![Figure 11 - DOM XSS](<week 7/Screenshot 2026-03-03 150857.png>)

*Figure 11. DOM XSS payload executed in the Juice Shop search field, triggering a browser alert.*

**Key points shown in Figure 11:**

- The search field contains the injected iframe payload.
- The alert box confirms that the script executed in the browser context.
- This is direct evidence of DOM-based XSS rather than a failed attempt.
- Such execution could be abused for session theft or page manipulation.

![Figure 12 - Privacy Policy](<week 7/Screenshot 2026-03-03 151542.png>)

*Figure 12. Privacy Policy challenge completed by locating and visiting a public policy page within Juice Shop.*

**Key points shown in Figure 12:**

- The completion banner shows that the page was discovered successfully.
- The task demonstrates how minor information disclosure supports site mapping.
- Even low-impact findings can contribute to wider privacy-related reconnaissance.

![Figure 13 - Mass Dispel](<week 7/Screenshot 2026-03-03 151908.png>)

*Figure 13. Mass Dispel challenge completed by clearing multiple challenge notifications in one action.*

**Key points shown in Figure 13:**

- The screenshot confirms that multiple notifications were dismissed together.
- The behaviour reflects weak state management inside the application.
- Unexpected state changes can reveal assumptions that attackers may exploit.

![Figure 14 - Error Handling](<week 7/Screenshot 2026-03-03 152733.png>)

*Figure 14. Error Handling challenge completed after provoking an application error that was not managed safely.*

**Key points shown in Figure 14:**

- The completion banner confirms that the error-handling weakness was triggered.
- The challenge shows that application responses can leak useful behavioural clues.
- Poorly handled failures can aid reconnaissance and later exploit development.

![Figure 15 - Score Board](<week 7/Screenshot 2026-03-03 152952.png>)

*Figure 15. Hidden Score Board page within OWASP Juice Shop after successful discovery of the `/#/score-board` route.*

**Key points shown in Figure 15:**

- The browser address shows the hidden `/#/score-board` path.
- The score progress panel confirms that the hidden page was reached successfully.
- Discoverable hidden pages support reconnaissance and show why obscurity alone is not a reliable defence.

### 3.4 Findings and analysis

The most technically significant part of this lab was the XSS work. Figures 10 and 11 demonstrated that unsanitised client-side input could reach the DOM and execute attacker-controlled content in OWASP Juice Shop [5], [6]. In a real application, that could lead to session theft, phishing or unauthorised actions performed in the victim's browser.

The other challenges showed that not all serious security problems come from classic code injection. Figure 7 highlighted weak authentication controls, Figure 8 showed business logic abuse, Figure 9 demonstrated the effect of stale trust decisions, Figure 14 reinforced the value of clean defensive failure, and Figure 15 showed how hidden content can still be discovered through direct browsing. The solved-challenges overview also confirmed the Confidential Document task as an example of confidentiality failure. Even apparently simple tasks such as the Privacy Policy challenge in Figure 12 reflected a real-world truth: attackers often start by collecting small pieces of information.

These XSS, authentication, content-discovery and business logic issues link directly to confidentiality, integrity and privacy because they can expose session or personal data, alter trusted page behaviour, reveal hidden resources, and allow unauthorised access or manipulated workflows that undermine user trust. In real systems, the combination shown in Figures 7-11 and Figure 15, together with the Confidential Document challenge recorded in the solved-challenges overview, could lead to direct account abuse, unauthorised content manipulation and privacy breaches affecting both customers and administrators.

### 3.5 Reflection

This lab improved my understanding of how web vulnerabilities behave in practice. Instead of reading about XSS or authentication weaknesses in theory, I had to craft inputs, observe the application's responses and recognise successful exploitation. In a real system, the main mitigations would include secure authentication controls, strong input validation and output encoding, better business logic checks, protection of sensitive documents, and safer error handling [5], [6].

---

## 4. Week 08 - Vulnerability Assessment Lab (Nmap and SSH)

### 4.1 Aim

Week 08 combined reconnaissance and defence using Nmap [7], [8] and SSH [9], [10]. This lab links directly to LO1 and LO2 because Nmap identified services that required protection and SSH demonstrated how confidentiality, integrity and availability can be preserved during remote administration.

### 4.2 Method

I first identified the target addressing with `ip a`, then used Nmap to perform host discovery and service enumeration across the lab network. After identifying the exposed SSH services, I used SSH to demonstrate password-based login, public-key deployment, local port forwarding and further session-control options [7]–[10].

### 4.3 Evidence

#### 4.3.1 Nmap evidence

![Figure 16 - IP configuration on WordPress host](<Week 8/Screenshot 2026-03-17 125018.png>)

*Figure 16. IP configuration output identifying the WordPress host address before network scanning.*

**Key points shown in Figure 16:**

- The host address `192.168.123.30` is visible in the configuration output.
- The screenshot confirms the intended target for the later Nmap activity.
- Establishing the correct address helps ensure scan results are interpreted accurately.

![Figure 17 - Host discovery and service enumeration](<Week 8/Screenshot 2026-03-17 133136.png>)

*Figure 17. Nmap host discovery identifying live systems and exposed services on the lab subnet.*

**Key points shown in Figure 17:**

- Nmap identifies multiple live hosts on the subnet.
- The output lists the principal reachable services on discovered systems.
- The screenshot demonstrates how quickly an attacker or defender can map the environment.

![Figure 18 - Service detection on WordPress host](<Week 8/Screenshot 2026-03-17 141817.png>)

*Figure 18. Nmap service detection on the WordPress host identifying exposed SSH, HTTP and MySQL services.*

**Key points shown in Figure 18:**

- The scan output confirms SSH, HTTP and MySQL are open on `192.168.123.30`.
- Service and version details increase the value of reconnaissance.
- Exposed database access expands the attack surface beyond the web server.

![Figure 19 - TCP connect and SYN scan comparison](<Week 8/Screenshot 2026-03-17 142444.png>)

*Figure 19. Comparison of Nmap TCP connect and SYN scan results for `192.168.123.1`.*

**Key points shown in Figure 19:**

- Both scan types identify SSH and NRPE on the target host.
- The evidence shows comparable findings from two different techniques.
- The screenshot also illustrates the privilege requirement and operational difference of SYN scanning.

| Target | Observed services | Interpretation | Risk note |
|---|---|---|---|
| `192.168.123.1` | `22/tcp ssh`, `5666/tcp nrpe` | Remote administration and monitoring services were exposed. | NRPE should only be reachable by trusted management hosts. |
| `192.168.123.30` | `22/tcp ssh`, `80/tcp http`, `3306/tcp mysql` | The host provided web, database and administration services. | Exposed database services increase the attack surface. |
| `192.168.123.0/24` | Three live hosts discovered | Basic host discovery successfully mapped the active lab. | Reconnaissance is fast and valuable to attackers. |

#### 4.3.2 SSH evidence

![Figure 20 - Password-based SSH login](<Week 8/Screenshot 2026-03-19 155132.png>)

*Figure 20. Password-based SSH connection to `student@192.168.123.1` after host key verification.*

**Key points shown in Figure 20:**

- The host key check is shown before the session is trusted.
- The user successfully establishes an encrypted remote session.
- This evidences secure administration over SSH rather than plaintext remote access.

![Figure 21 - SSH key deployment with ssh-copy-id](<Week 8/Screenshot 2026-03-19 163337.png>)

*Figure 21. Public-key deployment to `192.168.123.30` using `ssh-copy-id`.*

**Key points shown in Figure 21:**

- The command installs a public key on the remote host.
- The screenshot shows a stronger administrative method than password-only login.
- This supports good practice for secure remote access.

![Figure 22 - SSH local port forwarding](<Week 8/Screenshot 2026-03-19 174440.png>)

*Figure 22. SSH local port forwarding command protecting access to the internal web service.*

**Key points shown in Figure 22:**

- The `ssh -L` command forwards local port `8081` to the remote web service.
- The technique allows access without exposing the internal service directly.
- The screenshot demonstrates a practical confidentiality-preserving administration method.

![Figure 23 - SSH session control](<Week 8/Screenshot 2026-03-19 174902.png>)

*Figure 23. SSH shared-connection control options used after establishing the remote administrative session.*

**Key points shown in Figure 23:**

- The screenshot shows further SSH command-line management after the main session was established.
- Shared-connection control options are visible in the terminal output.
- This still supports the Week 08 focus on secure remote administration over protected channels.

### 4.4 Findings and analysis

The combination of Nmap [8] and SSH [10] made the security lesson especially clear. Figures 17-19 showed what was reachable, while Figures 20-23 showed a secure way to interact with those systems once the service had been identified. The WordPress host exposing MySQL alongside HTTP and SSH would be a concern in a production network unless it was properly segmented.

From a confidentiality, integrity and availability perspective, SSH contributed directly to secure operations. Encryption protected confidentiality, host key verification supported integrity by helping prevent man-in-the-middle attacks, and tunnelling plus controlled SSH administration supported availability of management tasks without needing to expose more services than necessary. This strengthens the LO2 link because the lab moved beyond simple connectivity and demonstrated secure administration in practice.

The lab also reinforced LO1 because reconnaissance results such as those in Figure 18 identified services that would require hardening, restriction or segmentation in a real environment. Week 08 therefore linked technical discovery to secure administration rather than treating them as separate tasks.

### 4.5 Reflection

The most important lesson from this lab was that security tools work best in sequence. Reconnaissance identifies the surface area, and secure administration controls how that surface is managed. If I were improving this environment, I would restrict MySQL and NRPE to trusted systems only, prefer key-based authentication over passwords wherever possible and hide management workflows behind tunnels or firewall policy rather than exposing them broadly.

---

## 5. Week 09 - Vulnerability Scanning and Mitigation Lab (Nessus)

### 5.1 Aim

The final lab focused on formal vulnerability scanning with Nessus [11]–[13]. The task involved installing or configuring the scanner, accessing the web interface, creating scans, reviewing findings and exporting reports. This lab moved beyond ad hoc testing into a more structured vulnerability management workflow.

This lab links most directly to LO1 and LO2 because Nessus identified weaknesses that required mitigation and highlighted an SSH issue affecting integrity on one of the scanned hosts [12]–[14].

### 5.2 Method

I used the Nessus web interface at `https://localhost:8834` to configure the scanner, create two scans, run them against the Ubuntu and WordPress hosts, review the vulnerability results, and export both reports for later analysis [11]–[13].

### 5.3 Evidence

![Figure 24 - Nessus login page](<Week 9/Screenshot 2026-03-19 184239.png>)

*Figure 24. Nessus web interface login page confirming local access to the scanner at `https://localhost:8834`.*

**Key points shown in Figure 24:**

- The Nessus service is reachable through its web interface.
- The address confirms that the scanner is running locally in the lab environment.
- This establishes the platform used for the later scan evidence.

![Figure 25 - Nessus dashboard after setup](<Week 9/Screenshot 2026-03-19 191214.png>)

*Figure 25. Nessus dashboard during initial setup, showing the plugin compilation notice and scan creation option.*

**Key points shown in Figure 25:**

- The dashboard shows the scanner interface after installation.
- The plugin compilation notice is visible during the setup stage.
- The screenshot also shows where a new scan can be created once setup is complete.

![Figure 26 - Two scans created](<Week 9/Screenshot 2026-03-19 192649.png>)

*Figure 26. Nessus scan list showing separate jobs for the WordPress and Ubuntu targets.*

**Key points shown in Figure 26:**

- Two distinct scan jobs are configured.
- The jobs correspond to both required lab assets.
- This makes the later comparison between hosts traceable and auditable.

![Figure 27 - Ubuntu scan results](<Week 9/Screenshot 2026-03-19 192844.png>)

*Figure 27. Nessus results for the Ubuntu host, dominated by informational findings with one low-severity issue.*

**Key points shown in Figure 27:**

- The severity breakdown is visible within the scan results.
- Informational findings dominate the Ubuntu assessment.
- One low-severity issue is present, with no critical, high or medium findings shown.
- The authentication column records `Fail`, confirming that the captured scan was unauthenticated.

![Figure 28 - Completed scan list](<Week 9/Screenshot 2026-03-19 193758.png>)

*Figure 28. Nessus scan list confirming that both assessments completed successfully.*

**Key points shown in Figure 28:**

- Both scan jobs show completed status.
- Completion supports the reliability of the comparative analysis.
- The screenshot confirms that the evidence is based on finished scans rather than partial results.

![Figure 29 - Exported reports stored](<Week 9/Screenshot 2026-03-19 193806.png>)

*Figure 29. Exported Nessus PDF reports stored as evidence for later review and comparison.*

**Key points shown in Figure 29:**

- Both PDF exports are visible in the file listing.
- The reports preserve the findings outside the live Nessus interface.
- This supports auditability and later analysis in the coursework report.

### 5.4 Findings and analysis

| Target | Evidence source | Severity summary | Most important finding |
|---|---|---|---|
| Ubuntu host `192.168.123.1` | `ubunto_rpb70j.pdf` | 0 Critical, 0 High, 0 Medium, 1 Low, 24 Info | `ICMP Timestamp Request Remote Date Disclosure` |
| WordPress host `192.168.123.30` | `wordpress_9dsnz3.pdf` | 0 Critical, 0 High, 1 Medium, 1 Low, 32 Info | `SSH Terrapin Prefix Truncation Weakness (CVE-2023-48795)` |

![Figure 30 - Week 9 Nessus severity comparison graph](<Week 9/week9_nessus_severity_chart.png>)

*Figure 30. Severity comparison graph generated from the exported Nessus PDF reports for the Ubuntu and WordPress hosts.*

**Key points shown in Figure 30:**

- The graph compares severity counts across both hosts in one view.
- Informational findings dominate both scans.
- Only the WordPress host shows a medium-severity issue.
- The visual summary supports prioritisation more quickly than raw tables alone.

The graph in Figure 30 provides a clearer comparison of the two exported scans [14]. It shows that both hosts were dominated by informational findings, but only the WordPress host contained a medium-severity issue. This visual comparison strengthens the Week 09 analysis because it makes the difference in risk profile immediately visible rather than leaving it only in table form.

### 5.5 Analysis

The Ubuntu scan, based on the exported Nessus report [14], was relatively clean in severity terms. It produced mainly informational findings, with the only low-severity issue being ICMP timestamp disclosure. That means the host did not show obvious severe remotely visible weaknesses in the captured assessment, although the informational findings still revealed useful platform detail to an attacker.

The WordPress host produced the more important result. Nessus [12], [13] reported `SSH Terrapin Prefix Truncation Weakness (CVE-2023-48795)` as a medium-severity issue affecting the SSH service in the exported report [14]. This matters because it can weaken integrity protections during a man-in-the-middle scenario when certain algorithms are enabled. The host also returned the same ICMP timestamp disclosure seen on Ubuntu.

| Finding | Affected host | Why it matters | Recommended mitigation |
|---|---|---|---|
| SSH Terrapin Prefix Truncation Weakness (CVE-2023-48795) | `192.168.123.30` | The SSH service may be vulnerable to a downgrade of integrity protections in a man-in-the-middle scenario. | Apply OpenSSH vendor updates with strict key exchange countermeasures or disable affected algorithms where appropriate. |
| ICMP Timestamp Request Remote Date Disclosure | `192.168.123.1` and `192.168.123.30` | Accurate time information is revealed to unauthenticated remote probes. | Filter ICMP timestamp request and reply types if not operationally required. |
| Large number of informational findings | Both hosts | Informational results do not always indicate exploitability, but they show how much platform detail is visible. | Reduce unnecessary exposure, keep systems patched and use credentialed scans for higher confidence. |

One particularly useful detail from the screenshots was that Figure 27 showed authentication as failed, which meant the assessment was effectively remote and unauthenticated. That was still useful, but it also meant a follow-up credentialed Nessus scan [13] would likely produce deeper and more accurate results. This limitation did not invalidate the reported findings; instead, it defined the scope of what the scan could confidently claim.

This also strengthens the LO1 and LO2 link for Week 09, because the lab moved from raw detection to practical prioritisation and mitigation planning while still recognising how scan configuration affects confidence in the results.

### 5.5 Reflection

This lab showed how vulnerability management differs from one-off testing. Running a scan is only the first step. The more valuable part is interpreting the output, prioritising the findings and converting them into mitigation actions. Nessus [12], [13] was especially useful because it turned the technical observations into a reportable format, which is important in professional security work.

---

## 6. Overall Reflection and Conclusion

Across the four labs, I used scanning, exploitation and secure administration techniques to examine security from different angles in a way that aligns closely with the coursework brief [1]. Week 05 showed how a WordPress site can leak operational detail through enumeration. Week 07 demonstrated how application flaws can be abused directly. Week 08 connected network reconnaissance with secure remote access, and Week 09 formalised the process through structured vulnerability scanning and reporting.

The strongest overall lesson was that security work requires both technical skill and critical judgment. Tools can identify possible weaknesses, but the analyst still has to decide what those results mean, how severe they really are and what the most suitable mitigation should be. This portfolio helped develop that combination of practical and analytical thinking.

---

## 7. AI Use Statement

I used ChatGPT [15] as an editorial support tool to help organise my existing lab evidence into a coherent report, refine figure captions and key-point summaries, improve grammar and consistency, and standardise IEEE-style citations and references. The screenshots, commands, scan outputs, exported reports, tables and technical findings remained grounded in my own lab work and evidence. AI was not used to fabricate evidence, invent vulnerabilities, or generate unsupported claims.

---

## 8. References

[1] University of Roehampton, "Assessment brief CMP-X305 portfolio," module handout, Mar. 2026.

[2] University of Roehampton, "Portfolio lab on WPScan for penetration testing of a WordPress site," lab sheet, Week 05, 2026.

[3] WPScan Team, "WPScan WordPress Security Scanner," WPScan. [Online]. Available: https://wpscan.com/. [Accessed: Mar. 24, 2026].

[4] University of Roehampton, "BSC Juice-Shop Lab," lab sheet, Week 07, 2026.

[5] OWASP Foundation, "OWASP Juice Shop," OWASP. [Online]. Available: https://owasp.org/www-project-juice-shop/. [Accessed: Mar. 24, 2026].

[6] OWASP Foundation, "Pwning OWASP Juice Shop," OWASP. [Online]. Available: https://pwning.owasp-juice.shop/. [Accessed: Mar. 24, 2026].

[7] University of Roehampton, "An Introduction to Nmap," lab sheet, Week 08, 2026.

[8] Nmap Project, "Nmap Reference Guide," Nmap. [Online]. Available: https://nmap.org/book/man.html. [Accessed: Mar. 24, 2026].

[9] University of Roehampton, "Introduction to SSH (Secure Shell)," lab sheet, Week 08, 2026.

[10] OpenSSH, "Manual Pages," OpenSSH. [Online]. Available: https://www.openssh.com/manual.html. [Accessed: Mar. 24, 2026].

[11] University of Roehampton, "Vulnerability Scanning Using Nessus Lab," lab sheet, Week 09, 2026.

[12] Tenable, "Nessus," Tenable. [Online]. Available: https://www.tenable.com/products/nessus. [Accessed: Mar. 24, 2026].

[13] Tenable, "Nessus Documentation," Tenable Documentation. [Online]. Available: https://docs.tenable.com/nessus/. [Accessed: Mar. 24, 2026].

[14] Tenable Nessus, "ubunto_rpb70j" and "wordpress_9dsnz3," exported vulnerability scan reports, Mar. 19, 2026.

[15] OpenAI, "ChatGPT," OpenAI. [Online]. Available: https://chatgpt.com/. [Accessed: Mar. 24, 2026].
