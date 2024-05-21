from database.DAO import DAO

countries = DAO.getAllCountries()

idMap = {}
for c in countries:
    idMap[c.CCode] = c


borders = DAO.getCountryPairs(idMap,1980)

print(countries)
print(borders)