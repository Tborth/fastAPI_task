1-first you have to change thw DB_host ip to your ip ,you check ip addr command in ubuntu 

2-then just ./config.sh
	if you facing some issue in the realted to the ./config.sh file then 
	run command chmod 777 config.sh

	or 

	you can also run command docker-compose up -d --build 

	http://localhost:8001/docs

3-claim_process/Upload Used to add the data with csv file in claim table

4-"/claim_process/claims used to  add the data in json format"

 5-"/claim_process/generate Used to generate the unique id"
 
 
 6-"/claim_process/compute/<submitted_procedure> Used to compute the fees"
 
 payments route just call the claim route with requests libraray to to calcuate the claim
 
 if their is the load and some instance down so it will manage by the loadbalancer
