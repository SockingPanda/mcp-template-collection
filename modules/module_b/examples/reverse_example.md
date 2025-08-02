# Reverse Tool Example

Request:
```
curl -X POST http://localhost:8000/module_b/streamable \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"reverse","arguments":{"text":"Hello"}}}'
```
