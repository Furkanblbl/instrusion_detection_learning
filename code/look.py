import joblib

# .pkl dosyasını yükle
model = joblib.load('kmeans_model.pkl')

# Modelin özelliklerini yazdır
print("Model türü:", type(model))

# KMeans ise, cluster_centers_ ve diğer özellikleri yazdır
if hasattr(model, 'cluster_centers_'):
    print("Cluster merkezleri:\n", model.cluster_centers_)
if hasattr(model, 'n_clusters'):
    print("Küme sayısı:", model.n_clusters)
if hasattr(model, 'feature_names_in_'):
    print("Kullanılan özellik adları:", model.feature_names_in_)
