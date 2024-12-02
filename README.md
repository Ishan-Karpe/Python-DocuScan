# Python-DocuScan

## This repo converts pictures of documents into top-down pdf views of the document. 
------------------------------------
### If you don't know who I am, my name is Ishan. I am a teenager who is a PCAP certified programmer, who is now coding unique projects so that I can learn how to write code efficiently in Python and make it understandable to ANYONE through my comments.
------------------------------
# Installation instructions

1. Clone the repo
2. Create a virtual environment .venv using the command palette
3. then select the interpreter to be the python3 interpreter that is recommended and has the .venv
4. execute "python3 -m pip install -r requirements.txt" (no quotes)
5. To run the project DO NOT click on the run button, instead follow the following command

   python scan.py --image (PATH TO THE FILE YOU WANT TO BE SCANNED)
   example: python scan.py --image images/receipt.jpg
   6. if you get xcb error, run this command => export QT_QPA_PLATFORM=xcb , then rerun the command from above

   7. After executing the above command, you will see the images, contours, and top-down view. 

![image](https://github.com/user-attachments/assets/34a9d978-ceaa-47d3-a964-fbd0c162658d)
