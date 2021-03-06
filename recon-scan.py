#!/bin/python
# coding: utf-8

import sys
from optparse import OptionParser
# external APIs
from lib.yatedo.yatedoAPI import YatedoAPI
from lib.piplAPI.piplAPI import PiplAPI
from lib.emailFormatAPI.emailFormatAPI import EmailFormatAPI
from lib.haveibeenpwnedAPI.haveibeenpwnedAPI import haveibeenpwnedAPI


VERBOSE_MODE = False


def display_message(s):
    global VERBOSE_MODE
    if VERBOSE_MODE:
        print '[verbose] %s' % s


def main():
    global VERBOSE_MODE
    parser = OptionParser()
    parser.add_option("-c", "--company", dest="company", help="Company you want to gather info", default=None)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose mode")

    (options, args) = parser.parse_args()

    if options.verbose:
        VERBOSE_MODE = True

    if options.company is None:
        parser.print_help()
        sys.exit(-1)

    # get employees
    display_message('Retrieving employees for the company "%s"' % (options.company))
    company = YatedoAPI().get_employees(options.company)
    display_message('%s employees found' % (len(company['employees'])))

    # retrieve info for each employee
    for employee in company['employees']:
        display_message('Retrieving info for user "%s"' % (employee['name']))
        employee['profiles'] = PiplAPI().get_info(employee['name'])
         # displaying all profiles we gathered
        for profile_url in employee['profiles']:
            print 'On: %s' % (profile_url)

    # retrieve emails
    mails = EmailFormatAPI().get(options.company)
    display_message('%s mails found' % (len(mails)))
    for mail in mails:
        display_message('"%s" pwned? %s' % (mail, haveibeenpwnedAPI().is_compromised(mail) != []))

if __name__ == '__main__':
    main()
