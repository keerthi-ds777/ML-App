from src.datacleaning import DataCleaning,concat_ll,concat_features
from src.preprocess import Preprocess
from src.training import Training




def main():
       files=[r'C:\Users\loges\Documents\GitHub\ML-App\data\bangalore_cars.xlsx',
       r'C:\Users\loges\Documents\GitHub\ML-App\data\chennai_cars.xlsx',
       r'C:\Users\loges\Documents\GitHub\ML-App\data\delhi.xlsx',
       r'C:\Users\loges\Documents\GitHub\ML-App\data\hyderabad_cars.xlsx',
       r'C:\Users\loges\Documents\GitHub\ML-App\data\jaipur_cars.xlsx',
       r'C:\Users\loges\Documents\GitHub\ML-App\data\kolkata_cars.xlsx']


       file_names=['bangalore_cars.xlsx','chennai_cars.xlsx',
              'delhi.xlsx','hyderabad_cars.xlsx',
              'jaipur_cars.xlsx','kolkata_cars.xlsx']

       file_path='C:\\Users\\loges\\Desktop\\python\\sample projects\\GUVI\\MLapp\\data\\cleaned_data\\'

       output_path=[]
       dfs=[]

       for i in file_names:
              output_path.append(file_path+i)

       for i in range(len(files)):
       
              Object=DataCleaning(files[i],output_path[i])
              Object.call()

       for o in output_path:
              k=concat_features(o)
              dfs.append(k)

       concat_ll(dfs)
       
       pre=Preprocess(r'C:\Users\loges\Documents\GitHub\ML-App\data\features\final_data.xlsx')
       x_train, x_test, y_train, y_test=pre.call()
       training_obj=Training(x_train, x_test, y_train, y_test)
       training_obj.model_train()

     


if __name__ == "__main__":
    main()



