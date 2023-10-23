# PDF to ICS - Worktime planning
    #### Video Demo:  <URL HERE>
    #### Description:
    
    Some jobs require differents shifts that are different every week, that gives possibility to people to mistake a shift in a certain day.
    One of the easiest tools that we have availible are cellphones where a Calendar app is always installed. 

    In my current job(10.2023) we get a weekley worktime plan from the system, wich only can be stored as a pdf and/or printed. Thant makes the task of registring our shifts manually in our cellphones tedious. 
    The generated pdf have an specific structure given from the system, that means that this program will only work for that specific pdf structure and not for other documents. 

    The program runs with an argument wich indicates the pdf file name to use. If the extension is incorrect or the file name doesn't exist will return an Error and inform the user. 
    This program reads the pdf and extract the table that contains the dates, worker names and the respectives shifts. 
    Prompts the user for the worker name so the program return an ics file corresponding to the sifts of the indicated worker. 
    Some days contain more than one event based in worktimes for different areas in the same company, these area is indicated with a code that comes before the time frame of the task. So the program has to extract and create an event for each one of them and add to the name event the description of the corresponding code. 

    

