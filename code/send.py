import pandas as pd
import socket
import json

def send_packet(packet, server_ip='127.0.0.1', server_port=8888):
    """Sunucuya bir paket gönderir."""
    try:
        # TCP istemci soketi oluştur
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        # Paketi JSON formatına çevir ve sunucuya gönder
        packet_json = json.dumps(packet)
        client_socket.send(packet_json.encode('utf-8'))

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    # Gönderilecek örnek paket
    file_path_full_training_set = '../nsl-kdd/KDDTrain+.txt'
    file_path_test = '../nsl-kdd/KDDTest+.txt'


    #df = pd.read_csv(file_path_20_percent)
    test_df = pd.read_csv(file_path_test)


    # add the column labels
    columns = (['duration' ,'protocol_type' ,'service' ,'flag' ,'src_bytes' ,'dst_bytes' ,'land' ,'wrong_fragment' ,'urgent' ,'hot' ,'num_failed_logins' ,'logged_in'
    ,'num_compromised' ,'root_shell' ,'su_attempted' ,'num_root' ,'num_file_creations' ,'num_shells' ,'num_access_files' ,'num_outbound_cmds' ,'is_host_login'
    ,'is_guest_login' ,'count' ,'srv_count' ,'serror_rate' ,'srv_serror_rate' ,'rerror_rate' ,'srv_rerror_rate' ,'same_srv_rate' ,'diff_srv_rate'
    ,'srv_diff_host_rate' ,'dst_host_count' ,'dst_host_srv_count' ,'dst_host_same_srv_rate' ,'dst_host_diff_srv_rate' ,'dst_host_same_src_port_rate'
    ,'dst_host_srv_diff_host_rate' ,'dst_host_serror_rate' ,'dst_host_srv_serror_rate' ,'dst_host_rerror_rate' ,'dst_host_srv_rerror_rate'
    ,'attack' ,'level'])

    test_df.columns = columns

    for i in range(10000):
        d  = test_df["duration"].iloc[i]
        sb = test_df["src_bytes"].iloc[i]
        db = test_df["dst_bytes"].iloc[i]
        print(i, ": ", test_df["attack"].iloc[i], d, sb, db)
        packet = {
            "duration":  int(d),        # Bağlantı süresi (örnek değer)
            "src_bytes": int(sb),     # Kaynaktan gönderilen bayt sayısı
            "dst_bytes": int(db),      # Hedefe gönderilen bayt sayısı
        }

        # Sunucuya paketi gönder
        send_packet(packet)
