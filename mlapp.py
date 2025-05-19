import streamlit as st 
import pandas as pd 
import numpy as np
import joblib

car = pd.read_excel(r'car_features_without_impute.xlsx')


brand_dic = {'Kia': 0, 'Hyundai': 1, 'Mercedes-Benz': 2, 'Maruti': 3, 'Volkswagen': 4, 'Honda': 5, 'Nissan': 6, 'Toyota': 7, 'BMW': 8, 'Mini': 9, 'MG': 10,
              'Tata': 11, 'Skoda': 12, 'Mahindra': 13, 'Isuzu': 14, 'Audi': 15, 'Fiat': 16, 'Renault': 17, 'Jeep': 18, 'Datsun': 19, 'Ford': 20,
                'Mitsubishi': 21, 'Land Rover': 22, 'Lexus': 23, 'Volvo': 24, 'Porsche': 25, 'Jaguar': 26, 'Chevrolet': 27, 'Mahindra Ssangyong': 28,
                  'Citroen': 29, 'Opel': 30, 'Mahindra Renault': 31, 'Hindustan Motors': 32}

body_dic = {'SUV': 0, 'Hatchback': 1, 'Sedan': 2, 'MUV': 3, 'Coupe': 4, 'Convertibles': 5,
             'Wagon': 7, 'Pickup Trucks': 8, 'Minivans': 9, 'Hybrids': 10}

engine_dic ={'Diesel': 0, 'Petrol': 1, 'CNG': 2, 'Electric': 3, 'LPG': 4}

transmission_dic = {'Automatic': 0, 'Manual': 1}

Incurance_dic = {'Third Party insurance': 0, 'Zero Dep': 1, 'Comprehensive': 2, 'Third Party': 3, 'Not Available': 4, }

model_dic = {'Kia Seltos': 0, 'Hyundai Creta': 1, 'Mercedes-Benz GLC': 2, 'Maruti Swift': 3, 'Kia Sonet': 4, 'Hyundai Aura': 5,
              'Volkswagen Polo': 6, 'Hyundai Grand i10 Nios': 7, 'Maruti Baleno': 8, 'Honda Brio': 9, 'Nissan Kicks': 10, 'Toyota Camry': 11, 'BMW 5 Series': 12, 'Mini Cooper SE': 13, 'Toyota Innova Crysta': 14, 'MG Gloster': 15, 'BMW X1': 16, 'Tata Safari Storme': 17, 'Hyundai Venue': 18, 'Maruti Zen Estilo': 19, 'Skoda Kushaq': 20, 'Tata Altroz': 21, 'Maruti Ignis': 22, 'BMW 7 Series': 23, 'BMW 3 Series GT': 24, 'Hyundai Grand i10': 25, 'Mahindra XUV500': 26, 'MG Hector Plus': 27, 'Honda Amaze': 28, 'Hyundai i10': 29, 'Toyota Corolla Altis': 30, 'Toyota Etios': 31, 'Maruti Wagon R': 32, 'Isuzu MU-X': 33, 'Maruti Swift Dzire': 34, 'Mahindra Scorpio': 35, 'Honda Jazz': 36, 'Maruti Brezza': 37, 'Tata Tiago': 38, 'Audi A6': 39, 'Hyundai Santro': 40, 'Maruti Celerio': 41, 'Mercedes-Benz S-Class': 42, 'Fiat Linea': 43, 'Nissan Terrano': 44, 'Renault KWID': 45, 'Honda City': 46, 'Audi Q5': 47, 'BMW X5': 48, 'Hyundai i20': 49, 'Mercedes-Benz E-Class': 50, 'Maruti Ertiga': 51, 'Toyota Glanza': 52, 'Jeep Compass': 53, 'Renault Triber': 54, 'Maruti Vitara Brezza': 55, 'Jeep Wrangler': 56, 'Hyundai Elantra': 57, 'Mahindra Scorpio N': 58, 'Datsun RediGO': 59, 'Hyundai Xcent': 60, 'Tata Tigor': 61, 'Ford Ecosport': 62, 'Hyundai EON': 63, 'Mahindra Thar': 64, 'Mercedes-Benz GLA Class': 65, 'Maruti A-Star': 66, 'Mitsubishi Pajero': 67, 'Mahindra XUV700': 68, 'Toyota Etios Cross': 69, 'Volkswagen Vento': 70, 'Audi A4': 71, 'BMW X4': 72, 'Land Rover Defender': 73, 'Tata Nexon': 74, 'Honda WR-V': 75, 'Toyota Etios Liva': 76, 'Mercedes-Benz GLC Coupe': 77, 'Maruti Celerio X': 78, 'Maruti Wagon R Stingray': 79, 'Lexus RX': 80, 'Hyundai Verna': 81, 'Audi A3': 82, 'Mitsubishi Outlander': 83, 'Mercedes-Benz CLA': 84, 'Kia Carnival': 85, 'Skoda Rapid': 86, 'Maruti Alto 800': 87, 'Land Rover Range Rover Sport': 88, 'Tata Indica V2': 89, 'Skoda Octavia': 90, 'Mercedes-Benz GLS': 91, 'Toyota Fortuner': 92, 'Audi Q7': 93, 'BMW 6 Series': 94, 'Maruti Ciaz': 95, 'Mercedes-Benz M-Class': 96, 'Tata Harrier': 97, 'Mercedes-Benz CLS-Class': 98, 'Maruti Jimny': 99, 'Volvo XC60': 100, 'Mini Cooper Clubman': 101, 'Land Rover Discovery': 102, 'Mercedes-Benz GLE': 103, 'Ford Aspire': 104, 'Land Rover Discovery Sport': 105, 'Mercedes-Benz C-Class': 106, 'Ford Figo': 107, 'MG Astor': 108, 'Ford Endeavour': 109, 'Land Rover Range Rover Evoque': 110, 'Mercedes-Benz AMG A 35': 111, 'Porsche Cayenne': 112, 'Audi Q3': 113, 'Mercedes-Benz AMG G 63': 114, 'Volkswagen Ameo': 115, 'Tata New Safari': 116, 'BMW X7': 117, 'Renault Duster': 118, 'Audi Q3 Sportback': 119, 'Audi Q2': 120, 'Maruti Swift Dzire Tour': 121, 'Volvo XC40': 122, 'Hyundai i20 Active': 123, 'Maruti Alto K10': 124, 'Maruti S-Presso': 125, 'Mercedes-Benz GLA': 126, 'Honda CR-V': 127, 'Porsche Macan': 128, 'Mercedes-Benz G': 129, 'Mini Cooper Convertible': 130, 'Volvo XC 90': 131, 'Nissan Magnite': 132, 'Tata Hexa': 133, 'Maruti SX4 S Cross': 134, 'BMW 3 Series Gran Limousine': 135, 'MG Hector': 136, 'Tata Punch': 137, 'Mahindra KUV 100': 138, 'Skoda Fabia': 139, 'Mini Cooper': 140, 'Renault Kiger': 141, 'Toyota Vellfire': 142, 'Mahindra Bolero Power Plus': 143, 'Mahindra XUV300': 144, 'BMW 3 Series': 145, 'Hyundai Accent': 146, 'Toyota Land Cruiser 300': 147, 'Toyota Fortuner Legender': 148, 'Jaguar XF': 149, 'Nissan Micra': 150, 'Jaguar F-Pace': 151, 'Mahindra Scorpio Classic': 152, 'Jaguar XE': 153, 'Hyundai Tucson': 154, 'Tata Zest': 155, 'Volkswagen Jetta': 156, 'Volvo S90': 157, 'Maruti XL6': 158, 'Toyota Urban cruiser': 159, 'Skoda Superb': 160, 'Mercedes-Benz SLC': 161, 'Mercedes-Benz A-Class Limousine': 162, 'Chevrolet Beat': 163, 'Maruti Ritz': 164, 'Ford Freestyle': 165, 'Datsun GO Plus': 166, 'Skoda Slavia': 167, 'Mahindra KUV 100 NXT': 168, 'Volkswagen Taigun': 169, 'Chevrolet Spark': 170, 'Maruti Alto': 171, 'Isuzu D-Max': 172, 'Maruti Grand Vitara': 173, 'Hyundai Santro Xing': 174, 'Honda Civic': 175, 'Toyota Yaris': 176, 'Nissan Sunny': 177, 'Chevrolet Optra': 178, 'Hyundai Alcazar': 179, 'Mahindra TUV 300': 180, 'Honda Mobilio': 181, 'Tata Manza': 182, 'Toyota Hyryder': 183, 'Mini Cooper Countryman': 184, 'Mercedes-Benz GL-Class': 185, 'Tata Nexon EV Prime': 186, 'Fiat Punto': 187, 'Mercedes-Benz A Class': 188, 'Toyota Innova': 189, 'Maruti SX4': 190, 'Ford Fiesta Classic': 191, 'Maruti FRONX': 192, 'Hyundai i20 N Line': 193, 'Maruti Celerio Tour 2018-2021': 194, 'Lexus ES': 195, 'Jaguar XJ': 196, 'Mahindra Alturas G4': 197, 'Maruti 800': 198, 'Mahindra Bolero': 199, 'Datsun GO': 200, 'Mini 3 DOOR': 201, 'Hyundai Getz': 202, 'Renault Lodgy': 203, 'BMW X3': 204, 'Volvo S60': 205, 'Volkswagen T-Roc': 206, 'Hyundai Santa Fe': 207, 'Maruti Baleno RS': 208, 'Renault Captur': 209, 'Mahindra Ssangyong Rexton': 210, 'Ford Ikon': 211, 'Mitsubishi Cedia': 212, 'Mercedes-Benz B Class': 213, 'Skoda Laura': 214, 'Mahindra Verito': 215, 'Maruti Gypsy': 216, 'Mahindra e2o Plus': 217, 'MG Comet EV': 218, 'Maruti Omni': 219, 'Volkswagen Tiguan': 220, 'Tata Nexon EV Max': 221, 'Chevrolet Cruze': 222, 'Fiat Punto Abarth': 223, 'Maruti Eeco': 224, 'Maruti 1000': 225, 'Citroen C5 Aircross': 226, 'Maruti Zen': 227, 'Mahindra Quanto': 228, 'Land Rover Freelander 2': 229, 'OpelCorsa': 230, 'Mahindra Xylo': 231, 'Honda New Accord': 232, 'Skoda Yeti': 233, 'Chevrolet Tavera': 234, 'Mahindra Renault Logan': 235, 'Citroen C3': 236, 'Tata Nano': 237, 'Maruti Esteem': 238, 'Nissan Micra Active': 239, 'Mitsubishi Lancer': 240, 'Ford Fiesta': 241, 'Mahindra Bolero Camper': 242, 'Kia Carens': 243, 'Chevrolet Enjoy': 244, 'Volkswagen Tiguan Allspace': 245, 'Mahindra Marazzo': 246, 'Tata Indigo': 247, 'Tata Sumo': 248, 'Ford Mondeo': 249, 'Fiat Palio': 250, 'Maruti Estilo': 251, 'Jeep Meridian': 252, 'BMW 1 Series': 253, 'Audi A3 cabriolet': 254, 'Fiat Punto EVO': 255, 'Renault Fluence': 256, 'Tata Nexon EV': 257, 'Chevrolet Sail': 258, 'Hyundai Sonata': 259, 'Maruti Ertiga Tour': 260, 'Isuzu MU 7': 261, 'Tata Indica': 262, 'Honda BR-V': 263, 'Skoda Kodiaq': 264, 'Tata Tiago NRG': 265, 'BMW 2 Series': 266, 'Mini 5 DOOR': 267, 'Fiat Grande Punto': 268, 'Chevrolet Aveo': 269, 'Land Rover Range Rover Velar': 270, 'Maruti Versa': 271, 'Fiat Punto Pure': 272, 'Volvo S 80': 273, 'Audi A8': 274, 'Mercedes-Benz AMG GLA 35': 275, 'Volkswagen Virtus': 276, 'Mahindra TUV 300 Plus': 277, 'Mahindra Jeep': 278, 'Toyota Qualis': 279, 'Volkswagen Passat': 280, 'Land Rover Range Rover': 281, 'Fiat Avventura': 282, 'Renault Scala': 283, 'Honda City Hybrid': 284, 'Tata Aria': 285, 'Volvo V40': 286, 'Tata Bolt': 287, 'MG ZS EV': 288, 'Mahindra E Verito': 289, 'Hyundai Xcent Prime': 290, 'Mercedes-Benz EQC': 291, 'Fiat Abarth Avventura': 292, 'Hindustan Motors Contessa': 293, 'Mahindra Bolero Neo': 294, 'Tata Yodha Pickup': 295, 'Tata Indigo Marina': 296, 'Chevrolet Captiva': 297, 'Mahindra Bolero Pik Up Extra Long': 298, 'Toyota Corolla': 299, 'Ambassador': 300, 'Volvo S60 Cross Country': 301, 'Jeep Compass Trailhawk': 302, 'Tata Sumo Victa': 303, 'Porsche Panamera': 304, 'Mercedes-Benz AMG GT': 305, 'Audi S5 Sportback': 306, 'Renault Pulse': 307, 'Jaguar F-TYPE': 308, 'Tata Tigor EV': 309, 'Mercedes-Benz AMG GLC 43': 310, 'Chevrolet Aveo U-VA': 311, 'Hyundai Kona': 312, 'Porsche 911': 313, 'Volkswagen CrossPolo': 314}

owner_dic = {"1st owner": 1, "2nd owner": 2, "3rd owner": 3}

seats_dic = {'5 Seats': 0, '4 Seats': 1, '7 Seats': 2, '6 Seats': 3, '8 Seats': 4, '2 Seats': 6, '10 Seats': 7, '9 Seats': 8}

#list of categorical lable
brand_list = ['Kia', 'Hyundai', 'Mercedes-Benz', 'Maruti', 'Volkswagen', 'Honda',
       'Nissan', 'Toyota', 'BMW', 'Mini', 'MG', 'Tata', 'Skoda',
       'Mahindra', 'Isuzu', 'Audi', 'Fiat', 'Renault', 'Jeep', 'Datsun',
       'Ford', 'Mitsubishi', 'Land Rover', 'Lexus', 'Volvo', 'Porsche',
       'Jaguar', 'Chevrolet', 'Mahindra Ssangyong', 'Citroen', 'Opel',
       'Mahindra Renault', 'Hindustan Motors']

body_list = ['SUV', 'Hatchback', 'Sedan', 'MUV', 'Coupe', 'Convertibles',
       'Wagon', 'Pickup Trucks', 'Minivans', 'Hybrids']

#get a list of car models
model_list = ['Kia Seltos',
 'Hyundai Creta',
 'Mercedes-Benz GLC',
 'Maruti Swift',
 'Kia Sonet',
 'Hyundai Aura',
 'Volkswagen Polo',
 'Hyundai Grand i10 Nios',
 'Maruti Baleno',
 'Honda Brio',
 'Nissan Kicks',
 'Toyota Camry',
 'BMW 5 Series',
 'Mini Cooper SE',
 'Toyota Innova Crysta',
 'MG Gloster',
 'BMW X1',
 'Tata Safari Storme',
 'Hyundai Venue',
 'Maruti Zen Estilo',
 'Skoda Kushaq',
 'Tata Altroz',
 'Maruti Ignis',
 'BMW 7 Series',
 'BMW 3 Series GT',
 'Hyundai Grand i10',
 'Mahindra XUV500',
 'MG Hector Plus',
 'Honda Amaze',
 'Hyundai i10',
 'Toyota Corolla Altis',
 'Toyota Etios',
 'Maruti Wagon R',
 'Isuzu MU-X',
 'Maruti Swift Dzire',
 'Mahindra Scorpio',
 'Honda Jazz',
 'Maruti Brezza',
 'Tata Tiago',
 'Audi A6',
 'Hyundai Santro',
 'Maruti Celerio',
 'Mercedes-Benz S-Class',
 'Fiat Linea',
 'Nissan Terrano',
 'Renault KWID',
 'Honda City',
 'Audi Q5',
 'BMW X5',
 'Hyundai i20',
 'Mercedes-Benz E-Class',
 'Maruti Ertiga',
 'Toyota Glanza',
 'Jeep Compass',
 'Renault Triber',
 'Maruti Vitara Brezza',
 'Jeep Wrangler',
 'Hyundai Elantra',
 'Mahindra Scorpio N',
 'Datsun RediGO',
 'Hyundai Xcent',
 'Tata Tigor',
 'Ford Ecosport',
 'Hyundai EON',
 'Mahindra Thar',
 'Mercedes-Benz GLA Class',
 'Maruti A-Star',
 'Mitsubishi Pajero',
 'Mahindra XUV700',
 'Toyota Etios Cross',
 'Volkswagen Vento',
 'Audi A4',
 'BMW X4',
 'Land Rover Defender',
 'Tata Nexon',
 'Honda WR-V',
 'Toyota Etios Liva',
 'Mercedes-Benz GLC Coupe',
 'Maruti Celerio X',
 'Maruti Wagon R Stingray',
 'Lexus RX',
 'Hyundai Verna',
 'Audi A3',
 'Mitsubishi Outlander',
 'Mercedes-Benz CLA',
 'Kia Carnival',
 'Skoda Rapid',
 'Maruti Alto 800',
 'Land Rover Range Rover Sport',
 'Tata Indica V2',
 'Skoda Octavia',
 'Mercedes-Benz GLS',
 'Toyota Fortuner',
 'Audi Q7',
 'BMW 6 Series',
 'Maruti Ciaz',
 'Mercedes-Benz M-Class',
 'Tata Harrier',
 'Mercedes-Benz CLS-Class',
 'Maruti Jimny',
 'Volvo XC60',
 'Mini Cooper Clubman',
 'Land Rover Discovery',
 'Mercedes-Benz GLE',
 'Ford Aspire',
 'Land Rover Discovery Sport',
 'Mercedes-Benz C-Class',
 'Ford Figo',
 'MG Astor',
 'Ford Endeavour',
 'Land Rover Range Rover Evoque',
 'Mercedes-Benz AMG A 35',
 'Porsche Cayenne',
 'Audi Q3',
 'Mercedes-Benz AMG G 63',
 'Volkswagen Ameo',
 'Tata New Safari',
 'BMW X7',
 'Renault Duster',
 'Audi Q3 Sportback',
 'Audi Q2',
 'Maruti Swift Dzire Tour',
 'Volvo XC40',
 'Hyundai i20 Active',
 'Maruti Alto K10',
 'Maruti S-Presso',
 'Mercedes-Benz GLA',
 'Honda CR-V',
 'Porsche Macan',
 'Mercedes-Benz G',
 'Mini Cooper Convertible',
 'Volvo XC 90',
 'Nissan Magnite',
 'Tata Hexa',
 'Maruti SX4 S Cross',
 'BMW 3 Series Gran Limousine',
 'MG Hector',
 'Tata Punch',
 'Mahindra KUV 100',
 'Skoda Fabia',
 'Mini Cooper',
 'Renault Kiger',
 'Toyota Vellfire',
 'Mahindra Bolero Power Plus',
 'Mahindra XUV300',
 'BMW 3 Series',
 'Hyundai Accent',
 'Toyota Land Cruiser 300',
 'Toyota Fortuner Legender',
 'Jaguar XF',
 'Nissan Micra',
 'Jaguar F-Pace',
 'Mahindra Scorpio Classic',
 'Jaguar XE',
 'Hyundai Tucson',
 'Tata Zest',
 'Volkswagen Jetta',
 'Volvo S90',
 'Maruti XL6',
 'Toyota Urban cruiser',
 'Skoda Superb',
 'Mercedes-Benz SLC',
 'Mercedes-Benz A-Class Limousine',
 'Chevrolet Beat',
 'Maruti Ritz',
 'Ford Freestyle',
 'Datsun GO Plus',
 'Skoda Slavia',
 'Mahindra KUV 100 NXT',
 'Volkswagen Taigun',
 'Chevrolet Spark',
 'Maruti Alto',
 'Isuzu D-Max',
 'Maruti Grand Vitara',
 'Hyundai Santro Xing',
 'Honda Civic',
 'Toyota Yaris',
 'Nissan Sunny',
 'Chevrolet Optra',
 'Hyundai Alcazar',
 'Mahindra TUV 300',
 'Honda Mobilio',
 'Tata Manza',
 'Toyota Hyryder',
 'Mini Cooper Countryman',
 'Mercedes-Benz GL-Class',
 'Tata Nexon EV Prime',
 'Fiat Punto',
 'Mercedes-Benz A Class',
 'Toyota Innova',
 'Maruti SX4',
 'Ford Fiesta Classic',
 'Maruti FRONX',
 'Hyundai i20 N Line',
 'Maruti Celerio Tour 2018-2021',
 'Lexus ES',
 'Jaguar XJ',
 'Mahindra Alturas G4',
 'Maruti 800',
 'Mahindra Bolero',
 'Datsun GO',
 'Mini 3 DOOR',
 'Hyundai Getz',
 'Renault Lodgy',
 'BMW X3',
 'Volvo S60',
 'Volkswagen T-Roc',
 'Hyundai Santa Fe',
 'Maruti Baleno RS',
 'Renault Captur',
 'Mahindra Ssangyong Rexton',
 'Ford Ikon',
 'Mitsubishi Cedia',
 'Mercedes-Benz B Class',
 'Skoda Laura',
 'Mahindra Verito',
 'Maruti Gypsy',
 'Mahindra e2o Plus',
 'MG Comet EV',
 'Maruti Omni',
 'Volkswagen Tiguan',
 'Tata Nexon EV Max',
 'Chevrolet Cruze',
 'Fiat Punto Abarth',
 'Maruti Eeco',
 'Maruti 1000',
 'Citroen C5 Aircross',
 'Maruti Zen',
 'Mahindra Quanto',
 'Land Rover Freelander 2',
 'OpelCorsa',
 'Mahindra Xylo',
 'Honda New Accord',
 'Skoda Yeti',
 'Chevrolet Tavera',
 'Mahindra Renault Logan',
 'Citroen C3',
 'Tata Nano',
 'Maruti Esteem',
 'Nissan Micra Active',
 'Mitsubishi Lancer',
 'Ford Fiesta',
 'Mahindra Bolero Camper',
 'Kia Carens',
 'Chevrolet Enjoy',
 'Volkswagen Tiguan Allspace',
 'Mahindra Marazzo',
 'Tata Indigo',
 'Tata Sumo',
 'Ford Mondeo',
 'Fiat Palio',
 'Maruti Estilo',
 'Jeep Meridian',
 'BMW 1 Series',
 'Audi A3 cabriolet',
 'Fiat Punto EVO',
 'Renault Fluence',
 'Tata Nexon EV',
 'Chevrolet Sail',
 'Hyundai Sonata',
 'Maruti Ertiga Tour',
 'Isuzu MU 7',
 'Tata Indica',
 'Honda BR-V',
 'Skoda Kodiaq',
 'Tata Tiago NRG',
 'BMW 2 Series',
 'Mini 5 DOOR',
 'Fiat Grande Punto',
 'Chevrolet Aveo',
 'Land Rover Range Rover Velar',
 'Maruti Versa',
 'Fiat Punto Pure',
 'Volvo S 80',
 'Audi A8',
 'Mercedes-Benz AMG GLA 35',
 'Volkswagen Virtus',
 'Mahindra TUV 300 Plus',
 'Mahindra Jeep',
 'Toyota Qualis',
 'Volkswagen Passat',
 'Land Rover Range Rover',
 'Fiat Avventura',
 'Renault Scala',
 'Honda City Hybrid',
 'Tata Aria',
 'Volvo V40',
 'Tata Bolt',
 'MG ZS EV',
 'Mahindra E Verito',
 'Hyundai Xcent Prime',
 'Mercedes-Benz EQC',
 'Fiat Abarth Avventura',
 'Hindustan Motors Contessa',
 'Mahindra Bolero Neo',
 'Tata Yodha Pickup',
 'Tata Indigo Marina',
 'Chevrolet Captiva',
 'Mahindra Bolero Pik Up Extra Long',
 'Toyota Corolla',
 'Ambassador',
 'Volvo S60 Cross Country',
 'Jeep Compass Trailhawk',
 'Tata Sumo Victa',
 'Porsche Panamera',
 'Mercedes-Benz AMG GT',
 'Audi S5 Sportback',
 'Renault Pulse',
 'Jaguar F-TYPE',
 'Tata Tigor EV',
 'Mercedes-Benz AMG GLC 43',
 'Chevrolet Aveo U-VA',
 'Hyundai Kona',
 'Porsche 911',
 'Volkswagen CrossPolo']

seats_list = ['5 Seats', '4 Seats', '7 Seats', '6 Seats', '8 Seats',
       '2 Seats', '10 Seats', '9 Seats']

engine_list = ['Diesel', 'Petrol', 'CNG', 'Electric', 'LPG']

transmission_list = ['Automatic', 'Manual']

incurance_list = ['Third Party insurance', 'Zero Dep', 'Comprehensive', 'Third Party', 'Not Available']


models_with_brand = {'Kia': ['Kia Seltos', 'Kia Sonet'],
 'Hyundai': ['Hyundai Creta',
  'Hyundai Aura',
  'Hyundai Grand i10 Nios',
  'Hyundai Venue',
  'Hyundai Grand i10',
  'Hyundai i10',
  'Hyundai Santro',
  'Hyundai i20',
  'Hyundai Elantra',
  'Hyundai Xcent',
  'Hyundai EON',
  'Hyundai Verna',
  'Hyundai Kona'],
 'Mercedes-Benz': ['Mercedes-Benz GLC',
  'Mercedes-Benz S-Class',
  'Mercedes-Benz E-Class',
  'Mercedes-Benz GLA Class',
  'Mercedes-Benz GLC Coupe',
  'Mercedes-Benz AMG GT',
  'Mercedes-Benz AMG GLC 43'],
 'Maruti': ['Maruti Swift',
  'Maruti Baleno',
  'Maruti Zen Estilo',
  'Maruti Ignis',
  'Maruti Wagon R',
  'Maruti Swift Dzire',
  'Maruti Brezza',
  'Maruti Celerio',
  'Maruti Ertiga',
  'Maruti Vitara Brezza',
  'Maruti A-Star',
  'Maruti Celerio X',
  'Maruti Wagon R Stingray'],
 'Volkswagen': ['Volkswagen Polo', 'Volkswagen Vento', 'Volkswagen CrossPolo'],
 'Honda': ['Honda Brio',
  'Honda Amaze',
  'Honda Jazz',
  'Honda City',
  'Honda WR-V'],
 'Nissan': ['Nissan Kicks', 'Nissan Terrano'],
 'Toyota': ['Toyota Camry',
  'Toyota Innova Crysta',
  'Toyota Corolla Altis',
  'Toyota Etios',
  'Toyota Glanza',
  'Toyota Etios Cross',
  'Toyota Etios Liva'],
 'BMW': ['BMW 5 Series',
  'BMW X1',
  'BMW 7 Series',
  'BMW 3 Series GT',
  'BMW X5',
  'BMW X4'],
 'Mini': ['Mini Cooper SE'],
 'MG': ['MG Gloster', 'MG Hector Plus'],
 'Tata': ['Tata Safari Storme',
  'Tata Altroz',
  'Tata Tiago',
  'Tata Tigor',
  'Tata Nexon',
  'Tata Sumo Victa',
  'Tata Tigor EV'],
 'Skoda': ['Skoda Kushaq'],
 'Mahindra': ['Mahindra XUV500',
  'Mahindra Scorpio',
  'Mahindra Scorpio N',
  'Mahindra Thar',
  'Mahindra XUV700'],
 'Isuzu': ['Isuzu MU-X'],
 'Audi': ['Audi A6', 'Audi Q5', 'Audi A4', 'Audi A3', 'Audi S5 Sportback'],
 'Fiat': ['Fiat Linea'],
 'Renault': ['Renault KWID', 'Renault Triber', 'Renault Pulse'],
 'Jeep': ['Jeep Compass', 'Jeep Wrangler', 'Jeep Compass Trailhawk'],
 'Datsun': ['Datsun RediGO'],
 'Ford': ['Ford Ecosport'],
 'Mitsubishi': ['Mitsubishi Pajero', 'Mitsubishi Outlander'],
 'Land Rover': ['Land Rover Defender'],
 'Lexus': ['Lexus RX'],
 'Volvo': [],
 'Porsche': ['Porsche Panamera', 'Porsche 911'],
 'Jaguar': ['Jaguar F-TYPE'],
 'Chevrolet': ['Chevrolet Aveo U-VA'],
 'Mahindra Ssangyong': [],
 'Citroen': [],
 'Opel': [],
 'Mahindra Renault': [],
 'Hindustan Motors': []}


# setting custom tab
st.set_page_config(page_title="Used Car Price Prediction")





# creating  function for filtering the bran for its corresponding model
def filter_model(brand):
  
    
    pattern = rf'\b{brand}\b'

    brand = car[car['model'].str.contains(pattern,case= False,na=False)]

    return list(brand['model'].unique())




# loading the model
@st.cache(allow_output_mutation=True)
def model_loader(path):
    model=joblib.load(path)
    return model

#loading both models 
with st.spinner("Hold on, the app is loading..."):
    model = model_loader("stacked_model.pkl")





# writing header 

st.title("Used Car Price Prediction")
st.markdown("<h2 style='text-align-center;'>  Used Car Price Prediction  </h2>",unsafe_allow_html=True)


col1,col2 = st.columns(2)


# let's start aking inputs 

#1.fuel_type
fuel_type = col1.selectbox(label="Select the fuel type for the car",options=engine_list,help="what fuel type car do you prefer?")
fuel_type=engine_dic[fuel_type]

#2. body type
body_type = col1.selectbox("Select the body type of the car " ,options= body_list, help= "Which type of car you looking for ?")
body_type = body_dic[body_type]

#3. taking milage information
miles_driven = col1.number_input(label="Enter that how many miles the should have driven eg. 200 miles(enter number only)",help ="Enter how much the car driven")

#4. selecting car's brand and 8.model type
brand_inp =col1.selectbox(label="Select the brand of the car " ,options=brand_list,help = "Which brand the car is?" )

model_inp = col1.selectbox(f"Enter the model for the brand {brand_inp}", options=models_with_brand[brand_inp]) # using the brand_inp variable before encoding by assigning it to dictionary

model_inp = model_dic[model_inp]

brand_inp = brand_dic[brand_inp]


#5. transmission
transmission_type = col1.selectbox(label="Select the type of transmission you want in the car ",options=transmission_list,help= "Enter the type of transmission you want")
transmission_type = transmission_dic[transmission_type]

#6. ownership of the transmission
ownership =  col1.selectbox(label="Enter ownership of the transmission:",options=["1st owner", "2nd owner", "3rd owner"],help="Owner of the transmission")
ownership = owner_dic[ownership]

#7. taking car's model year
year = col1.slider(label="Enter the model year you are looking for...", min_value=1980, max_value=2025, value=2005, help="From which year the car was manufactured?")



"""def model_type(brand_name):
    if brand_inp == brand_name:
        model_inp= col1.selectbox(f"Enter the model for the brand {brand_name}", options= filter_model(brand_name))
        model_inp = model_dic[model_inp]"""

#9. taking car's engine volume intiger  model brand
engineV = col1.number_input(label="Enter the engine capacity of the car you want.", help= "In which gas the car has to run?")
engineV = float(engineV)

#10. seats input
seats_inp =col1.selectbox(label="Enter the number of seats you want in the car.",options=seats_list,help="What is your preferable seater")
seats_inp = seats_dic[seats_inp]





inp_array = np.array([fuel_type,body_type,miles_driven,brand_inp,transmission_type,ownership,year,model_inp,engineV,seats_inp])

inp_array = inp_array.reshape(1,-1)

predict = col1.button('Predict')


if predict:
    pred = model.predict(inp_array)
    if pred < 0:
        st.error("The input values must be irrelevent, try agian by giving relevent informations.")
    pred=round(float(pred), 3)
    st.write(f"The predicted price of the car is ${pred}")
    st.success("success")
    st.balloons()



# writing some information about the project

st.header("Little information about the project")

prj_info = """ 

            Here you can predict used car 🚙 price by giving some information like car brand, model of the car, how much the car has been driven and so on.
            Then just click on predict button, I recommend to choose 'RandomForest Regressor' stacked with Linear Regression for predict the price because it will give more accurate 
            result.\n
            
            I am sharing the full project's notebooks along with dataset. \n
            In case if you want to run the file. - [drive link](https://drive.google.com/drive/folders/12OcDJD-ajF9fRSk5foWffrc5nZ71W-J7?usp=drive_link)\n
            Only want to look at the code? - [Github]() \n
            In case want to contact with me -  keerthiraman234@gmail.com 📫"""


st.write(prj_info)
st.header("""Untll then ❤""")