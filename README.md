#  STEP 1 -> How to Order
* Open request_report.py
* Enter the cin and company name
* run the script with *python request_report.py*

# STEP 2 -> How to get the processed directory
* Before proccessing make sure docker is running.
* Run in terminal *docker run -p 8050:8050 scrapinghub/splash*
* when Crimecheck has hit the callback url then run *python process_report.py*
* your report will be in output directory with cin_requestID as directory name

# How it all works
* You hit crimecheck api endpoint with cin , address, comapnyname
* When crimecheck responds to our callback_url *http://api.altinfo.com/api/callback/crimecheck* with JSON, they send a json, which is stored on S3 by our server.
* On Slack you will receive a notification that Crimecheck has processed a ORDER.
* Then you can process_report.py using STEP2. It will genereate output in output folder you configured in .env.
* *process_report.py* will download all files from s3. Then it will see in memory which orders needs to be processed.

Note: - You can run *process_report.py* anytime you want. But run *request_report.py* only when you need it.



