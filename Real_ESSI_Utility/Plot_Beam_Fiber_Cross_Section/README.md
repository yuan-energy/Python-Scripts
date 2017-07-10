# REAL-ESSI_Utility_Tools

### Usage

It contains a lot of frequently used codes that I have developed over time 
to my post/pre processing easy for Real-ESSI input and output files respectively


### Plot_Cross_Section.py
It is used to plot crossection of all sections while using Beam-Fiber element 

#####Synatx 

```script
python Plot_Cross_Section.py < filename >
```

#####Example 

```script
python Plot_Cross_Section.py Examples/Square_RC_Column.fei
```
![alt text](./Output/Crossection_1.png "Cross-Section")


### Visualize_Contact.py
It is used to post-process and visualize the contact elemnts for each time step

#####Synatx 

```script
python Visualize_Contact.py < hdf5_output_file >
```

#####Example 

```script
python Visualize_Contact.py Examples/Square_RC_Column.fei
```
![alt text](./Output/Crossection_1.png "Cross-Section")
