from django.urls import path
from .views import (
    FirestoreObjectCRUD,
    FirestoreDocumentCRUD,
    FirestoreCollectionManager,
    CustomFunctionEndpoint
)

urlpatterns = [
    path('firestore/object/', FirestoreObjectCRUD.as_view(), name='firestore-object-crud'),
    path('firestore/document/', FirestoreDocumentCRUD.as_view(), name='firestore-document-crud'),
    path('firestore/collection/', FirestoreCollectionManager.as_view(), name='firestore-collection-crud'),
    path('custom/', CustomFunctionEndpoint.as_view(), name='custom-function'),
]
