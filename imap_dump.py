#!/usr/bin/env python
__author__ = 'daneel'

''' Takes params from command line and dumps inbox into file system
    date format: see 'date --rfc-3339=seconds' format NOTE: IMAP4 does not provide filtering by time!
'''

import imaplib
from imaplib import IMAP4
import getpass
import argparse

ERR_NONE = 0
# Invalid credentials ne12mb85325299wic
# [AUTHENTICATIONFAILED] Invalid credentials (Failure)
# command SEARCH illegal in state AUTH, only allowed in states SELECTED
# SEARCH command error: BAD ['Could not parse command']
ERR_CONN = -1
ERR_ABRT = -2
ERR_OTHR = -10

error_string = {ERR_NONE: "OK",
                ERR_CONN: "Error communicating with server",
                ERR_ABRT: "Connection aborted",
                ERR_OTHR: "Other connection error"}


def manage_errors(errcode, err_obj=''):
    print "Error " + error_string[errcode] + ", " + str(err_obj)
    exit(errcode)


def download_and_save(folder_name, filter='ALL'):
    try:
        # TODO search only for emails since the start_date parameter
        typ, data = gmail.search(None, filter)
        if typ == 'OK':
            for num in data[0].split():
                print "Saving mail"
                typ, data = gmail.fetch(num, '(RFC822)')
                if typ == 'OK':
                    # TODO modify file name
                    f = open('%s/%s.eml' % (args.local_folder, folder_name + num), 'w')
                    print >> f, data[0][1]
    except IMAP4.error as e:
        return ERR_CONN, e
    except IMAP4.abort as e:
        print "Connection aborted"
        return ERR_ABRT, e
    except Exception as e:
        return ERR_OTHR, e

    return ERR_NONE, ""


def open_connection():
    try:
        mailbox = imaplib.IMAP4_SSL(args.host)
        mailbox.login(args.username, getpass.getpass())
    except IMAP4.error as e:
        return ERR_CONN, e
    except IMAP4.abort as e:
        print "Connection aborted"
        return ERR_ABRT, e
    except Exception as e:
        return ERR_OTHR, e
    return mailbox, ''


def close_connection(mailbox):
    try:
        mailbox.close()
        mailbox.logout()
    except:  # no actions anymore
        return

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Dump a IMAP folder into .eml files")
    argparser.add_argument('-s', dest='host', help="IMAP host, like imap.gmail.com", required=True)
    argparser.add_argument('-u', dest='username', help="IMAP username", required=True)
    argparser.add_argument('-r', dest='remote_folder', help="Remote folder to download", default='ALL')
    argparser.add_argument('-l', dest='local_folder', help="Local folder where to save .eml files", default='.')
    argparser.add_argument('-d', dest='date_from', help="Starting date in dd-mm-yyyy hh24:mi:ss format", default='.')
    args = argparser.parse_args()

    gmail, exc = open_connection()
    if gmail < 0:
        manage_errors(gmail, exc)

    if args.remote_folder == 'ALL':
        for folder in [{"name": "Inbox", "folder": "INBOX"},
                       {"name": "Drafts", "folder": "[Gmail]/Drafts"},
                       {"name": "Sent", "folder": "[Gmail]/Sent Mail"},
                       {"name": "Trash", "folder": "[Gmail]/Trash"}]:
            gmail.select(folder['folder'], readonly=1)
            ret, exc = download_and_save(folder['name'], 'ALL')
            if ret < 0:
                manage_errors(ret, exc)
    else:
        gmail.select(args.remote_folder, readonly=1)
        ret, exc = download_and_save(args.remote_folder)
        if ret < 0:
            manage_errors(ret, exc)

    close_connection(gmail)
    # Nothing to check anymore

    exit(0)