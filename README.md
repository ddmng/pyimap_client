#imap_client

Python imaps client that takes account params from command line and dumps inbox into file system 
date format: see 'date --rfc-3339=seconds' format.

__NOTE: IMAP4 does not provide filtering by time!

Emails are stored in files called:

* Inbox1.eml
* Inbox2.eml
* ...
* Inboxn.eml
* Sent1.eml
* ...

