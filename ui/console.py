from multiprocessing.sharedctypes import Value
from service.melodii_service import melodii_service
from validators.melodii_validator import validator

class console:
    def __init__(self):
        self.__serv = melodii_service()
        self.__validator = validator()
    
    def start(self):
        comm = self.commands()
        while True:
            for i,com in enumerate(comm):
                print("{}.{}".format(i+1, com[0]))
            
            selection = input("Introdu numarul comenzii alese:")
            try:
                comm[int(selection)-1][1]()
            except ValueError as error:
                print(error)
                
    def protocolAfisare(self):
        print('-'*10)
        ent_lst = self.__serv.getAll()
        for ent in ent_lst:
            print("{};{};{};{}".format(ent.getTitlu(), ent.getArtist(), ent.getGen(), ent.getData()))  
    
    def protocolModif(self):
        print("-"*10)
        ok = False
        while not ok:
            titlu = input("Introdu titlul melodiei cautate: ")
            artist = input("Introdu autorul melodiei cautate: ")
            
            gen = input("Introdu genul ales: ")
            data = input("Introdu data modificata(format zz/ll/aaaa): ")
            
            
            errors = []
            pos = -1
            try:
                pos = self.__serv.searchElem(titlu, artist)
            except ValueError as error:
                errors.append(error)
                


                try:
                    self.__validator.validateGen(gen)
                except ValueError as error:
                    errors.append(error)

                try:
                    self.__validator.validateData(data)
                except ValueError as error:
                    errors.append(error)
                        
                try:
                    self.__serv.modifElem(pos, gen, data)
                    ok = True
                except:
                    pass
            
            if not ok:
                print()
                for err in errors:
                    print(err)
                print()
                cont = input("Incerci din nou? (da/nu): ")
                if cont.lower() == "nu":
                    ok = True
        
    def protocolCreare(self):
        
        pass
    
    def commands(self):
        return [("Modifica melodie", self.protocolModif ),
                ("Afiseaza toate melodiile", self.protocolAfisare),
                ("Creeaza melodii", self.protocolCreare)
                ("Exit",exit)]
    