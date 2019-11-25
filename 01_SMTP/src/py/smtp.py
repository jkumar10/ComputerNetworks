"""/***************************************************************
/* SOURCE FILE - Jainendra Kumar (jaikumar)
/* CREATED: 09/19/2019
/* 
/* This is a code file for Networks Assignment Task 2 
/* The purpose of this code is to develop a simple client that uses
/* the network to talk to IU SMTP mail server. Smtplib library of  
/* python is used to achieve this functionality.
/*
/* TO RUN THE CODE:
/* $python smtp.py <servername> <fromaddress> <toaddress> <message>   
/****************************************************************/"""

#!/usr/bin/env python3
import os
import time
import argparse
import smtplib


# Entry function for sending mail via SMTP.The input arguments allow you to
# contruct a well-formed email message and send it a specific server.
def send_mail(server, faddr, taddr, msg):
   try:
       print(server, faddr, taddr, msg)
       header  = 'From: %s\n' % faddr
       header += 'Subject: %s\n\n' % 'Jainendra Kumar Assignment 01 SMTP Task 2'
       msg = header + msg
       smtpob = smtplib.SMTP(server)
       smtpob.starttls()
       smtpob.sendmail(faddr, taddr, msg)
       print("Mail accepted for delivery")
       smtpob.quit()
   except:
       print("Error: Mail not sent")

# Main to input arguments
# For example $python smtp.py "mailservername" "fromaddress" "toddress" "message" 
def main():
    parser = argparse.ArgumentParser(description="SICE Network SMTP Client")
    parser.add_argument('mail_server', type=str,
                        help='Server hostname or IP')
    parser.add_argument('from_address', type=str,
                        help='My email address')
    parser.add_argument('to_address', type=str,
                        help='Receiver address')
    parser.add_argument('message', type=str,
                        help='Message text to send')

    args = parser.parse_args()

    mail_server=args.mail_server
    from_address=args.from_address
    to_address=args.to_address
    message=args.message

    send_mail(mail_server,from_address,to_address,message)


if __name__ == "__main__":
    main()
