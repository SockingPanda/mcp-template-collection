# Add Tool Example

Request:
```
curl -X POST http://localhost:8000/module_a/streamable \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"add","arguments":{"a":1,"b":2}}}'
```
