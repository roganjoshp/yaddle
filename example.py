from yaddle.parser import Parser


parser = Parser('test_file.yoda')
parsed = parser.parse()

results = parsed['/ZplusJet_UE/NCharged_Transverse_Ys=0.500000_Yb=0.500000']['results']
print(results.head())