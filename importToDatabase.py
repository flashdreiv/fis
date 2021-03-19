a_file = open("a.html", "r")

list_of_lists = []
for line in a_file:
  stripped_line = line.strip()
  list_of_lists.append(stripped_line)

a_file.close()

val = ''
for list in list_of_lists:
    val += f"('{list}',92),"

text = f"insert into ph_locations_barangay(name,city_id) \nvalues {val}"

print(text)
    
    