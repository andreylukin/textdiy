import meetup.api

client = meetup.api.Client('14d567219591212802f2c32315851b')

name = 'DIY'
city = 'Atlanta'

arg1 = {}
arg1.update({'text': name},)

groups = client.GetFindGroups(arg1) #groups with "DIY" in name

categ = client.GetFindGroups({'category': [15]}) #groups in "hobbies and crafts"


#searches for groups in "hobbies and crafts" in the requested city puts first 5 in array

arr = []

count = 0

for x in categ.items:
	if count > 5:
		break
	else:
		if city in x.get('city') :
			arr.append(x.get('name') + "\n" + "Link: " + x.get('link'))
			count+=1

for x in arr:
	print(x)



# searches for groups with DIY in name in the requested city
# for x in groups.items:
# 	if name in x.get('name') and city in x.get('city'):
# 		print(x.get('name') + "\n" + "Link: " + x.get('link'))




# print(groups.items[0].keys())



