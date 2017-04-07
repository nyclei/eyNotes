## Security Test

Before we mark AEM servers ready in production environment, some preliminary security tests were performed against Homepage served by origin production server.

#### Penetration Test
- Network enumeration and mapping test with `Nmap`
 - scan network data: ip, hostname, tracert, etc
 - scan open ports (80 and 443 only)
 - scan open services
 - scan HTTP methods: OPTIONS TRACE GET HEAD POST
 - scan WebServer, operating system
 - scan ssl data: cert, public key type/bits, sig algorithm,etc  


- Reconnaissance (in homepage)
 - no leaking information of key personnel
 - no email address
 - no software/patch level
 - generic contact us information only


- Basic Vulnerability scanning
 - Production site: Direct DOS attack is prevented by Akamai
 - Checking SSL Certificate Signing Hashing Algorithm
 - Production AEM: Access are granted to valid accounts with corresponding permissions

- AEM checklist before it's ready for production

#### Suggested repairs
- Homepage: fix the embedded external content issue http://media.royalcaribbean.com/pagedown-sep-2013/jquery-1.3.2.min.js
- Homepage: fix the embedded external content issue http://media.royalcaribbean.com/pagedown-sep-2013/cufon-yui.js?1299901221
- Homepage: fix the embedded external content issue http://media.royalcaribbean.com/pagedown-sep-2013/Gotham_Ultra_900.font.js?1302546032
- AEM: Install Hotfix 12190
- AEM: Navigate to Apache Felix OSGi Management Console and change OSGi Web Console username and password
- AEM: Use different account in replication agents, rather than 'admin'
- AEM: Remove CRX development bundles from production Author and publish
- AEM: Disable WebDav
- 
