def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False

def read(file_path):
  
  file = open(file_path,'r')
  for line in file:
    lido = line.strip().split(";")
    if(check_float(lido[0]) == False):
        print(lido[0])
    else:
        print(float(lido[0]))

  file.close()

read("data.csv")