from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FirestoreCollectionSerializer, FirestoreObjectSerializer
from .firestore_utils import initialize_firebase
import json

db = initialize_firebase()

class FirestoreObjectCRUD(APIView):
    """
    Endpoint for CRUD operations on Firestore objects within specific documents
    URl: /api/firestore/object/
    """

    def post(self, request):
        serializer = FirestoreObjectSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                doc_ref = db.collection(data['collection']).document(data['document'])
                doc_ref.set(data['data'])
                return Response({"status": "success", "id": doc_ref.id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        serializer = FirestoreObjectSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                # print(data)
                doc_ref = db.collection(data['collection']).document(data['document'])
                # print(doc_ref)
                doc = doc_ref.get()
                # print(doc)
                # print("hello")
                try:
                    if doc.exists:
                        return Response(doc.to_dict(), status=status.HTTP_200_OK)
                except Exception:
                    if isinstance(doc.to_dict(), dict):
                        print(doc.to_dict(), isinstance(doc.to_dict(), dict), "it worked😁")
                        return Response(doc.to_dict(), status=status.HTTP_200_OK)
                return Response({"error": "Document not found"}, status= status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        serializer = FirestoreObjectSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                doc_ref = db.collection(data['collection']).document(data['document'])
                doc_ref.update(data['data'])
                return Response({"status": "success"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = FirestoreObjectSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                db.collection(data['collection']).document(data['document']).delete()
                return Response({"status": "success"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FirestoreDocumentCRUD(APIView):
    """
    Endpoint for CRUD operations with Firestore documents
    URL: /api/firestore/document/
    """

    def post(self, request):
        serializer = FirestoreCollectionSerializer(data=request.data)
        if serializer.is_valid():
            data =  serializer.validated_data
            try:
                if 'document' in data:
                    doc_ref = db.collection(data['collection']).document(data['document'])
                else:
                    doc_ref = db.collection(data['collection']).document()
                if 'data' in request.data:
                    doc_ref.set(request.data['data'])
                else:
                    doc_ref.set({})

                return Response({"status": "success", "id": doc_ref.id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        serializer = FirestoreCollectionSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                if 'document' in data:
                    # Get single document
                    doc_ref = db.collection(data['collection']).document(data['document'])
                    doc = doc_ref.get()
                    if doc.exists:
                        return Response(doc.to_dict(), status=status.HTTP_200_OK)
                    return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    # Gest all document in collection
                    docs = db.collection(data['collection']).stream()
                    result = {doc.id: doc.to_dict() for doc in docs}
                    return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request):
        serializer = FirestoreCollectionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                if 'document' in data:
                    # Delete specific document
                    db.collection(data['collection']).document(data['document']).delete()
                else:
                    # Delete specific documents in collection (but not the collection itself)
                    docs = db.collection(data['collection']).stream()
                    for doc in docs:
                        doc.reference.delete()
                return Response({"status": "success"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FirestoreCollectionManager(APIView):
    """
    Endpoint for createing and deleting collections
    URL: /api/firestore/collection/
    """

    def post(self, request):
        serializer = FirestoreCollectionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                # In Firestore, collections are created implicitly when adding documents
                # So we'll just add an empty document to create the collection
                db.collection(data['collection']).document().set({'created': True})
                return Response({'status': "success"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        serializer = FirestoreCollectionSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            print(data)
            try:
                # To delete a collection, we need to delete all the document in it
                docs = db.collection(data['collection']).stream()
                for doc in docs:
                    doc.reference.delete()
                return Response({"status" : "success"}, status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomFunctionEndpoint(APIView):
    """
    Endpoint for your custom functions 
    URL: /api/custom/
    """

    def post(self, request):
        # Example custom functions - Add logic here
        try:
            data = request.data
            feed = ''
            # Custom logic here
            if data['type'].lower().strip() == 'ai':
                feed = "Hello i'm an AI"
            if data['type'].lower().strip() == 'firebase':
                docs_data = data['prompt'].split('|')
                feed = []
                docs = db.collection(docs_data[0]).stream()
                if docs_data[1] == 'doc-id':
                    for doc in docs:
                        feed.append(doc.id)
                elif docs_data[1] == 'custom' and len(docs_data) == 3:
                    for doc in docs:
                        if docs_data[2] in doc.to_dict():
                            feed.append(doc.to_dict())
                else:
                    return Response({"Error": "Invalid prompt format"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                print(data['prompt'])
            result = {"processed": True, "input": data, 'output': feed}
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)