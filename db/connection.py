from pinecone import Pinecone, ServerlessSpec # type: ignore

pc = Pinecone(api_key='ac402b3b-444a-4267-8a8d-d09a0e4f8aac')

#Create a serverless index
index_name = "contracts-index"

#Delete the old index before recreating
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)

pc.create_index(
    name=index_name,
    dimension=8,
    metric="cosine",
    spec=ServerlessSpec(
        cloud='aws', 
        region='us-east-1'
    ) 
)
index = pc.Index(index_name)
# print(index.describe_index_stats())
print(index)
index.upsert(
    vectors=[
        {"id": "vec1", "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]},
        {"id": "vec2", "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]},
        {"id": "vec3", "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
        {"id": "vec4", "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
    ],
    namespace="ns1"
)
# print(index.describe_index_stats())