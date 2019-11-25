/***************************************************************
/* SOURCE FILE - Jainendra Kumar (jaikumar)
/* CREATED: 09/19/2019
/* 
/* This is a code file for Networks Assignment Task 3 
/* This code demonstrates the functionality of C's getaddrinfo()
/* to resolve the mail server argument, printing the IPs 
/* using inet_ntoa() and using socket() to read 255 bytes of data.
/*
/* HOW TO RUN THIS CODE:
/* $make
/* $./smtp-socket <mail-server-name>
/* e.g. $./smtp-socket mail-relay.iu.edu   
/****************************************************************/
 
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <string.h>
#include <unistd.h>

struct addrinfo hints, *infoptr, *i;
struct sockaddr_in *ipv4;
int sockfd,b;
char readBuff[256];

int main(int argc, char **argv)
{
if (argc < 1) 
{
 fprintf(stderr,"Enter server name\n",argv[0]);
 exit(1);
}     
 char *server = argv[1];
 memset(&hints,0,sizeof hints);       
 hints.ai_family = AF_UNSPEC;
 hints.ai_socktype = SOCK_STREAM;

 /*Use getaddrinfo() to resolve the server argument in the client. 
 Making sure to provide hints and the service (port number).*/
 int result = getaddrinfo(server, "25", &hints, &infoptr);

 /*Printing the IP address(es) of the server using inet_ntoa(), 
 passing in the expected sockaddr_in struct from the results 
 of the getaddrinfo() call.*/ 
 printf("IP addresses of mail server are:\n");
 for(i=infoptr; i!=NULL; i=i->ai_next)
 {
  ipv4 = (struct sockaddr_in *)i->ai_addr;
  printf("\n");
  printf(inet_ntoa( ipv4->sin_addr));
  printf("\n");
 }	

 /*Use the resulting list of addrinfo structs to create a socket, 
 using the socket() method. 
 Attempting to connect() to the created socket. 
 Performing appropriate error checking here.*/
 sockfd = socket(AF_INET,SOCK_STREAM,0);
 int con = connect(sockfd,infoptr->ai_addr,infoptr->ai_addrlen);
 if(con==-1)
 {
  printf("Error connecting");
  exit(1);
 }

 /*Reading 255 bytes from a successfully connected socket and 
 printing this buffer to display the mail server’s welcome 
 message*/
 memset(readBuff, 0, 256);
 b = read (sockfd, readBuff, 255);
 printf("%s",readBuff); 
 close(sockfd);
 freeaddrinfo(infoptr);
 exit(0);
	
}

 
