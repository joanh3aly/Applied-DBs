import connectToDb
import pymysql
import pymongo
from re import compile

def display_menu():
  print('')
  print('MENU')
  print('1 - View 15 Cities')
  print('2 - View Cities by Population')
  print('3 - Add New City')
  print('4 - Find Car by Engine Size')
  print('5 - Add New Car')
  print('6 - View Countries by Name')
  print('7 - View Countries by Population')
  print('x - Exit Application')
  print('')

def sanitiseMenuInput():
  choice = input('Choice: ')
  print('')
  if (choice == 'x'):
    print('Goodbye')
    return exit(0)
  elif (choice.isdigit() == False or int(choice) < 1 or int(choice) > 7):
    print('Please choose a number from 1 to 7. Press x to exit.')
  else:
    return choice
  
def sanitiseComparisonInput():
  compare = input('Enter < > or = : ')
  if (compare == '<' or compare == '>' or compare == '='):
    return compare
  else:
    print('Invalid input')
    return sanitiseComparisonInput()

def sanitiseNumericInput(inputType):
  inputData = input("Enter {} : ".format(inputType))
  if (inputData.isdigit() == False):
    print('Please enter numbers, not letters or other characters.')
    return sanitiseNumericInput(inputType)
  else:
    return int(inputData)
  
def sanitiseAlphabeticInput(inputType):
  inputData = ''
  inputData = input("Enter {} : ".format(inputType))
  if (inputData.isalpha() == True and inputType == 'country code' and len(inputData) > 3):
    print('Please enter 3 letters max.')
    outputData = sanitiseAlphabeticInput(inputType)
  elif (inputData.isalpha() == False):
    print('Please enter letters not numbers or other characters.')
    outputData = sanitiseAlphabeticInput(inputType)   
  else:
    outputData = inputData
  return outputData

def sanitiseFloatInput():
  engineSize = input('Enter engine size: ')
  try:
      engineSizeFloat = float(engineSize)
  except Exception as e:
    print(e, 'Please enter a floating point number with no more than 1 decimal place.')
    return sanitiseFloatInput() 
  if (0.5 <= engineSizeFloat < 10 and round(engineSizeFloat,1) == engineSizeFloat):
    return engineSizeFloat
  else:
    print('Please enter a floating point number between 0.5 and 10 with no more than 1 decimal place.')
    return sanitiseFloatInput() 

def sanitiseRegPlateInput():
  regNumber = input('Enter registration: ')
  plate_format = compile('^[0-9]{2,3}-[a-zA-z]{2}-[0-9]{2,3}$')
  if (plate_format.match(regNumber) is not None):
    return regNumber
  else:
    print('Please enter a registration number in the format nn-ll-nn or nnn-ll-nnn.')
    return sanitiseRegPlateInput()

def countryInputResults():
  print('Countries by name')
  print('-----------------')
  countryName = sanitiseAlphabeticInput('country name')
  countries = connectToDb.countryNames(countryName) 
  while (not countries):
    print('No results for this input')
    print('')
    return countryInputResults()
  else:
    return countries   

def countryLoop(countries):
  for country in countries:
    print(country['Name'],'|', country['Continent'],'|', country['Population'],'|', country['HeadOfState'])

def populationInputResults():
  print('Countries by population')
  print('-----------------------')
  compare = sanitiseComparisonInput()
  pop = sanitiseNumericInput('population')
  countryPopulations = connectToDb.countryPopulations(compare,pop)
  if (not countryPopulations):
    print('No results for this input')
    print('')
    return populationInputResults()
  else:
    return countryPopulations

def countryPopLoop(countryPopulations):
  for populations in countryPopulations:
    print(populations['Name'],'|', populations['Continent'],'|', populations['Population'],'|', populations['HeadOfState'])


def main():
  display_menu()
  qSixCounter = 0
  qSevenCounter = 0

  while True:
    choice = sanitiseMenuInput()
    if (choice == '1'):
      print('First 15 cities')
      print('---------------')
      cities = connectToDb.cities()
      for city in cities:
        print(city['ID'], '|', city['Name'],'|', city['CountryCode'],'|', city['District'],'|', city['Population'])
      display_menu()
    elif (choice == '2'):
      print('Cities by population')
      print('--------------------')
      compare = sanitiseComparisonInput()
      pop = sanitiseNumericInput('population')
      populations = connectToDb.population(compare,pop)
      if (not populations):
        print('No results for this input')
      else:
        for population in populations:
          print(population['ID'], '|', population['Name'],'|', population['CountryCode'],'|', population['District'],'|', population['Population'])
      display_menu()
    elif (choice == '3'):
      print('Add new city')
      print('------------')
      newCityName = sanitiseAlphabeticInput('city name')
      countryCode = sanitiseAlphabeticInput('country code')
      district = sanitiseAlphabeticInput('district')
      population = sanitiseNumericInput('population')
      connectToDb.addCity(newCityName,countryCode,district,population)
      print(' ')
      display_menu()
    elif (choice == '4'):
      print('Show cars by engine size')
      print('-------------------------')
      engineSize = sanitiseFloatInput()
      engines = connectToDb.engineSize(engineSize)
      if (engines.count() > 0):
        for engine in engines:
          print(engine) 
      else:
        print('No results for this input')
      display_menu()
    elif (choice == '5'):
      print('Add new car')
      print('-----------')
      carId = sanitiseNumericInput('_id:')
      regNumber = sanitiseRegPlateInput()
      engineSize2 = sanitiseFloatInput()
      connectToDb.addCar(carId,regNumber,engineSize2)
      display_menu()
    elif (choice == '6' and qSixCounter == 0):
      countries = countryInputResults()
      countryLoop(countries)
      qSixCounter += 1
      display_menu()
    elif (choice == '6' and qSixCounter > 0):
      print('Countries by name')
      print('-----------------')
      countryLoop(countries)
      display_menu() 
    elif (choice == '7' and qSevenCounter == 0):
      countryPopulations = populationInputResults()
      countryPopLoop(countryPopulations)
      qSevenCounter += 1
      display_menu()
    elif (choice == '7' and qSevenCounter > 0):
      print('Countries by population')
      print('-----------------------')
      countryPopLoop(countryPopulations)
      display_menu()
    else:  
      display_menu()


if __name__ == '__main__':
  main()