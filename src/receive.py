import socket
import pandas as pd
import numpy as np
import joblib
from scipy.stats import zscore


# Önceden eğitilmiş modeli yükle
kmeans_model = joblib.load("../kmeans-model/kmeans_model.pkl")

# Eğitimde kullanılan sütunlar
column_order = ["duration", "src_bytes", "dst_bytes"]

numeric_features = ["duration", "src_bytes", "dst_bytes"]
threshold = 10  # Anomali eşik değeri


def preprocess_packet(packet):
    """Gelen paketi işleyip modelin kabul edeceği formata çevirir."""
    # Örnek veri formatı: {'duration': 5, 'src_bytes': 1000, 'dst_bytes': 500, 'protocol_type': 'tcp', 'service': 'http', 'flag': 'SF'}
    encoded_data = pd.get_dummies(pd.DataFrame([packet]))
    missing_columns = set(column_order) - set(encoded_data.columns)
    for col in missing_columns:
        encoded_data[col] = 0

    # Sütun sırasını düzenle
    encoded_data = encoded_data[column_order]

    # Sadece sayısal özellikleri al
    numeric_data = pd.DataFrame([packet])[numeric_features]

    # Çakışan sütunları kaldır
    numeric_data = numeric_data.drop(
        columns=[col for col in numeric_features if col in encoded_data.columns],
        errors="ignore",
    )

    # İşlenmiş veriyi birleştir
    processed_data = pd.concat([encoded_data, numeric_data], axis=1)
    return processed_data

def detect_anomaly(processed_data, indeks):
    """KMeans modeli ile anomali tespiti yapar."""
    prediction = kmeans_model.predict(processed_data)
    cluster_centers = kmeans_model.cluster_centers_
    distances = np.linalg.norm(cluster_centers - processed_data.values, axis=0)

    if np.min(distances) > 2900 and np.min(distances) <= 3000:
        print(
            f"Anomali Tespit Edildi: {indeks}: {np.min(distances)}, "
            f"{int(processed_data['duration'].iloc[0])}, "
            f"{int(processed_data['src_bytes'].iloc[0])}, "
            f"{int(processed_data['dst_bytes'].iloc[0])}"
        )

    else:
        print(
            f"Normal               : {np.min(distances)}, "
            f"{int(processed_data['duration'].iloc[0])}, "
            f"{int(processed_data['src_bytes'].iloc[0])}, "
            f"{int(processed_data['dst_bytes'].iloc[0])}"
        )


def start_server():
    """TCP sunucusunu başlatır ve gelen paketleri işler."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8888))
    server_socket.listen(5)

    print("Sunucu dinliyor...")
    indeks = 0

    while True:
        client_socket, addr = server_socket.accept()
        # print(f"Bağlantı alındı: {addr}")

        try:
            data = client_socket.recv(1024).decode("utf-8")

            # Veriyi JSON formatında çözümle
            packet = eval(data)  # NOT: eval güvenli değilse json.loads kullanın

            # Veriyi işleyin
            processed_data = preprocess_packet(packet)

            # Anomali tespiti yap
            is_anomaly = detect_anomaly(processed_data, indeks)
            indeks+=1
        except Exception as e:
            print(f"Hata: {e}")

        finally:
            client_socket.close()


if __name__ == "__main__":
    start_server()
