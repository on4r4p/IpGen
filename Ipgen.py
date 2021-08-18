#!/usr/bin/env python3
from argparse import ArgumentParser
from itertools import chain
import ipaddress,sys,os



def ipRange(start,end,filename):
   if os.path.isfile(filename) is True:

        print("Filename already exist.")
        Ok=input("Rename or Append ? (type r or a) :")
        while Ok != "r" and Ok != "a":
              Ok=input("Rename or Append ? (type r or a) :")
        if Ok is "r":
            filename = input("Enter new filename ouput :")
            while os.path.isfile(filename) == True:
                print("Filename already exist.")
                filename = input("Enter new filename ouput :")
   else:
        f = open(filename, "x") 

   try:
          Ip_Gen = list(ipaddress.summarize_address_range(start,end))
   except Exception as E:
          print("Error: ",E)
          sys.exit(1)

   Ip_List = list(chain.from_iterable(Ip_Gen))

   for Ip in Ip_List:
      for j in range(0,10):
          Final=str(Ip)+str(j)
          with open(filename,"a") as f:
                          print("Saving ip Final :",Final)
                          f.write(str(Final)+"\n")

def Checking(user_input,mode):

  if mode is "ip":
     try:
         check = ipaddress.ip_address(user_input)
         return
     except :
         print("Address is not valid: "+user_input)
         sys.exit(1)
  if mode is "cidr":
    try:
         check = ipaddress.ip_network(user_input)
         return
    except ValueError:
         print("Address or Netmask is not valid: "+user_input)
         sys.exit(1)




parser = ArgumentParser()
parser.add_argument("-m","--Min",dest="Min",help="Starting Ipv4",default=None,metavar="MIN")
parser.add_argument("-M","--Max",dest="Max",help="Last Ipv4",default=None,metavar="Max")
parser.add_argument("-c","--Cidr",dest="Cidr",help="Ipv4/prefix",default=None,metavar="Cidr")
parser.add_argument("-o","--output",dest="Output",help="Output filename",default=None,metavar="Output")
Args = parser.parse_args()



if Args.Cidr is None and (Args.Min is None or Args.Max is None):
    print("Argument Error!\n")
    parser.print_help(sys.stderr)
    sys.exit(1)
if Args.Cidr is not None and (Args.Min is not None or Args.Max is not None):
    print("-c can't be used with -m and -M .\nArgument Error!\n")
    parser.print_help(sys.stderr)
    sys.exit(1)


if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if Args.Output is None:

   Args.Output = str(Args.Min)+"-"+str(Args.Max)+".list"



if Args.Cidr is not None: 
    Checking(Args.Cidr,"cidr")
    
    Args.Min = ipaddress.ip_network(Args.Cidr)[0]
    Args.Max = ipaddress.ip_network(Args.Cidr)[-1]
else:
    Checking(Args.Min,"ip")
    Checking(Args.Max,"ip")
    
    Args.Min = ipaddress.ip_address(Args.Min)
    Args.Max = ipaddress.ip_address(Args.Max)

ip_range = ipRange(Args.Min,Args.Max,Args.Output)
