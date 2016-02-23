# HW 2
---

### Best Assets (largest rsquared sum) (Part a) 

### HW 1 BEST ASSET
*Assets:  							ACE,DEI,PPG,WCC,EOG,RJF,ULTI,LB,AEP,KIM
R-Squared Sum:  			361.33979851841366

### HW 2 BEST ASSET (with new algorithm that does not remove the selected assets from all assets when running regression, approximately 10 larger than previous HW 1 result)

Assets: 							ACE,DEI,PPG,WCC,EOG,RJF,ULTI,LB,AEP,KIM
R-Squared Sum: 				371.339798518

### Data Processing (Part b)

	./process_data data.json

The results of F, Q, R, V, V^T*F*V will be dumped to a txt file preceded by the selected asset tickers.

### myopt (Part c)

Enter ``myopt/src`` and run:

	make && ../bin/myopt ../data/f1.dat

The iteration is currently set to 20; optionally, we can use a command line argument to set that.

