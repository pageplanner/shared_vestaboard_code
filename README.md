# Shared Vestaboard Example Code

### THIS CODE IS OPEN SOURCE
### IT MAY NOT WORK
### THERE IS NO GUARANTEE
### THERE IS NO SUPPORT
### THE PROVIDER WILL NOT BE RESPONSIBLE FOR ANY PROBLEMS

* To use this code, you will need to download it to a computer that has Python installed.  I have used it on Windows and Linux 
* The vestaboard.py file contains common functions that are used byu the other Python scripts in this directory
* It is currently set up to use the Local API, so it will communicate directly to your Vestabaord without connecting to Vestaboard over the internet.  The API address in the vb.url file will need to be updated with your board's IP address
* If you choose to use the local API, you'll need to open a support ticket with Vestaboard support to enable the API, then you'll need to create a file called vb.key and paste the API key provided by Vestaboard
* If you prefer to use the Vestaboard internet-based Read/Write API, you will need to update the vb.url file, vb.key file and call_vestaboard_api subroutine in vestaboard.py
