#
#		Project AAKI's Rankings
#		Data Analyser
#			Reads data from impossible.com database
#			Creates Naive Bayes learning model
#
#	Steven and Max
#		https://github.com/stevenjlm/impossible
#		License in README.markdown

from nvbclass import nvbclass

data=nvbclass()
data.MySQLtext(2000)
data.naive_bayes()
data.apply_model()