from lib2to3.pytree import convert
import county_demographics
import sys

from build_data import convert_county
from data import CountyDemographics


#task 1
def display(county:CountyDemographics): #prints information about counties
    print("Age:")
    for i in county.age:
        print("\t{}: {}".format(i, county.age[i]))

    print("County:")
    print("\t{}".format(i, county.county))

    print("Education:")
    for i in county.education:
        print("\t{}: {}".format(i, county.education[i]))

    print("Ethnicities:")
    for i in county.ethnicities:
        print("\t{}: {}".format(i, county.ethnicities[i]))

    print("Income:")
    for i in county.income:
        print("\t{}: {}".format(i, county.income[i]))

    print("Population:")
    for i in county.population:
        print("\t{}: {}".format(i, county.population[i]))

    print("State:")
    print("\t{}".format(i, county.state))

def filterstate(datascope, state): #filters by  counties of the specified state
    newscope = []
    for i in datascope:
        if i.state == state:
            newscope.append(i)
    return newscope

def filtergt(datascope, field, num): #filters by counties greater than the specified number
    newscope = []
    farray = field.split(".")
    for i in datascope:
        if farray[0] == "Education":
            if i.education[farray[1]] > num:
                newscope.append(i)
        if farray[0] == "Ethnicities":
            if i.ethnicities[farray[1]] > num:
                newscope.append(i)
        if farray[0] == "Income":
            if i.income[farray[1]] > num:
                newscope.append(i)
    return newscope

def filterlt(datascope, field, num): #filters by counties less than the specified number
    farray = field.split(".")

    newscope = []
    for i in datascope:
        if farray[0] == "Education":
            if i.education[farray[1]] < num:
                newscope.append(i)
        if farray[0] == "Ethnicities":
            if i.ethnicities[farray[1]] < num:
                newscope.append(i)
        if farray[0] == "Income":
            if i.income[farray[1]] < num:
                newscope.append(i)
    return newscope

def pop_total(datascope): #returns total 2014 population of all countries
    total = 0
    try:
        for i in datascope:
            total += i.population['2014 Population']
        print("2014 population: {}".format(total))
    except KeyError as e:
        print(e)
    return total

def population(datascope, field): #returns total population per specification
    farray = field.split(".")

    total = 0
    for i in datascope:
        if farray[0] == "Education":
            total += i.population['2014 Population']*i.education[farray[1]]
        if farray[0] == "Ethnicities":
            total += i.population['2014 Population'] * i.ethnicities[farray[1]]
        if farray[0] == "Income":
            total += i.population['2014 Population'] * i.income[farray[1]]
    return total

def percent(datascope, field): #returns percentage of the total subpopulation per specified specification
    farray = field.split(".")

    total = 0
    subtotal = 0
    for i in datascope:
        if farray[0] == "Education":
            total += i.population['2014 Population']
            subtotal += i.population['2014 Population'] * i.education[farray[1]]
        if farray[0] == "Ethnicities":
            total += i.population['2014 Population']
            subtotal += i.population['2014 Population'] * i.ethnicities[farray[1]]
        if farray[0] == "Income":
            total += i.population['2014 Population']
            subtotal += i.population['2014 Population'] * i.income[farray[1]]
        percent = subtotal/total
    return percent

def execute_operation(): #reads the operation file and runs its operations
    entries = 0
    linenum = 0
    try:
        f = open(str(sys.argv[1]))
        data = open("county_demographics.data")
        counties = [convert_county(county) for county in county_demographics.get_report()]
        datascope = counties
        entries = len(counties)
        print("{} records loaded".format(entries))
        for i in f:
            #preparing string for interpretation
            ops = i.split(":")
            for z in range(len(ops)):
                if "\n" in ops[z]:
                    ops[z] = ops[z][:-1]

            #display
            if ops[0] == "display":
                for z in datascope:
                    display(z)

            #filterstate
            elif ops[0] == "filter-state":
                datascope = filterstate(datascope, ops[1])
                print("Filter: state == {} ({} entries)".format(ops[1], len(datascope)))

            #filter-gt
            elif ops[0] == "filter-gt":
                try:
                    datascope = filtergt(datascope, ops[1], float(ops[2]))
                    print("Filter: {} > {} ({} entries)".format(ops[1], ops[2], len(datascope)))
                except:
                    print("One or more arguments invalid.")

            #filter-lt
            elif ops[0] == "filter-lt":
                try:
                    datascope = filterlt(datascope, ops[1], float(ops[2]))
                    print("Filter: {} < {} ({} entries)".format(ops[1], ops[2], len(datascope)))
                except:
                    print("One or more arguments invalid.")

            #population-total
            elif ops[0] == "population-total":
                pop_total(datascope)

            #population
            elif ops[0] == "population":
                print("2014 {} population: {}".format(ops[1], population(datascope, ops[1])))

            #percent
            elif ops[0] == "percent":
                print("2014 {} percentage: {}".format(ops[1], percent(datascope, ops[1])))

            #none
            else:
                    print("Could not read operation. Skipping line.")
            linenum += 1
        f.close()
        data.close()
    except KeyError as e:
        print(e)

if __name__ == "__main__":
    execute_operation()
