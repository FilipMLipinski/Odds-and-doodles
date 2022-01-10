##Handwriting recognition project - recognising digits

#panit_nums.py
is a script that I use to generate my data. A little 50x50 canvas pops up. Write your digit
and type the apropriate key on keyboard to label it. The data will be saved to a file and you can repeat that.

#interactive.py
is the main app that makes use of the pickled model.

#how?
So far I'm just using the sklearn.ensemble.RandomForestClassifier, and the model only differentiates 0,1,2.

To be added:
	- Deep learning
	- differentiating all the digits 0..9