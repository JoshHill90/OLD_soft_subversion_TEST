def col3_col6_col3(list_items):
	col1 = []
	col2 = []
	col3 = []

	balancer_1 = 0
	balancer_2 = 1
	balancer_3 = 0

	port = 'portrait'
	land = 'landscape'
	square = 'square'

	port_list = []
	land_list = []
	left_ratio = 0
	right_ratio = 0 

	for size in list_items:
		if port in size:
			port_list.append(size)
			
		elif land in size:
			land_list.append(size)
   
		elif square in size:
			land_list.append(size)

			
	for item in list_items:

		left_ratio = (balancer_2 - balancer_1) - left_ratio + 1
		right_ratio = (balancer_2 - balancer_3) - right_ratio + 1
		if item in port_list:
			if balancer_1 < balancer_3 and balancer_1 < balancer_2 or balancer_1 == 0:
				balancer_1 += 2
				col1.append(item)
			elif balancer_3 < balancer_2:
				balancer_3 += 2
				col3.append(item)
			elif balancer_1 < left_ratio:
				balancer_1 += 2
				col1.append(item)
			elif balancer_3 < right_ratio:
				balancer_3 += 2
				col3.append(item)
			else: 
				balancer_2 += 2
				col2.append(item)				


		elif item in land_list:
			if balancer_1 < balancer_3 and balancer_1 < balancer_2 or balancer_1 == 0:
				balancer_1 += .5
				col1.append(item)
			elif balancer_3 < balancer_2:
				balancer_3 += .5
				col3.append(item)
			elif balancer_1 < left_ratio:
				balancer_1 += .5
				col1.append(item)
			elif balancer_3 < right_ratio:
				balancer_3 += .5
				col3.append(item)
			else: 
				balancer_2 += .5
				col2.append(item)
    
    
		elif item in land_list:
			if balancer_1 < balancer_3 and balancer_1 < balancer_2 or balancer_1 == 0:
				balancer_1 += 1
				col1.append(item)
			elif balancer_3 < balancer_2:
				balancer_3 += 1
				col3.append(item)
			elif balancer_1 < left_ratio:
				balancer_1 += 1
				col1.append(item)
			elif balancer_3 < right_ratio:
				balancer_3 += 1
				col3.append(item)
			else: 
				balancer_2 += 1
				col2.append(item)

	return col1, col2, col3 



