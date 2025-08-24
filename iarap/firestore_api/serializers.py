# firestore_api/serializers.py
from rest_framework import serializers

class FirestoreObjectSerializer(serializers.Serializer):
    data = serializers.DictField()
    collection = serializers.CharField()
    document = serializers.CharField(required=False)

class FirestoreCollectionSerializer(serializers.Serializer):
    collection = serializers.CharField()
    document = serializers.CharField(required=False)
    query = serializers.DictField(required=False)