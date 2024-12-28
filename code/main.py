# module imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import random
import warnings

# model imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans

# processing imports
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

# FutureWarning türündeki uyarıları devre dışı bırak
warnings.simplefilter(action='ignore', category=FutureWarning)
print('Welcome!')

# fetch the training fil../nsl-kdd/KDDTrain+_20Percent.txt'
file_path_full_training_set = '../nsl-kdd/KDDTrain+.txt'
file_path_test = '../nsl-kdd/KDDTest+.txt'

#df = pd.read_csv(file_path_20_percent)
df = pd.read_csv(file_path_full_training_set)
test_df = pd.read_csv(file_path_test)


# add the column labels
columns = (['duration' ,'protocol_type' ,'service' ,'flag' ,'src_bytes' ,'dst_bytes' ,'land' ,'wrong_fragment' ,'urgent' ,'hot' ,'num_failed_logins' ,'logged_in'
,'num_compromised' ,'root_shell' ,'su_attempted' ,'num_root' ,'num_file_creations' ,'num_shells' ,'num_access_files' ,'num_outbound_cmds' ,'is_host_login'
,'is_guest_login' ,'count' ,'srv_count' ,'serror_rate' ,'srv_serror_rate' ,'rerror_rate' ,'srv_rerror_rate' ,'same_srv_rate' ,'diff_srv_rate'
,'srv_diff_host_rate' ,'dst_host_count' ,'dst_host_srv_count' ,'dst_host_same_srv_rate' ,'dst_host_diff_srv_rate' ,'dst_host_same_src_port_rate'
,'dst_host_srv_diff_host_rate' ,'dst_host_serror_rate' ,'dst_host_srv_serror_rate' ,'dst_host_rerror_rate' ,'dst_host_srv_rerror_rate'
,'attack' ,'level'])

df.columns = columns
test_df.columns = columns

# sanity check
print("df.head()",df.head())

# map normal to 0, all attacks to 1
is_attack = df.attack.map(lambda a: 0 if a == 'normal' else 1)
test_attack = test_df.attack.map(lambda a: 0 if a == 'normal' else 1)

#data_with_attack = df.join(is_attack, rsuffix='_flag')
df['attack_flag'] = is_attack
test_df['attack_flag'] = test_attack

# view the result
print("df.head(): ",df.head())
print("np.shape(df): ",np.shape(df))

set(df['protocol_type'])
set(df['attack'])
set(df['service'])


# lists to hold our attack classifications
dos_attacks = ['apache2','back','land','neptune','mailbomb','pod','processtable','smurf','teardrop','udpstorm','worm']
probe_attacks = ['ipsweep','mscan','nmap','portsweep','saint','satan']
privilege_attacks = ['buffer_overflow','loadmdoule','perl','ps','rootkit','sqlattack','xterm']
access_attacks = ['ftp_write','guess_passwd','http_tunnel','imap','multihop','named','phf','sendmail','snmpgetattack','snmpguess','spy','warezclient','warezmaster','xclock','xsnoop']

# we will use these for plotting below
attack_labels = ['Normal','DoS','Probe','Privilege','Access']

# helper function to pass to data frame mapping
def map_attack(attack):
    if attack in dos_attacks:
        # dos_attacks map to 1
        attack_type = 1
    elif attack in probe_attacks:
        # probe_attacks mapt to 2
        attack_type = 2
    elif attack in privilege_attacks:
        # privilege escalation attacks map to 3
        attack_type = 3
    elif attack in access_attacks:
        # remote access attacks map to 4
        attack_type = 4
    else:
        # normal maps to 0
        attack_type = 0

    return attack_type

# map the data and join to the data set
attack_map = df.attack.apply(map_attack)
df['attack_map'] = attack_map

test_attack_map = test_df.attack.apply(map_attack)
test_df['attack_map'] = test_attack_map

# view the result
print("df.head()",df.head())

set(df['attack_map'])

# get the intial set of encoded features and encode them
features_to_encode = ['protocol_type', 'service', 'flag']
encoded = pd.get_dummies(df[features_to_encode])
test_encoded_base = pd.get_dummies(test_df[features_to_encode])

# not all of the features are in the test set, so we need to account for diffs
test_index = np.arange(len(test_df.index))
column_diffs = list(set(encoded.columns.values)-set(test_encoded_base.columns.values))

diff_df = pd.DataFrame(0, index=test_index, columns=column_diffs)

# we'll also need to reorder the columns to match, so let's get those
column_order = encoded.columns.to_list()

# append the new columns
test_encoded_temp = test_encoded_base.join(diff_df)

# reorder the columns
test_final = test_encoded_temp[column_order].fillna(0)

# get numeric features, we won't worry about encoding these at this point
numeric_features = ['duration', 'src_bytes', 'dst_bytes']

# model to fit/test
to_fit = encoded.join(df[numeric_features])
test_set = test_final.join(test_df[numeric_features])

# create our target classifications
binary_y = df['attack_flag']
multi_y = df['attack_map']

# build the training sets
binary_train_X, binary_val_X, binary_train_y, binary_val_y = train_test_split(to_fit, binary_y, test_size=0.6)
multi_train_X, multi_val_X, multi_train_y, multi_val_y = train_test_split(to_fit, multi_y, test_size = 0.6)

print(binary_train_X.info())
print(binary_train_X.sample(5))

# model for the binary classification
binary_model = RandomForestClassifier()
binary_model.fit(binary_train_X, binary_train_y)
binary_predictions = binary_model.predict(binary_val_X)

# calculate and display our base accuracty
base_rf_score = accuracy_score(binary_predictions,binary_val_y)
print(base_rf_score)

# define the list of models that we want to test
models = [
    KMeans(n_clusters=2),
]

# Performansı değerlendirmek için boş bir liste
model_comps = []

# Modeller üzerinde geçiş yaparak performansı topluyoruz
for model in models:
    model_name = model.__class__.__name__
    if model_name == 'KMeans':  # KMeans için özel işlem
        model.fit(binary_train_X)  # KMeans, etiketler ile eğitilmez, sadece veri ile çalışır
        predictions = model.predict(binary_val_X)  # Küme tahminleri yapılır
    else:
        accuracies = cross_val_score(model, binary_train_X, binary_train_y, scoring='accuracy')
        for count, accuracy in enumerate(accuracies):
            model_comps.append((model_name, count, accuracy))

    # Eğer KMeans modeli ise, sonuçları listeye ekleyelim
    if model_name == 'KMeans':
        accuracy = accuracy_score(binary_val_y, predictions)  # KMeans ile doğruluğu hesaplamak
        model_comps.append((model_name, 0, accuracy))

# a box plot will do well to show us overall performance and the variation in the models.
result_df = pd.DataFrame(model_comps, columns=['model_name', 'count', 'accuracy'])
result_df.pivot(index='count',columns='model_name',values='accuracy').boxplot(rot=45)

print('Model Comparison:')
print(result_df.groupby('model_name').accuracy.mean())

# model for the mulit classification
multi_model = RandomForestClassifier()
multi_model.fit(multi_train_X, multi_train_y)
multi_predictions = multi_model.predict(multi_val_X)

multi_model1 = KMeans(n_clusters=2)
multi_model1.fit(multi_train_X, multi_train_y)
multi_predictions1 = multi_model1.predict(multi_val_X)

# get the score
print("aaaaa")
print(accuracy_score(multi_predictions,multi_val_y))
print("bbbbbb")
print(accuracy_score(multi_predictions1,multi_val_y))