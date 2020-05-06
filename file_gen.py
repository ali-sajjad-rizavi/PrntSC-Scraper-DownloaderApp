

print('A total of 2,176,782,336 string combinations are going to be generated and written to a CSV file.')
input('This will take about 2 hours. Press [ENTER] to continue or [Ctrl+C] to exit...')

Alpha_numeric = 'abcdefghijklmnopqrstuvwxyz0123456789'
total_strings = 0

with open('sixchar.csv', 'w') as file:
	count1 = 0
	count2 = 0
	count3 = 0
	print(100*count1/36, '% ', 100*count2/36, '% ', 100*count3/36, '%')
	for c1 in Alpha_numeric:
		count2 = 0
		for c2 in Alpha_numeric:
			count3 = 0
			for c3 in Alpha_numeric:
				for c4 in Alpha_numeric:
					for c5 in Alpha_numeric:
						for c6 in Alpha_numeric:
							file.write(c1 + c2 + c3 + c4 + c5 + c6 + '\n')
							total_strings += 1
				count3 += 1
				print(100*count1/36, '% ', 100*count2/36, '% ', 100*count3/36, '%')
			count2 += 1
			print(100*count1/36, '% ', 100*count2/36, '% ', 100*count3/36, '%')
		count1 += 1
		print(100*count1/36, '% ', 100*count2/36, '% ', 100*count3/36, '%')

#-------------------

print('--------------------------------------------------')
print('- Total strings written:', total_strings)