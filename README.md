# batchReplaceSupersetData

Suppose we need to replace database A with database B in bulk,follow the steps below

Step1 : Export a zip package of all datasets, or charts, or dashboards ,at this point the data source of the zip packet is A

Step2 : Create an arbitrary dataset based on database B, export it as zip package as well

Step3 : Put the zip package of step1 into the  folder named from, put the zip package of step2 into the  folder named to

Step4 :  Execute the python command ```python3 importSuperset.py```

Step5 : After successful execution, pack each folder of the From folder as a zip

Step6 : Import new zip packages to superset one by one

