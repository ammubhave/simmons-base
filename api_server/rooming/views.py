from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from oauth2_provider.decorators import protected_resource
from rooming.models import Room, Resident
import simplejson as json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@protected_resource()
def taken(request):
    result = list(Room.objects.filter(number__in=Resident.objects.all().values_list('room__number', flat=True)).values_list('number', flat=True))
    return JsonResponse(result, safe=False)

@protected_resource()
def occupants(request):
    d = {}
    result = Resident.objects.all()
    for entry in result:
        d[entry.athena] = entry.room.number
    return JsonResponse(d, safe=False)

@csrf_exempt
@login_required
def run_randomization(request):
    if not (request.user.is_superuser or request.user.groups.filter(name__in=['RAC']).exists()):
        return HttpResponseForbidden('403.html')
    else:
        #################################
        # Simmons Rooming Randomization #
        #################################

        #################################
        # Instructions:
        #
        # 1. Create a csv file named "in.csv" with the following format:
        #    - Column 1 has names of students in any format you wish.
        #    - Column 2 has years matching the format specified in YEARS_ORDER below.
        #
        # 2. Place the csv file in the same directory as this file.
        #
        # 3. Agree upon a randomly chosen seed: chosen with witnesses or from
        #       an agreed-upon external source of randomness (day's lottery numbers...)
        #    By choosing this seed, the randomization process can be repeated and code
        #       verified by interested third parties.
        #
        # 4. Set RANDOM_SEED to this value.
        #
        # 5. Run 'python rooming-randomization.py'.
        #
        # 6. The randomized ordering will be written to the file "out.csv".
        #
        #################################

        import csv, random
        from collections import defaultdict

        RANDOM_SEED = int(request.POST['randomseed'])
        YEARS_ORDER = ["Junior", "Sophomore", "Incoming Sophomore", "Freshman", "Incoming Freshman"]
        OUTPUT_FILENAME = "/tmp/out.csv"

        def initRandom():
            random.seed(RANDOM_SEED)

        # Returns a shuffled copy of the given list.
        def shuffleList(originalList):
            newList = originalList[:]
            random.shuffle(newList)
            return newList

        # Generates namesDict, a mapping from year names to lists of names in that year.
        def setupNamesDict():
            namesDict = dict()
            for year in YEARS_ORDER:
                namesDict[year] = []
            return namesDict

        # Reads the names dictionary from the input file.
        def importNames():
            namesDict = setupNamesDict()
            csvFile = request.FILES['incsv']
            csvReader = csv.reader(csvFile, delimiter=',')
            for row in csvReader:
                name = row[0]
                year = row[1]
                if year not in namesDict:
                    print "ERROR: ", name, "has invalid year", year
                else:
                    namesDict[year].append(name)
            return namesDict

        # Randomizes the name list for each year in the names dict.
        def shuffleNames(namesDict):
            shuffledNamesDict = dict()
            for (year, namesList) in namesDict.items():
                shuffledNamesDict[year] = shuffleList(namesList)
            return shuffledNamesDict

        # Merges the years into a list of tuples [(name, year, finalCount)]
        # with finalCount being the final overall ranking.
        def getFinalOrder(shuffledNamesDict):
            finalOrder = []
            finalCount = 0
            for year in YEARS_ORDER:
                shuffledNames = shuffledNamesDict[year]
                for name in shuffledNames:
                    finalCount += 1
                    finalOrder.append((name, year, finalCount))
            return finalOrder

        # Writes the final ordering to the output file.
        def exportNames(outputFilename, finalOrder):
            outFile = open(outputFilename, 'w')
            csvWriter = csv.writer(outFile)
            for orderTuple in finalOrder:
                csvWriter.writerow(orderTuple)
            outFile.close()

        # Runs the process.
        def main():
            initRandom()
            namesDict = importNames()
            shuffledNamesDict = shuffleNames(namesDict)
            finalOrder = getFinalOrder(shuffledNamesDict)
            exportNames(OUTPUT_FILENAME, finalOrder)

        # Kick it off!
        main()
        with open(OUTPUT_FILENAME, 'r') as myfile:
            response = HttpResponse(myfile.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=out.csv'
            return response
