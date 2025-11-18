# Shared Vestaboard Example Code

```
**** THIS IS SAMPLE CODE ****
Copyright (c) 2025 Pageplanner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## How To Use These Scripts

To use this code, you will need to download it to a computer that has Python installed.  I have used it with Python 3 on Windows and Linux 

The vestaboard.py file contains common functions that are used byu the other Python scripts in this directory

It is currently set up to use the Local API, so it will communicate directly to your Vestabaord without connecting to Vestaboard over the internet.
The API address in the vb.url file will need to be updated with your board's IP address

If you choose to use the local API, you'll need to open a support ticket with Vestaboard support to enable the API,
then you'll need to create a file called vb.key and paste the API key provided by Vestaboard

If you prefer to use the Vestaboard internet-based Read/Write API, you will need to update the
vb.url file, vb.key file and call_vestaboard_api subroutine in vestaboard.py

To use the ticker.py Stock Ticker example, you will need to install the latest version of the yfinance Pythion module 

You may also need to use "pip install" to install any modules missing on your computer,
read any error messages from Python to know which modules need to be installed

**IF YOU GET AN ERROR WHEN RUNNING THE PYTHON SCRIPT, READ THE ERROR MESSAGE**
I have found that ChatGPT is helpful in troubleshooting Python scripts.

## Helpful Vestaboard URLs

* Vestaboard Character Codes: https://docs-v1.vestaboard.com/characters
* Vestaboard Local API: https://docs.vestaboard.com/docs/local-api/introduction
* Vestaboard Read/Write API: https://docs.vestaboard.com/docs/read-write-api/introduction
* yfinance Pythion module: https://pypi.org/project/yfinance/

