import numpy as np
points = {
	"A+": 4.00,
	"A": 3.75,
	"A-": 3.50,
	"B+": 3.25,
	"B": 3.00,
	"B-": 2.75,
	"C+": 2.50,
	"C": 2.25,
	"D": 2.00,
	"F": 0.00
}

def cgpa(grades, cradits):
	s = 0
	if "F" in grades:
		return "Fail"
	for i, g in enumerate(grades):
		s += points[g]*cradits[i]
	res = np.sum(cradits)
	return '{0:.2f}'.format(s/res)
