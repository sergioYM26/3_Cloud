# Advertisements

- Partition Key: "ad_id"

schema: 

```json
{
  "ad_id" : "string",
  "title": "string",
  "description": "string",
  "price": "integer",
  "comments": [
    {
      "date": "timestamp", 
      "user": "string", 
      "message": "string"
    }
  ],
  "createdAt": "timestamp",
  "expiresAt": "timestamp
}
```