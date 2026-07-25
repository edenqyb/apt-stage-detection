import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler

#Data loading and organization
monday_pub = '/csv/enp0s3-monday.pcap_Flow.csv'
monday_pv = '/csv/enp0s3-monday-pvt.pcap_Flow.csv'
tuesday_pub = '/csv/enp0s3-public-tuesday.pcap_Flow.csv'
tuesday_pv = '/csv/enp0s3-pvt-tuesday.pcap_Flow.csv'
wednesday_pub = '/csv/enp0s3-public-wednesday.pcap_Flow.csv'
wednesday_pv = '/csv/enp0s3-pvt-wednesday.pcap_Flow.csv'
thursday_pub = '/csv/enp0s3-public-thursday.pcap_Flow.csv'
thursday_pv = '/csv/enp0s3-pvt-thursday.pcap_Flow.csv'
friday_pub = '/csv/enp0s3-tcpdump-friday.pcap_Flow.csv'
friday_pv = '/csv/enp0s3-tcpdump-pvt-friday.pcap_Flow.csv'

mon_pub = pd.read_csv(monday_pub, header=0)
mon_pv = pd.read_csv(monday_pv, header=0)
tue_pub = pd.read_csv(tuesday_pub, header=0)
tue_pv = pd.read_csv(tuesday_pv, header=0)
wed_pub = pd.read_csv(wednesday_pub, header=0)
wed_pv = pd.read_csv(wednesday_pv, header=0)
thu_pub = pd.read_csv(thursday_pub, header=0)
thu_pv = pd.read_csv(thursday_pv, header=0)
fri_pub = pd.read_csv(friday_pub, header=0)
fri_pv = pd.read_csv(friday_pv, header=0)

#Correcting columns for dataframe "thu_pv"
thu_pv.columns = ['Flow ID', 'Src IP', 'Src Port', 'Dst IP', 'Dst Port', 'Protocol',
       'Timestamp', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets',
       'Total Length of Fwd Packet', 'Total Length of Bwd Packet',
       'Fwd Packet Length Max', 'Fwd Packet Length Min',
       'Fwd Packet Length Mean', 'Fwd Packet Length Std',
       'Bwd Packet Length Max', 'Bwd Packet Length Min',
       'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s',
       'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max',
       'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std',
       'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean',
       'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags',
       'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length',
       'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s',
       'Packet Length Min', 'Packet Length Max', 'Packet Length Mean',
       'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count',
       'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count',
       'URG Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio',
       'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg',
       'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg',
       'Bwd Bytes/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Bwd Bulk Rate Avg',
       'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
       'Subflow Bwd Bytes', 'FWD Init Win Bytes', 'Bwd Init Win Bytes',
       'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std',
       'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max',
       'Idle Min', 'Activity', 'Stage']
dfs = [mon_pub, mon_pv, tue_pub, tue_pv, wed_pub, wed_pv, thu_pub, thu_pv, fri_pub, fri_pv]

# Checking dataframes before concating
for df in dfs:
    print(df.isnull().sum())

for df in dfs:
    df.reset_index(drop=True, inplace=True)

dapt = pd.concat(dfs, axis=0, ignore_index=True)

#Data Cleaning
#Checking for missing values in the entire DataFrame
print(dapt.isnull().any().any())

#changing categorical_columns to numerical
categorical_columns = ['Src IP', 'Dst IP', 'Flow ID']

#Method1: Using Sparse Matrices
# encoder = OneHotEncoder(sparse_output=True)
# encoded_features = encoder.fit_transform(dapt[['Src IP', 'Dst IP', 'Flow ID']])
# encoded_df = pd.DataFrame.sparse.from_spmatrix(encoded_features)
# dapt_encoded = pd.concat([dapt.drop(['Src IP', 'Dst IP', 'Flow ID'], axis=1), encoded_df], axis=1)
# print(dapt_encoded.head())

#Method 2: using OrdinalEncoder from sklearn to avoid one-hot encoding
encoder = OrdinalEncoder()
encoded_features = encoder.fit_transform(dapt[['Src IP', 'Dst IP', 'Flow ID']])

encoded_df = pd.DataFrame(encoded_features, columns=['Src IP', 'Dst IP', 'Flow ID'])

dapt[['Src IP', 'Dst IP', 'Flow ID']] = encoded_df

#Converting Timestamp into datetime format to use it for temporal information
dapt['Timestamp'] = pd.to_datetime(dapt['Timestamp'], format='%d/%m/%Y %I:%M:%S %p')

#Target label encoding:
#Method1: Label encoding
# label_encoder = LabelEncoder()
# dapt['Activity_encoded'] = label_encoder.fit_transform(dapt['Activity'])
# dapt['Stage_encoded'] = label_encoder.fit_transform(dapt['Stage'])

#Method2: One-Hot Encoding
# dapt = pd.get_dummies(dapt, columns=['Activity', 'Stage'])

#Method3: Ordinal Encoding:
# dapt[['Activity_encoded', 'Stage_encoded']] = encoder.fit_transform(dapt[['Activity', 'Stage']])

#Finding outliers
# sns.boxplot(data=dapt)
# plt.show()

#Labeling the dataset

#Method1: 0 for normal and benign data and 1 for attacks
# dapt['target'] = np.where((dapt['Activity'] == 'Normal') | (dapt['Activity'] == 'benign') | (dapt['Activity'] == 'BENIGN'), 0, 1)
# dapt.drop(['Activity', 'Stage'], axis=1, inplace=True)
# print(dapt.head())

# label_counts = dapt['target'].value_counts()

# # Print the count of target=1 and target=0
# print("Count of target=0 (Normal or benign):", label_counts[0])
# print("Count of target=1 (Other activities):", label_counts[1])

#Method2: multi class
unique_stages = dapt['Stage'].unique()
# for stage_label in unique_stages:
#     print("Stages:\t" + stage_label)

unique_activity = dapt['Activity'].unique()
# for activity_label in unique_activity:
#     print("Activity:\t" + activity_label)

class_mapping = {
    'Benign': 0,
    'BENIGN': 0,
    'Reconnaissance': 1,
    'Establish Foothold': 2,
    'Lateral Movement': 3,
    'Data Exfiltration': 4
}

class_counts = dapt['Stage'].value_counts()
dapt['Label'] = dapt['Stage'].map(class_mapping)

plt.bar(class_counts.index, class_counts.values)

plt.xlabel('Class')
plt.ylabel('Count')
plt.title('Class Distribution in the Dataset')
plt.show()

print(dapt.columns)
print(dapt.head())

X = dapt.iloc[:, :].values

replaceInfinity = 1
replaceNan = 0
nColumns = len(X[0])

if replaceInfinity == "1":
    print("Replacing Infinity with the max value of the feature and nan with " + str(replaceNan) + ".")    
    strippedDataset = []
    for i in range(len(X)):
        if 'nan' not in X[i] and 'Infinity' not in X[i]:
            strippedDataset.append(X[i])
    strippedDataset = np.array(strippedDataset) 

    maxValues = []
    stringColumns = []
    infinityColumns = []

    for j in range(nColumns):
        try:
            maxValue = np.amax(X[:, j])
            if maxValue == 'Infinity':
                maxValue = float(np.amax(strippedDataset[:, j])) * 2
            maxValue = float(maxValue)            
        except: 
            maxValue = 0
            stringColumns.append(j)
        finally: 
            maxValues.append(maxValue)                    
    for i in range(len(X)):
        for j in range(nColumns):
            if str.lower(str(X[i, j])) == "infinity":                
                X[i, j] = float(maxValues[j])
            elif str.lower(str(X[i, j])) == 'nan':
                X[i, j] = replaceNan
else:
    print("\n\n\nReplacing Infinity and nan with " + str(replaceInfinity) + ", " + str(replaceNan) + ".")                          
    for i in range(len(X)):
        for j in range(nColumns):
            if str.lower(str(X[i, j])) == 'infinity':
                X[i, j] = replaceInfinity
            elif str.lower(str(X[i, j])) == 'nan':
                X[i, j] = replaceNan
  
print("Creating cleaned file.")
fileCleaned = "dapt_data.csv"
column_headers = dapt.columns.tolist()
np.savetxt(fileCleaned, np.array(X), delimiter=',', fmt="%s", header=",".join(column_headers), comments='')
print("Cleaned file " + fileCleaned + " has been created.")  