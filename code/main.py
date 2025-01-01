# module imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import joblib

# model imports
from sklearn.cluster import KMeans

# processing imports
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# FutureWarning türündeki uyarıları devre dışı bırak
warnings.simplefilter(action='ignore', category=FutureWarning)
print('Welcome!')

# fetch the training file
file_path_20_percent = '/instrusion_detector_learning/nsl-kdd/KDDTrain+_20Percent.txt'
file_path_full_training_set = '/instrusion_detector_learning/nsl-kdd/KDDTrain+.txt'
file_path_test = '/instrusion_detector_learning/nsl-kdd/KDDTest+.txt'

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

# Set the dataset column names
df.columns = columns
test_df.columns = columns

# sanity check
print("df.head()\n",df.head())

# map normal to 0, all attacks to 1
is_attack = df.attack.map(lambda a: 0 if a == 'normal' else 1)
test_attack = test_df.attack.map(lambda a: 0 if a == 'normal' else 1)

#data_with_attack = df.join(is_attack, rsuffix='_flag')
df['attack_flag'] = is_attack
test_df['attack_flag'] = test_attack

# view the result
print("df.head():\n",df.head())
print("np.shape(df):\n",np.shape(df))

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

# get numeric features, we won't worry about encoding these at this point
numeric_features = ['duration', 'src_bytes', 'dst_bytes']

# model to fit/test
to_fit = df[numeric_features]

# create our target classifications
binary_y = df['attack_flag']
multi_y = df['attack_map']

# build the training sets
binary_train_X, binary_val_X, binary_train_y, binary_val_y = train_test_split(to_fit, binary_y, test_size=0.6)
multi_train_X, multi_val_X, multi_train_y, multi_val_y = train_test_split(to_fit, multi_y, test_size = 0.6)

multi_model1 = KMeans(n_clusters=2)
multi_model1.fit(multi_train_X, multi_train_y)
multi_predictions1 = multi_model1.predict(multi_val_X)

joblib.dump(multi_model1, 'kmeans_model1.pkl')

# get the score
print("kmeans accurarcy")
print(accuracy_score(multi_predictions1,multi_val_y))