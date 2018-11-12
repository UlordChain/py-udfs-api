# py-udfs-api

## Usage python2.7

Create an UDFS instance with:
```python
connect = udfsapi.connect(host=host, port=port)
```

upload the file:
```python
connect.add(filepath)
```

To add a file and bakeup other masternode use (the push method returns a list of merklenodes, in this case there is only one element):
```python
connect.push(filepath)
```

download file from the UDFS according to the udfs hash:
```python
self.connect.get(filehash, filepath=filepath)
```
