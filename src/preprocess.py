import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
class Preprocess:
    def __init__(self, file_path: str):
        self.df=pd.read_excel(file_path)
        self.numeric_df = None
        self.non_numeric_df = None
        self.x=None
        self.y=None
        self.x_train=None
        self.x_test=None
        self.y_train=None
        self.y_test=None
        
    def drop(self):
        self.df.drop(['priceActual', 'priceSaving', 'priceFixedText', 'heading', 'Unnamed: 1',
                  'trendingText.desc','bottomData','data','Registration Year Icon',
                 'Insurance Validity Icon','Fuel Type Icon','Seats Icon',
                  'Kms Driven Icon' ,'Ownership Icon','Engine Displacement Icon',
                  'Transmission Icon','Year of Manufacture Icon','RTO Icon','heading.1','commonIcon','Engine','Seats.1','owner','trendingText.imgUrl',
                   'trendingText.heading' ]
                  ,axis=1,inplace=True,errors='ignore')
    

    def clean(self):
        # Remove all non-numeric characters while keeping numbers and decimals
        # Assuming df is your DataFrame
        columns_to_clean = ['price', 'Registration Year', 'Seats', 'Kms Driven', 
                            'Engine Displacement', 'Mileage', 'Max Power', 
                            'Torque','Wheel Size']

        # Remove non-numeric characters while keeping numbers and decimals
        self.df[columns_to_clean] = self.df[columns_to_clean].replace(r'[^0-9.]', '', regex=True)

        # Convert to numeric type
        self.df[columns_to_clean] = self.df[columns_to_clean].apply(pd.to_numeric, errors='coerce')


    def to_numeric(self):
        
        self.df=self.df[['ft','bt','km','oem',
                         'model','transmission','ownerNo','modelYear',
                        'Engine Displacement',"Seats","price"]]
        self.numeric_df = self.df.select_dtypes(include=['number'])
        self.non_numeric_df = self.df.select_dtypes(exclude=['number'])

    def encode(self):
        
        le = LabelEncoder()

        # Apply label encoding to categorical columns
        self.df[self.non_numeric_df.columns]= le.fit_transform(self.df[self.non_numeric_df.columns])



    def split(self):
       
        self.x = self.df.drop('price', axis=1)
        self.y = self.df['price']

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.2, random_state=42)
   
   
    def scale(self):
        scaler = StandardScaler()
        self.x_train = scaler.fit_transform(self.x_train)
        self.x_test = scaler.transform(self.x_test)


    def call(self):
        self.drop()
        self.clean()
        self.to_numeric()
        self.encode()
        self.split()
        self.scale()
        return self.x_train, self.x_test, self.y_train, self.y_test